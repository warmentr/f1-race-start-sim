class Car:
    def __init__(self, car_id: int, lane: int, position: int = 0, speed: int = 0, max_speed: int = 5):
        self.car_id = car_id
        self.lane = lane
        self.position = position
        self.speed = speed
        self.max_speed = max_speed
    
    def update(self):
        """
        Updates the position of the car based on current:
        - position
        - speed
        - acceleration
        """
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        
        self.position += self.speed

    def __repr__(self):
        return f"Car(id={self.car_id} | lane={self.lane} | pos={self.position:.2f} | speed={self.speed:.2f})"