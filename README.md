# F1 Race Start Simulation

A bio-inspired computing project that simulates a simplified Formula 1-style race environment using **cellular automata**, **evolutionary algorithms**, and **collective behavior systems**.

The goal of this project is to model how multiple cars interact at race start and through early track sections, including acceleration, braking, overtaking, slipstreaming, lane choice, and pack behavior. The simulation is inspired by real F1 racing dynamics and by class topics in bio-inspired computation.

## Project Overview

This project focuses on three main ideas:

- **Cellular automata** to model local car behavior such as moving forward, slowing down, avoiding collisions, and passing.
- **Evolutionary systems / genetic algorithms** to optimize driving style parameters such as braking aggressiveness, preferred spacing, and overtaking tendencies.
- **Collective systems** to model emergent group effects such as traffic buildup, raceline convergence, and slipstreaming.

Rather than building a fully realistic motorsport simulator, this project aims to create a simplified but meaningful environment where complex race behavior can emerge from relatively simple rules.

## Core Features

- 2D race track representation
- Multiple cars on track at once
- Grid-based or lane-based race start simulation
- Cellular automata update rules for car decisions
- Slipstream effects between nearby cars
- Raceline preference and convergence
- Overtaking and blocking behavior
- Traffic jams and pack dynamics
- Evolutionary tuning of driver/car parameters
- Visualization of the simulation over time
- Metrics for comparing strategies and outcomes

## Main Questions the Project Explores

- How much realistic racing behavior can emerge from simple local rules?
- Can cars evolve more effective braking and passing strategies?
- How do slipstreams and pack behavior affect race outcomes?
- What tradeoffs emerge between aggressive and conservative driving styles?
- Can an optimal racing line emerge naturally from repeated simulation?

## Repository Structure

```text
f1-race-sim/
│
├── README.md
├── requirements.txt
├── main.py
│
├── config/
│   └── simulation_config.py
│
├── src/
│   ├── track/
│   │   ├── track.py
│   │   └── track_generator.py
│   │
│   ├── cars/
│   │   ├── car.py
│   │   ├── driver_profile.py
│   │   └── population.py
│   │
│   ├── simulation/
│   │   ├── race_simulation.py
│   │   ├── cellular_automata.py
│   │   ├── collision_logic.py
│   │   └── slipstream.py
│   │
│   ├── evolution/
│   │   ├── genetic_algorithm.py
│   │   ├── fitness.py
│   │   └── mutation.py
│   │
│   ├── visualization/
│   │   ├── renderer.py
│   │   ├── animation.py
│   │   └── plotting.py
│   │
│   └── utils/
│       ├── helpers.py
│       └── constants.py
│
├── experiments/
│   ├── baseline_run.py
│   ├── ga_tuning_run.py
│   └── compare_strategies.py
│
├── outputs/
│   ├── plots/
│   ├── logs/
│   └── videos/
│
└── docs/
    ├── design_notes.md
    └── final_report.md
```

## File and Folder Descriptions

### `main.py`
Entry point for running the simulation. This should initialize the track, cars, simulation rules, and optional visualization.

### `config/`
Stores adjustable parameters such as:
- number of cars
- timestep count
- track size
- maximum speed
- braking thresholds
- slipstream strength
- mutation rate
- crossover rate

### `src/track/`
Contains track-related code.

- `track.py`: defines the track layout and its lanes or grid cells
- `track_generator.py`: optional helper for building straightaways, turns, and custom layouts

### `src/cars/`
Defines the cars and their behavior parameters.

- `car.py`: individual car state such as position, velocity, lane, and status
- `driver_profile.py`: stores behavior traits like aggression, braking tendency, and overtaking willingness
- `population.py`: manages collections of cars for simulations and evolution

### `src/simulation/`
Contains the core simulation logic.

- `race_simulation.py`: main update loop
- `cellular_automata.py`: local movement rules for cars
- `collision_logic.py`: determines unsafe occupancy and prevents overlapping moves
- `slipstream.py`: computes drafting effects from nearby lead cars

### `src/evolution/`
Handles optimization of driver behavior.

- `genetic_algorithm.py`: selection, crossover, and generation updates
- `fitness.py`: defines how performance is scored
- `mutation.py`: applies random changes to driver parameters

### `src/visualization/`
Responsible for displaying and analyzing the simulation.

- `renderer.py`: draws the track and cars
- `animation.py`: runs time-based animation of race steps
- `plotting.py`: creates summary plots and comparisons

### `experiments/`
Contains scripts for running focused studies.

- `baseline_run.py`: simulation without evolutionary tuning
- `ga_tuning_run.py`: simulation with genetic algorithm optimization
- `compare_strategies.py`: compares driver profiles or rule variants

### `outputs/`
Stores generated artifacts such as:
- performance plots
- logs
- saved simulation videos
- experiment results

### `docs/`
Project documentation, notes, and final writeup.

## Suggested Development Order

A good way to build the project is in stages:

### 1. Build the track and car model
Start with:
- track representation
- car class
- simple forward movement

At this stage, cars can just move on a straight track with no passing.

### 2. Add cellular automata rules
Implement local update rules such as:
- accelerate if space ahead is open
- slow down if another car is too close
- change lane or pass if blocked
- maintain safe spacing

This gives the project its first meaningful race behavior.

### 3. Add race interactions
Introduce:
- collision avoidance
- overtaking opportunities
- slipstream bonuses
- raceline preference

This is where pack behavior starts to emerge.

### 4. Add visualization
Display:
- car positions over time
- lane occupancy
- congestion zones
- speed changes

Visualization makes it much easier to debug and explain the simulation.

### 5. Add evolutionary optimization
Use a genetic algorithm to tune driver or car parameters such as:
- aggression
- reaction distance
- braking threshold
- slipstream sensitivity
- lane-change willingness

### 6. Run experiments and compare outcomes
Measure things like:
- average finishing time
- number of overtakes
- collision rate
- pack density
- success of aggressive vs. conservative strategies

## Example Simulation Logic

A simplified car update might work like this:

1. Check distance to the car ahead
2. If enough space exists, accelerate
3. If space is limited, brake
4. If blocked and another lane is open, attempt overtake
5. If behind another car, gain a slipstream bonus
6. Update position for the next timestep

This rule set is simple, but when many cars follow it at once, more complex patterns can emerge.

## Evolutionary Component

The evolutionary system can treat each driver as a parameter set, for example:

- aggression: how willing the driver is to attempt overtakes
- braking sensitivity: how early the driver slows down
- spacing preference: desired gap to the next car
- slipstream preference: how strongly the driver tries to stay in a draft
- lane bias: preference for inside, outside, or optimal line

A fitness function might reward:
- fast completion time
- successful overtakes
- few collisions
- efficient use of track space

Over multiple generations, the simulation can test whether better driving styles emerge.

## Possible Metrics

The following metrics could be useful for analysis:

- average lap or sector time
- number of overtakes
- average speed
- collision count
- lane changes per car
- congestion frequency
- pack size
- percentage of time spent in slipstream
- best evolved fitness over generations

## Tools and Libraries

Possible Python libraries for this project:

- `numpy` for numerical operations
- `matplotlib` for plotting and simple visualization
- `pygame` for interactive 2D rendering
- `random` for stochastic behavior
- `dataclasses` for clean object models

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/f1-race-sim.git
cd f1-race-sim
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

To run the main simulation:

```bash
python main.py
```

To run a specific experiment:

```bash
python experiments/baseline_run.py
```

or

```bash
python experiments/ga_tuning_run.py
```

## Current Status

Planned system components include:

- [ ] Track representation
- [ ] Car and driver classes
- [ ] Cellular automata movement rules
- [ ] Collision avoidance
- [ ] Slipstream behavior
- [ ] Overtaking logic
- [ ] Visualization
- [ ] Evolutionary optimization
- [ ] Experiment scripts
- [ ] Final analysis and report

## Future Extensions

Potential improvements after the base version:

- curved track geometry
- weather or grip effects
- tire wear and pit strategy
- different car archetypes
- team strategy behavior
- reinforcement learning comparison
- more realistic F1-style race rules

## Authors

Ethan Dietrich  
William Armentrout

## Course Context

This project was created for a bio-inspired computing course and is intended to demonstrate how ideas from:
- cellular systems
- collective behavior
- evolutionary computation

can be applied to a racing simulation scenario.

## Summary

This project combines simple local racing rules with bio-inspired optimization and group behavior to model a race start scenario in a Formula 1-inspired environment. The emphasis is not on full physical realism, but on showing how complex behavior can emerge from rule-based systems and evolutionary adaptation.
