class ImageProcessingResult():
    def __init__(self, soil_area, unhealthy_area, healthy_area, filepath) -> None:
        self.file_path = filepath
        self.unhealthy_percent = unhealthy_area / \
            (unhealthy_area + healthy_area)
        self.healthy_percent = healthy_area / (unhealthy_area + healthy_area)
        self.soil_percent = soil_area / \
            (healthy_area + unhealthy_area + soil_area)
