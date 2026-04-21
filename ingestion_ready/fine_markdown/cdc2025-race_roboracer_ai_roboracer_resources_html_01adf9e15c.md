# RoboRacer Resources

## Build

The RoboRacer Autonomous Vehicle System is an open-source platform for autonomous systems research and education on a 1:10 scale. It includes sensors and computation power for autonomous driving algorithms. To participate in the in-person competition, you must bring your own RoboRacer racecar. Detailed build instructions, including videos, are available at: [RoboRacer Build Instructions](https://roboracer.ai/build.html)

## Simulation

Heavy development in simulation is crucial for evaluating autonomous driving algorithms before deploying them on physical vehicles. We offer several simulation environments:

*   **RoboRacer Gym**: An asynchronous, 2D Python simulator that runs faster than real-time (30x). It provides realistic vehicle simulation, collision detection, supports multiple vehicle instances, and publishes laser scan and odometry data.
*   **RoboRacer ROS Simulator**: This simulator provides ROS messages from the RoboRacer car within a simulation environment, useful for close vehicle development.

## Digital Twin

The [AutoDRIVE Simulator](https://autodrive-ecosystem.github.io/) allows you to simulate high-fidelity 3D digital twins of the RoboRacer racecar on virtual racetracks in real-time. It features photorealistic graphics, high-fidelity vehicle dynamics, and physically accurate sensor/actuator models to bridge the sim-to-real gap. The simulator has a track record of enabling zero-shot sim2real transfer of autonomy algorithms. It supports single and multi-agent racing scenarios (human vs. human, AI vs. AI, human vs. AI) and offers various APIs for algorithm development and HMIs for real-time interaction. You can use this simulator to prototype algorithms before deploying them on physical vehicles. AutoDRIVE Simulator is open-source and customizable.

## Autonomous Racing

For those new to autonomous racing, we provide learning resources:

*   The complete material from the RoboRacer Penn course is available online at [RoboRacer Learn](https://roboracer.ai/learn.html). This course covers autonomous driving foundations, RoboRacer car tutorials, and autonomous racing techniques like raceline finding.
*   All lectures are recorded and can be found on YouTube at the [RoboRacer Autonomous Racing Course](https://youtu.be/zENhppcxwzY).
