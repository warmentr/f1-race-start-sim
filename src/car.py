class Car:
    def __init__(self, car_id: int, lane: int, position: int = 0, speed: int = 0, max_speed: int = 5, 
                 aggression: float = 0.5, braking_sensitivity: float = 0.5, reaction_distance: float = 0.5, line_preference: float = 0.5):
        
        self.car_id = car_id
        self.lane = lane
        self.position = position
        self.speed = speed
        self.max_speed = max_speed

        # personality traits (what will be tuned by Evolutionary Algorithm)
        self.aggression = aggression
        self.braking_sensitivity = braking_sensitivity
        self.reaction_distance = reaction_distance
        self.line_preference = line_preference

        # metrics
        self.steps_taken = 0
        self.total_speed = 0
        self.max_reached_speed = speed
        self.lane_changes = 0
        self.times_braked = 0
        self.slipstream_steps = 0
        self.turn_steps = 0
        self.stopped_steps = 0
        self.distance_traveled = 0
        self.finished = False
        self.finish_time = None
    
    def update(self):
        """
        Updates the position of the car based on current:
        - position
        - speed
        """
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        
        self.position += self.speed

    def average_speed(self) -> float:
        """
        Calculates the average speed from internal metrics and returns avg_speed as a float
        """
        if self.steps_taken == 0:
            return 0.0
        return self.total_speed / self.steps_taken
    
    def print_metrics(self):
            print(
                f"Car {self.car_id}: "
                f"steps={self.steps_taken}, "
                f"avg_speed={self.average_speed():.2f}, "
                f"max_speed={self.max_reached_speed}, "
                f"lane_changes={self.lane_changes}, "
                f"brakes={self.times_braked}, "
                f"slipstream_steps={self.slipstream_steps}, "
                f"turn_steps={self.turn_steps}, "
                f"stopped_steps={self.stopped_steps}, "
                f"distance={self.distance_traveled}, "
                f"finished={self.finished}, "
                f"finish_time={self.finish_time}"
            )

    def __repr__(self):
        return f"Car(id={self.car_id} | lane={self.lane} | pos={self.position} | speed={self.speed})"