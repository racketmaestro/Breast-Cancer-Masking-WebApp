"""
Functions to process and crop out the region of interest for the mammogram images
"""

import numpy as np
import cv2
import copy


def crop_roi(mask, og_image, height_og, width_og):
    crop1 = mask[
        int(height_og * 0.05) : int(height_og * 0.95),
        int(width_og * 0.03) : int(width_og * 0.97),
    ]
    imcopy = copy.copy(crop1)

    crop1 = imcopy[:]

    height, width = crop1.shape

    smaller_crop = crop1[int(height / 3) : int(height * 2 / 3)]
    points = np.argwhere(smaller_crop == 255)  # find where the black pixels are
    xpoints = points[:, 1]  # the x values

    # check left or right, get sum of pixels of each half of image
    area_L = crop1[:, : int(width / 2)]
    area_R = crop1[:, int(width / 2) :]

    # if crop1[int(height/2),0] == 255: # breast on left side
    if np.sum(area_L) > np.sum(area_R):  #  left side
        # print('left')
        maxpoint = np.max(xpoints)
        # print(maxpoint)
        b = points[:, 1] == maxpoint
        loc = np.nonzero(b > 0)[0][0]
        small_y, x = points[loc]

        y = small_y + height / 3

        # print(loc)
        # print(y,x)

        box_wid = int(width * 0.6)
        box_hei = int(height * 0.6)

        y = int(y + 0.05 * height_og)
        x = int(x + 0.03 * width_og)

        x_start = x - box_wid

        if x_start < 1:
            x_start = 0
        # saving the cropped roi image
        final_img = og_image[int(y - box_hei / 2) : int(y + box_hei / 2), x_start:x]

    elif np.sum(area_R) > np.sum(area_L):  # breast on right side
        # print('right')
        maxpoint = np.min(xpoints)
        # print(maxpoint)

        b = points[:, 1] == maxpoint
        loc = np.nonzero(b > 0)[0][0]
        small_y, x = points[loc]

        y = small_y + height / 3

        # print(loc)
        # print(y,x)

        box_wid = int(width * 0.6)
        box_hei = int(height * 0.6)

        y = int(y + 0.05 * height_og)
        x = int(x + 0.03 * width_og)

        x_end = x + box_wid

        if x_end > (width_og - 1):
            x_end = width_og - 1

        final_img = og_image[int(y - box_hei / 2) : int(y + box_hei / 2), x:x_end]
        # cv2.rectangle(img_copy, ( x, int(y-box_hei/2)), (x+box_wid, int(y+box_hei/2)), (255, 0, 0) , 20)

    else:
        final_image = og_image
        print("image error")

    return final_img


def find_roi(img):
    img_copy = copy.copy(img[:, :, :])

    height_og, width_og, c = img.shape
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # grayscale
    mask = np.zeros(
        gray_img.shape, dtype=np.uint8
    )  # mask initialized to image dimensions
    blur_img = cv2.GaussianBlur(gray_img, (41, 41), 0)  # blur used to normalise image
    ret, binary = cv2.threshold(blur_img, 25, 255, cv2.THRESH_BINARY)  # threshold image

    contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    if len(contours) <= 1:
        # basically this means that the breast takes up the whole of the mammogram,
        # so might as well just take the entire crop 1 region

        # final_img  = img_copy[int(height_og*0.05):int(height_og*0.95)]
        mask = binary
        final_img = crop_roi(mask, img_copy, height_og, width_og)

    else:
        for i in contours:
            x, y, w, h = cv2.boundingRect(i)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 20)
            area = w * h

            # only the biggest rectangle considered, ignore small ones
            if (
                area > 0.3 * height_og * width_og
            ):  # 50% of area chosen for now, somewhat arbitrarily
                cv2.drawContours(mask, [i], -1, (255, 255, 255), -1)

        final_img = crop_roi(mask, img_copy, height_og, width_og)

    final_img = cv2.resize(final_img, (128, 128))

    return final_img
