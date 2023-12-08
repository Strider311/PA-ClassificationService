from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from PIL import Image
from Models.ImageProcessingResult import ImageProcessingResult


class OpenCvClassifier():
    def __init__(self, session_dir, soil_max, unhealthy_max, index) -> None:
        self.index = index
        self.session_dir = session_dir
        self.soil_max = soil_max
        self.unhealthy_max = unhealthy_max
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.4
        self.thickness = 1
        self.soil_color = (53, 82, 160)
        self.healthy_color = (0, 255, 0)
        self.unhealthy_color = (0, 255, 255)

    def load_np_matrix_from_txt(self, file_name: str):
        file = os.path.join(
            self.session_dir, self.index, "numpy", file_name)
        if not os.path.exists(file):
            raise FileNotFoundError("Cant load file")

        matrix = np.loadtxt(file, dtype="float32")
        return matrix

    def apply_filter(self, file_name: str) -> ImageProcessingResult:
        original = self.load_np_matrix_from_txt(file_name)
        soil_cnt = self.__find_soil_contours__(original)
        healthy_cnt = self.__find_healthy_contours__(original)
        unhealthy_cnt = self.__find_unhealthy_contours__(original)
        img, areas = self.__apply_cv2_contours__(
            original, soil_cnt, healthy_cnt, unhealthy_cnt)
        file_name = file_name.replace("txt", "jpg")
        file_output = os.path.join(
            self.session_dir, self.index, "classified")
        if not (os.path.exists(file_output)):
            os.makedirs(file_output)

        file_output_path = os.path.join(file_output, file_name)

        cv2.imwrite(file_output_path, img)

        result = ImageProcessingResult(

            areas['soil'], areas['unhealthy'], areas['healthy'], filepath=file_output_path)
        return result

    def __find_soil_contours__(self, img):
        contours = self.__get_countours__(img, -1, self.soil_max)
        return contours

    def __find_healthy_contours__(self, img):
        processed_img, area = self.__get_countours__(
            img, self.unhealthy_max, 1)
        return processed_img, area

    def __find_unhealthy_contours__(self, img):
        processed_img, area = self.__get_countours__(
            img, self.soil_max, self.unhealthy_max)
        return processed_img, area

    def __get_countours__(self, img, min, max):
        mask = cv2.inRange(img, min, max)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        cnts = cv2.findContours(
            opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("mask", mask)

        return cnts

    def __apply_cv2_contours__(self, img, soil_cnt, healthy_cnt, unhealthy_cnt):

        soil_cnt = soil_cnt[0] if len(soil_cnt) == 2 else soil_cnt[1]
        healthy_cnt = healthy_cnt[0] if len(
            healthy_cnt) == 2 else healthy_cnt[1]
        unhealthy_cnt = unhealthy_cnt[0] if len(
            unhealthy_cnt) == 2 else unhealthy_cnt[1]

        soil_area = 0
        unhealthy_area = 0
        healthy_area = 0
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        for c in unhealthy_cnt:
            unhealthy_area += cv2.contourArea(c)
            cv2.drawContours(
                img, [c], 0, self.unhealthy_color, thickness=cv2.FILLED)

        for c in healthy_cnt:
            healthy_area += cv2.contourArea(c)
            cv2.drawContours(img, [c], 0, self.healthy_color,
                             thickness=cv2.FILLED)

        for c in soil_cnt:
            soil_area += cv2.contourArea(c)
            cv2.drawContours(img, [c], 0, (0, 0, 255),
                             thickness=cv2.FILLED)

        areas = {
            "soil": soil_area,
            "unhealthy": unhealthy_area,
            "healthy": healthy_area
        }
        return img, areas
