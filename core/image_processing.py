"""
Image processing functions.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
import numpy as np
from PIL import Image
import cv2
import math


# cv2 colormap names in order of index value
colormaps = [
    "AUTUMN",
    "BONE",
    "JET",
    "WINTER",
    "RAINBOW",
    "OCEAN",
    "SUMMER",
    "SPRING",
    "COOL",
    "HSV",
    "PINK",
    "HOT",
    "PARULA",
    "MAGMA",
    "INFERNO",
    "PLASMA",
    "VIRIDIS",
    "CIVIDIS",
    "TWILIGHT",
    "TWILIGHT_SHIFTED",
    "TURBO",
    "DEEPGREEN"]


def to_color_img_array(arr, colormap_index=5):
    """
    Creates and returns an 8-bit color image array.

    Applies the selected OpenCV colormap to an array.

    Params:
        colormap_index: cv2 colormap applied to image

    Returns:
        np.ndarray: 8-bit color array with shape [y, x, 3]

    Raises:
        AssertionError: assertions fail
    """
    assert(colormap_index >= 0 and colormap_index < len(colormaps)),\
        "colormap_index value '{}' is invalid. Must be an integer in range 0 to {}.".format(
            colormap_index, len(colormaps))

    # Rescale to 8 bit color
    img = 255 * (arr - arr.min()) / (arr.max() - arr.min())

    # Apply colormap
    color_arr = cv2.applyColorMap(img.astype(np.uint8), colormap_index)

    return color_arr


def to_pil_image(color_arr, width=None):
    """
    Creates and returns an PIL Image using a 3D image array.

    Creates PIL.Image.Image object and and scales image to a set width
    (maintaining aspect ratio).
    Params:
        color_arr: 3D image array
        width: width of output image (keeps aspect ratio)

    Returns:
        PIL.Image.Image: 8-bit color image

    Raises:
        AssertionError: assertions fail
    """
    assert (width is None or width > 0), \
        "Width value must be greater than 0."

    # Convert to PIl.Image.Image
    color_img = Image.fromarray(color_arr, 'RGB')

    # Scale if required
    if width is not None and width != color_img.width:
        color_img = scale_resize_image(
            img=color_img,
            width=width)

    return color_img


def scale_resize_image(img, width):
    """
    Scales an image by its width, maintaining its aspect ratio.

    Params:
        img - [PIL.Image.Image] image to be resized
        width - [int] new width

    Returns:
        [PIL.Image.Image] resized Image object

    Raises:
        [AssertionError] assertion failed
    """
    assert (width > 0), \
        "Width must be greater than 0."
    aspect_ratio = img.height / img.width
    return img.resize((width, round(width * aspect_ratio)))


def keep_box_within_bounds(arr, x, y, w, h):
    """
    Sets box coordinates to be within the bounds of an array.

    Modify box coordinates that are out-of-bounds of the passed
    array to be the closest correct value.

    Params:
        arr: 3D image array
        x: top-left x coordinate of the box
        y: top-left y coordinate of the box
        w: width of the box
        h: height of the box

    Returns:
        [int] x value within the bounds of the image array
        [int] y value within the bounds of the image array
        [int] w value within the bounds of the image array
        [int] h value within the bounds of the image array
    """
    max_y = len(arr) - 1
    max_x = len(arr[0]) - 1

    if x < 0:
        w += x
        x = 0
    if y < 0:
        h += y
        y = 0
    
    if x > max_x:
        x = max_x
        w = 0
    if y > max_y:
        y = max_y
        h = 0
        
    if x + w > max_x:
        w = max_x - x
    if y + h > max_y:
        h = max_y - y
    
    if w < 0:
        w = 0
    if h < 0:
        h = 0

    return x, y, w, h


def crop_face_in_image_array(arr, x, y, w, h, x_zoom_out=0.33, y_zoom_out=0.33):
    """
    Returns a slices array containing just the face in an image.

    Allows specification of an amount to zoom out of the box by.

    Params:
        arr: [np.array] 3D image array
        x: [int] row index top-left of the face in the array
        y: [int] column index top-left of the face in the array
        w: [int] width of the face in the array
        h: [int] height of the face in the array
        x_zoom_out: [float] zoom-out percentage for the width of the image
        y_zoom_out: [float] zoom-out percentage for the height of the image

    Returns:
        [np.array] sliced array
    """
    assert (type(arr) == np.ndarray), \
        "Expected type list or np.ndarray but got {}.".format(type(arr))

    # calculate amounts to zoom out by using percentage provided
    x_zoom = math.ceil(w * x_zoom_out)
    y_zoom = math.ceil(h * y_zoom_out)

    x = x - x_zoom//2
    y = y - y_zoom//2
    w = w + x_zoom
    h = h + y_zoom

    # if the zoom-out has caused the indexes to go out-of-bounds, set
    # indexes to be their closest in-bound value
    x, y, w, h = keep_box_within_bounds(arr, x, y, w, h)

    # crop and return
    return crop_image_array(
        arr=arr,
        x=x,
        y=y,
        w=w,
        h=h)


def crop_image_array(arr, x, y, w, h):
    """
    Returns a slices array containing a specified slice of an array.

    Params:
        arr: [np.array] 3D image array
        x: [int] row index top-left
        y: [int] column index top-left
        w: [int] width
        h: [int] height

    Returns:
        [np.array] sliced array
    """
    if type(arr) == list:
        arr = np.array(arr)
    assert (type(arr) == np.ndarray), \
        "Expected type list or np.ndarray but got {}.".format(type(arr))
    assert (len(arr) > y and len(arr) > y + h and y > 0 and h >= 0), \
        "y crop index outside bounds of the array ({}, {}).".format(y, y + h)
    assert (len(arr[0]) > x and len(arr[0]) > x + w and x > 0 and w >= 0), \
        "x crop index outside bounds of the array ({}, {}).".format(x, x + w)
    return arr[y:y+h, x:x+w]


def get_max_array_value(arr):
    """
    Returns the maximum value in an array.

    Flattens an array and finds the maximum value.
    If the array provided is of type list, it is
    converted to an numpy array.

    Parameters:
        arr: any array

    Returns:
        value: max value of the array
    """
    if type(arr) == list:
        arr = np.array(arr)
    assert (type(arr) == np.ndarray), \
        "Expected type list or np.ndarray but got {}.".format(type(arr))
    return np.amax(arr)


def draw_face_box(face, arr, color, text="face", box_thickness=1, text_thickness=1):
    """
    Draws boxes and text around face detections.

    Params:
        face: [Face] Face object
        arr: [np.array] 3D image array
        color: [list] color of the box
        text: [str] text to be drawn next to the detection
        box_thickness: [int] thickness of the box drawn
        text_thickness: [int] thickness of the text drawn

    Returns:
        arr: [np.array] 3D image array with detection box and text drawn
    """
    # correct out-of-bounds values
    face.detection.x, face.detection.y, face.detection.w, face.detection.h =\
        keep_box_within_bounds(arr, face.detection.x, face.detection.y, face.detection.w, face.detection.h)

    # draw box
    cv2.rectangle(img=arr,
                  pt1=(face.detection.x, face.detection.y),
                  pt2=(face.detection.x + face.detection.w, face.detection.y + face.detection.h),
                  color=color,
                  thickness=box_thickness)

    # draw text
    cv2.putText(img=arr,
                text=text,
                org=(face.detection.x+(face.detection.w//2), face.detection.y-2),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.4,
                color=color,
                thickness=text_thickness)
    return arr
