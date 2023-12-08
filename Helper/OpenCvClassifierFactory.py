from Modules.OpenCvClassifier import OpenCvClassifier


class OpenCvClassifierFactory():
    def GetClassifier(index: str, session_dir: str) -> OpenCvClassifier:

        match index.lower():
            case "ndvi":
                classifier = OpenCvClassifier(
                    session_dir=session_dir, soil_max=0.1, unhealthy_max=0.45, index=index)
                return classifier
            case _:
                raise ValueError("NOT IMPLEMENTED")
