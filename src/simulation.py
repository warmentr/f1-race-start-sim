from src.track import Track
from src.car import Car

class Simulation:
    def __init__(self, track: Track, cars: list[Car], safe_gap: int = 1):
        self.track = track
        self.cars = cars
        self.safe_gap = safe_gap
        self.time_step = 0
    
    def build_occupancy(self):
        """
        Returns a 2D grid where each cell contains either None or a car.
        grid[lane][position] = car or None
        """
        grid = [[None for _ in range(self.track.length)] for _ in range(self.track.num_lanes)]

        for car in self.cars:
            if 0 <= car.position < self.track.length:
                grid[car.lane][car.position] = car

        return grid

    def distance_to_next_car(self, grid, lane: int, position: int) -> int:
        """
        Returns number of empty cells ahead before the next car.
        If no car ahead, returns distance to end of track.
        """
        distance = 0
        for pos in range(position + 1, self.track.length):
            if grid[lane][pos] is not None:
                return distance
            distance += 1
        return distance
    
    def next_turn_info(self, car: Car, lookahead: int = 6):
        """
        Look ahead for the next turn and return:
        (turn_position, inside_lane) or (None, None)
        """
        for pos in range(car.position, min(self.track.length, car.position + lookahead + 1)):
            if self.track.is_turn(pos):
                return pos, self.track.get_inside_lane(pos)
        return None, None
    
    def lane_score(self, grid, car: Car, lane: int) -> float:
        """
        Score a lane using:
        - open space ahead
        - how close it is to the inside lane of the next turn
        """
        gap = self.distance_to_next_car(grid, lane, car.position)

        score = gap

        turn_pos, inside_lane = self.next_turn_info(car, lookahead=6)

        if turn_pos is not None and inside_lane is not None:
            lane_distance = abs(lane - inside_lane)

            # reward being close to inside lane
            score += car.line_preference * max(0, 3 - lane_distance)

            if lane == inside_lane:
                score += 2 * car.line_preference
        
        return score

    def lane_change_possible(self, grid, car: Car, target_lane: int) -> bool:
        """
        A lange change is allowed if:
        - target lane exists
        - same position in target lane is empty
        - nearby cells around target position are clear enough
        """
        if not (0 <= target_lane < self.track.num_lanes):
            return False
        
        pos = car.position

        if grid[target_lane][pos] is not None:
            return False
        
        for check_pos in range(max(0, pos - self.safe_gap), min(self.track.length, pos + self.safe_gap + 1)):
            if grid[target_lane][check_pos] is not None:
                return False
            
        return True

    def choose_lane(self, grid, car: Car) -> int:
        """
        If blocked, try changing lanes.
        Prefer a lane with more open space ahead.
        """
        current_gap = self.distance_to_next_car(grid, car.lane, car.position)

        best_lane = car.lane
        best_score = self.lane_score(grid, car, car.lane)

        for delta in (-1, 1):
            target_lane = car.lane + delta
            if self.lane_change_possible(grid, car, target_lane):
                score = self.lane_score(grid, car, target_lane)
                if score > best_score:
                    best_score = score
                    best_lane = target_lane
        
        return best_lane
    
    def upcoming_speed_limit(self, car: Car, lookahead: int = 3) -> int:
        """
        Look ahead a few cells and use the most restrictive speed limit.
        Designed to make the car break before entering turns.
        """
        limits = []
        for pos in range(car.position, min(self.track.length, car.position + lookahead + 1)):
            limits.append(self.track.get_speed_limit(pos, default=car.max_speed))
        
        if not limits:
            return car.max_speed
        
        return min(limits)
    
    def effective_turn_speed_limit(self, car: Car, lane: int, base_limit: int) -> int:
        """
        Cars in the inside lane of a turn get an advantage.
        """
        turn_pos, inside_lane = self.next_turn_info(car, lookahead=1)
        if turn_pos is not None and inside_lane is not None:
            if lane == inside_lane:
                return base_limit + 2
            
        return base_limit

    def step(self):
        """
        Apply CA rules:
        1. accelerate
        2. brake for upcoming turns
        3. if blocked, try lane change (when passing allowed)
        4. maintain safe spacing
        5. move
        """
        grid = self.build_occupancy()

        # sort cars front to back to reduce update weirdness
        ordered_cars = sorted(self.cars, key=lambda c: (c.position, c.lane), reverse=True)

        planned_updates = []

        for car in ordered_cars:
            if self.track.is_finished(car):
                planned_updates.append((car, car.lane, car.position, car.speed))
                continue

            current_position = car.position
            current_lane = car.lane
            new_lane = current_lane

             # Rule 1: accelerate
            new_speed = min(car.speed + 1, car.max_speed)

            # Rule 2: brake for turns when needed
            track_speed_limit = self.upcoming_speed_limit(car, lookahead=3)
            track_speed_limit = self.effective_turn_speed_limit(car, new_lane, track_speed_limit)
            new_speed = min(new_speed, track_speed_limit)

            # Rule 3: check traffic ahead
            gap_ahead = self.distance_to_next_car(grid, car.lane, car.position)

            if gap_ahead < new_speed or self.next_turn_info(car, lookahead=6)[0] is not None:
                if self.track.passing_allowed(current_position):
                    candidate_lane = self.choose_lane(grid, car)
                    if candidate_lane != car.lane:
                        new_lane = candidate_lane
                        gap_ahead = self.distance_to_next_car(grid, new_lane, car.position)

                        track_speed_limit = self.upcoming_speed_limit(car, lookahead=3)
                        track_speed_limit = self.effective_turn_speed_limit(car, new_lane, track_speed_limit)
                        new_speed = min(new_speed, track_speed_limit)
            
            # Rule 4: maintain safe spacing
            new_speed = min(new_speed, gap_ahead)

            # Rule 5: move
            new_position = car.position + new_speed
            if new_position >= self.track.length:
                new_position = self.track.length - 1

            planned_updates.append((car, new_lane, new_position, new_speed))

        # Resolve updates
        occupied_next = set()
        for car, new_lane, new_position, new_speed in planned_updates:
            # prevent two cars in the same cell
            while (new_lane, new_position) in occupied_next and new_position > car.position:
                new_position -= 1
                new_speed = max(0, new_position - car.position)

            occupied_next.add((new_lane, new_position))
            car.lane = new_lane
            car.position = new_position
            car.speed = new_speed

        self.time_step += 1

    def draw(self):
        """
        Create a text based depiction of the step in the simulation
        S = straight, T = turn
        """
        grid = [["." for _ in range(self.track.length)] for _ in range(self.track.num_lanes)]

        for car in self.cars:
            if 0 <= car.position < self.track.length:
                grid[car.lane][car.position] = str(car.car_id)

        guide = []
        for pos in range(self.track.length):
            guide.append("T" if self.track.is_turn(pos) else "S")
        
        print("Type  : " + "".join(guide))

        for lane_index, lane_cells in enumerate(grid):
            print(f"Lane {lane_index}: " + "".join(lane_cells))