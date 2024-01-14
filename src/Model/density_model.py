"""
Script to train the density classification model. The model was trained using a pre-trained EfficientNetB0 
model with noisy student weights.
The model was trained on google colab, and the paths represent the directories where the mammogram images were saved
"""

import tensorflow as tf

# initialize parameters
BATCH_SIZE = 25
NUM_EPOCHS_FINAL_LAYERS = 10
NUM_EPOCHS_FULL_MODEL = 100
BASE_MODEL = "EFFB0"
MODEL_VERSION = 1
INPUT_SHAPE = (128, 128, 3)
POOLING = "avg"
WEIGHT = "/content/drive/MyDrive/silcock-sons/noisy.student.notop-b0.h5"


# load datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    "/content/drive/MyDrive/silcock-sons/cbis-data-roi/train",
    batch_size=None,
    image_size=(128, 128),
    color_mode="rgb",
)
test_ds = tf.keras.utils.image_dataset_from_directory(
    "/content/drive/MyDrive/silcock-sons/cbis-data-roi/test",
    batch_size=None,
    image_size=(128, 128),
    color_mode="rgb",
)

# batch datasets
train_size = len(train_ds)
train_ds = train_ds.cache().batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_ds = test_ds.cache().batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# Initialize the Efficent Net model
base = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights=WEIGHT,  # Here we are using Noisy Student Weights
    input_shape=INPUT_SHAPE,
    pooling=POOLING,
)

base.trainable = False  # freezing the base layers
model_name = f"BiradClassificationModel"

# Adding the final Dense layers with some Dropout, and a dense layer with 4 nodes for 4 output classes
layer1 = base.output
layer1 = tf.keras.layers.Dropout(0.1, name="pooling_drop")(layer1)
layer2 = tf.keras.layers.Dense(1024, name="hidden_dense", activation="relu")(layer1)
layer2 = tf.keras.layers.Dropout(0.1, name="hidden2_drop")(layer2)
quality = tf.keras.layers.Dense(4, activation="softmax", name="quality")(layer2)
model = tf.keras.models.Model(base.input, outputs=quality, name=model_name)

# Freeze the original efficient net network
# And train the newly attached layers at a higher learning rate
# Train for a few epochs first then unfreeze and train at a lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.SGD(
        learning_rate=1e-2, weight_decay=1e-6, momentum=0.9
    ),  # Using a slighty higher Learning rate of 1e-2
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
)
print("Model compiled for initial training of final layers. Summary:")
# print(model.summary(show_trainable=True))

history = model.fit(
    train_ds,
    epochs=NUM_EPOCHS_FINAL_LAYERS,
    batch_size=BATCH_SIZE,
    verbose=2,
)


# Modify which layers are trainable
# Unfreezing some of the other blocks (block 4 onwards) of the newtwork to do finetuning.
# Determine what layer number does block 4 start from
start_layer_num = 0
for layer_number in range(len(model.layers)):
    if model.layers[layer_number].name.startswith("block4"):
        start_layer_num = (
            layer_number  # layers from this layer onwards will be trainable
        )
        break
print("Unfreeze from layer:", start_layer_num)

for layer_number in range(start_layer_num, len(model.layers)):
    # layer.trainable = False
    # Make sure Batch Norm layer is set to trainable = False.
    if isinstance(model.layers[layer_number], tf.keras.layers.BatchNormalization):
        continue
    model.layers[layer_number].trainable = True

# Recompile the model because we unfroze some layers
# Compile model with much lower learning rate and loss function
model.compile(
    optimizer=tf.keras.optimizers.SGD(
        learning_rate=1e-4, weight_decay=1e-6, momentum=0.9
    ),  # Lower the learning rate to 1e-4
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"],
)
print("Model compiled for 2nd step training with block 4 onwards unfrozen. Summary:")
# print(model.summary(show_trainable=True))

# Using callbacks to stop the model early if performance is stagnant
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    verbose=1,
    patience=20,
    mode="max",
    restore_best_weights=False,  # Set to false if we want to save our model at the final epoch
)

save_model = tf.keras.callbacks.ModelCheckpoint(
    filepath=f"outputs/{model_name}_checkpoint_bestValidationAcc.h5",
    monitor="val_accuracy",
    verbose=1,
    save_best_only=True,
    mode="max",
)
callback = [save_model, early_stopping]

# Start finetuning with validation set
history = model.fit(
    train_ds,
    epochs=NUM_EPOCHS_FULL_MODEL,
    batch_size=BATCH_SIZE,
    callbacks=[callback],
    verbose=2,
    validation_data=val_ds,
)

# print("Saving model at final epoch...")

# Save the model at the final epoch
model.save(f"outputs/{model_name}_finalEpoch.h5")

print("Finishing experiment...")
