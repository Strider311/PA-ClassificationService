import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cv2
import os
from scipy import ndimage


class NumpyClassifier():
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max
        self.root_dir = "C:\\Users\\saif_\\Main\\Projects\\PrecisionAgriculture\\data\\Processed\\Testing-11_11_2023-21_11_03\\ndvi\\numpy"
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.4
        self.thickness = 1

    def load_np_matrix_from_txt(self, file_name: str):
        file = os.path.join(self.root_dir, file_name)

        if not os.path.exists(file):
            raise FileNotFoundError

        matrix = np.loadtxt(file, dtype="float32")
        return matrix

    def apply_filter(self, file_name: str):
        original = self.load_np_matrix_from_txt(file_name)
        soil, soil_area = self.__find_soil__(original)
        healthy, healthy_area = self.__find_healthy__(original)
        final, unhealthy_area = self.__find_unhealthy__(original)
        total_area = soil_area + healthy_area + unhealthy_area

        print(
            f"Healthy area: {healthy_area/total_area*100}\nUnhealthy area: {unhealthy_area/total_area*100}\nSoil area: {soil_area/total_area*100}")
        cv2.imshow("Soil", soil)
        cv2.imshow("Healthy", healthy)
        cv2.imshow("Unhealthy", final)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def __find_soil__(self, img):
        color = (53, 53, 100)
        processed_img, area = self.__apply_cv2_mask__(img, 0, 0.3, color)
        return processed_img, area

    def __find_healthy__(self, img):
        color = (0, 255, 0)
        processed_img, area = self.__apply_cv2_mask__(img, 0.55, 1, color)
        return processed_img, area

    def __find_unhealthy__(self, img):
        color = (0, 255, 255)
        processed_img, area = self.__apply_cv2_mask__(img, 0.3, 0.55, color)
        return processed_img, area

    def __apply_cv2_mask__(self, img, min, max, color: list):
        original = img
        mask = cv2.inRange(img, min, max)
        detected = cv2.bitwise_and(img, img, mask=mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        cnts = cv2.findContours(
            opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        area = 0
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        for c in cnts:
            area += cv2.contourArea(c)
            cv2.drawContours(img, [c], 0, color, thickness=cv2.FILLED)

        # cv2.imshow("Mask", mask)
        # cv2.imshow("Original", original)
        # cv2.imshow("Unhealthy plant tissue", img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        return img, area


ndvi_classifier = NumpyClassifier(0.35, 0.55)
ndvi_classifier.apply_filter("Image_006.txt")
