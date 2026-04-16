import time
from src.track import Track
from src.car import Car

def draw_track(track, cars):
    """
    Creates a text based visualization of the track
    Parameters:
        track (Track): track that is being represented
        cars ([Car]): list of cars on the track
    """
    display_length = min(track.length, 60)
    line = ["."] * display_length

    for car in cars:
        pos = min(int(car.position), display_length - 1)
        line[pos] = str(car.car_id)

    print("".join(line))

def run_simulation():
    track = Track(length=100)

    cars = [
        Car(car_id=1, position=0, speed=0, acceleration=1, max_speed=5),
        Car(car_id=2, position=0, speed=0, acceleration=2, max_speed=4)
    ]

    timestep = 0
    max_steps = 30

    print("Starting simulation...\n")

    while timestep < max_steps:
        print(f"Time step {timestep}")

        all_finished = True

        for car in cars:
            if not track.is_finished(car.position):
                car.update()
            
            print(car)

            if not track.is_finished(car.position):
                all_finished = False
        
        draw_track(track, cars)
        print("-" * 40)

        if all_finished:
            print("All cars finished the track.")
            break

        timestep += 1
        time.sleep(0.5)
        

if __name__ == "__main__":
    run_simulation()