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
import time
import os

# module imports
from core.lepton import LeptonCamera, to_celsius
from core.inference import YoloInference
from core.image_processing import (get_max_array_value,
                                   crop_face_in_image_array,
                                   to_color_img_array,
                                   to_pil_image,
                                   draw_face_box,
                                   keep_box_within_bounds,
                                   colormaps)

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, ".."))
YOLO_FILES_PATH = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, "yolo"))


class Face:
    def __init__(self, detection, temp, img):
        self.detection = detection
        self.temp = temp
        self.img = img


class FeverMonitor:
    def __init__(self,
                 temp_threshold=38.0,
                 colormap_index=5,
                 yolo_model="Standard",
                 confidence_threshold=0.5,
                 use_gpu=False):
        self._lepton_camera = LeptonCamera()

        # init variables
        self._temp_threshold = 0.0
        self._colormap_index = 0
        self._yolo_inf = None
        self._model_name_selected = ""
        self._confidence_threshold = 0.0
        self._using_gpu = False

        # set parameters passed
        self.set_temp_threshold(temp_threshold)
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
            raise Exception("Model name passed not recognised.")

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
            self._yolo_inf.set_network_dimensions(128, 128)  # TODO: set to 160 x 128

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

        img = self._lepton_camera.get_img()

        # load into inf object and run inference
        self._yolo_inf.load_image(to_color_img_array(arr=img, colormap_index=5))
        detections, inference_time = self._yolo_inf.run(threshold=self._confidence_threshold)

        # correct bounding boxes that are outside the bounds of the image
        for d in detections:
            d.x, d.y, d.w, d.h = keep_box_within_bounds(img, d.x, d.y, d.w, d.h)

        face_objects = []

        # for each face detected
        for d in detections:

            # get face max temperature
            face_temp = to_celsius(get_max_array_value(
                arr=crop_face_in_image_array(img, d.x, d.y, d.w, d.h, y_zoom_out=0, x_zoom_out=0)))

            # zoom out of face slightly image of whole head
            face_img = to_pil_image(
                crop_face_in_image_array(img, d.x, d.y, d.w, d.h, y_zoom_out=0.3, x_zoom_out=0.3))

            face = Face(detection=d, temp=face_temp, img=face_img)
            face_objects.append(face)

            # determine properties of displayed boxes
            if face_temp >= self._temp_threshold:
                box_color = (50, 205, 50)  # green for below threshold
                box_thickness = 1
                text_thickness = 1
            else:
                box_color = (255, 0, 0)  # red for above threshold
                box_thickness = 2
                text_thickness = 2

            # draw box around faces in the image
            color_img = draw_face_box(
                face=face,
                arr=color_img,
                color=box_color,
                text="{}".format(str(round(face_temp, 1))),
                box_thickness=box_thickness,
                text_thickness=text_thickness)

        # convert image array to PIL image
        pil_image = to_pil_image(to_color_img_array(arr=img, colormap_index=self._colormap_index))

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
