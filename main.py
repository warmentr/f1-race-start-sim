import time
from src.track import Track
from src.car import Car
from src.simulation import Simulation

def main():
    track = Track(length=200, num_lanes=3)

    cars = [
        Car(car_id=1, lane=0, position=0, speed=0, max_speed=6),
        Car(car_id=2, lane=0, position=6, speed=0, max_speed=3),
        Car(car_id=3, lane=1, position=2, speed=0, max_speed=4),
        Car(car_id=4, lane=0, position=0, speed=0, max_speed=5),
        Car(car_id=5, lane=0, position=6, speed=0, max_speed=2),
        Car(car_id=6, lane=1, position=2, speed=0, max_speed=4)
    ]

    sim = Simulation(track, cars, safe_gap=1)

    for _ in range(50):
        print(f"\nTime step {sim.time_step}")
        sim.draw()
        for car in sim.cars:
            print(car)
        
        sim.step()
        time.sleep(0.5)

if __name__ == "__main__":
    main()