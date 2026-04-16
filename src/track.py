class Track:
    def __init__(self, length: int):
        self.length = length

    def is_finished(self, position: float) -> bool:
        return position >= self.length