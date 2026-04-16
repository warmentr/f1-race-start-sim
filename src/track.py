class Track:
    def __init__(self, cells: list[dict], num_lanes: int):
        self.cells = cells
        self.length = len(cells)
        self.num_lanes = num_lanes

    def in_bounds(self, lane: int, position: int) -> bool:
        return 0 <= self.num_lanes and 0 <= position < self.length

    def get_cell(self, position: int) -> dict | None:
        if 0 <= position < self.length:
            return self.cells[position]
        return None

    def get_speed_limit(self, position: int, default: int = 5) -> int:
        cell = self.get_cell(position)
        if cell is None:
            return default
        return cell.get("speed_limit", default)

    def passing_allowed(self, position: int) -> bool:
        cell = self.get_cell(position)
        if cell is None:
            return True
        return cell.get("passing_allowed", True)

    def is_turn(self, position: int) -> bool:
        cell = self.get_cell(position)
        if cell is None:
            return False
        return cell.get("type", "straight") == "turn"
    
    def get_inside_lane(self, position: int) -> int | None:
        cell = self.get_cell(position)
        if cell is None:
            return None
        return cell.get("inside_lane", None)

    def is_finished(self, car) -> bool:
        return car.position >= self.length - 1