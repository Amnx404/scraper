# RoboRacer Sim Racing League @ ICRA 2025

## About

**RoboRacer Autonomous Racing** is a competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **24th RoboRacer Autonomous Racing Competition** at [ICRA 2025](https://2025.ieee-icra.org) will write software for a 1:10 scaled autonomous racecar. The objective is to **_drive fast but don’t crash!_**

This event is the third **RoboRacer Sim Racing League**, which uses the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to simulate a RoboRacer racecar on a virtual racetrack.

The Sim Racing League is a virtual competition accessible globally. For the [ICRA 2025](https://2025.ieee-icra.org) competition, each team will receive a standardized simulation setup: a digital twin of the RoboRacer vehicle and the Porto racetrack, within the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit). Teams must develop perception, planning, and control algorithms to process real-time sensor data from the simulator and generate control commands for the simulated vehicle.

The competition has two stages:

*   **Qualification Race:** Teams must complete multiple laps around a practice track without colliding with track boundaries.
*   **Time-Attack Race:** Teams compete against the clock on a new racetrack to achieve the best position on the leaderboard.

Since the vehicle, sensors, simulator, and devkit are standardized, teams need to develop robust racing algorithms capable of handling uncertainties on an unseen racetrack.

If you are interested in racing physical RoboRacer vehicles, please visit the website for the [24th RoboRacer Autonomous Racing Competition](https://icra2025-race.roboracer.ai), which will be held in person at [ICRA 2025](https://2025.ieee-icra.org). You can register for both physical and virtual competitions.

## Organizers

|                                                              |                                                              |                                                              |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| ![Rahul Mangharam](/../assets/images/people/Rahul Mangharam.png) | ![Venkat Krovi](/../assets/images/people/Venkat Krovi.png)   | ![Johannes Betz](/../assets/images/people/Johannes Betz.png) |
| [**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu)       | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu)             | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de)         |
| ![Chinmay Samak](/../assets/images/people/Chinmay Samak.png) | ![Tanmay Samak](/../assets/images/people/Tanmay Samak.png)   | ![Ahmad Amine](/../assets/images/people/Ahmad Amine.png)     |
| [**Chinmay Samak**](mailto:csamak@clemson.edu)                 | [**Tanmay Samak**](mailto:tsamak@clemson.edu)                 | [**Ahmad Amine**](mailto:aminea@seas.upenn.edu)               |

## Timeline

**Timeline is subject to change. Please keep checking this page for any updates.**

| DATE                      | EVENT                               |
| :------------------------ | :---------------------------------- |
| Feb 20, 2025              | Registration Opens                  |
| Apr 15, 2025              | Registration Closes                 |
| Apr 16, 2025 (5:30 – 6:30 PM EDT) | [Online Orientation](https://clemson.zoom.us/j/94807115758) |
| May 03 – May 05, 2025       | Qualification Round                 |
| May 06, 2025              | Qualification Results Declared      |
| May 08, 2025              | Competition Track Released          |
| May 11 – May 13, 2025       | Final Race                          |
| May 14, 2025              | Competition Results Declared        |

Summary of each event:

*   **Registration:** Interested teams register for the Sim Racing League.
*   **Online Orientation:** Organizers explain competition rules and guidelines and demonstrate the simulation framework.
*   **Qualification Round:** Teams demonstrate successful completion of 10 laps around the provided practice track.
*   **Qualification Results Declared:** Standings of qualified teams are released.
*   **Competition Track Released:** Organizers release the "competition track" for the final race, which may be replicated in the physical race.
*   **Final Race:** Organizers collect containerized algorithms from teams and connect them with the containerized simulator. Team performance metrics are recorded.
*   **Competition Results Declared:** Standings of all teams for the final race are released.

The RoboRacer Sim Racing League will be held approximately one week before [ICRA 2025](https://2025.ieee-icra.org), and performance metrics will be made available to teams. Discussions are ongoing with the ICRA organizing team to allow teams to analyze and present their approaches/results in a short presentation during a special session at [ICRA 2025](https://2025.ieee-icra.org).

## Resources

![AutoDRIVE Logo](/../assets/images/logos/AutoDRIVE Logo.png)

[AutoDRIVE](https://autodrive-ecosystem.github.io/) is an open, comprehensive, flexible, and integrated cyber-physical ecosystem for autonomous driving research and education. It connects software simulation with hardware deployment through the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Testbed](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Testbed). It also provides the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) for rapid development of autonomy algorithms. For the Sim Racing League, teams will use the AutoDRIVE Devkit to interface with the AutoDRIVE Simulator in real-time.

![RoboRacer Logo](/../assets/images/logos/RoboRacer Logo.png)

[RoboRacer](https://roboracer.ai) is an [international community](https://roboracer.ai/about.html) of researchers, engineers, and autonomous systems enthusiasts focused on converting 1:10 scale RC cars into autonomous vehicles for research and education. You can find documentation to build your own RoboRacer autonomous racecar, open-sourced course material for beginners, and information on research and physical RoboRacer races. While a physical RoboRacer vehicle is not required for the Sim Racing League, the learning resources are valuable for understanding autonomous racing fundamentals.

Recommended resources for participating in the RoboRacer Sim Racing League:

*   **Competition Documents**

    Learn about the competition rules and technical aspects of the framework.

    [ **Competition Rules**](../roboracer-sim-racing-rules-2025)

    [ **Technical Guide**](../roboracer-sim-racing-guide-2025)

*   **Docker Containers**

    Download base container images for the competition and start developing your algorithms.

    [ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-explore/images/sha256-71556ca735c7d3726150495bae8ffe2093b4c3e6441420d595906f076422bb58) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-practice/images/sha256-b047b7345d9dd81ef4c1faf86a94dd62f4022c78cc8c1693aee39abda0f6208c) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-compete/images/sha256-00a15bc00d60f67e321391b1a8fc0767a0eadf30b50fe07c399e95670111a791)

    [ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-explore/images/sha256-5cca86a81db106773685b41b42301adeeb7721c91cde3cf39e9cf9537b1bdcfe) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-practice/images/sha256-d086c01fa7f6025da18a6b73295e98b62bb6b6ceb9c86fa07a172135c3ceddce) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-compete/images/sha256-98962da9647b124c61176b531e3c788b1c50a77bcb7d5ae44ef5c69034d87b71)

*   **Local Resources**

    Get started with the competition framework locally before focusing on containerization.

    **AutoDRIVE Simulator:**

    `explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_macos.zip)

    `practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_macos.zip)

    `compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_macos.zip)

    **AutoDRIVE Devkit:**

    [ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_devkit.zip)

*   **Quick Links**

    Useful links for the competition.

    **Schedule:** Timeline

    **Registration:** [ Form](https://forms.gle/zjj5dLDajUhnuTdL9)

    **Orientation:** [ Zoom](https://clemson.zoom.us/j/94807115758) | [ Recording](https://youtu.be/Mit9c8B-06o) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/orientation_slides.zip)

    **Communication:** [ Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw)

    **Submission:** [ Phase 1](https://forms.gle/ioZy5SXYrA6DCnhG6) | [ Phase 2](https://forms.gle/MMVAPszcowRppESw9)

    **Results:** Phase 1 | Phase 2

You can post general questions on the [AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace. Technical questions can also be posted as [GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/issues) or [GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/discussions). For other questions, contact [Chinmay Samak](mailto:csamak@clemson.edu) or [Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration

This competition is open to everyone worldwide. Teams can consist of multiple members or a single person.

[Registration Form](https://forms.gle/zjj5dLDajUhnuTdL9)

Registration for the Sim Racing League is free and separate from the Physical Racing League and conference registrations. The form registers you for the Sim Racing League, its orientation, and information sessions. While participation in the Sim Racing League does not require attending the conference, it is strongly encouraged for networking and witnessing the physical RoboRacer competition.

Registered teams are listed below:

| SR. NO. | TEAM NAME                  | TEAM MEMBERS
