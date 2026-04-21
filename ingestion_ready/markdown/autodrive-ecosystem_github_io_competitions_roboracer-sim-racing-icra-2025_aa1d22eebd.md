Skip to content

# RoboRacer Sim Racing League @ ICRA 2025¶

![RoboRacer Sim Racing League @ ICRA 2025](../../assets/images/banners/RoboRacer%20Sim%20Racing%20%40%20ICRA%202025.png)

## About¶

**RoboRacer Autonomous Racing** is a semi-regular competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **24th RoboRacer Autonomous Racing Competition** at [ICRA 2025](https://2025.ieee-icra.org) will write software for a 1:10 scaled autonomous racecar to fulfill the objectives of the competition: **_drive fast but don’t crash!_**

This time, we are organizing the third **RoboRacer Sim Racing League** , which leverages [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to model and simulate the digital twin of a RoboRacer racecar within a virtual racetrack. Please see the accompanying video for a glimpse of the RoboRacer digital twins in action.

The main focus of the Sim Racing League is a virtual competition with simulated cars and environments, which is accessible to everyone across the globe. For the [ICRA 2025](https://2025.ieee-icra.org) competition, each team will be provided with a standardized simulation setup (in the form of a digital twin of the RoboRacer vehicle, and a digital twin of the Porto racetrack) within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to get started with developing their autonomy algorithms. Teams will have to develop perception, planning, and control algorithms to parse the real-time sensor data streamed from the simulator and generate control commands to be fed back to the simulated vehicle.

The competition will take place in 2 stages:

  * **Qualification Race:** Teams will demonstrate their ability to complete multiple laps around the practice track without colliding with the track bounds at run time.
  * **Time-Attack Race:** Teams will compete against the clock, on a previously unseen racetrack, to secure a position on the leaderboard.

Since the vehicle, the sensors, the simulator, and the devkit are standardized, teams must develop robust racing algorithms that can deal with the uncertainties of an unseen racetrack.

Tip

If you are interested in autonomously racing physical RoboRacer vehicles, please check out the website for [24th RoboRacer Autonomous Racing Competition](https://icra2025-race.roboracer.ai), which will be held in person at [ICRA 2025](https://2025.ieee-icra.org). You can always register and compete in both physical and virtual competitions!

## Organizers¶

![](/../assets/images/people/Rahul Mangharam.png) | ![](/../assets/images/people/Venkat Krovi.png) | ![](/../assets/images/people/Johannes Betz.png)
---|---|---
[**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu) | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu) | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de)
![](/../assets/images/people/Chinmay Samak.png) | ![](/../assets/images/people/Tanmay Samak.png) | ![](/../assets/images/people/Ahmad Amine.png)
[**Chinmay Samak**](mailto:csamak@clemson.edu) | [**Tanmay Samak**](mailto:tsamak@clemson.edu) | [**Ahmad Amine**](mailto:aminea@seas.upenn.edu)

## Timeline¶

Warning

Timeline is subject to change. Please keep checking this page for any updates.

DATE | EVENT
---|---
Feb 20, 2025 | Registration Opens
Apr 15, 2025 | Registration Closes
Apr 16, 2025 (5:30 – 6:30 PM EDT) | [Online Orientation](https://clemson.zoom.us/j/94807115758)
May 03 – May 05, 2025 | Qualification Round
May 06, 2025 | Qualification Results Declared
May 08, 2025 | Competition Track Released
May 11 – May 13, 2025 | Final Race
May 14, 2025 | Competition Results Declared

Following is a brief summary of each event:

  * **Registration:** Interested teams will register for the Sim Racing League.
  * **Online Orientation:** Organizers will explain the competition rules and guidelines, and demonstrate how to use the simulation framework.
  * **Qualification Round:** Teams will demonstrate successful completion of 10 laps around the practice track provided ahead of time.
  * **Qualification Results Declared:** Standings of all the qualified teams will be released.
  * **Competition Track Released:** Organizers will release the actual "competition track", which will be used for the final race. This track may be replicated in the physical race as well.
  * **Final Race:** Organizers will collect containerized algorithms from each team and connect them with the containerized simulator. Performance metrics of each team will be recorded.
  * **Competition Results Declared:** Standings of all the teams for the final race will be released.

Info

The RoboRacer Sim Racing League will be held approximately 1 week ahead of [ICRA 2025](https://2025.ieee-icra.org) and the performance metrics will be made available to the teams. Discussions are underway with the ICRA organizing team to allow teams to analyze and present their approach/results in a short (~10 min) presentation in a special session at [ICRA 2025](https://2025.ieee-icra.org).

## Resources¶

![](/../assets/images/logos/AutoDRIVE Logo.png)

[AutoDRIVE](https://autodrive-ecosystem.github.io/) is envisioned to be an open, comprehensive, flexible and integrated cyber-physical ecosystem for enhancing autonomous driving research and education. It bridges the gap between software simulation and hardware deployment by providing the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Testbed](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Testbed), a well-suited duo for real2sim and sim2real transfer targeting vehicles and environments of varying scales and operational design domains. It also offers [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit), a developer's kit for rapid and flexible development of autonomy algorithms using a variety of programming languages and software frameworks. For the Sim Racing League, teams will develop their autonomous racing algorithms using the AutoDRIVE Devkit to interface with the AutoDRIVE Simulator in real-time.

![](/../assets/images/logos/RoboRacer Logo.png)

[RoboRacer](https://roboracer.ai) is an [international community](https://roboracer.ai/about.html) of researchers, engineers, and autonomous systems enthusiasts. It is centered around the idea of converting a 1:10 scale RC car into an autonomous vehicle for research and education; check out the [documentation](https://roboracer.ai/build.html) to build your own RoboRacer autonomous racecar. Additionally, if you are new to the field of autonomous racing, you can refer to the complete [course material](https://roboracer.ai/learn.html), which is open sourced. If you already have some experience with autonomous racing, feel free to delve deeper into the [research](https://roboracer.ai/research.html) enabled by RoboRacer. Lastly, you can also check out the physical [RoboRacer races](https://roboracer.ai/race.html) that are being organized all around the world. For the Sim Racing League, teams will not require a physical RoboRacer vehicle; however, the learning resources can certainly be useful to get your autonomous racing fundamentals right!

We recommend all the teams interested in participating in the RoboRacer Sim Racing League to get accustomed with the competition. Following are a few resources to get you started:

  * **Competition Documents**

* * *

Learn about the competition rules and technical aspects of the framework.

[ **Competition Rules**](../roboracer-sim-racing-rules-2025)

[ **Technical Guide**](../roboracer-sim-racing-guide-2025)

  * **Docker Containers**

* * *

Download base container images for the competition and start developing your algorithms.

[ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-explore/images/sha256-71556ca735c7d3726150495bae8ffe2093b4c3e6441420d595906f076422bb58) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-practice/images/sha256-b047b7345d9dd81ef4c1faf86a94dd62f4022c78cc8c1693aee39abda0f6208c) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-icra-compete/images/sha256-00a15bc00d60f67e321391b1a8fc0767a0eadf30b50fe07c399e95670111a791)

[ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-explore/images/sha256-5cca86a81db106773685b41b42301adeeb7721c91cde3cf39e9cf9537b1bdcfe) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-practice/images/sha256-d086c01fa7f6025da18a6b73295e98b62bb6b6ceb9c86fa07a172135c3ceddce) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-icra-compete/images/sha256-98962da9647b124c61176b531e3c788b1c50a77bcb7d5ae44ef5c69034d87b71)

  * **Local Resources**

* * *

Get started with the competition framework locally, and worry about containerization later.

**AutoDRIVE Simulator:**

`explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_explore_macos.zip)

`practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_practice_macos.zip)

`compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_simulator_compete_macos.zip)

**AutoDRIVE Devkit:**

[ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/autodrive_devkit.zip)

  * **Quick Links**

* * *

Links to be kept at your fingertips, for a smooth ride throughout the competition.

**Schedule:** Timeline

**Registration:** [ Form](https://forms.gle/zjj5dLDajUhnuTdL9)

**Orientation:** [ Zoom](https://clemson.zoom.us/j/94807115758) | [ Recording](https://youtu.be/Mit9c8B-06o) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-icra/orientation_slides.zip)

**Communication:** [ Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw)

**Submission:** [ Phase 1](https://forms.gle/ioZy5SXYrA6DCnhG6) | [ Phase 2](https://forms.gle/MMVAPszcowRppESw9)

**Results:** Phase 1 |  Phase 2

Question

You can post general questions on the [ AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace; this is the preferred modality. Technical questions can be also posted as [ GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/issues) or [ GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/discussions). For any other questions or concerns that cannot be posted publicly, please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration¶

This competition is open to everyone around the world - students, researchers, hobbyists, professionals, or anyone else who is interested. A team can consist of multiple teammates. Teams with only one person are also allowed.

[ Registration Form](https://forms.gle/zjj5dLDajUhnuTdL9)

Registration for the Sim Racing League is free of cost and separate from the Physical Racing League and the conference registrations themselves. The above form signs you up only for the Sim Racing League, and for its orientation and information sessions. Although you can participate in the Sim Racing League without attending the conference, we strongly encourage all competition participants to attend the conference in person. This will help you connect with the broader AutoDRIVE and RoboRacer communities, and you can also witness/participate in the physical RoboRacer autonomous racing competition!

Registered teams are added to the following table:

SR. NO. | TEAM NAME | TEAM MEMBERS | ORGANIZATION | COUNTRY
01 | fsociety | Ritesh Gole
Kartikeya Gupta
Raj Shah
Goutham Jyothilal | Personal | India
02 | Chasing Cop Car | Jaihind J
Aditya Ravichander | Personal | India
03 | Alp Autonomous | Ble Auriol | Alpha Space Robotics | Côte d'Ivoire
04 | Bushra AlShehhi | Bushra AlShehhi | Khalifa University | United Arab Emirates (UAE)
05 | Technion F1TENTH Team | Andrés Kaminker | Technion | Israel
06 | bracavisionai | Luis Bracamontes | Personal | Mexico
07 | Finding Theta | Michael Kudlaty | Personal | United States of America (USA)
08 | Team | Rajdeep Singh | Personal | India
09 | Mostafa Ahmed Sayed | Mostafa Hassan | Personal | Egypt
10 | Invincibles | Elyas Saeed
Ahmad Aljallaf
Ali Asaad Al-Behadili
Abdelrahman Zidan | Khalifa University | United Arab Emirates (UAE)
11 | FuzzyGreenBlurs | Akhil Sankar | Rutgers University | United States of America (USA)
12 | CarGoesVroom | WenYang Lim | Personal | Malaysia
13 | Autobots | Shubham Barge
Anshuman Jena
Saivamshi Jilla | Personal | India
14 | Baby Driver | Mason Notz
Pallavi Kulkarni | Personal | United States of America (USA)
15 | TURTLEBOT | Jit Ern Lim
Dustin Lim | Personal | Malaysia, Indonesia
16 | Cair's | Siddhant Diwaker
Chirag Makwana | Personal | India
17 | BONG_RACERS | Srinjoy Ganguly
Pritish Saha
Srijit Das | Personal | India
18 | AA Lab | Taha Kocyigit
Omer Geyikci | Bogazici University | Türkiye
19 | SUST Autodrive | Abul Bashar Raz | Shahjalal University of Science and Technology | Bangladesh
20 | Beep Beep | Jeremy Seyssaud | Personal | France
21 | Circuit Breakers | Thanushraam Suresh Kumar
Dhruv Pathak
Atharva Patil | University of Colorado, Boulder | United States of America (USA)
22 | Mamba | Hariharan Ravichandran | Personal | United States of America (USA)
23 | Racer X | Jonathan Nixon
Roberto Ligeralde | Autonomous Racing at Penn | United States of America (USA)
24 | IDEA_LAB | Ji-Hong Park
Kim Ju-Young
Chanki Kim
Sujin Park
Se Yeon Lee | Gyeongsang National University | South Korea
25 | Abdulrahman Mahmoud | Abdulrahman Mahmoud | Personal | Egypt
26 | ESL | Christopher Flood
Nico Martin
JC Schoeman | Stellenbosch University | South Africa
27 | VAUL | William Fecteau
Nicolas Lauzon
Tommy Bouchard-Lebrun | Laval University | Canada
28 | Wall-E | Vinura Wanniarachchi | Personal | Sri Lanka
29 | SoloDriver | Hana Nabhan | Personal | Egypt
30 | Robotikusu | Ananay Shiv | Indian Institute of Technology, Kharagpur | India
31 | Shelby | S. Srikaanth
S. Vignesh
S. A. Gogulnath | Personal | India
32 | MMS Autonomous | Osama Helal
Ahmed Mwafy
Abdelrahman Arafa
Kirellos Youssef
Kareem El Zahaby | Mansoura University | Egypt
33 | Escuderia Poliposition | Fernando Zolubas Preto
Antonio Colombini Neto
Carlos Alberto Arronte Delgado
Gabriel Stephano Santos
Luccas Barsotti
Francisco Rodrigues Marazia
Amanda Spagolla | Polytechnic School of the University of São Paulo | Brazil
34 | Raptor | Ji Su Lee | Personal | South Korea
35 | Humble-CV | Ayush David
Basil Shaji
Cyril Jacob | Karunya Institute of Technology and Sciences | India
36 | Zancle E-Drive | Gaetano Pio Pispisa
Giovanni Lombardo
Simone Castorino
Gabriele Rinaldi
Andrea Ferdinando Longoni | University of Messina | Italy
37 | Riverside Racers | Alexander Totah
Marcus Hsieh
Amber Lin
James Liu
Hang Qiu | University of California, Riverside | United States of America (USA)
38 | IslandDriver | Eunhye Lee | Stony Brook University | United States of America (USA)
39 | ICPS | Juan Tique
Donovan Ho
Andrew Mitchell | iCPS Lab, University of Central Florida | United States of America (USA)
40 | Kanka | Yukang Cao
Goktug Poyrazoglu | University of Minnesota | United States of America (USA)
41 | Ctrl+Drift | Aditya Jambhale
Chaitanya Bhatia
Kaustubh Krishna
Akshat Tambi
Prerna Sharma
Yashowardhan Singh | SRM Institute of Science and Technology | India
42 | Overtechnologia | Aditya Paul | Personal | India
43 | Autonomous Ground Vehicle | Swaminathan S K
Shreyansh Kansal
Daksh Yadav
Ninaad Desai
Rohan Singh
Sandip Das
Utsab Karan
Varun Thirupathy
Aditya Srivastava
Sreyas Venkataraman
Theyanesh E R | Indian Institute of Technology, Kharagpur | India
44 | CAVREL-UCF | Israel Charles
Babak Soorchaei
Devin Hunter
Yaser Fallah | University of Central Florida | United States of America (USA)
45 | Autoware Aces | Po-Jen Wang
Tran Huu Nhat Huy
Alexander Kalmykov
Atanasko Boris Mitrev | Autoware Foundation | United States of America (USA), Japan, Russia, North Macedonia
46 | Ashesi ARCLab | Emmanuel Korankye
William Akuffo
Joshua Nti
Reginald Andrew Sai-Obadai
Baron Afutu
Joel Osei-Asamoah
Kobena Enyam
Samuel Akwensivie
Appenteng Adjepong
Desmond Hammond | Ashesi University | Ghana
47 | QuillKraft | Aryan Iyer | Indian Institute of Technology, Bombay | India
48 | PowerZero | Ramana Botta
Venkat Prasad | Personal | India
49 | WARRacing | Dominik Schneider
Danit Niwattananan
Parham Rahimi | Personal | Germany
50 | The Impressionists | Tanay Shah | Personal | India
51 | WATonomous | Rodney Dong
Mark Do
Harsharan Rakhra
Manjot Dola | University of Waterloo WATonomous Design Team | Canada
52 | UO Autonomous Drive | David Miranda
Lucía Sánchez
Miguel Santamaría | University of Oviedo | Spain
53 | Smirnov Racing | Kirill Smirnov | K. Smirnov Robotics Ltd. | Cyprus
54 | RUN-RUN-ChuraTaro | Soya Aoki | Chura DATA Inc. | Japan
55 | Arcanine | Shreyas Raorane | University of Pennslvania | United States of America (USA)
56 | orangetongue | Vittorio Cataffo
Francesca Cataffo
Federica Cataffo | Personal | Italy
57 | AsTenth Martin | Ajay Shankar Sriram | Chura DATA Inc. | United States of America (USA)
58 | PITT | Aragya Goyal
Robert Exley | University of Pittsburgh | United States of America (USA)

Note

The above table will be updated with newly registered teams within a few days of registration. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you do not see your team entry for more than 7 days after registering.

![](/../assets/images/competitions/2025 icra roboracer sim racing league/Collage.png)

## Submission¶

Use the secure form below to make your team's submission for Phase 1 (Qualification Round) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 1 Submission Form](https://forms.gle/ioZy5SXYrA6DCnhG6)

Warning

Phase 1 submission window will close on May 03, 2025 (anywhere on Earth). Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

Use the secure form below to make your team's submission for Phase 2 (Final Race) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 2 Submission Form](https://forms.gle/MMVAPszcowRppESw9)

Warning

Phase 2 submission window will close on May 11, 2025 (anywhere on Earth). Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

## Results¶

**Phase 1: Qualification**

The following teams have qualified for the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 👏 Autonomous Ground Vehicle | 67.86 s | 0 | 67.86 s | 6.77 s | [ YouTube](https://www.youtube.com/watch?v=VKbfRomFJDs)
02 | 👏 VAUL | 71.30 s | 0 | 71.30 s | 7.06 s | [ YouTube](https://www.youtube.com/watch?v=XvATpKFpMTk)
03 | 👏 Ctrl+Drift | 81.32 s | 0 | 81.32 s | 8.03 s | [ YouTube](https://www.youtube.com/watch?v=AmnK0JQ3ayQ)
04 | 👏 Ashesi ARCLab | 82.02 s | 0 | 82.02 s | 8.12 s | [ YouTube](https://www.youtube.com/watch?v=atS4VkU-NDc)
05 | 👏 ICPS | 82.70 s | 0 | 82.70 s | 8.24 s | [ YouTube](https://www.youtube.com/watch?v=PafZhFbtwP8)
06 | 👏 Escuderia Poliposition | 75.18 s | 1 | 85.18 s | 7.40 s | [ YouTube](https://www.youtube.com/watch?v=V7Xzswo91Ic)
07 | 👏 TURTLEBOT | 84.48 s | 1 | 94.48 s | 8.03 s | [ YouTube](https://www.youtube.com/watch?v=pxmvkxcWw7c)
08 | 👏 IDEA_LAB | 95.12 s | 0 | 95.12 s | 9.35 s | [ YouTube](https://www.youtube.com/watch?v=XdkDexM9oWE)
09 | 👏 UO Autonomous Drive | 81.37 s | 2 | 101.37 s | 8.01 s | [ YouTube](https://www.youtube.com/watch?v=k0GN7XYCuxU)
10 | 👏 Chasing Cop Car | 90.97 s | 2 | 110.97 s | 9.04 s | [ YouTube](https://www.youtube.com/watch?v=Q2wCUHkaB3c)
11 | 👏 Mamba | 118.15 s | 0 | 118.15 s | 11.79 s | [ YouTube](https://www.youtube.com/watch?v=p8Qr2_OBiQU)
12 | 👏 Racer X | 97.65 s | 3 | 127.65 s | 9.57 s | [ YouTube](https://www.youtube.com/watch?v=gAqO3CEhe4c)
13 | 👏 Zancle E-Drive | 128.71 s | 0 | 128.71 s | 12.69 s | [ YouTube](https://www.youtube.com/watch?v=9hFu3PFkdEc)
14 | 👏 WARRacing | 128.76 s | 1 | 138.76 s | 12.79 s | [ YouTube](https://www.youtube.com/watch?v=LBekcSYnj1s)
15 | 👏 MMS Autonomous | 120.25 s | 3 | 150.25 s | 11.74 s | [ YouTube](https://www.youtube.com/watch?v=MWCyzOFxg6I)
16 | 👏 RUN-RUN-ChuraTaro | 94.35 s | 6 | 154.35 s | 8.89 s | [ YouTube](https://www.youtube.com/watch?v=evYS4Ko18vo)
17 | 👏 Kanka | 141.43 s | 2 | 161.43 s | 13.86 s | [ YouTube](https://www.youtube.com/watch?v=Qen9MtQQS3Q)
18 | 👏 Autoware Aces | 71.14 s | 10 | 171.14 s | 6.89 s | [ YouTube](https://www.youtube.com/watch?v=0xlkFJhtXHY)
19 | 👏 bracavisionai | 187.69 s | 1 | 197.69 s | 18.56 s | [ YouTube](https://www.youtube.com/watch?v=fguceh6xZ-k)
20 | 👏 Bushra AlShehhi | 226.40 s | 1 | 236.40 s | 22.26 s | [ YouTube](https://www.youtube.com/watch?v=mci9wVYnv-w)
21 | 👏 ESL | 290.78 s | 1 | 300.78 s | 28.97 s | [ YouTube](https://www.youtube.com/watch?v=lb_aRrXptFM)

**Phase 2: Competition**

The following teams successfully finished the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 🥇 VAUL | 111.46 s | 0 | 111.46 s | 11.28 s | [ YouTube](https://www.youtube.com/watch?v=oZ2VSZ34sW0)
02 | 🥈 Autoware Aces | 122.16 s | 0 | 122.16 s | 12.08 s | [ YouTube](https://www.youtube.com/watch?v=oaA02UnakHA)
03 | 🥉 Kanka | 129.28 s | 0 | 129.28 s | 12.76 s | [ YouTube](https://www.youtube.com/watch?v=XbWIewaOPfM)
04 | 👏 UO Autonomous Drive | 137.42 s | 0 | 137.42 s | 13.70 s | [ YouTube](https://www.youtube.com/watch?v=tarOUcH42_8)
05 | 👏 ESL | 155.81 s | 0 | 155.81 s | 15.52 s | [ YouTube](https://www.youtube.com/watch?v=AkMqvP502co)
06 | 👏 IDEA_LAB | 193.24 s | 0 | 193.24 s | 18.33 s | [ YouTube](https://www.youtube.com/watch?v=7dDAAQbR4dY)
07 | 👏 Ashesi ARCLab | 188.67 s | 2 | 208.67 s | 18.67 s | [ YouTube](https://www.youtube.com/watch?v=sRbtkivA7tY)
08 | 👏 bracavisionai | 221.03 s | 0 | 221.03 s | 22.06 s | [ YouTube](https://www.youtube.com/watch?v=IHeRv5ammHU)
09 | 👏 Autonomous Ground Vehicle | 226.71 s | 0 | 226.71 s | 22.54 s | [ YouTube](https://www.youtube.com/watch?v=U9_lRkEmCtQ)
10 | 👏 Zancle E-Drive | 149.19 s | 10 | 249.19 s | 14.81 s | [ YouTube](https://www.youtube.com/watch?v=Wy4rXx_UaUk)
10 | 👏 RUN-RUN-ChuraTaro | 275.71 s | 0 | 275.71 s | 27.36 s | [ YouTube](https://www.youtube.com/watch?v=VujkuVcB3eg)
12 | 👏 Escuderia Poliposition | 191.05 s | 10 | 291.05 s | 19.05 s | [ YouTube](https://www.youtube.com/watch?v=dkC1mroUt5k)
13 | 👏 ICPS | 297.31 s | 4 | 337.31 s | 29.02 s | [ YouTube](https://www.youtube.com/watch?v=YMzhB9NgW7E)
14 | 👏 Ctrl+Drift | 287.98 s | 10 | 387.98 s | 28.74 s | [ YouTube](https://www.youtube.com/watch?v=bL3KXh52gs4)
15 | 👏 Bushra AlShehhi | 395.36 s | 1 | 405.36 s | 37.76 s | [ YouTube](https://www.youtube.com/watch?v=gFaLzf5wjSA)

## Summary¶

Back to top
