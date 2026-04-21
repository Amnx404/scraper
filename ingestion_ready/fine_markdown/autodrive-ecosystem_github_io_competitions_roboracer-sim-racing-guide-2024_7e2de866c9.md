# Technical Guide

This document describes the technical details of the competition framework for the RoboRacer Sim Racing League. It covers the simulator, devkit, submission system, process, and evaluation.

**Prerequisites:** Teams are expected to have a strong background in autonomous racing concepts, programming languages (Python, C++), frameworks (ROS 2), containerization (Docker), and version control (Git). Extensive technical support is not provided.

**Vehicle and API:** The **RoboRacer** is the only vehicle allowed. The **ROS 2** API is the only API permitted.

Refer to the accompanying video for a step-by-step tutorial.

## 1. AutoDRIVE Simulator

The AutoDRIVE Simulator, part of the AutoDRIVE Ecosystem, models and simulates vehicle and environment digital twins with a focus on high-fidelity physics and graphics. It is modular, supports CPU multi-threading and GPU instancing, and is cross-platform. For this competition, a standardized simulation setup including the RoboRacer vehicle and the Porto racetrack is provided.

### 1.1. System Requirements

**Minimum Requirements:**

*   **Platform:** Ubuntu 20.04+, Windows 10+, macOS 10.14+
*   **Processor:** Quad-core CPU (e.g., Intel Core i5 or AMD Ryzen 5)
*   **Memory:** 8 GB RAM
*   **Graphics:** Integrated graphics or NVIDIA GeForce GTX 1050 (2 GB VRAM)
*   **Storage:** 10 GB free disk space
*   **Display:** 1280x720 px at 60 Hz
*   **Network:** 1 Mbps stable internet connection

**Recommended Requirements:**

*   **Platform:** Ubuntu 20.04/22.04, Windows 10/11
*   **Processor:** Octa-core CPU (e.g., Intel Core i7 or AMD Ryzen 7)
*   **Memory:** 16 GB RAM
*   **Graphics:** NVIDIA GeForce GTX 1660 or RTX 2060 (4+ GB VRAM)
*   **Storage:** 20 GB free disk space
*   **Display:** 1920x1080 px at 144 Hz
*   **Network:** 10 Mbps fast internet connection

**Organizer's Workstation:** Intel Core i9 14th Gen 14900K, NVIDIA GeForce RTX 4090, 64 GB RAM. Algorithms should consider these computational demands.

### 1.2. User Interface

The simulator GUI includes a **Menu** panel for configuration and control, and a **Heads-Up Display (HUD)** panel for real-time visualization and data recording.

#### 1.2.1. Menu Panel

*   **IP Address Field:** IP address of the devkit machine (default: 127.0.0.1).
*   **Port Number Field:** Port number of the devkit machine (default: 4567).
*   **Connection Button:** Establishes connection with the devkit.
*   **Driving Mode Button:** Toggles between Manual and Autonomous driving.
*   **Camera View Button:** Toggles camera views (Driver's Eye, Bird's Eye, God's Eye).
*   **Graphics Quality Button:** Toggles graphics quality (Low, High, Ultra).
*   **Scene Light Button:** Enables/disables environmental lighting.
*   **Reset Button:** Resets the simulator to initial conditions.
*   **Quit Button:** Exits the simulator.

#### 1.2.2. HUD Panel

*   **Simulation Time:** Elapsed time since simulation start.
*   **Frame Rate:** Running average FPS.
*   **Driving Mode:** Current driving mode (Manual/Autonomous).
*   **Gear:** Vehicle gear (D/R).
*   **Speed:** Vehicle speed (m/s).
*   **Throttle:** Instantaneous throttle input (%).
*   **Steering:** Instantaneous steering angle (rad).
*   **Encoder Ticks:** Rear-left and rear-right encoder ticks.
*   **IPS Data:** Vehicle position [x, y, z] (m).
*   **IMU Data:** Orientation [x, y, z] (rad), angular velocity [x, y, z] (rad/s), linear acceleration [x, y, z] (m/s²).
*   **LIDAR Measurement:** 2D LIDAR range measurements (m).
*   **Camera Preview:** Raw image from the front camera.
*   **Race Telemetry:** Current lap time, last lap time, best lap time, lap count.
*   **Data Recorder:** Saves time-synchronized simulation data.

#### 1.2.3. Data Recorder

Records time-synchronized simulation data at approximately 30 Hz. Data is saved in `CSV` format, with camera frames as timestamped `JPG` files.

**CSV Data Entries:**

| timestamp             | throttle | steering | leftTicks | rightTicks | posX | posY | posZ | roll | pitch | yaw | speed | angX  | angY  | angZ  | accX  | accY  | accZ  | camera   | lidar            |
| :-------------------- | :------- | :------- | :-------- | :--------- | :--- | :--- | :--- | :--- | :---- | :-- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :------- | :--------------- |
| yyyy_MM_dd_HH_mm_ss_fff | norm%    | rad      | count     | count      | m    | m    | m    | rad  | rad   | rad | m/s   | rad/s | rad/s | rad/s | m/s²  | m/s²  | m/s²  | img_path | array(float)     |

Trigger recording with the `Record Data` button or `R` hotkey. The first trigger prompts for a directory. Subsequent triggers start/stop recording.

**Note:** If recording multiple times without resetting, data is appended. Reset or specify a new directory to avoid this.

### 1.3. Vehicle

The RoboRacer vehicle is simulated with detailed rigid body dynamics, suspension, actuators, and tires. It includes physically-based sensor simulation.

#### 1.3.1. Transforms

Coordinate frames are right-handed (x-axis: red, y-axis: green, z-axis: blue).

| FRAME          | x    | y     | z    | R   | P   | Y   |
| :------------- | :--- | :---- | :--- | :-- | :-- | :-- |
| `left_encoder` | 0.0  | 0.118 | 0.0  | 0.0 |     | 0.0 |
| `right_encoder`| 0.0  | -0.118| 0.0  | 0.0 |     | 0.0 |
| `ips`          | 0.08 | 0.0   | 0.055| 0.0 | 0.0 | 0.0 |
| `imu`          | 0.08 | 0.0   | 0.055| 0.0 | 0.0 | 0.0 |
| `lidar`        | 0.2733| 0.0   | 0.096| 0.0 | 0.0 | 0.0 |
| `front_camera` | -0.015| 0.0   | 0.15 | 0.0 | 10.0| 0.0 |
| `front_left_wheel`| 0.33 | 0.118 | 0.0  | 0.0 | 0.0 |     |
| `front_right_wheel`| 0.33| -0.118| 0.0  | 0.0 | 0.0 |     |
| `rear_left_wheel`| 0.0  | 0.118 | 0.0  | 0.0 |     | 0.0 |
| `rear_right_wheel`| 0.0 | -0.118| 0.0  | 0.0 |     | 0.0 |

All transforms are relative to the vehicle frame (`f1tenth_1`), located at the center of the rear axle.

#### 1.3.2. Vehicle Dynamics

The vehicle model combines rigid body and sprung mass representations.

*   **Suspension Force:** Calculated based on sprung/unsprung mass displacements, damping, and spring coefficients.
*   **Tire Forces:** Computed using a two-piece cubic spline approximation of the friction curve, based on longitudinal and lateral slip.
*   **Vehicle Parameters:**

    | Parameter             | Value      |
    | :-------------------- | :--------- |
    | Car Length            | 0.5000 m   |
    | Car Width             | 0.2700 m   |
    | Wheelbase             | 0.3240 m   |
    | Track Width           | 0.2360 m   |
    | Front Overhang        | 0.0900 m   |
    | Rear Overhang         | 0.0800 m   |
    | Wheel Radius          | 0.0590 m   |
    | Wheel Width           | 0.0450 m   |
    | Total Mass            | 3.906 kg   |
    | Sprung Mass           | 3.470 kg   |
    | Unsprung Mass         | 0.436 kg   |
    | Center of Mass (X,Y,Z)| (0.15532, 0.0, 0.01434) m |
    | Suspension Spring     | 500 N/m    |
    | Suspension Damper     | 100 Ns/m   |
    | Longitudinal Tire Limits (Slip, Force) | Extremum: (0.15, 0.72), Asymptote: (0.25, 0.464) |
    | Lateral Tire Limits (Slip, Force) | Extremum: (0.01, 1.00), Asymptote: (0.10, 0.500) |

#### 1.3.3. Actuator Dynamics

*   **Driving Actuator:** Simulates torque applied to wheels.
    *   **DRIVING ACTUATOR:** All-wheel drive, Throttle Limits [-1,1], Motor Torque 428 Nm, Top Speed 22.88 m/s.
*   **Steering Actuator:** Implements Ackermann steering geometry.
    *   **STEERING ACTUATOR:** Ackermann steering, Steering Limits [-1,1], Angle Limits [-0.5236, 0.5236] rad, Rate 3.2 rad/s.

#### 1.3.4. Sensor Physics

*   **Throttle/Steering Sensors:** Instantaneous feedback.
*   **Incremental Encoders:** Measure rear wheel rotation.
    *   **ENCODERS:** Pulses Per Revolution 16, Conversion Ratio 120.
*   **IPS & IMU:** Based on rigid-body transform updates.
    *   **IPS:** Provides 3-DOF position [x, y, z] (m).
    *   **IMU:** Provides orientation (quaternion/Euler angles), angular velocity, and linear acceleration.
*   **LIDAR:** Uses iterative ray-casting.
    *   **LIDAR:** Scan Rate 40 Hz, Angular Resolution 0.25 deg, Measurements Per Scan 1080, Range [0.06 m, 10.0 m].
*   **Camera:** Parameterized by focal length, sensor size, resolution, and clipping planes.
    *   **CAMERA:** FOV 48.8311 deg, Sensor Size (3.68 mm, 2.76 mm), Shutter Speed 0.005 s, Focal Length 3.04 m, Aperture f/16, Output RGB Image (16:9, 75% JPG).

### 1.4. Environment

The Porto racetrack is simulated based on an occupancy grid map, created using 3D modeling software.

#### 1.4.1. Transforms

The `world` frame is the global reference. The vehicle frame `f1tenth_1` is defined relative to `world`.

#### 1.4.2. Size and Structure

*   Racetrack dimensions similar to physical RoboRacer tracks, approximately 30x10 m².
*   Borders made of 33 cm diameter air ducts.
*   Minimum track width of 90 cm.

#### 1.4.3. Design and Features

*   Road surface: Polished concrete (flat and reflective).
*   Potential gaps in border ducts for LiDAR.
*   Varied course features: straights, chicanes, bifurcations, obstacles.

**Note:** The racetrack may change across competition phases and iterations. Participants will be notified of any changes.

## 2. AutoDRIVE Devkit

The AutoDRIVE Devkit provides APIs, libraries, and tools for developing autonomous driving algorithms, targeting both the simulator and physical testbeds. It supports local and distributed computing. For the competition, a standardized ROS 2 API for the RoboRacer digital twin is provided.

### 2.1. System Requirements

**Minimum Requirements:**

*   **Platform:** Ubuntu 20.04, Windows 10 (VS 2019), macOS 10.14
*   **Processor:** Dual-core CPU (e.g., Intel Core i3 or AMD Ryzen 3)
*   **Memory:** 4 GB RAM
*   **Graphics:** Integrated graphics
*   **Storage:** 5 GB free disk space
*   **Display:** 1280x720 px at 60 Hz
*   **Network:** 1 Mbps stable internet connection

**Recommended Requirements:**

*   **Platform:** Ubuntu 20.04
*   **Processor:** Quad-core CPU (e.g., Intel Core i5 or AMD Ryzen 5)
*   **Memory:** 8 GB RAM
*   **Graphics:** NVIDIA GeForce GT 1030
*   **Storage:** 10 GB free disk space
*   **Display:** 1920x1080 px at 60 Hz
*   **Network:** 10 Mbps fast internet connection

### 2.2. Package Structure

The ROS 2 package structure for the AutoDRIVE Devkit:

```
autodrive_devkit
├───package.xml
├───setup.cfg
├───setup.py
│
├───autodrive_f1tenth
│   └───autodrive_bridge.py
│   └───config.py
│   └───teleop_keyboard.py
│   └───__init__.py
│
├───launch
│   └───simulator_bringup_headless.launch.py
│   └───simulator_bringup_rviz.launch.py
│
├───resource
│   └───autodrive_f1tenth
│
├───rviz
│   └───simulator.rviz
│
└───test
    └───test_copyright.py
    └───test_flake8.py
    └───test_pep257.py
```

**Warning:** Modifying the `autodrive_f1tenth` package is not permitted. Teams must create their own packages.

### 2.3. Data Streams

ROS 2 topics provided by the AutoDRIVE Devkit:

| TOPIC                          | TYPE            | MESSAGE              | ACCESS     |
| :----------------------------- | :-------------- | :------------------- | :--------- |
| `/autodrive/f1tenth_1/best_lap_time` | Debugging       | `Float32`            | Restricted |
| `/autodrive/f1tenth_1/collision_count`| Debugging       | `Int32`              | Restricted |
| `/autodrive/f1tenth_1/front_camera`| Sensor          | `Image`              | Input      |
| `/autodrive/f1tenth_1/imu`     | Sensor          | `Imu`                | Input      |
| `/autodrive/f1tenth_1/ips`     | Sensor          | `Point`              | Restricted |
| `/autodrive/f1tenth_1/lap_count` | Debugging       | `Int32`              | Restricted |
| `/autodrive/f1tenth_1/lap_time`| Debugging       | `Float32`            | Restricted |
| `/autodrive/f1tenth_1/last_lap_time`| Debugging       | `Float32`            | Restricted |
| `/autodrive/f1tenth_1/left_encoder`| Sensor          | `JointState`         | Input      |
| `/autodrive/f1tenth_1/lidar`   | Sensor          | `LaserScan`          | Input      |
| `/autodrive/f1tenth_1/right_encoder`| Sensor          | `JointState`         | Input      |
| `/autodrive/f1tenth_1/speed`   | Debugging       | `Float32`            | Restricted |
| `/autodrive/f1tenth_1/steering`| Sensor          | `Float32`            | Input      |
| `/autodrive/f1tenth_1/steering_command`| Actuator        | `Float32`            | Output     |
| `/autodrive/f1tenth_1/throttle`| Sensor          | `Float32`            | Input      |
| `/autodrive/f1tenth_1/throttle_command`| Actuator        | `Float32`            | Output     |
| `/autodrive/reset_command`     | Debugging       | `Bool`               | Restricted |
| `/tf`                          | Debugging       | `TFMessage`          | Restricted |

**Warning:** Restricted topics are for debugging/training only, not for autonomous racing at runtime.

**Info:** Reset the simulation by publishing `True` to `/autodrive/reset_command`. Remember to set it back to `False`.

## 3. Competition Submission

The competition uses a containerization workflow for reproducible evaluation. Teams must submit a containerized autonomous racing software stack.

### 3.1. Container Setup

1.  Install [Docker](https://docs.docker.com/engine/install).
2.  Install NVIDIA GPU Drivers and [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html).
3.  Pull the AutoDRIVE Simulator Docker image:
    ```bash
    docker pull autodriveecosystem/autodrive_f1tenth_sim:<TAG>
    ```
4.  Pull the AutoDRIVE Devkit Docker image:
    ```bash
    docker pull autodriveecosystem/autodrive_f1tenth_api:<TAG>
    ```
    Replace `<TAG>` with the appropriate tag (e.g., `explore`, `practice`, `compete`).

### 3.2. Container Execution

1.  Enable display forwarding: `xhost local:root`
2.  Run the simulator container:
    ```bash
    docker run --name autodrive_f1tenth_sim --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_f1tenth_sim:<TAG>
    ```
3.  (Optional) Start additional bash sessions: `docker exec -it autodrive_f1tenth_sim bash`
4.  Run the devkit container:
    ```bash
    docker run --name autodrive_f1tenth_api --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_f1tenth_api:<TAG>
    ```
5.  (Optional) Start additional bash sessions: `docker exec -it autodrive_f1tenth_api bash`

#### 3.2.1. GUI Mode Operations

1.  Launch AutoDRIVE Simulator: `./AutoDRIVE\ Simulator.x86_64`
2.  Launch AutoDRIVE Devkit: `ros2 launch autodrive_f1tenth simulator_bringup_rviz.launch.py`
3.  Configure IP address and connect using the simulator's Menu panel. Toggle driving mode.

#### 3.2.2. Headless Mode Operations

1.  Launch AutoDRIVE Simulator (no graphics):
    `./AutoDRIVE\ Simulator.x86_64 -batchmode -nographics -ip 127.0.0.1 -port 4567`
2.  Launch AutoDRIVE Simulator (headless):
    `xvfb-run ./AutoDRIVE\ Simulator.x86_64 -ip 127.0.0.1 -port 4567`
3.  Launch AutoDRIVE Devkit (headless):
    `ros2 launch autodrive_f1tenth simulator_bringup_headless.launch.py`

#### 3.2.3. Distributed Computing Mode

Run the simulator and devkit on separate machines or connect the devkit to a physical RoboRacer for Hardware-in-the-Loop (HIL) simulation.

**Tip:** If GPU issues arise with Docker, run the simulator locally and the devkit in a container.

### 3.3. Container Troubleshooting

*   Access running container: `docker exec -it <CONTAINER NAME> bash`
*   Exit session: `exit`
*   Kill container: `docker kill <CONTAINER NAME>`
*   Remove container: `docker rm <CONTAINER NAME>`
*   Check disk usage: `docker system df`
*   Prune unused resources: `docker system prune -a`
*   Switch Docker context: `docker context use default`

### 3.4. Algorithm Development

Create ROS 2 packages for your algorithms separately from the `autodrive_f1tenth` package. Refer to the data streams and their access restrictions.

**Tip:** Develop and test locally first, then containerize for submission.

### 3.5. Container Submission

Your submitted container should automatically start necessary nodes. Upon connecting the simulator, the vehicle should start running. Include all setup commands in the `entrypoint` script (`autodrive_devkit.sh`). Do not use `~/.bashrc` for automation.

1.  Run your image:
    ```bash
    xhost local:root
    docker run --name autodrive_f1tenth_api --rm -it --entrypoint /bin/bash --network=host --ipc=host -v /tmp/.X11-unix:/tmp.X11-umix:rw --env DISPLAY --privileged --gpus all autodriveecosystem/autodrive_f1tenth_api:<TAG>
    ```
2.  Note the `CONTAINER ID` from `docker ps -a`.
3.  Commit changes: `docker commit ... <CONTAINER ID> <username>/<image_name>:<TAG>`
4.  Login to DockerHub: `docker login`
5.  Push to DockerHub: `docker push <username>/<image_name>:<TAG>`
6.  Submit the DockerHub repository link.

## 4. Citation

We encourage you to cite the following papers if you use any part of this framework:

*   **AutoDRIVE: A Comprehensive, Flexible and Integrated Digital Twin Ecosystem for Enhancing Autonomous Driving Research and Education**
    *   Published in MDPI Robotics.
    *   [Link](https://www.mdpi.com/2218-6581/12/3/77)
*   **AutoDRIVE Simulator: A Simulator for Scaled Autonomous Vehicle Research and Education**
    *   Published at CCRIS'21.
    *   [Link](https://dl.acm.org/doi/abs/10.1145/3483845.3483846)
