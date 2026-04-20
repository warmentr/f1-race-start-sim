import time
from src.track import Track
from src.car import Car
from src.simulation import Simulation

def build_track():
    cells = (
        [{"type": "straight", "speed_limit": 5, "passing_allowed": True} for _ in range(15)] +
        [{"type": "turn", "speed_limit": 2, "passing_allowed": False, "inside_lane": 4} for _ in range(6)] +
        [{"type": "straight", "speed_limit": 5, "passing_allowed": True} for _ in range(12)] +
        [{"type": "turn", "speed_limit": 1, "passing_allowed": False, "inside_lane": 0} for _ in range(5)] +
        [{"type": "straight", "speed_limit": 5, "passing_allowed": True} for _ in range(12)]
    )
    return Track(cells=cells, num_lanes=3)

def main():
    track = build_track()
    placement = []

    # cars = [
    #     Car(car_id=1, lane=1, position=6, speed=0, max_speed=5, line_preference=1),
    #     Car(car_id=2, lane=3, position=5, speed=0, max_speed=5, line_preference=1),
    #     Car(car_id=3, lane=1, position=4, speed=0, max_speed=5, line_preference=1),
    #     Car(car_id=4, lane=3, position=3, speed=0, max_speed=5, line_preference=1),
    #     Car(car_id=5, lane=1, position=2, speed=0, max_speed=5, line_preference=1),
    #     Car(car_id=6, lane=3, position=1, speed=0, max_speed=5, line_preference=1)
    # ]

    cars = [
        Car(1, lane=1, position=0, speed=0, max_speed=5,
        aggression=0.9, braking_sensitivity=0.2,
        reaction_distance=0.4, line_preference=0.7),

        Car(2, lane=2, position=0, speed=0, max_speed=5,
            aggression=0.3, braking_sensitivity=0.8,
            reaction_distance=0.9, line_preference=0.6),

        Car(3, lane=0, position=0, speed=0, max_speed=5,
            aggression=0.5, braking_sensitivity=0.5,
            reaction_distance=0.5, line_preference=1.0)
    ]

    sim = Simulation(track, cars, safe_gap=1)

    for _ in range(50):

        if not sim.cars:
            print("\n=== All cars have finished ===\n")
            break

        print(f"\nTime step {sim.time_step}")
        sim.draw()
        for car in sim.cars:
            print(car)
        
        sim.step()
        for car in sim.cars:
            if track.is_finished(car=car) and car.car_id not in placement:
                placement.append(car.car_id)
                cars.remove(car)
        
        time.sleep(0.5)
    
    print("\nFinal Placement\n")
    for place, car_id in enumerate(placement, start=1):
        suffix = "th"
        if place == 1:
            suffix = "st"
        elif place == 2:
            suffix = "nd"
        elif place == 3:
            suffix = "rd"

        print(f"{place}{suffix}. Car {car_id}")

if __name__ == "__main__":
    main()