"""
TODO:
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"
__status__ = "Prototype"


# external module imports
import numpy as np
from PIL import Image
import cv2
import math


# cv2 colormap names in order of index value
colormaps = [
    "AUTUMN",
    "JET",
    "BONE",
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
    assert(colormap_index >= 0 or colormap_index < len(colormaps)),\
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
    Scales an image by its width maintaining its aspect ratio.

    TODO:
    """
    aspect_ratio = img.height / img.width
    return img.resize((width, round(width * aspect_ratio)))


def crop_face_in_image_array(arr, x, y, w, h, x_zoom_out=0.33, y_zoom_out=0.33):
    """
    TODO
    """
    assert (type(arr) == np.ndarray), \
        "Expected type list or np.ndarray but got {}.".format(type(arr))

    # calculate amounts to zoom out by using percentage provided
    x_zoom = math.ceil(w * x_zoom_out)
    y_zoom = math.ceil(h * y_zoom_out)

    x = x - x_zoom
    y = y - y_zoom
    w = w + (x_zoom * 2)
    h = h + (y_zoom * 2)

    # if the zoom-out has caused the indexes to go out-of-bounds, set
    # indexes to be their closest in-bound value
    if 0 > y:
        y = 0
    if 0 > x:
        x = 0
    if len(arr) <= y + h:
        h = len(arr) - y - 1
    if len(arr[0]) <= x + w:
        w = len(arr[0]) - x - 1

    # crop and return
    return crop_image_array(
        arr=arr,
        x=x,
        y=y,
        w=w,
        h=h)


def crop_image_array(arr, x, y, w, h):
    """
    TODO
    """
    if type(arr) == list:
        arr = np.array(arr)
    assert (type(arr) == np.ndarray), \
        "Expected type list or np.ndarray but got {}.".format(type(arr))
    assert (len(arr) > y and len(arr) > y + h), \
        "y crop index outside bounds of the array ({}, {}).".format(y, y + h)
    assert (len(arr[0]) > x and len(arr[0]) > x + w), \
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


def generate_random_colors(n):
    """
    Generates an array of random 8-bit colors.

    Parameters:
        n: number of colors to generate

    Returns:
        np.ndarray: colors generated
    """
    np.random.seed(4)
    return np.random.randint(0, 255, size=(n, 3), dtype="uint8")


def draw_face_box(face, image, color, text="face"):
    """
    Draws boxes around detections... TODO: short des

    TODO:
    """
    assert(0 <= face.detection.x < len(image[0])), \
        "X1 value '{}' out of bounds".format(face.detection.x)
    assert(0 <= face.detection.y < len(image)), \
        "Y1 value '{}' out of bounds".format(face.detection.y)
    assert(0 <= face.detection.x + face.detection.w < len(image[0])), \
        "X2 value '{}' out of bounds".format(face.detection.x + face.detection.w)
    assert(0 <= face.detection.y + face.detection.h < len(image)), \
        "Y2 value '{}' out of bounds".format(face.detection.y + face.detection.h)

    cv2.rectangle(image, (face.detection.x, face.detection.y), (face.detection.x + face.detection.w, face.detection.y + face.detection.h),
                  [int(c) for c in color], 1)
    cv2.putText(img=image, text=text, org=(face.detection.x+(face.detection.w//2), face.detection.y - 5), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.4, color=[int(c) for c in color], thickness=1)
    return image

"""
def draw_boxes(detections, image, colors, labels):
    for d in detections:
        text = "{}: {:.4f}".format(labels[d.class_id], d.confidence)
        color = [int(c) for c in colors[d.class_id]]
        cv2.rectangle(img=image, pt1=(d.x, d.y), pt2=(d.x + d.w, d.y + d.h), color=color, thickness=2)
        cv2.putText(img=image, text=text, org=(d.x + (d.w // 2), d.y - 5), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5, color=color, thickness=2)
"""