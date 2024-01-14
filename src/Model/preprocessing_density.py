"""
Functions to process and crop out the region of interest for the mammogram images
"""

import numpy as np
import cv2
import copy


def crop_roi(mask, og_image, height_og, width_og):
    """cropping the ROI, reducing the black space in the image

    Args:
        mask (arr): masked image with noise removed
        og_image (arr): original mammogram image
        height_og (int): original image height
        width_og (int): original image width

    Returns:
        final_image: cropped roi image
    """

    crop1 = mask[:]
    height, width = crop1.shape

    # smaller crop to remove even more of the noise
    smaller_crop = crop1[int(height / 3) : int(height * 2 / 3)]

    # find where the white pixels are
    points = np.argwhere(smaller_crop == 255)

    xpoints = points[:, 1]  # the x values of all the white pixels

    # check whether image is left or right laterality with the sum of pixels of each half of image
    area_L = crop1[:, : int(width / 2)]
    area_R = crop1[:, int(width / 2) :]

    if np.sum(area_L) > np.sum(area_R):  #  more white pixels on left side
        maxpoint = np.max(
            xpoints
        )  # furthest most white pixel which indicates the end of the breast in the image

        # get coordinates of that white pixel
        b = points[:, 1] == maxpoint
        loc = np.nonzero(b > 0)[0][0]
        small_y, x = points[loc]

        # adjust y to the cropped image
        y = small_y + height / 3

        # dimensions of box to be cropped, chosen arbitrarily
        box_wid = int(width * 0.6)
        box_hei = int(height * 0.6)

        # adjust y to the original image
        y = int(y + 0.05 * height_og)
        x = int(x + 0.03 * width_og)

        # if x coordinate in the box is out of range of the image, adjust it to the edges
        x_start = x - box_wid

        if x_start < 1:
            x_start = 0

        # output the cropped roi image
        final_img = og_image[int(y - box_hei / 2) : int(y + box_hei / 2), x_start:x]

    elif np.sum(area_R) > np.sum(area_L):  #  more white pixels on right side
        maxpoint = np.min(
            xpoints
        )  # furthest most white pixel which indicates the end of the breast in the image

        b = points[:, 1] == maxpoint
        loc = np.nonzero(b > 0)[0][0]
        small_y, x = points[loc]

        y = small_y + height / 3

        box_wid = int(width * 0.6)
        box_hei = int(height * 0.6)

        y = int(y + 0.05 * height_og)
        x = int(x + 0.03 * width_og)

        x_end = x + box_wid

        if x_end > (width_og - 1):
            x_end = width_og - 1

        final_img = og_image[int(y - box_hei / 2) : int(y + box_hei / 2), x:x_end]

    else:
        final_image = og_image
        print("image error")

    return final_img


def find_roi(img):
    img_copy = copy.copy(img[:, :, :])
    height_og, width_og, c = img.shape

    # cropping edges of the image because there is noise present
    img = img[
        int(height_og * 0.05) : int(height_og * 0.95),
        int(width_og * 0.03) : int(width_og * 0.97),
    ]

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # grayscale image
    mask = np.zeros(
        gray_img.shape, dtype=np.uint8
    )  # mask initialized to image dimensions
    blur_img = cv2.GaussianBlur(gray_img, (41, 41), 0)  # blur used to normalise image
    ret, binary = cv2.threshold(
        blur_img, 25, 255, cv2.THRESH_BINARY
    )  # threshold image to identify noise

    # the below code draws contours around all object in the image such as noise (like letters)
    # anf then ignores all the contours that are small because they correspond to noise
    contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    if len(contours) <= 1:
        # this means that the breast takes up the whole of the mammogram, no mini objects identified
        # so we will just take the entire image as the roi
        final_img = crop_roi(mask, img_copy, height_og, width_og)

    else:
        for i in contours:
            x, y, w, h = cv2.boundingRect(i)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 20)
            area = w * h

            # only the bigger rectangle considered, which will include the breast but not the noise
            if (
                area > 0.3 * height_og * width_og
            ):  # 50% of area chosen for now, somewhat arbitrarily
                cv2.drawContours(mask, [i], -1, (255, 255, 255), -1)

        # running the function above which identifies the edge white pixels corresponding to
        # the end of the breast, identifying the region of interest
        final_img = crop_roi(mask, img_copy, height_og, width_og)

    final_img = cv2.resize(
        final_img, (128, 128)
    )  # resize image to train model and run inference

    return final_img
