# RoboRacer Sim Racing League @ CDC 2024

![RoboRacer Sim Racing League @ CDC 2024](../../assets/images/banners/RoboRacer%20Sim%20Racing%20%40%20CDC%202024.png)

## About

**RoboRacer Autonomous Racing** is a semi-regular competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **22nd RoboRacer Autonomous Grand Prix** at [CDC 2024](https://cdc2024.ieeecss.org) will write software for a 1:10 scaled autonomous racecar to fulfill the objectives of the competition: **_drive fast but don’t crash!_**

This time, we are organizing the second **RoboRacer Sim Racing League**, which leverages [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to model and simulate the digital twin of a RoboRacer racecar within a virtual racetrack.

The main focus of the Sim Racing League is a virtual competition with simulated cars and environments, which is accessible to everyone across the globe. For the [CDC 2024](https://cdc2024.ieeecss.org) competition, each team will be provided with a standardized simulation setup (in the form of a digital twin of the RoboRacer vehicle, and a digital twin of the Porto racetrack) within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to get started with developing their autonomy algorithms. Teams will have to develop perception, planning, and control algorithms to parse the real-time sensor data streamed from the simulator and generate control commands to be fed back to the simulated vehicle.

The competition will take place in 2 stages:

*   **Qualification Race:** Teams will demonstrate their ability to complete multiple laps around the practice track without colliding with the track bounds at run time.
*   **Time-Attack Race:** Teams will compete against the clock, on a previously unseen racetrack, to secure a position on the leaderboard.

Since the vehicle, the sensors, the simulator, and the devkit are standardized, teams must develop robust racing algorithms that can deal with the uncertainties of an unseen racetrack.

If you are interested in autonomously racing physical RoboRacer vehicles, please check out the website for [22nd RoboRacer Autonomous Racing Competition](https://cdc2024-race.f1tenth.org), which will be held in person at [CDC 2024](https://cdc2024.ieeecss.org). You can always register and compete in both physical and virtual competitions!

## Organizers

[**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu) | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu) | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de) | [**Chinmay Samak**](mailto:csamak@clemson.edu) | [**Tanmay Samak**](mailto:tsamak@clemson.edu)
[**Ahmad Amine**](mailto:aminea@seas.upenn.edu) | [**Dr. Paolo Burgio**](mailto:paolo.burgio@unimore.it) | [**Dr. Maria Prandini**](mailto:maria.prandini@polimi.it) | [**Dr. Martina Maggio**](mailto:maggio@cs.uni-saarland.de) | [**Dr. Alessio Masola**](mailto:alessio.masola@unimore.it)
[**Dr. Filippo Muzzini**](mailto:filippo.muzzini@unimore.it) | [**Dr. Federico Gavioli**](mailto:224833@studenti.unimore.it) | [**Antonio Russo**](mailto:270201@studenti.unimore.it) | [**Enrico Mannocci**](mailto:enrico.mannocci3@unibo.it) |

## Timeline

Timeline is subject to change. Please keep checking this page for any updates.

| DATE                       | EVENT                                     |
| :------------------------- | :---------------------------------------- |
| Aug 01, 2024               | Registration Opens                        |
| Oct 31, 2024               | Registration Closes                       |
| Nov 08, 2024 (5:30 – 6:30 PM EST) | [Online Orientation 1](https://clemson.zoom.us/j/92399406829) |
| Nov 23, 2024 (1:00 – 2:00 PM EST) | [Online Orientation 2](https://clemson.zoom.us/j/98938663143) |
| Nov 30 – Dec 01, 2024      | Qualification Round                       |
| Dec 02, 2024               | Qualification Results Declared            |
| Dec 04, 2024               | Competition Track Released                |
| Dec 07 – Dec 08, 2024      | Final Race                                |
| Dec 09, 2024               | Competition Results Declared              |

Following is a brief summary of each event:

*   **Registration:** Interested teams will register for the Sim Racing League.
*   **Online Orientation 1:** Organizers will explain the competition rules and guidelines, and demonstrate how to use the simulation framework.
*   **Online Orientation 2:** Organizers will check progress of the participating teams and help with any technical difficulties.
*   **Qualification Round:** Teams will demonstrate successful completion of 10 laps around the practice track provided ahead of time.
*   **Qualification Results Declared:** Standings of all the qualified teams will be released.
*   **Competition Track Released:** Organizers will release the actual "competition track", which will be used for the final race. This track may be replicated in the physical race as well.
*   **Final Race:** Organizers will collect containerized algorithms from each team and connect them with the containerized simulator. Performance metrics of each team will be recorded.
*   **Competition Results Declared:** Standings of all the teams for the final race will be released.

The RoboRacer Sim Racing League will be held approximately 1 week ahead of [CDC 2024](https://cdc2024.ieeecss.org) and the performance metrics will be made available to the teams. We have also been able to organize a [special session](https://css.paperplaza.net/conferences/conferences/CDC24/program/CDC24_ContentListWeb_1.html#moevsp1_01) for [RoboRacer Sim Racing League Celebration](https://cdc2024.ieeecss.org/program/competitions#session-10-44) on Monday (Dec 16), 18:00-19:00 CET with the help of the CDC organizing committee. Join the celebration event to relive the nail-biting races, hear the top teams brag about their winning strategies (~5 min presentations), and start your engines for the physical competition.

## Resources

[AutoDRIVE](https://autodrive-ecosystem.github.io/) is envisioned to be an open, comprehensive, flexible and integrated cyber-physical ecosystem for enhancing autonomous driving research and education. It bridges the gap between software simulation and hardware deployment by providing the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Testbed](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Testbed), a well-suited duo for real2sim and sim2real transfer targeting vehicles and environments of varying scales and operational design domains. It also offers [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit), a developer's kit for rapid and flexible development of autonomy algorithms using a variety of programming languages and software frameworks. For the Sim Racing League, teams will develop their autonomous racing algorithms using the AutoDRIVE Devkit to interface with the AutoDRIVE Simulator in real-time.

[RoboRacer](https://roboracer.ai) is an [international community](https://roboracer.ai/about.html) of researchers, engineers, and autonomous systems enthusiasts. It is centered around the idea of converting a 1:10 scale RC car into an autonomous vehicle for research and education; check out the [documentation](https://roboracer.ai/build.html) to build your own RoboRacer autonomous racecar. Additionally, if you are new to the field of autonomous racing, you can refer to the complete [course material](https://roboracer.ai/learn.html), which is open sourced. If you already have some experience with autonomous racing, feel free to delve deeper into the [research](https://roboracer.ai/research.html) enabled by RoboRacer. Lastly, you can also check out the physical [RoboRacer races](https://roboracer.ai/race.html) that are being organized all around the world. For the Sim Racing League, teams will not require a physical RoboRacer vehicle; however, the learning resources can certainly be useful to get your autonomous racing fundamentals right!

We recommend all the teams interested in participating in the RoboRacer Sim Racing League to get accustomed with the competition. Following are a few resources to get you started:

*   **Competition Documents**

    Learn about the competition rules and technical aspects of the framework.

    [ **Competition Rules**](../roboracer-sim-racing-rules-2024)

    [ **Technical Guide**](../roboracer-sim-racing-guide-2024)

*   **Docker Containers**

    Download base container images for the competition and start developing your algorithms.

    [ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-explore/images/sha256-6a4a9aab20e5deafdcf1a8318b4f270d409b557ba198888fd701eb56506760c7) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-practice/images/sha256-07126b3b4bcf7d6ff43a7d76f9ba84412b2553784026d27b7e4ebdab269c4c6f) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-compete/images/sha256-e0b511807cdc5597e9da3e3c1f630750476dd9a6a56f14187f79ca15ad72ad5e)

    [ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-explore/images/sha256-221ab09c92720fc9ed324839ec81da6aceb4c5c12ae1e46b8733c2275cb000f1) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-practice/images/sha256-d3fd68b51ec6934d8de283c14be5d5b5d8e3c536599eeeef652a16f47cce103d) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-compete/images/sha256-6596fa4eed9521f61d2fb3dc43c52bb0affbf3e7e2a197e1afb6ef03894694a7)

*   **Local Resources**

    Get started with the competition framework locally, and worry about containerization later.

    **AutoDRIVE Simulator:**

    `explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_macos.zip)

    `practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_macos.zip)

    `compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_macos.zip)

    **AutoDRIVE Devkit:**

    [ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_devkit.zip)

*   **Orientation Resources**

    Join the online orientation sessions or review what we covered there.

    **Orientation 1:**

    Meeting Link: [ Zoom](https://clemson.zoom.us/j/92399406829)

    Review Links: [ Recording](https://youtu.be/WQyhXQtFC0o) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/orientation_1_slides.zip)

    **Orientation 2:**

    Meeting Link: [ Zoom](https://clemson.zoom.us/j/98938663143)

    Review Links: [ Recording](https://youtu.be/MxCDt1A4Wbo) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/orientation_2_slides.zip)

You can post general questions on the [ AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace; this is the preferred modality. Technical questions can be also posted as [ GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/issues) or [ GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/discussions). For any other questions or concerns that cannot be posted publicly, please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration

This competition is open to everyone around the world - students, researchers, hobbyists, professionals, or anyone else who is interested. A team can consist of multiple teammates. Teams with only one person are also allowed.

[ Registration Form](https://forms.gle/D6X2C5PMwmDWEWbo9)

Registration for the Sim Racing League is free of cost and separate from the Physical Racing League and the conference registrations themselves. The above form signs you up only for the Sim Racing League, and for its orientation and information sessions. Although you can participate in the Sim Racing League without attending the conference, we strongly encourage all competition participants to attend the conference in person. This will help you connect with the broader AutoDRIVE and RoboRacer communities, and you can also witness/participate in the physical RoboRacer autonomous racing competition!

Registered teams are added to the following table:

| SR. NO. | TEAM NAME                                                  | TEAM MEMBERS
