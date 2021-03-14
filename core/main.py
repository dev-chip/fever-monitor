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
                                   scale_resize_image,
                                   to_color_img_array,
                                   to_pil_image,
                                   generate_random_colors,
                                   draw_boxes)


def continuous_capture():
    lc = LeptonCamera()

    inf = YoloInference(
        weights_path=r'G:\Darknet\live2\backup\yolo-obj_best.weights',
        cfg_path=r'G:\Darknet\live2\yolo-obj.cfg',
        labels_path=r'G:\Darknet\live2\data\obj.names',
        use_gpu=False)
    inf.set_network_dimensions(128, 128)

    class_colors = generate_random_colors(len(inf.labels))

    start = time.time()
    for _ in range(100):
        # capture image
        lc.capture()
        img = lc.get_img()

        # convert to 8-bit color array
        color_img = to_color_img_array(arr=img, colormap_index=5)

        # load into inf object and run inference
        inf.load_image(color_img)
        detections, t = inf.run(threshold=0.3)

        # draw boxes for each detection
        for d in detections:

            face_arr = crop_face_in_image_array(img, d.x, d.y, d.w, d.h, y_zoom_out=0, x_zoom_out=0)
            print(to_celsius(get_max_array_value(arr=face_arr)))

            color_img = draw_boxes(
                detections=detections,
                image=color_img,
                colors=class_colors,
                labels=inf.labels)



        # convert image array to PIL image
        pil_image = to_pil_image(color_img)

    end = time.time()
    elapsed = end - start
    average = elapsed / 100
    print("elapsed:\t", elapsed)
    print("average:\t", average)
    print("fps:\t\t", 1/average)

continuous_capture()