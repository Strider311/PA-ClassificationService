import json


class CreateMetricsRequest():
    def __init__(self, index: str, healthy_percent: float, unhealthy_percent: float, file_path: str) -> None:
        self.index = index
        self.healthy_percent = healthy_percent
        self.unhealthy_percent = unhealthy_percent
        self.image_path = file_path

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
