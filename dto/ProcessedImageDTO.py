class ProcessedImageDTO():

    def __init__(self, id: str, session_id: str, fileName: str, indices, session_dir: str):
        self.id = id
        self.fileName = fileName
        self.indices = indices
        self.session_dir = session_dir
        self.session_id = session_id
