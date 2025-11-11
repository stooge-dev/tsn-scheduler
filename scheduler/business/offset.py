from .network import Link

class Offset:
    def __init__(self, link: Link, stream_name: str, frame_idx: int, value: int):
        self.link = link
        self.stream_name = stream_name
        self.frame_idx = frame_idx
        self.value = value