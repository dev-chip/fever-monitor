"""
Unit tests for the image_processing module.
"""

# unit test imports
import unittest

# project imports
from core.image_processing import (crop_face_in_image_array,
                                   crop_image_array,
                                   draw_face_box,
                                   get_max_array_value,
                                   keep_box_within_bounds,
                                   scale_resize_image,
                                   to_color_img_array,
                                   to_pil_image)


class TestImageProcessingModule(unittest.TestCase):
    def test_to_color_img_array_001(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
