class Track:
    def __init__(self, length: int, num_lanes: int):
        self.length = length
        self.num_lanes = num_lanes

    def in_bounds(self, lane: int, position: int) -> bool:
        return 0 <= self.num_lanes and 0 <= position < self.length

    def is_finished(self, car) -> bool:
        return car.position >= self.length - 1