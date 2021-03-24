"""
TODO
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
import os

# module imports
from core.lepton import (LeptonCamera,
                         to_celsius,
                         to_fahrenheit,
                         to_kelvin)
from core.inference import YoloInference
from core.image_processing import (get_max_array_value,
                                   crop_face_in_image_array,
                                   to_color_img_array,
                                   to_pil_image,
                                   draw_face_box,
                                   keep_box_within_bounds,
                                   colormaps)

# logger
from qtgui.logger import init_console_logger
import logging
logger = init_console_logger(log_level=logging.INFO, name="fever_monitor", stream_handler=True, file_handler=True)


# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, ".."))
YOLO_FILES_PATH = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, "yolo"))


class Face:
    def __init__(self, detection, temp, img, over_threshold):
        self.detection = detection
        self.temp = temp
        self.img = img
        self.over_threshold = over_threshold


class FeverMonitor:
    def __init__(self,
                 temp_threshold=38.0,
                 temp_unit="Celsius",
                 colormap_index=5,
                 yolo_model="Standard",
                 confidence_threshold=0.5,
                 use_gpu=False):
        self._lepton_camera = LeptonCamera()

        # init variables
        self._temp_threshold = 0.0
        self._temp_unit_index=0
        self._colormap_index = 0
        self._yolo_inf = None
        self._model_name_selected = ""
        self._confidence_threshold = 0.0
        self._using_gpu = False

        # set parameters passed
        self.set_temp_threshold(temp_threshold)
        self.set_temp_unit(temp_unit)
        self.set_yolo_model(yolo_model)
        self.set_confidence_threshold(confidence_threshold)
        self.set_colormap_index(colormap_index)
        self.set_gpu(use_gpu)

    def set_temp_threshold(self, temp):
        """
        TODO
        """
        assert(type(temp) == int or type(temp) == float)
        self._temp_threshold = temp

    def set_temp_unit(self, unit):
        """
        TODO
        """
        if unit == "Celsius":
            self._temp_unit_index = 0

        elif unit == "Fahrenheit":
            self._temp_unit_index = 1

        elif unit == "Kelvin":
            self._temp_unit_index = 2

        else:
            raise Exception("Temperature unit '{}' not recognised".format(unit))

    def set_colormap_index(self, index):
        """
        TODO
        """
        assert(0 <= index < len(colormaps))
        self._colormap_index = index

    def set_yolo_model(self, model="Standard"):
        """
        TODO
        """
        # define path to file containing class names
        labels_path = os.path.join(YOLO_FILES_PATH, 'obj.names')

        # choose model
        if model == "Standard":
            weights_path = os.path.join(YOLO_FILES_PATH, 'Standard', 'yolo-obj_best.weights')
            cfg_path = os.path.join(YOLO_FILES_PATH, 'Standard', 'yolo-obj.cfg')
        elif model == "Lightweight":
            weights_path = os.path.join(YOLO_FILES_PATH, 'Lightweight', 'tiny_yolo_3l_best.weights')
            cfg_path = os.path.join(YOLO_FILES_PATH, 'Lightweight', 'tiny_yolo_3l.cfg')
        else:
            raise Exception("Model name '{}' not recognised.".format(model))

        # if the model selected is not the model currently setup
        # then create a new model
        if model != self._model_name_selected:
            self._model_name_selected = model

            # create model
            self._yolo_inf = YoloInference(
                weights_path=weights_path,
                cfg_path=cfg_path,
                labels_path=labels_path,
                use_gpu=self._using_gpu)

            # set model network size
            self._yolo_inf.set_network_dimensions(160, 128)

    def set_confidence_threshold(self, threshold):
        """
        TODO
        """
        assert(0 <= threshold <= 1)
        self._confidence_threshold = threshold

    def set_gpu(self, use):
        """
        TODO
        """
        assert(type(use) == bool)
        self._yolo_inf.set_gpu(use)
        self._using_gpu = use

    def is_using_gpu(self):
        """
        TODO
        """
        return self._using_gpu

    def get_colormap_index(self):
        """
        TODO
        """
        return self._colormap_index

    def get_temp_threshold(self):
        """
        TODO
        """
        return self._temp_threshold

    def get_confidence_threshold(self):
        """
        TODO
        """
        return self._confidence_threshold

    def get_model_name_selected(self):
        """
        TODO
        """
        return self._model_name_selected

    def run(self):
        """
        TODO
        """
        try:
            # capture image
            self._lepton_camera.capture()
        except Exception as e:
            if not self._lepton_camera.lepton_connected():
                raise Exception("Lepton camera disconnected.")
            raise e

        logger.debug("capturing image...")
        img = self._lepton_camera.get_img()

        # load into inf object and run inference
        logger.debug("loading image...")
        self._yolo_inf.load_image(to_color_img_array(arr=img, colormap_index=5))
        logger.debug("running inference...")
        detections, inference_time = self._yolo_inf.run(threshold=self._confidence_threshold)

        logger.debug("correcting BBs...")
        # correct bounding boxes that are outside the bounds of the image
        for d in detections:
            d.x, d.y, d.w, d.h = keep_box_within_bounds(img, d.x, d.y, d.w, d.h)

        logger.debug("converting image to color image...")
        # convert image to color image using a user-set colormap
        color_img = to_color_img_array(arr=img, colormap_index=self._colormap_index)

        face_objects = []

        # for each face detected
        for d in detections:

            # get face max temperature
            logger.debug("getting max face temp...")
            face_temp = get_max_array_value(arr=crop_face_in_image_array(img, d.x, d.y, d.w, d.h, x_zoom_out=0, y_zoom_out=0))

            # convert max face temperature
            logger.debug("converting max face temp...")
            if self._temp_unit_index == 0:
                face_temp = to_celsius(face_temp)
            elif self._temp_unit_index == 1:
                face_temp = to_fahrenheit(face_temp)
            elif self._temp_unit_index == 2:
                face_temp = to_kelvin(face_temp)

            # zoom out of face slightly image of whole head
            logger.debug("getting face image (zoomed out)...")
            face_img = to_pil_image(
                crop_face_in_image_array(img, d.x, d.y, d.w, d.h, x_zoom_out=0.3, y_zoom_out=0.3))

            # create face object
            logger.debug("creating face object...")
            face = Face(
                detection=d,
                temp=face_temp,
                img=face_img,
                over_threshold=(face_temp >= self._temp_threshold))
            face_objects.append(face)

            # determine properties of displayed boxes
            logger.debug("determining colors...")
            if face_temp < self._temp_threshold:
                box_color = (50, 205, 50)  # green for below threshold
            else:
                box_color = (255, 0, 0)  # red for above threshold

            #draw box around faces in the image
            logger.debug("drawing box around face ({}, {}, {}, {})...".format(
                face.detection.x,
                face.detection.y,
                face.detection.x + face.detection.w,
                face.detection.y + face.detection.h))
            color_img = draw_face_box(
                face=face,
                arr=color_img,
                color=box_color,
                text="{}".format(str(round(face_temp, 1))),
                box_thickness=1,
                text_thickness=1)

        # convert image array to PIL image
        logger.debug("converting image to pil...")
        pil_image = to_pil_image(color_img)

        logger.debug("done -> returning results...")
        return pil_image, face_objects


# --------------------- #
#     Profile Code      #
# --------------------- #
if __name__ == "__main__":
    import pstats
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    # fever_monitor = FeverMonitor(
    #     cfg_path=r'G:\Darknet\live2_2\yolo-obj.cfg',
    #     labels_path=r'G:\Darknet\live2_2\data\obj.names',
    #     weights_path=r'G:\Darknet\live2_2\backup\yolo-obj_best.weights',
    #     use_gpu=False)
    fever_monitor = FeverMonitor(
        cfg_path=r'G:\Darknet\tiny_3l\tiny_yolo_3l.cfg',
        labels_path=r'G:\Darknet\tiny_3l\data\obj.names',
        weights_path=r'G:\Darknet\tiny_3l\backup\tiny_yolo_3l_best.weights',
        use_gpu=False)
    for i in range(100):
        fever_monitor.run()
    pr.disable()
    stats = pstats.Stats(pr).sort_stats('cumtime')
    stats.print_stats()
