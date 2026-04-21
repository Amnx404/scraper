Skip to content

# Technical Guide

This document describes the technical details of the competition framework for the RoboRacer Sim Racing League. It covers details pertaining to the simulator and devkit, as well as important aspects of the submission system, process, and evaluation.

**Warning:** It is expected that teams have sufficient background knowledge in autonomous racing, programming languages (Python, C++, etc.), frameworks (ROS 2), containerization (Docker), and version control (Git). Extensive technical support cannot be provided by the organizers.

**Note:** The **only** vehicle allowed for this competition is the **RoboRacer**, and the **only** API allowed is **ROS 2**.

Please see the accompanying video for a step-by-step tutorial on setting up and using the competition framework.

## 1. AutoDRIVE Simulator

AutoDRIVE Simulator (part of the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io)) is an autonomy-oriented tool for simulating vehicle and environment digital twins. It prioritizes both backend physics and frontend graphics for high-fidelity, real-time simulation. The framework is modular, object-oriented, and supports CPU multi-threading and GPU instancing for parallel processing, with cross-platform compatibility.

For the RoboRacer Sim Racing League, each team will receive a standardized simulation setup, including a digital twin of the RoboRacer vehicle and the Porto racetrack within the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator).

### 1.1. System Requirements

**Minimum Requirements:**

*   **Platform:** Ubuntu 20.04+, Windows 10+, macOS 10.14+
*   **Processor:** Quad-core CPU (e.g., Intel Core i5 or AMD Ryzen 5)
*   **Memory:** 8 GB RAM
*   **Graphics:** Integrated graphics (e.g., Intel HD Graphics) or low-end discrete GPU (e.g., NVIDIA GeForce GTX 1050) with 2 GB VRAM
*   **Storage:** 10 GB free disk space
*   **Display:** 1280x720 px resolution, 60 Hz refresh rate
*   **Network:** Stable internet connection (1 Mbps)

**Recommended Requirements:**

*   **Platform:** Ubuntu 20.04/22.04, Windows 10/11
*   **Processor:** Octa-core CPU (e.g., Intel Core i7 or AMD Ryzen 7)
*   **Memory:** 16 GB RAM
*   **Graphics:** Mid-range discrete GPU (e.g., NVIDIA GeForce GTX 1660 or RTX 2060) with 4+ GB VRAM
*   **Storage:** 20 GB free disk space
*   **Display:** 1920x1080 px resolution, 144 Hz refresh rate
*   **Network:** Fast internet connection (10 Mbps)

**Info:** The organizers will use a workstation with an Intel Core i9 14th Gen 14900K CPU, NVIDIA GeForce RTX 4090 GPU, and 64 GB RAM for running the competition framework, including the simulator, devkit, screen recorder, and data logger. Develop your algorithms considering these computational requirements.

### 1.2. User Interface

The AutoDRIVE Simulator GUI includes a toolbar with two panels: **Menu** and **Heads-Up Display (HUD)**.

#### 1.2.1. Menu Panel

*   **IP Address Field:** IP address of the machine running the devkit (default: 127.0.0.1).
*   **Port Number Field:** Port number for the devkit (default: 4567).
*   **Connection Button:** Establishes connection with the devkit.
*   **Driving Mode Button:** Toggles between Manual and Autonomous driving modes.
*   **Camera View Button:** Toggles camera view between Driver’s Eye, Bird’s Eye, and God’s Eye.
*   **Graphics Quality Button:** Toggles graphics quality between Low, High, and Ultra.
*   **Scene Light Button:** Enables/disables environmental lighting.
*   **Reset Button:** Resets the simulator to initial conditions.
*   **Quit Button:** Exits the simulator application.

#### 1.2.2. HUD Panel

*   **Simulation Time:** Time since simulation start (HH:MM:SS).
*   **Frame Rate:** Running average FPS (Hz).
*   **Driving Mode:** Current driving mode (Manual or Autonomous).
*   **Gear:** Vehicle gear (D or R).
*   **Speed:** Forward velocity (m/s).
*   **Throttle:** Instantaneous throttle input (%).
*   **Steering:** Instantaneous steering angle (rad).
*   **Encoder Ticks:** Ticks from rear-left and rear-right incremental encoders.
*   **IPS Data:** Vehicle position [x, y, z] (m).
*   **IMU Data:** Orientation [x, y, z] (rad), angular velocity [x, y, z] (rad/s), linear acceleration [x, y, z] (m/s²).
*   **LIDAR Measurement:** 270° FOV 2D LIDAR range measurements (m).
*   **Camera Preview:** Raw image from the front camera.
*   **Race Telemetry:** Current lap time, last lap time, best lap time, lap count, collision count.
*   **Data Recorder:** Saves time-synchronized simulation data.

#### 1.2.3. Data Recorder

The data recorder exports simulation data at approximately 30 Hz. Data is saved in `CSV` format, with raw camera frames as timestamped `JPG` files.

**DATA** | timestamp | throttle | steering | leftTicks | rightTicks | posX | posY | posZ | roll | pitch | yaw | linX | linY | linZ | angX | angY | angZ | accX | accY | accZ | camera | lidar
**UNIT** | yyyy_MM_dd_HH_mm_ss_fff | norm% | rad | count | count | m | m | m | rad | rad | rad | m/s | m/s | m/s | rad/s | rad/s | rad/s | m/s^2 | m/s^2 | m/s^2 | img_path | array(float)

Recording is triggered by the `Record Data` button in the HUD or the `R` hotkey. The first trigger prompts for a save directory. Subsequent triggers start/stop recording.

**Info:** When selecting a directory for data storage, click the directory once; do not double-click to enter it.

**Warning:** The actual recording rate depends on compute power and OS scheduler, but data will remain time-synchronized.

**Note:** Consecutive recordings without resetting the simulator will append data to the same files. To avoid this, reset or restart the simulator and specify a new directory.

### 1.3. Vehicle

Vehicles in AutoDRIVE Simulator are simulated with attention to rigid body dynamics, suspension, actuators, and tire dynamics. The simulator detects mesh-mesh interference and computes contact forces, friction, momentum transfer, and drag. It also offers physically-based sensor simulation.

#### 1.3.1. Transforms

All coordinate frames are right-handed (red=x, green=y, blue=z).

FRAME | x | y | z | R | P | Y
`left_encoder` | 0.0 | 0.118 | 0.0 | 0.0 |  | 0.0
`right_encoder` | 0.0 | -0.118 | 0.0 | 0.0 |  | 0.0
`ips` | 0.08 | 0.0 | 0.055 | 0.0 | 0.0 | 0.0
`imu` | 0.08 | 0.0 | 0.055 | 0.0 | 0.0 | 0.0
`lidar` | 0.2733 | 0.0 | 0.096 | 0.0 | 0.0 | 0.0
`front_camera` | -0.015 | 0.0 | 0.15 | 0.0 | 10.0 | 0.0
`front_left_wheel` | 0.33 | 0.118 | 0.0 | 0.0 | 0.0 |
`front_right_wheel` | 0.33 | -0.118 | 0.0 | 0.0 | 0.0 |
`rear_left_wheel` | 0.0 | 0.118 | 0.0 | 0.0 |  | 0.0
`rear_right_wheel` | 0.0 | -0.118 | 0.0 | 0.0 |  | 0.0

**Note:** Frame transforms are defined with respect to the vehicle's local frame (`roboracer_1`), located at the center of the rear axle (x-axis forward, y-axis left, z-axis up).

#### 1.3.2. Vehicle Dynamics

The vehicle model combines a rigid body and sprung masses. Suspension forces are calculated based on spring and damping coefficients. Tire forces are computed using a friction curve approximated by a two-piece cubic spline.

VEHICLE PARAMETERS |
---|---
Car Length | 0.5000 m
Car Width | 0.2700 m
Wheelbase | 0.3240 m
Track Width | 0.2360 m
Front Overhang | 0.0900 m
Rear Overhang | 0.0800 m
Wheel Radius | 0.0590 m
Wheel Width | 0.0450 m
Total Mass | 3.906 kg
Sprung Mass | 3.470 kg
Unsprung Mass | 0.436 kg
Center of Mass | X: 0.15532 m, Y: 0.00000 m, Z: 0.01434 m
Suspension Spring | 500 N/m
Suspension Damper | 100 Ns/m
Longitudinal Tire Limits (Slip, Force) | Extremum: (0.15, 0.72), Asymptote: (0.25, 0.464)
Lateral Tire Limits (Slip, Force) | Extremum: (0.01, 1.00), Asymptote: (0.10, 0.500)

#### 1.3.3. Actuator Dynamics

Driving actuators apply torque to the wheels. Steering is handled by an Ackermann steering actuator.

DRIVING ACTUATOR |
---|---
Drive Type | All wheel drive
Throttle Limits | [-1,1]
Motor Torque | 428 Nm
Vehicle Top Speed | 22.88 m/s

STEERING ACTUATOR |
---|---
Steer Type | Ackermann steering
Steering Limits | [-1,1]
Steering Angle Limits | [-0.5236,0.5236] rad
Steering Rate | 3.2 rad/s

#### 1.3.4. Sensor Physics

*   **Throttle and Steering Sensors:** Simulated with instantaneous feedback.
*   **Incremental Encoders:** Measure rear wheel rotation.
    THROTTLE SENSOR |
    ---|---
    Type | Virtual Sensor
    Class | Actuator Feedback
    Supported Outputs | [-1, 1]
    STEERING SENSOR |
    ---|---
    Type | Virtual Sensor
    Class | Actuator Feedback
    Supported Outputs | [-1, 1]
    ENCODERS |
    ---|---
    Type | Simulated Sensor
    Class | Proprioceptive
    Pulses Per Revolution | 16
    Conversion Ratio | 120
    Supported Outputs | Ticks
    Angles
*   **IPS and IMU:** Simulated based on rigid-body transform updates. IPS provides position [x,y,z], IMU provides linear accelerations, angular velocities, and orientation.
    IPS |
    ---|---
    Type | Simulated Sensor
    Class | Proprioceptive
    Supported Outputs | Position Vector [x, y, z] m
    IMU |
    ---|---
    Type | Simulated Sensor
    Class | Proprioceptive
    Supported Outputs | Orientation Quaternion [x, y, z, w], Orientation Euler Angles [x, y, z] rad, Angular Velocity Vector [x, y, z] rad/s, Linear Acceleration Vector [x, y, z] m/s2
*   **LIDAR:** Simulates range measurements using iterative ray-casting.
    LIDAR |
    ---|---
    Type | Simulated Sensor
    Class | Exteroceptive
    Scan Rate | 40 Hz
    Angular Resolution | 0.25 deg
    Measurements Per Scan | 1080
    Minimum Linear Range | 0.06 m
    Maximum Linear Range | 10.0 m
    Minimum Angular Range | -135 deg
    Maximum Angular Range | +135 deg
    Supported Outputs | Range Array (m), Intensity Array
*   **Cameras:** Parameterized by focal length, sensor size, resolution, and clipping planes. Rendering involves view and projection matrices, followed by perspective division and rasterization. Post-processing simulates lens and film effects.
    CAMERA |
    ---|---
    Type | Simulated Sensor
    Class | Exteroceptive
    Field of View | 48.8311 deg
    Sensor Size | X: 3.68 mm, Y: 2.76 mm
    Shutter Speed | 0.005 s
    Focal Length | 3.04 m
    Aperture | f/16
    Target Image | 16:9 (75% JPG Compression)
    Supported Outputs | RGB Image

### 1.4. Environment

Environments can be developed using AutoDRIVE's IDK or imported from third-party tools. The Porto racetrack is a digital twin created from a real-world track's occupancy grid map.

#### 1.4.1. Transforms

Coordinate frames are right-handed (red=x, green=y, blue=z).

FRAME | x | y | z | R | P | Y
`world` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0
`roboracer_1` |  |  |  |  |  |

**Note:** Transforms are defined with respect to the global `world` frame. `roboracer_1` defines the ground-truth pose of the vehicle.

**Warning:** The location of the fixed environmental frame may differ depending on the racetrack version.

#### 1.4.2. Size and Structure

*   The simulated racetrack dimensions and materials will mimic physical RoboRacer tracks.
*   The track will fit within approximately 30x10 m².
*   The border will be constructed from air ducts (~33 cm diameter).
*   The track width will be at least 3 car widths (90 cm).

#### 1.4.3. Design and Features

*   The road surface will have properties of polished concrete, making perception challenging.
*   Gaps in the track border may allow LiDAR beams to pass through, creating apparent obstacle-free spaces.
*   The racetrack may include straights, chicanes, bifurcations, and obstacles.

**Warning:** The racetrack is subject to change across different competition phases and iterations. Participants will be informed of any track changes.

## 2. AutoDRIVE Devkit

AutoDRIVE Devkit (part of the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io)) provides APIs, HMIs, languages, libraries, and tools for developing autonomous driving and traffic management algorithms. It supports targeting algorithms to both the simulator and a physical testbed, and facilitates both local and distributed computing.

For the RoboRacer Sim Racing League, teams will use a standardized ROS 2 API implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to develop their autonomy algorithms. Teams must develop perception, planning, and control algorithms to process sensor data from the simulator and generate control commands.

### 2.1. System Requirements

**Minimum Requirements:**

*   **Platform:** Ubuntu 20.04, Windows 10 (VS 2019), macOS 10.14
*   **Processor:** Dual-core CPU (e.g., Intel Core i3 or AMD Ryzen 3)
*   **Memory:** 4 GB RAM
*   **Graphics:** Integrated graphics (e.g., Intel HD Graphics)
*   **Storage:** 5 GB free disk space
*   **Display:** 1280x720 px resolution, 60 Hz refresh rate
*   **Network:** Stable internet connection (1 Mbps)

**Recommended Requirements:**

*   **Platform:** Ubuntu 20.04
*   **Processor:** Quad-core CPU (e.g., Intel Core i5 or AMD Ryzen 5)
*   **Memory:** 8 GB RAM
*   **Graphics:** Low-end discrete GPU (e.g., NVIDIA GeForce GT 1030)
*   **Storage:** 10 GB free disk space
*   **Display:** 1920x1080 px resolution, 60 Hz refresh rate
*   **Network:** Fast internet connection (10 Mbps)

**Info:** The organizers will use a high-end workstation for the competition framework. Develop your algorithms considering these computational requirements.

### 2.2. Package Structure

The ROS 2 package structure for the AutoDRIVE Devkit is as follows:

```
autodrive_devkit
├───README.md
├───package.xml
├───setup.cfg
├───setup.py
├───requirements_python_3.8.txt
├───requirements_python_3.9.txt
├───requirements_python_3.10.txt
│
├───autodrive_roboracer
│   └───autodrive_bridge.py
│   └───config.py
│   └───teleop_keyboard.py
│   └───__init__.py
│
├───launch
│   └───bringup_headless.launch.py
│   └───bringup_graphics.launch.py
│
├───resource
│   └───autodrive_roboracer
│
├───
│   └───autodrive_roboracer.
│
└───test
    └───test_copyright.py
    └───test_flake8.py
    └───test_pep257.py
```

**Warning:** Modifying the `autodrive_roboracer` package is **not permitted**. Create your own separate package(s) for your algorithms.

### 2.3. Data Streams

Data streams are exposed as ROS 2 topics via the AutoDRIVE Devkit.

TOPIC | TYPE | MESSAGE | ACCESS
---|---|---|---
`/autodrive/roboracer_1/lidar` | Sensor | `sensor_msgs/msg/LaserScan` | Input
`/autodrive/roboracer_1/front_camera` | Sensor | `sensor_msgs/msg/Image` | Input
`/autodrive/roboracer_1/imu` | Sensor | `sensor_msgs/msg/Imu` | Input
`/autodrive/roboracer_1/ips` | Sensor | `geometry_msgs/msg/Point` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/left_encoder` | Sensor | `sensor_msgs/msg/JointState` | Input
`/autodrive/roboracer_1/right_encoder` | Sensor | `sensor_msgs/msg/JointState` | Input
`/autodrive/roboracer_1/odom` | Debugging | `nav_msgs/msg/Odometry` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/steering` | Sensor | `std_msgs/msg/Float32` | Input
`/autodrive/roboracer_1/steering_command` | Actuator | `std_msgs/msg/Float32` | Output
`/autodrive/roboracer_1/throttle` | Sensor | `std_msgs/msg/Float32` | Input
`/autodrive/roboracer_1/throttle_command` | Actuator | `std_msgs/msg/Float32` | Output
`/autodrive/reset_command` | Debugging | `std_msgs/msg/Bool` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/collision_count` | Debugging | `std_msgs/msg/Int32` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/lap_count` | Debugging | `std_msgs/msg/Int32` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/lap_time` | Debugging | `std_msgs/msg/Float32` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/best_lap_time` | Debugging | `std_msgs/msg/Float32` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/autodrive/roboracer_1/last_lap_time` | Debugging | `std_msgs/msg/Float32` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted
`/tf` | Debugging | `tf2_msgs/msg/TFMessage` | ![⚠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/26a0.svg) Restricted

**Warning:** Restricted topics can be used for debugging but not during autonomous racing at run-time.

**Info:** To reset the simulation, publish `True` to `/autodrive/reset_command`. Remember to set it back to `False`.

## 3. Competition Submission

The RoboRacer Sim Racing League uses a containerization workflow for reproducible evaluation. Teams must submit a containerized version of their autonomous racing software stack.

### 3.1. Container Setup

1.  Install [Docker](https://docs.docker.com/engine/install).
2.  Install NVIDIA GPU Drivers and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html).
3.  Pull the AutoDRIVE Simulator Docker image:
    ```bash
    docker pull autodriveecosystem/autodrive_roboracer_sim:<TAG>
    ```
4.  Pull the AutoDRIVE Devkit Docker image:
    ```bash
    docker pull autodriveecosystem/autodrive_roboracer_api:<TAG>
    ```

**Note:** Pay attention to the `<TAG>` (e.g., `explore`, `practice`, `compete`, or `<YEAR>-<EVENT>-<PHASE>`).

### 3.2. Container Execution

1.  Enable display forwarding for the simulator:
    ```bash
    xhost local:root
    ```
2.  Run the simulator container:
    ```bash
    docker run --name autodrive_roboracer_sim --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_roboracer_sim:<TAG>
    ```
3.  [OPTIONAL] Start additional bash sessions within the simulator container:
    ```bash
    docker exec -it autodrive_roboracer_sim bash
    ```
4.  Enable display forwarding for the devkit:
    ```bash
    xhost local:root
    ```
5.  Run the devkit container:
    ```bash
    docker run --name autodrive_roboracer_api --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_roboracer_api:<TAG>
    ```
6.  [OPTIONAL] Start additional bash sessions within the devkit container:
    ```bash
    docker exec -it autodrive_roboracer_api bash
    ```

#### 3.2.1. GUI Mode Operations

1.  Launch AutoDRIVE Simulator in `graphics` mode:
    ```bash
    ./AutoDRIVE\ Simulator.x86_64
    ```
2.  Launch AutoDRIVE Devkit in `graphics` mode:
    ```bash
    ros2 launch autodrive_roboracer bringup_graphics.launch.py
    ```
3.  Configure the simulator GUI menu:
    *   Enter the IP address of the devkit machine.
    *   Click the `Connection` button.
    *   Toggle the `Driving Mode` between `Manual` and `Autonomous`.

#### 3.2.2. Headless Mode Operations

1.  Launch AutoDRIVE Simulator in `no-graphics` mode:
    ```bash
    ./AutoDRIVE\ Simulator.x86_64 -batchmode -nographics -ip 127.0.0.1 -port 4567
    ```
2.  Launch AutoDRIVE Simulator in `headless` mode:
    ```bash
    xvfb-run ./AutoDRIVE\ Simulator.x86_64 -ip 127.0.0.1 -port 4567
    ```
3.  Launch AutoDRIVE Devkit in `headless` mode:
    ```bash
    ros2 launch autodrive_roboracer bringup_headless.launch.py
    ```

**Info:** You can mix `graphics` and `headless/no-graphics` modes for the simulator and devkit.

#### 3.2.3. Distributed Computing Mode

Run the simulator and devkit on separate machines connected via a network. Configure the simulator with the devkit's IP address. This approach allows for workload distribution and better performance. It's also possible to use a physical RoboRacer vehicle with the devkit for a hardware-in-the-loop (HIL) setup.

**Tip:** If GPU access with Docker is problematic, run the simulator locally and the devkit in a container.

### 3.3. Container Troubleshooting

1.  Access a running container:
    ```bash
    docker exec -it <CONTAINER NAME> bash
    ```
2.  Exit a bash session:
    ```bash
    exit
    ```
3.  Kill a container:
    ```bash
    docker kill <CONTAINER NAME>
    ```
4.  Remove a container:
    ```bash
    docker rm <CONTAINER NAME>
    ```
5.  Check Docker disk usage:
    ```bash
    docker system df
    ```
6.  Prune unused Docker resources:
    ```bash
    docker system prune -a
    ```
7.  Switch to the default Docker context if needed:
    ```bash
    docker context ls
    docker context use default
    ```

**Warning:** Docker Desktop is not recommended on Linux.

**Info:** For more information on containerization, visit [docker.com](https://www.docker.com).

### 3.4. Algorithm Development

Create your ROS 2 package(s) within the devkit container, separate from the `autodrive_roboracer` package. Refer to the data streams documentation for development.

**Tip:** Develop and test your algorithms locally first, then containerize them for final testing and submission.

### 3.5. Container Submission

Ensure your submitted container automatically starts all necessary nodes. The simulated vehicle should start running upon clicking the `Connection Button`. Include all setup commands in the `entrypoint` script (`autodrive_devkit.sh`). Do not use `~/.bashrc` for automatic execution. Provide detailed instructions in your Docker Hub repository.

1.  Run your image in a container:
    ```bash
    xhost local:root
    docker run --name autodrive_roboracer_api --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_roboracer_api:<TAG>
    ```
2.  Note the `CONTAINER ID` from `docker ps -a`.
3.  Commit changes:
    ```bash
    docker commit -m "<Sample commit message>" -a "<USERNAME>" <CONTAINER ID> <username>/<image_name>:<TAG>
    ```
4.  Log in to DockerHub:
    ```bash
    docker login
    ```
5.  Push the container:
    ```bash
    docker push <username>/<image_name>:<TAG>
    ```
6.  Submit the link to your DockerHub repository.

## 4. Citation

We encourage you to cite the following papers if you use any part of the competition framework:

*   **AutoDRIVE: A Comprehensive, Flexible and Integrated Digital Twin Ecosystem for Enhancing Autonomous Driving Research and Education**
    *   Published in MDPI Robotics.
    *   [Link](https://www.mdpi.com/2218-6581/12/3/77)
    *   BibTeX:
        ```bibtex
        @article{AutoDRIVE-Ecosystem-2023,
        author = {Samak, Tanmay and Samak, Chinmay and Kandhasamy, Sivanathan and Krovi, Venkat and Xie, Ming},
        title = {AutoDRIVE: A Comprehensive, Flexible and Integrated Digital Twin Ecosystem for Autonomous Driving Research & Education},
        journal = {Robotics},
        volume = {12},
        year = {2023},
        number = {3},
        article-number = {77},
        url = {https://www.mdpi.com/2218-6581/12/3/77},
        issn = {2218-6581},
        doi = {10.3390/robotics12030077}
        }
        ```

*   **AutoDRIVE Simulator: A Simulator for Scaled Autonomous Vehicle Research and Education**
    *   Published at 2021 International Conference on Control, Robotics and Intelligent System (CCRIS).
    *   [Link](https://dl.acm.org/doi/abs/10.1145/3483845.3483846)
    *   BibTeX:
        ```bibtex
        @inproceedings{AutoDRIVE-Simulator-2021,
        author = {Samak, Tanmay Vilas and Samak, Chinmay Vilas and Xie, Ming},
        title = {AutoDRIVE Simulator: A Simulator for Scaled Autonomous Vehicle Research and Education},
        year = {2021},
        isbn = {9781450390453},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3483845.3483846},
        doi = {10.1145/3483845.3483846},
        booktitle = {2021 2nd International Conference on Control, Robotics and Intelligent System},
        pages = {1–5},
        numpages = {5},
        location = {Qingdao, China},
        series = {CCRIS'21}
        }
        ```

Back to top
