﻿from config_manager import ConfigManager
import io
import numpy as np
import cv2
from transform_image import resize
import os
import datetime


class Camera:
    use_camera = ConfigManager.get_config()['use_camera'] == 'True'

    if use_camera:
        from picamera import PiCamera
        camera = PiCamera()
        camera.resolution = (650, 480)

    @staticmethod
    def capture_screenshot():
        if Camera.use_camera:
            Camera.camera.start_preview()

            stream = io.BytesIO()
            Camera.camera.capture(stream, format='jpeg')

            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            image = resize(image)

            Camera.camera.stop_preview()
        else:
            im_path = ConfigManager.get_config()['test_image_path']
            im = cv2.imread(im_path)
            image = resize(im)

        return image

    @staticmethod
    def save_image(image):
        save_path = ConfigManager.get_config()['save_image_path']
        if len(save_path) > 0:  # no logging needed otherwise
            count = len(os.listdir(save_path)) + 3  # + 3 just to be sure

            now = datetime.datetime.now()
            file_name = '{}_{}_{}_{}_{}_{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)

            file_path_name = '{}image{}_{}.jpg'.format(save_path, count, file_name)
            cv2.imwrite(file_path_name, image)