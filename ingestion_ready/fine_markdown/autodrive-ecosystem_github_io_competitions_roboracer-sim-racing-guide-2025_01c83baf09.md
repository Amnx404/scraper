Skip to content

# Technical Guide

This document describes the technical details of the competition framework for the RoboRacer Sim Racing League. It covers details pertaining to the simulator and devkit, as well as important aspects of the submission system, process, and evaluation.

**Warning:** It is expected that teams have sufficient background knowledge in autonomous racing, programming languages (Python, C++, etc.), frameworks (ROS 2), containerization (Docker), and version control (Git). Extensive technical support cannot be provided by the organizers.

**Note:** The **only** vehicle allowed for this competition is the **RoboRacer**, and the **only** API allowed is **ROS 2**.

Please see the accompanying video for a step-by-step tutorial on setting up and using the competition framework.

## 1. AutoDRIVE Simulator

AutoDRIVE Simulator (part of the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io)) is an autonomy-oriented tool for simulating vehicle and environment digital twins. It prioritizes both backend physics and frontend graphics for high-fidelity, real-time simulation. The framework is modular, object-oriented, and can leverage CPU multi-threading and GPU instancing for parallel processing, with cross-platform support.

For the RoboRacer Sim Racing League, each team will receive a standardized simulation setup, including a digital twin of the RoboRacer vehicle and the Porto racetrack, within the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator).

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
*   **Driving Mode Button:** Toggles between Manual and Autonomous driving.
*   **Camera View Button:** Toggles camera view between Driver’s Eye, Bird’s Eye, and God’s Eye.
*   **Graphics Quality Button:** Toggles graphics quality between Low, High, and Ultra.
*   **Scene Light Button:** Enables/disables environmental lighting.
*   **Reset Button:** Resets the simulator to initial conditions.
*   **Quit Button:** Exits the simulator application.

#### 1.2.2. HUD Panel

*   **Simulation Time:** Time elapsed since simulation start.
*   **Frame Rate:** Running average of FPS.
*   **Driving Mode:** Current driving mode (Manual or Autonomous).
*   **Gear:** Vehicle gear (D or R).
*   **Speed:** Vehicle forward velocity (m/s).
*   **Throttle:** Instantaneous throttle input (%).
*   **Steering:** Instantaneous steering angle (rad).
*   **Encoder Ticks:** Ticks from rear-left and rear-right incremental encoders.
*   **IPS Data:** Vehicle position [x, y, z] (m).
*   **IMU Data:** Orientation [x, y, z] (rad), angular velocity [x, y, z] (rad/s), and linear acceleration [x, y, z] (m/s²) w.r.t. body frame.
*   **LIDAR Measurement:** 2D LIDAR range measurements (m) within a 270° FOV.
*   **Camera Preview:** Raw image from the front camera.
*   **Race Telemetry:** Current lap time, last lap time, best lap time, and total lap count.
*   **Data Recorder:** Saves time-synchronized simulation data.

#### 1.2.3. Data Recorder

The data recorder exports simulation data at 30 Hz. Data is saved in `CSV` format, with raw camera frames as timestamped `JPG` files. The `CSV` file contains the following data per timestamp:

| DATA           | timestamp             | throttle | steering | leftTicks | rightTicks | posX | posY | posZ | roll | pitch | yaw | speed | angX    | angY    | angZ    | accX    | accY    | accZ    | camera   | lidar              |
| :------------- | :-------------------- | :------- | :------- | :-------- | :--------- | :--- | :--- | :--- | :--- | :---- | :-- | :---- | :------ | :------ | :------ | :------ | :------ | :------ | :------- | :----------------- |
| **UNIT**       | yyyy_MM_dd_HH_mm_ss_fff | norm%    | rad      | count     | count      | m    | m    | m    | rad  | rad   | rad | m/s   | rad/s   | rad/s   | rad/s   | m/s^2   | m/s^2   | m/s^2   | img_path | array(float)       |

The data recorder is triggered by the `Record Data` button in the HUD or the `R` hotkey. The first trigger prompts for a save directory. Subsequent triggers start and stop recording.

**Info:** When selecting a directory, click once on the desired directory; do not double-click into it.

**Warning:** The actual recording rate may fluctuate based on compute power and OS scheduler, but data will remain time-synchronized.

**Note:** Recording data multiple times without resetting the simulator will append to the same files. To avoid this, reset or restart the simulator and specify a new directory.

### 1.3. Vehicle

Vehicles in AutoDRIVE Simulator can be developed using modular scripts or imported from third-party tools. The RoboRacer vehicle was reverse-engineered and recreated for the simulator.

Vehicles are simulated using rigid body and sprung mass representations, considering rigid body dynamics, suspension, actuators, and tires. The simulator detects mesh-mesh interference, computes contact and frictional forces, momentum transfer, and drag. It also offers physically-based sensor simulation.

#### 1.3.1. Transforms

All coordinate frames are right-handed, with red representing the x-axis, green the y-axis, and blue the z-axis.

| FRAME          | x    | y     | z     | R   | P   | Y   |
| :------------- | :--- | :---- | :---- | :-- | :-- | :-- |
| `left_encoder` | 0.0  | 0.118 | 0.0   | 0.0 |     | 0.0 |
| `right_encoder`| 0.0  | -0.118| 0.0   | 0.0 |     | 0.0 |
| `ips`          | 0.08 | 0.0   | 0.055 | 0.0 | 0.0 | 0.0 |
| `imu`          | 0.08 | 0.0   | 0.055 | 0.0 | 0.0 | 0.0 |
| `lidar`        | 0.2733| 0.0   | 0.096 | 0.0 | 0.0 | 0.0 |
| `front_camera` | -0.015| 0.0   | 0.15  | 0.0 | 10.0| 0.0 |
| `front_left_wheel`| 0.33 | 0.118 | 0.0   | 0.0 | 0.0 |     |
| `front_right_wheel`| 0.33 | -0.118| 0.0   | 0.0 | 0.0 |     |
| `rear_left_wheel`| 0.0  | 0.118 | 0.0   | 0.0 |     | 0.0 |
| `rear_right_wheel`| 0.0  | -0.118| 0.0   | 0.0 |     | 0.0 |

**Note:** All frame transforms are defined with respect to the vehicle frame `roboracer_1`, located at the center of the rear axle. x-axis points forward, y-axis points left, and z-axis points upwards. Columns x, y, z denote translations in meters (m), while R, P, Y denote rotations in degrees (deg).

#### 1.3.2. Vehicle Dynamics

The vehicle model combines a rigid body with sprung masses. Suspension forces are calculated based on displacements, damping, and spring coefficients. Tire forces are computed using a friction curve approximated by a two-piece cubic spline, based on longitudinal and lateral slips.

| VEHICLE PARAMETERS        |                               |
| :------------------------ | :---------------------------- |
| Car Length                | 0.5000 m                      |
| Car Width                 | 0.2700 m                      |
| Wheelbase                 | 0.3240 m                      |
| Track Width               | 0.2360 m                      |
| Front Overhang            | 0.0900 m                      |
| Rear Overhang             | 0.0800 m                      |
| Wheel Radius              | 0.0590 m                      |
| Wheel Width               | 0.0450 m                      |
| Total Mass                | 3.906 kg                      |
| Sprung Mass               | 3.470 kg                      |
| Unsprung Mass             | 0.436 kg                      |
| Center of Mass            | X: 0.15532 m, Y: 0.00000 m, Z: 0.01434 m |
| Suspension Spring         | 500 N/m                       |
| Suspension Damper         | 100 Ns/m                      |
| Longitudinal Tire Limits  | Extremum: (0.15, 0.72), Asymptote: (0.25, 0.464) |
| Lateral Tire Limits       | Extremum: (0.01, 1.00), Asymptote: (0.10, 0.500) |

#### 1.3.3. Actuator Dynamics

Driving actuators apply torque to the wheels. Steering actuators control the front wheels based on Ackermann steering geometry.

| DRIVING ACTUATOR |                   |
| :--------------- | :---------------- |
| Drive Type       | All wheel drive   |
| Throttle Limits  | [-1,1]            |
| Motor Torque     | 428 Nm            |
| Vehicle Top Speed| 22.88 m/s         |

| STEERING ACTUATOR |               |
| :---------------- | :------------ |
| Steer Type        | Ackermann     |
| Steering Limits   | [-1,1]        |
| Steering Angle Limits | [-0.5236,0.5236] rad |
| Steering Rate     | 3.2 rad/s     |

#### 1.3.4. Sensor Physics

*   **Throttle and Steering Sensors:** Simulated with instantaneous feedback.
*   **Incremental Encoders:** Measure rear wheel rotation.
    *   **Pulses Per Revolution:** 16
    *   **Conversion Ratio:** 120
*   **IPS and IMU:** Simulated based on rigid-body transform updates. IPS provides position [x, y, z], and IMU provides orientation, angular velocity, and linear acceleration.
*   **LIDAR:** Simulates range measurements using iterative ray-casting.
    *   **Scan Rate:** 40 Hz
    *   **Angular Resolution:** 0.25 deg
    *   **Measurements Per Scan:** 1080
    *   **Minimum Linear Range:** 0.06 m
    *   **Maximum Linear Range:** 10.0 m
    *   **Minimum Angular Range:** -135 deg
    *   **Maximum Angular Range:** +135 deg
*   **Cameras:** Parameterized by focal length, sensor size, resolution, and clipping planes. Includes a post-processing step for lens and film effects.
    *   **Field of View:** 48.8311 deg
    *   **Sensor Size:** X: 3.68 mm, Y: 2.76 mm
    *   **Shutter Speed:** 0.005 s
    *   **Focal Length:** 3.04 m
    *   **Aperture:** f/16
    *   **Target Image:** 16:9 (75% JPG Compression)

### 1.4. Environment

Environments can be developed using AutoDRIVE's Infrastructure Development Kit (IDK) or imported from third-party tools. The Porto racetrack was created based on an occupancy grid map and imported into the simulator.

Environments are simulated by detecting mesh-mesh interference and computing forces, momentum transfer, and drag.

#### 1.4.1. Transforms

The `world` frame is the global reference frame. `roboracer_1` represents the vehicle's pose within the world.

**Warning:** The location of the fixed environmental frame of reference may change depending on the racetrack.

#### 1.4.2. Size and Structure

*   The racetrack is designed to fit within approximately 30x10 m².
*   The border consists of air ducts (approx. 33 cm diameter).
*   The racetrack is at least 3 car widths (90 cm) wide.

#### 1.4.3. Design and Features

*   The road surface has properties of polished concrete, making perception challenging.
*   Gaps in the border may allow LiDAR beams to pass through, creating apparent obstacle-free spaces.
*   The racetrack may include straights, chicanes, bifurcations, and obstacles.

**Warning:** The racetrack is subject to change across different competition phases and iterations. Participants will be informed of any track changes.

## 2. AutoDRIVE Devkit

AutoDRIVE Devkit (part of the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io)) provides APIs, HMIs, and tools for developing autonomous driving algorithms. It supports targeting algorithms to both the simulator and testbeds, and facilitates local or distributed computing.

For the RoboRacer Sim Racing League, teams will use a standardized ROS 2 API implementation of the AutoDRIVE Devkit to develop perception, planning, and control algorithms.

### 2.1. System Requirements

**Minimum Requirements:**

*   **Platform:** Ubuntu 20.04, Windows 10 (VS 2019), macOS 10.14
*   **Processor:** Dual-core CPU (e.g., Intel Core i3 or AMD Ryzen 3)
*   **Memory:** 4 GB RAM
*   **Graphics:** Integrated graphics
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

**Warning:** Modifying the `autodrive_roboracer` package is not permitted. Create your own packages for autonomous racing algorithms.

### 2.3. Data Streams

Data streams are exposed as ROS 2 topics:

| TOPIC                           | TYPE      | MESSAGE              | ACCESS     |
| :------------------------------ | :-------- | :------------------- | :--------- |
| `/autodrive/roboracer_1/best_lap_time` | Debugging | `std_msgs/msg/Float32` | Restricted |
| `/autodrive/roboracer_1/collision_count`| Debugging | `std_msgs/msg/Int32` | Restricted |
| `/autodrive/roboracer_1/front_camera`| Sensor    | `sensor_msgs/msg/Image`| Input      |
| `/autodrive/roboracer_1/imu`    | Sensor    | `sensor_msgs/msg/Imu`| Input      |
| `/autodrive/roboracer_1/ips`    | Sensor    | `geometry_msgs/msg/Point`| Restricted |
| `/autodrive/roboracer_1/lap_count`| Debugging | `std_msgs/msg/Int32` | Restricted |
| `/autodrive/roboracer_1/lap_time`| Debugging | `std_msgs/msg/Float32` | Restricted |
| `/autodrive/roboracer_1/last_lap_time`| Debugging | `std_msgs/msg/Float32` | Restricted |
| `/autodrive/roboracer_1/left_encoder`| Sensor    | `sensor_msgs/msg/JointState`| Input      |
| `/autodrive/roboracer_1/lidar`  | Sensor    | `sensor_msgs/msg/LaserScan`| Input      |
| `/autodrive/roboracer_1/right_encoder`| Sensor    | `sensor_msgs/msg/JointState`| Input      |
| `/autodrive/roboracer_1/speed`  | Debugging | `std_msgs/msg/Float32` | Restricted |
| `/autodrive/roboracer_1/steering`| Sensor    | `std_msgs/msg/Float32` | Input      |
| `/autodrive/roboracer_1/steering_command`| Actuator  | `std_msgs/msg/Float32` | Output     |
| `/autodrive/roboracer_1/throttle`| Sensor    | `std_msgs/msg/Float32` | Input      |
| `/autodrive/roboracer_1/throttle_command`| Actuator  | `std_msgs/msg/Float32` | Output     |
| `/autodrive/reset_command`      | Debugging | `std_msgs/msg/Bool`  | Restricted |
| `/tf`                           | Debugging | `tf2_msgs/msg/TFMessage`| Restricted |

**Warning:** Restricted topics can be used for debugging but not during autonomous racing.

**Info:** Reset the simulation by publishing `True` to `/autodrive/reset_command`. Remember to set it back to `False`.

## 3. Competition Submission

The RoboRacer Sim Racing League uses a containerization workflow for reproducible evaluation. Each team must submit a containerized autonomous racing software stack.

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

**Note:** Pay attention to the `<TAG>` (e.g., `explore`, `practice`, `compete`). The convention is `<YEAR>-<EVENT>-<PHASE>`.

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
3.  Configure the simulator GUI:
    *   Enter the devkit's IP address.
    *   Click the `Connection` button.
    *   Toggle the `Driving Mode` to `Autonomous`.

#### 3.2.2. Headless Mode Operations

1.  Launch AutoDRIVE Simulator in `no-graphics` mode:
    ```bash
    ./AutoDRIVE\ Simulator.x86_64 -batchmode -nographics -ip 127.0.0.1 -port 4567
    ```
2.  Launch AutoDRIVE Simulator in `headless` mode (vehicle camera rendering enabled):
    ```bash
    xvfb-run ./AutoDRIVE\ Simulator.x86_64 -ip 127.0.0.1 -port 4567
    ```
3.  Launch AutoDRIVE Devkit in `headless` mode:
    ```bash
    ros2 launch autodrive_roboracer bringup_headless.launch.py
    ```

**Info:** The simulator and devkit can be run selectively in `graphics` or `headless` mode.

#### 3.2.3. Distributed Computing Mode

The simulator and devkit can run on separate machines. Configure the simulator with the devkit's IP address. This approach distributes the workload for better performance. It's also possible to use a physical RoboRacer vehicle with the devkit for a hardware-in-the-loop (HIL) setup.

**Tip:** If GPU access with Docker is problematic, run the simulator locally and the devkit within a container.

### 3.3. Container Troubleshooting

*   **Accessing a running container:** `docker exec -it <CONTAINER NAME> bash`
*   **Exiting a bash session:** `exit`
*   **Killing a container:** `docker kill <CONTAINER NAME>`
*   **Removing a container:** `docker rm <CONTAINER NAME>`
*   **Checking Docker disk usage:** `docker system df`
*   **Pruning unused Docker resources:** `docker system prune -a`
*   **Switching Docker context:**
    ```bash
    docker context ls
    docker context use default
    ```

**Warning:** Avoid using Docker Desktop on Linux; it can cause issues with GPU access.

**Info:** For more information on containerization, visit [docker.com](https://www.docker.com).

### 3.4. Algorithm Development

Create your ROS 2 package(s) for autonomous racing **separate** from the `autodrive_roboracer` package. Refer to the data streams and their access restrictions for algorithm development.

**Tip:** Develop and test algorithms locally before containerizing them for submission.

### 3.5. Container Submission

Ensure your submitted container automatically starts all necessary nodes. Upon connecting the simulator, the vehicle should start running. Include all necessary commands (sourcing workspaces, setting environment variables, launching nodes) within the `entrypoint` script (`autodrive_devkit.sh`). Do **NOT** use `~/.bashrc` or similar for automation.

1.  Run your image in a container:
    ```bash
    xhost local:root
    docker run --name autodrive_roboracer_api --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_roboracer_api:<TAG>
    ```
2.  Note the `CONTAINER ID` from `docker ps -a`.
3.  Commit changes:
    ```bash
    docker commit -m "<Commit message>" -a "<USERNAME>" <CONTAINER ID> <username>/<image_name>:<TAG>
    ```
4.  Log in to DockerHub:
    ```bash
    docker login
    ```
5.  Push the container to DockerHub:
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
    *   Published at 2021 2nd International Conference on Control, Robotics and Intelligent System (CCRIS).
    *   [Link](https://doi.org/10.1145/3483845.3483846)
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
