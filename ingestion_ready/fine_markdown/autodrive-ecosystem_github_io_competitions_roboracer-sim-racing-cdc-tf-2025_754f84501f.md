# RoboRacer Sim Racing League @ CDC 2025 and Techfest 2025

## About

**RoboRacer Autonomous Racing** is a competition organized by researchers, engineers, and autonomous systems enthusiasts. The 25th and 26th RoboRacer Autonomous Racing Competitions at [CDC 2025](https://cdc2025.ieeecss.org) and [Techfest 2025](https://techfest.org) challenge teams to write software for a 1:10 scaled autonomous racecar to "drive fast but don’t crash!"

This year features the fourth **RoboRacer Sim Racing League**, using the [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to simulate a RoboRacer digital twin on a virtual racetrack. The Sim Racing League is a virtual competition accessible globally. For the [CDC 2025](https://cdc2025.ieeecss.org) and [Techfest 2025](https://techfest.org) competition, teams receive a standardized simulation setup: a digital twin of the RoboRacer vehicle and the Porto racetrack within the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). They also get a working [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to develop perception, planning, and control algorithms that process real-time sensor data and generate control commands.

The competition has two stages:

*   **Qualification Race:** Teams must complete multiple laps around a practice track without colliding with track bounds.
*   **Time-Attack Race:** Teams compete against the clock on a new racetrack to achieve a top leaderboard position.

The standardized vehicle, sensors, simulator, and devkit require teams to develop robust racing algorithms capable of handling uncertainties on unseen racetracks.

For those interested in racing physical RoboRacer vehicles, see the [25th RoboRacer Autonomous Racing Competition](https://cdc2025-race.roboracer.ai) and [26th RoboRacer Autonomous Racing Competition](https://techfest.org/competitions/Roboracer) websites. Both physical and virtual competitions are open for registration.

## Organizers

|                                                              |                                                              |                                                              |                                                              |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu)       | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu)             | [**Dr. Archak Mittal**](mailto:archak@iitb.ac.in)             | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de)          |
|                                                              |                                                              |                                                              |                                                              |
| [**Chinmay Samak**](mailto:csamak@clemson.edu)               | [**Tanmay Samak**](mailto:tsamak@clemson.edu)                 | [**Ahmad Amine**](mailto:aminea@seas.upenn.edu)               | [**Michael Coraluzzi**](mailto:mike.coraluzzi@roboracer.ai) |

## Timeline

**Note:** Timeline is subject to change. Please check this page for updates.

| DATE                | EVENT                               |
| :------------------ | :---------------------------------- |
| Nov 01, 2025        | Registration Opens                  |
| Nov 28, 2025        | Registration Closes                 |
| Nov 29 – Nov 30, 2025 | Qualification Round                 |
| Dec 01, 2025        | Qualification Results Declared      |
| Dec 02, 2025        | Competition Track Released          |
| Dec 06 – Dec 07, 2025 | Final Race                          |
| Dec 08, 2025        | Competition Results Declared        |

**Event Summaries:**

*   **Registration:** Teams register for the Sim Racing League.
*   **Qualification Round:** Teams demonstrate successful completion of 10 laps on a provided practice track.
*   **Qualification Results Declared:** Standings for qualified teams are released.
*   **Competition Track Released:** The official "competition track" for the final race is released.
*   **Final Race:** Teams submit containerized algorithms, which are run in the containerized simulator. Performance metrics are recorded.
*   **Competition Results Declared:** Final race standings are released.

## Resources

[AutoDRIVE](https://autodrive-ecosystem.github.io/) is an open ecosystem for autonomous driving research and education, bridging simulation and hardware with the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Testbed](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Testbed). It also provides the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) for algorithm development. For the Sim Racing League, teams use the Devkit to interface with the Simulator.

[RoboRacer](https://roboracer.ai) is an international community focused on converting 1:10 scale RC cars into autonomous vehicles for research and education. Resources include [documentation](https://roboracer.ai/build.html), [course material](https://roboracer.ai/learn.html), and information on [research](https://roboracer.ai/research.html) and physical [RoboRacer races](https://roboracer.ai/race.html). While a physical RoboRacer is not needed for the Sim Racing League, the learning resources are beneficial.

Recommended resources for the RoboRacer Sim Racing League:

*   **Competition Documents**
    [ **Competition Rules**](../roboracer-sim-racing-rules-2025)
    [ **Technical Guide**](../roboracer-sim-racing-guide-2025)

*   **Docker Containers**
    [ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-explore/images/sha256-72887f78aaa12cf54913f77b41d4d057e8a98e5810b69c203b3653850b38f6c5) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-practice/images/sha256-c4cf1b17646b85036c008c5e1994e4f53a0e340a675fd05ec18c5e03c07f4c0d) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-compete/images/sha256-0ba6cc7c7427eb7fd031bd58b86ee4c65d9ad5e1ceea6725927f7dfb165e320b)
    [ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-explore/images/sha256-15a51f3b7b75085ff1d5a36f3c9b13343cc35c3aa3026afbce8e378c5c8c23b2) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-practice/images/sha256-f0e47bc1e694a366cc1e8fe7e0df9bb2ef77d1cce6b724af90f250ddeb83f395) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-compete/images/sha256-808683287d8d46515d3a9fb26aea97807eae30b7432ec8c2fbee14d1e6d3ca69)

*   **Local Resources**
    **AutoDRIVE Simulator:**
    `explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_macos.zip)
    `practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_macos.zip)
    `compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_macos.zip)
    **AutoDRIVE Devkit:**
    [ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_devkit.zip)

*   **Quick Links**
    **Schedule:** Timeline
    **Registration:** [ Form](https://forms.gle/wGQYoxS1ddevHMcu7)
    **Documentation:** [ Rule Book](../roboracer-sim-racing-rules-2025) | [ Tech Guide](../roboracer-sim-racing-guide-2025)
    **Communication:** [ Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw)
    **Submission:** [ Phase 1](https://forms.gle/X3aaPGwkR9zQTKqm7) | [ Phase 2](https://forms.gle/Y95VyREHS2ABWUgJA)
    **Results:** Phase 1 | Phase 2

Questions can be posted on the [AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw), as [GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/issues), or [GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/discussions). For other inquiries, contact [Chinmay Samak](mailto:csamak@clemson.edu) or [Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration

This competition is open to everyone worldwide. Teams can have multiple members, or be a single person. A person cannot be on more than one team.

[Registration Form](https://forms.gle/wGQYoxS1ddevHMcu7)

Registration for the Sim Racing League is free and separate from physical racing and conference registrations. Participating in the Sim Racing League does not require attending the conference, but attendance is encouraged for community engagement and to witness the physical RoboRacer competition.

Registered teams are listed below:

| SR. NO. | TEAM NAME                  | TEAM MEMBERS
