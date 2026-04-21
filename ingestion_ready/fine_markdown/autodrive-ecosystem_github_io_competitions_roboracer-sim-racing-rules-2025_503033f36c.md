# Competition Rules

This document describes the rules and regulations for the RoboRacer Sim Racing League. It covers definitions, requirements, evaluation criteria, and general guidelines.

**Note:** Rules are subject to change. Organizers reserve the right to amend existing rules and create new ones as needed.

## 1. General Guidelines

The RoboRacer Sim Racing League is a virtual competition that complements the physical RoboRacer Autonomous Racing Competition. It uses the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to simulate a digital twin of a RoboRacer vehicle on a virtual racetrack, aiming to make autonomous racing accessible globally.

### 1.1. Eligibility Criteria

This competition is open to everyone worldwide, including students, researchers, hobbyists, and professionals. There are no restrictions based on age, sex, nationality, or profession. Teams can have one or more participants, and multiple teams from the same organization are allowed. However, each participant can only be a member of one team.

Registration for the Sim Racing League is free and separate from the Physical Racing League and conference registrations. While participation in the Sim Racing League does not require attending the conference, it is strongly encouraged to engage with competition-related events and the broader community.

### 1.2. Competition Structure

Each team will receive a standardized simulation setup, including a digital twin of the RoboRacer vehicle and the Porto racetrack, within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to develop their autonomy algorithms. Teams must create perception, planning, and control algorithms to process real-time sensor data from the simulator and generate control commands for the simulated vehicle.

### 1.3. Competition Timeline

The competition consists of two stages:

*   **Qualification Race:** Teams must complete multiple laps around a practice track without colliding with the track boundaries.
*   **Time-Attack Race:** Teams compete against the clock on a new racetrack to achieve the best position on the leaderboard.

Key events include:

*   **Registration:** Teams register for the Sim Racing League.
*   **Online Orientation 1:** Organizers explain rules, guidelines, and the simulation framework.
*   **Online Orientation 2:** Organizers check team progress and provide technical assistance.
*   **Qualification Round:** Teams must complete 10 consecutive laps around the provided practice track.
*   **Qualification Results Declared:** Standings for qualified teams are released.
*   **Competition Track Released:** The official competition track is revealed, potentially mirroring the physical race track.
*   **Final Race:** Organizers collect containerized algorithms, run them with the simulator, and record performance metrics.
*   **Competition Results Declared:** Final race standings are released.

## 2. Competition Guidelines

This competition follows a **time-attack racing** format where each team competes independently on the same racetrack. Each race includes a warm-up lap, 10 race laps, and a cool-down lap.

### 2.1. Competition Requirements

To progress through each phase:

*   **Registration:** Teams must register before the deadline. Requests for deadline extensions will not be entertained. Early registration is recommended.
*   **Orientations:** Attending online orientation sessions is highly recommended to understand the code of conduct and simulation framework.
*   **Qualification:** Teams must complete 10 autonomous laps around the practice track without exceeding the collision tolerance. Speed is not critical in this phase, but failure to complete the laps will result in disqualification. Successful qualification allows participation in the final race.
*   **Competition:** Teams aim to complete 10 consecutive autonomous laps as quickly as possible without exceeding the collision tolerance. Exceeding the collision limit leads to disqualification. Teams are ranked by their total time for 10 race laps.

### 2.2. Competition Terminology

*   **Collision:** Contact between the simulated vehicle's colliders and the racetrack boundaries (excluding wheels on the ground). Each collision incurs a 10-second penalty (cumulative: 10s for the 1st, 20s for the 2nd, etc.). More than 10 collisions result in disqualification. Collisions reset the vehicle to the last checkpoint, and the lap timer does not reset.
*   **Warm-Up Lap:** The first lap. Time and collisions are not counted. This lap allows algorithms to initialize and connect with the simulator.
*   **Race Laps:** The 10 laps following the warm-up lap. Time and collisions during these laps are counted.
*   **Cool-Down Lap:** The final lap. Time and collisions are not counted. Completion is not mandatory but offers a chance to showcase skills without penalty.
*   **Checkpoints:** Virtual markers along the track, including the start/finish line. Their exact locations are not revealed. Passing all checkpoints before the finish line is required for a valid lap time.
*   **Lap Time:** The duration to complete one full lap. The timer starts when the previous lap ends and stops when the current lap ends.
*   **Race Time:** The cumulative time for 10 race laps. The timer starts after the warm-up lap ends and stops after the 10th race lap. Collision penalties are added separately.
*   **Best Lap Time:** The shortest lap time among the 10 race laps.
*   **Average Lap Time:** The mean lap time across the 10 race laps.

### 2.3. Competition Execution

A typical racing event proceeds as follows:

*   **Inspection:** Race stewards review team submissions.
*   **Simulator:** The containerized AutoDRIVE Simulator is launched with specific settings (e.g., "Ultra" graphics).
*   **Devkit:** The containerized AutoDRIVE Devkit with the team's algorithm is launched. A Bash session starts recording ROS 2 topics.
*   **Recording:** Screen recording and ROS 2 bag recording run in the background.
*   **Communication:** A communication channel between the simulator and devkit containers is established, initiating the race.
*   **Race:** The race consists of a warm-up lap, 10 race laps, and a cool-down lap. Only data from the 10 race laps is considered.
*   **Data:** Performance metrics, simulator screen recordings, and ROS 2 bags are stored.

### 2.4. Inspection Rules

**Warning:** Organizers reserve the right to reject submissions deemed illegal due to unethical exploitation of the competition framework. All submissions are examined by race stewards before the race.

**Warning:** Teams violating the code of conduct will be disqualified and publicly cited for "malpractice."

Modifications to the competition framework (simulator, vehicle, environment, communication interface, devkit, or containerization) are strictly prohibited. Such modifications will lead to immediate disqualification.

Autonomous racing algorithms using raw perception data for control commands are permissible (e.g., reactive planning, deep learning, reinforcement learning). However, using simulation ground truth data or controlling aspects beyond vehicle actuators is forbidden. Unethical exploitation of the framework (e.g., back-end access, frame-grabbing, exploiting loopholes, tampering with data) is considered serious malpractice.

**Info:** Refer to the [Technical Guide](https://autodrive-ecosystem.github.io/competitions/roboracer-sim-racing-guide-2025) for details on permissible and restricted data streams.

Teams must observe ethical integrity and adhere to the code of conduct. Malpractice or plagiarism will be considered a serious breach, potentially resulting in warnings, public citations, or disqualification.

### 2.5. Evaluation Criteria

*   The primary evaluation criterion is **total race time.** Tie-breakers may use best lap time or other metrics.
*   Collisions incur a **penalty** of 10 seconds per collision (cumulative).
*   A maximum of 10 collisions are permissible per race; exceeding this results in **disqualification.**
*   Only times and collisions during the **10 race laps** are considered.

**Note:** The race referee's decision is final. Rebuttals with supporting evidence may be considered at the organizers' discretion.

## 3. Submission Guidelines

Each team must submit a containerized version of their autonomous racing software stack. Submissions are made separately for each competition phase.

**Note:** Upon running the submitted container, all necessary nodes should start automatically. The `autodrive_devkit.sh` script within the `autodrive_roboracer_api` container should handle sourcing workspaces, setting environment variables, and launching nodes. Do **NOT** use `~/.bashrc` or similar methods for automation. Organizers must be able to open additional Bash sessions within the container for recording and inspection without automatically executing the codebase.

### 3.1. Submission Requirements

*   Each team must submit a Docker container image of their autonomous racing software stack.
*   The container must be self-sustainable, including all dependencies and configured to run commands automatically.
*   The container must be based on the official AutoDRIVE Devkit container.
*   Teams may add/modify ROS 2 packages within the AutoDRIVE Devkit container for their algorithms, but modifications to existing container elements are prohibited.
*   Teams do not need to submit the simulator container.

**Tip:** Test algorithms locally before containerizing and always test containers before submission.

### 3.2. Submission Process

Key milestones for submission:

*   **Containerize:** Package the autonomous racing software stack using [Docker](https://www.docker.com).
*   **Push:** Upload the container image to [DockerHub](https://hub.docker.com).
*   **Share:** Provide the link to the repository via a secure submission form (separate forms for each stage).

### 3.3. Submission Privacy

Teams can maintain source code and container privacy:

*   **Source Code:** Host code in a private [GitHub](https://github.com) repository.
*   **Containers:** Push Docker images to a private [DockerHub](https://hub.docker.com) repository (one free private repository per user account).
*   **Data:** Store data in encrypted cloud storage with link sharing disabled, or use local storage with backups.

After the competition, teams are encouraged to publish their source code under an open-source license and make their Docker containers public on DockerHub to enhance visibility and contribute to future competitions.

## 4. Citation

We encourage you to cite the following papers if you use any part of the competition framework:

#### [AutoDRIVE: A Comprehensive, Flexible and Integrated Digital Twin Ecosystem for Enhancing Autonomous Driving Research and Education](https://arxiv.org/abs/2212.05241)

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

Published in **MDPI Robotics.** Available on [MDPI](https://doi.org/10.3390/robotics12030077).

#### [AutoDRIVE Simulator: A Simulator for Scaled Autonomous Vehicle Research and Education](https://arxiv.org/abs/2103.10030)

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

Published at **2021 International Conference on Control, Robotics and Intelligent System (CCRIS).** Available on [ACM Digital Library](https://dl.acm.org/doi/abs/10.1145/3483845.3483846).
