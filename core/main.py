"""
TODO
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"
__status__ = "Prototype"


# external module imports
import time


# module imports
from core.lepton import LeptonCamera, to_celsius
from core.inference import YoloInference
from core.image_processing import (get_max_array_value,
                                   crop_face_in_image_array,
                                   to_color_img_array,
                                   to_pil_image,
                                   generate_random_colors,
                                   draw_face_box,
                                   keep_box_within_bounds)


class Face:
    def __init__(self, detection, temp, img):
        self.detection = detection
        self.temp = temp
        self.img = img


class FeverMonitor:
    def __init__(self, weights_path, cfg_path, labels_path, use_gpu=False):
        self._lepton_camera = LeptonCamera()

        self._inf = YoloInference(
            weights_path=weights_path,
            cfg_path=cfg_path,
            labels_path=labels_path,
            use_gpu=use_gpu)
        self._inf.set_network_dimensions(128, 128)
        
        self._class_colors = generate_random_colors(len(self._inf.labels))

    def run(self):
        start = time.time()

        # capture image
        self._lepton_camera.capture()
        img = self._lepton_camera.get_img()

        # convert to 8-bit color array
        color_img = to_color_img_array(arr=img, colormap_index=5)

        # load into inf object and run inference
        self._inf.load_image(color_img)
        detections, inference_time = self._inf.run(threshold=0.3)

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

            # draw box around faces in the image
            color_img = draw_face_box(
                face=face,
                arr=color_img,
                color=self._class_colors[0],
                text="{}".format(str(round(face_temp, 1))))

        # convert image array to PIL image
        pil_image = to_pil_image(color_img)

        # calculate elapsed time
        elapsed = time.time() - start

        return pil_image, face_objects, elapsed


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
