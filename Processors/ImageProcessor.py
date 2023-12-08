from Modules.OpenCvClassifier import OpenCvClassifier
from Modules.ProcessedImageReceiver import NewImageReceiver
from Helper.OpenCvClassifierFactory import OpenCvClassifierFactory
from dto.ProcessedImageDTO import ProcessedImageDTO
from dto.CreateMetricsRequest import CreateMetricsRequest
from Models.ImageProcessingResult import ImageProcessingResult
import logging
import os
import json
import requests


class ImageProcessor():
    def __init__(self) -> None:
        self.__init_logger__()
        self.metric_base_url = f"{os.getenv('API_BASE')}{os.getenv('METRIC_ENDPOINT')}"
        self.headers = {'Content-type': 'application/json'}
        self.message_receiver = NewImageReceiver(self.handle_new_message)

    def __init_logger__(self):
        logging.getLogger("matplotlib").setLevel(logging.WARNING)
        logging.getLogger("PIL").setLevel(logging.WARNING)
        self.logger = logging.getLogger('Main.Processor')
        self.logger.setLevel(logging.DEBUG)

    def handle_new_message(self, ch, method, properties, body):
        body_json = json.loads(body.decode())

        dto = self.map_incoming_msg(body_json)
        self.process_msg(dto)

    def process_msg(self, image: ProcessedImageDTO):
        for index in image.indices:
            classifier = OpenCvClassifierFactory.GetClassifier(
                index, image.session_dir)
            file_name = image.fileName.replace("jpg", "txt")
            result = classifier.apply_filter(file_name)

            self.post_metric(result, image, index)

    def map_incoming_msg(self, body):
        dto = ProcessedImageDTO(
            id=body['id'],
            session_dir=body['session_dir'],
            indices=body['indices'],
            session_id=body['session_id'],
            fileName=body['fileName'],
        )

        return dto

    def post_metric(self, result: ImageProcessingResult, image: ProcessedImageDTO, index: str):

        request = CreateMetricsRequest(
            index=index, unhealthy_percent=result.unhealthy_percent, healthy_percent=result.healthy_percent,  file_path=result.file_path).toJSON()

        url = self.metric_base_url + '/' + image.id.replace('"', '')
        response = requests.post(
            url, request, headers=self.headers)
        if (response.status_code != 200):
            raise Exception("Unable to update image")
