class Car:
    def __init__(self, car_id: int, lane: int, position: int = 0, speed: int = 0, max_speed: int = 5, 
                 aggression: float = 0.5, braking_sensitivity: float = 0.5, reaction_distance: float = 0.5, line_preference: float = 0.5):
        self.car_id = car_id
        self.lane = lane
        self.position = position
        self.speed = speed
        self.max_speed = max_speed

        self.aggression = aggression
        self.braking_sensitivity = braking_sensitivity
        self.reaction_distance = reaction_distance
        self.line_preference = line_preference
    
    def update(self):
        """
        Updates the position of the car based on current:
        - position
        - speed
        """
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        
        self.position += self.speed

    def __repr__(self):
        return f"Car(id={self.car_id} | lane={self.lane} | pos={self.position} | speed={self.speed})"