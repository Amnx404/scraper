Skip to content

# RoboRacer Sim Racing League @ CDC 2024¶

![RoboRacer Sim Racing League @ CDC 2024](../../assets/images/banners/RoboRacer%20Sim%20Racing%20%40%20CDC%202024.png)

## About¶

**RoboRacer Autonomous Racing** is a semi-regular competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **22nd RoboRacer Autonomous Grand Prix** at [CDC 2024](https://cdc2024.ieeecss.org) will write software for a 1:10 scaled autonomous racecar to fulfill the objectives of the competition: **_drive fast but don’t crash!_**

This time, we are organizing the second **RoboRacer Sim Racing League** , which leverages [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to model and simulate the digital twin of a RoboRacer racecar within a virtual racetrack. Please see the accompanying video for a glimpse of the RoboRacer digital twins in action.

The main focus of the Sim Racing League is a virtual competition with simulated cars and environments, which is accessible to everyone across the globe. For the [CDC 2024](https://cdc2024.ieeecss.org) competition, each team will be provided with a standardized simulation setup (in the form of a digital twin of the RoboRacer vehicle, and a digital twin of the Porto racetrack) within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to get started with developing their autonomy algorithms. Teams will have to develop perception, planning, and control algorithms to parse the real-time sensor data streamed from the simulator and generate control commands to be fed back to the simulated vehicle.

The competition will take place in 2 stages:

  * **Qualification Race:** Teams will demonstrate their ability to complete multiple laps around the practice track without colliding with the track bounds at run time.
  * **Time-Attack Race:** Teams will compete against the clock, on a previously unseen racetrack, to secure a position on the leaderboard.

Since the vehicle, the sensors, the simulator, and the devkit are standardized, teams must develop robust racing algorithms that can deal with the uncertainties of an unseen racetrack.

Tip

If you are interested in autonomously racing physical RoboRacer vehicles, please check out the website for [22nd RoboRacer Autonomous Racing Competition](https://cdc2024-race.f1tenth.org), which will be held in person at [CDC 2024](https://cdc2024.ieeecss.org). You can always register and compete in both physical and virtual competitions!

## Organizers¶

![](/../assets/images/people/Rahul Mangharam.png) | ![](/../assets/images/people/Venkat Krovi.png) | ![](/../assets/images/people/Johannes Betz.png) | ![](/../assets/images/people/Chinmay Samak.png) | ![](/../assets/images/people/Tanmay Samak.png)
[**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu) | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu) | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de) | [**Chinmay Samak**](mailto:csamak@clemson.edu) | [**Tanmay Samak**](mailto:tsamak@clemson.edu)
![](/../assets/images/people/Ahmad Amine.png) | ![](/../assets/images/people/Paolo Burgio.png) | ![](/../assets/images/people/Maria Prandini.png) | ![](/../assets/images/people/Martina Maggio.png) | ![](/../assets/images/people/Alessio Masola.png)
[**Ahmad Amine**](mailto:aminea@seas.upenn.edu) | [**Dr. Paolo Burgio**](mailto:paolo.burgio@unimore.it) | [**Dr. Maria Prandini**](mailto:maria.prandini@polimi.it) | [**Dr. Martina Maggio**](mailto:maggio@cs.uni-saarland.de) | [**Dr. Alessio Masola**](mailto:alessio.masola@unimore.it)
![](/../assets/images/people/Filippo Muzzini.png) | ![](/../assets/images/people/Federico Gavioli.png) | ![](/../assets/images/people/Antonio Russo.png) | ![](/../assets/images/people/Enrico Mannocci.png) |
[**Dr. Filippo Muzzini**](mailto:filippo.muzzini@unimore.it) | [**Dr. Federico Gavioli**](mailto:224833@studenti.unimore.it) | [**Antonio Russo**](mailto:270201@studenti.unimore.it) | [**Enrico Mannocci**](mailto:enrico.mannocci3@unibo.it) |

## Timeline¶

Warning

Timeline is subject to change. Please keep checking this page for any updates.

DATE | EVENT
---|---
Aug 01, 2024 | Registration Opens
Oct 31, 2024 | Registration Closes
Nov 08, 2024 (5:30 – 6:30 PM EST) | [Online Orientation 1](https://clemson.zoom.us/j/92399406829)
Nov 23, 2024 (1:00 – 2:00 PM EST) | [Online Orientation 2](https://clemson.zoom.us/j/98938663143)
Nov 30 – Dec 01, 2024 | Qualification Round
Dec 02, 2024 | Qualification Results Declared
Dec 04, 2024 | Competition Track Released
Dec 07 – Dec 08, 2024 | Final Race
Dec 09, 2024 | Competition Results Declared

Following is a brief summary of each event:

  * **Registration:** Interested teams will register for the Sim Racing League.
  * **Online Orientation 1:** Organizers will explain the competition rules and guidelines, and demonstrate how to use the simulation framework.
  * **Online Orientation 2:** Organizers will check progress of the participating teams and help with any technical difficulties.
  * **Qualification Round:** Teams will demonstrate successful completion of 10 laps around the practice track provided ahead of time.
  * **Qualification Results Declared:** Standings of all the qualified teams will be released.
  * **Competition Track Released:** Organizers will release the actual "competition track", which will be used for the final race. This track may be replicated in the physical race as well.
  * **Final Race:** Organizers will collect containerized algorithms from each team and connect them with the containerized simulator. Performance metrics of each team will be recorded.
  * **Competition Results Declared:** Standings of all the teams for the final race will be released.

Info

The RoboRacer Sim Racing League will be held approximately 1 week ahead of [CDC 2024](https://cdc2024.ieeecss.org) and the performance metrics will be made available to the teams. We have also been able to organize a [special session](https://css.paperplaza.net/conferences/conferences/CDC24/program/CDC24_ContentListWeb_1.html#moevsp1_01) for [RoboRacer Sim Racing League Celebration](https://cdc2024.ieeecss.org/program/competitions#session-10-44) on Monday (Dec 16), 18:00-19:00 CET with the help of the CDC organizing committee. Join the celebration event to relive the nail-biting races, hear the top teams brag about their winning strategies (~5 min presentations), and start your engines for the physical competition.

## Resources¶

![](/../assets/images/logos/AutoDRIVE Logo.png)

[AutoDRIVE](https://autodrive-ecosystem.github.io/) is envisioned to be an open, comprehensive, flexible and integrated cyber-physical ecosystem for enhancing autonomous driving research and education. It bridges the gap between software simulation and hardware deployment by providing the [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator) and [AutoDRIVE Testbed](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Testbed), a well-suited duo for real2sim and sim2real transfer targeting vehicles and environments of varying scales and operational design domains. It also offers [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit), a developer's kit for rapid and flexible development of autonomy algorithms using a variety of programming languages and software frameworks. For the Sim Racing League, teams will develop their autonomous racing algorithms using the AutoDRIVE Devkit to interface with the AutoDRIVE Simulator in real-time.

![](/../assets/images/logos/RoboRacer Logo.png)

[RoboRacer](https://roboracer.ai) is an [international community](https://roboracer.ai/about.html) of researchers, engineers, and autonomous systems enthusiasts. It is centered around the idea of converting a 1:10 scale RC car into an autonomous vehicle for research and education; check out the [documentation](https://roboracer.ai/build.html) to build your own RoboRacer autonomous racecar. Additionally, if you are new to the field of autonomous racing, you can refer to the complete [course material](https://roboracer.ai/learn.html), which is open sourced. If you already have some experience with autonomous racing, feel free to delve deeper into the [research](https://roboracer.ai/research.html) enabled by RoboRacer. Lastly, you can also check out the physical [RoboRacer races](https://roboracer.ai/race.html) that are being organized all around the world. For the Sim Racing League, teams will not require a physical RoboRacer vehicle; however, the learning resources can certainly be useful to get your autonomous racing fundamentals right!

We recommend all the teams interested in participating in the RoboRacer Sim Racing League to get accustomed with the competition. Following are a few resources to get you started:

  * **Competition Documents**

* * *

Learn about the competition rules and technical aspects of the framework.

[ **Competition Rules**](../roboracer-sim-racing-rules-2024)

[ **Technical Guide**](../roboracer-sim-racing-guide-2024)

  * **Docker Containers**

* * *

Download base container images for the competition and start developing your algorithms.

[ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-explore/images/sha256-6a4a9aab20e5deafdcf1a8318b4f270d409b557ba198888fd701eb56506760c7) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-practice/images/sha256-07126b3b4bcf7d6ff43a7d76f9ba84412b2553784026d27b7e4ebdab269c4c6f) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-cdc-compete/images/sha256-e0b511807cdc5597e9da3e3c1f630750476dd9a6a56f14187f79ca15ad72ad5e)

[ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-explore/images/sha256-221ab09c92720fc9ed324839ec81da6aceb4c5c12ae1e46b8733c2275cb000f1) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-practice/images/sha256-d3fd68b51ec6934d8de283c14be5d5b5d8e3c536599eeeef652a16f47cce103d) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-cdc-compete/images/sha256-6596fa4eed9521f61d2fb3dc43c52bb0affbf3e7e2a197e1afb6ef03894694a7)

  * **Local Resources**

* * *

Get started with the competition framework locally, and worry about containerization later.

**AutoDRIVE Simulator:**

`explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_explore_macos.zip)

`practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_practice_macos.zip)

`compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_simulator_compete_macos.zip)

**AutoDRIVE Devkit:**

[ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/autodrive_devkit.zip)

  * **Orientation Resources**

* * *

Join the online orientation sessions or review what we covered there.

**Orientation 1:**

Meeting Link: [ Zoom](https://clemson.zoom.us/j/92399406829)

Review Links: [ Recording](https://youtu.be/WQyhXQtFC0o) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/orientation_1_slides.zip)

**Orientation 2:**

Meeting Link: [ Zoom](https://clemson.zoom.us/j/98938663143)

Review Links: [ Recording](https://youtu.be/MxCDt1A4Wbo) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-cdc/orientation_2_slides.zip)

Question

You can post general questions on the [ AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace; this is the preferred modality. Technical questions can be also posted as [ GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/issues) or [ GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/discussions). For any other questions or concerns that cannot be posted publicly, please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration¶

This competition is open to everyone around the world - students, researchers, hobbyists, professionals, or anyone else who is interested. A team can consist of multiple teammates. Teams with only one person are also allowed.

[ Registration Form](https://forms.gle/D6X2C5PMwmDWEWbo9)

Registration for the Sim Racing League is free of cost and separate from the Physical Racing League and the conference registrations themselves. The above form signs you up only for the Sim Racing League, and for its orientation and information sessions. Although you can participate in the Sim Racing League without attending the conference, we strongly encourage all competition participants to attend the conference in person. This will help you connect with the broader AutoDRIVE and RoboRacer communities, and you can also witness/participate in the physical RoboRacer autonomous racing competition!

Registered teams are added to the following table:

SR. NO. | TEAM NAME | TEAM MEMBERS | ORGANIZATION | COUNTRY
01 | Beryllium | Ronnie Romman | Personal | United States of America (USA)
02 | AERObotics | Arif Anjum
Muhammed Sharjil | AEROBOTICS | South Africa
03 | Pharst Laps | Olivia Dry
Tian Zhao
Yitian Chen
Amir Ali Farzin | Australian National University | Australia
04 | SeDriCa-UMIC | Kshitij Vaidya
Yash Gupta
Manav Jain
Parth Agrawal
Sahil Kukreja
Johan Biju
Paawan Nenwani
Shivam Yadav | Indian Institute of Technology, Bombay | India
05 | Unimelb F1Tenth Racing | Henry Yapeter
Matthew Freeman
Nathan Ruslim
Harry Tauber | The University of Melbourne | Australia
06 | Donatello | Rahil Bhowal | Personal | United States of America (USA)
07 | VAUL | Tommy Bouchard-Lebrun
William Fecteau
Nicolas Lauzon | Laval University | Canada
08 | TUM Phoenix | Dean Mercer
Zara Zhotabayeva | Technische Universität München | Germany
09 | Autonomous Motorsports Purdue | Manav Gagvani
Alan Kang
Sivamurugan Velmurugan
Rohan Potta
Sangeet Mohan | Purdue University | United States of America (USA)
10 | Pegasus | Zeyuan Wang
Chao Wang | Personal | France, China
11 | ARCLab | William Akuffo
Joshua Nti
Reginald Andrew Sai-Obodai
Baron Afutu
Joel Osei-Asamoah | Ashesi University | Ghana
12 | YTU AESK | Mahmut Demir
Ahmet Çelik
İlayda Sena Şahin
Furkan Erdoğan
Alper Yılmaz
Enes Talha Günay
Taha İlter Akar
Hilal Horasan | Yıldız Technical University Alternative Energy Systems Society | Türkiye
13 | MMS Autonomous | Yousef Asal
Zaynap Ahmad
Omar Ashraf
Omar Elsharabasy
Abdallah Nabil
Ahmed ElShaboury | Mansoura University | Egypt
14 | HUN-REN SZTAKI | Csanád Budai
Tamás Széles | HUN-REN SZTAKI | Hungary
15 | bracaai | Luis Bracamontes | Personal | Mexico
16 | Velox | Karun Ashok Kumar | University of Twente | Netherlands
17 | Exhausted Lion | Mohamed Alaa | Personal | Egypt
18 | Sahruday Patti | Sahruday Patti | Personal | United States of America (USA)
19 | Als F1Tenth Racing | Auriol Ble | Alpha Space Robotics Lab | Côte d'Ivoire
20 | SoloDriver | Hana Nabhan | Personal | United Arab Emirates (UAE)
21 | Daniel's RL Experiment | Daniel Mittelman | Georgia Institute of Technology | United States of America (USA)
22 | TURTLEBOT | Jit Ern Lim | Personal | Singapore
23 | TractionX | Ameya Bagal
Ananya Das
Amizhthni PRK | Indian Institute of Technology, Madras | India
24 | Awareness | Guodong Zhu | Nanjing Forest University | China
25 | Byte Benders | Bhajneet Singh Bedi
Yaduraj Jagadeesan | Personal | India
26 | Eigenbots | Shubham Barge
Anshuman Jena | Personal | India
27 | __duronto__ | Md. Jesan
Muhammad Fahim Faisal
Abu Nafis Mohammod Noor Rohan
Rakibul Islam Rakib | BRAC University, Dhaka Residential Model College | Bangladesh
28 | MV33F110 | Vishwanath R | Personal | India
29 | F1NESSE - Formula 1 Neuro-Enhanced System for Smart Execution | Oscar Guerrero Rosado
Joris Kranz
Jan Honing
Wout Laracker | Radboud University, ROC Nijmegen | Netherlands
30 | Baby Driver | Mason Notz | Personal | United States of America (USA)
31 | Asturian Kingdom Team | David Miranda
Lucía Sánchez
Miguel Santamaría | University of Oviedo | Spain
32 | AsTenth Martin | Ajay Shankar Sriram | UC Irvine | United States of America (USA)
33 | Ray C.E.R.S. | Aditya Jambhale
Akshat Tambi | SRM Institute of Science and Technology | India
34 | Neutrino | Ahmed Elnely
Abdallah Atef
Mohamed Abdelmoneam
Noran Mohamed
Yasmin Khaled
Nouran Karam | Egyptian Russian University | Egypt
35 | Zancle E-Drive | Gaetano Pio Pispisa
Giovanni Lombardo
Simone Castorino | University of Messina, Italy | Italy
36 | sim_goes_brrrrrr_mha | Marzanul Momenine
Maidul Islam
Hironmoy Roy Rudra | Personal | Bangladesh
37 | Inertia | Mushfiqur Rahman
Al Mahir Ahmed
Suhail Haque Rafi
Abrar Ahmed | Personal | Bangladesh
38 | Assiut Motorsport | Omar Abbas
Kareem Salah
Mohamed Abd-El-Fattah
Ahmed Shehata
Doaa Ibrahem
Eslam Mohamed
Arwa Ibrahim
Maotaz Refaat
Fajr Mohamed
Ahmed Mohamed | Assiut University | Egypt
39 | SELF | Zhuo Ouyang
Pengcheng You
Chang Liu
Yingzhu Liu
Chengrui Qu | Peking University | China
40 | Triton AI | Yen-Ru Chen
Winston Chou
Kevin Shin
Samuel Lin
Surya Setty
Aryan Palaskar | University of California, San Diego | United States of America (USA)
41 | Escuderia Brasileira de Veículos Autônomos | Fernando Zolubas Preto
Antonio Colombini Neto
Felipe Gomes de Melo D'Elia
Carlos Alberto Arronte Delgado
Francisco Rodrigues Marazia
Luccas Barsotti
Caio Victor Goveia Freitas | Polytechnic School of the University of São Paulo - Brazil | Brazil
42 | Autonomous Ground Vehicle | Shreyansh Kansal
Swaminathan S K
Yash Sirvi
Aditya Srivastava
Akshit Goyal
Atul Singh
Rohan Singh
Theyanesh E R
Sandip Das
Arham J Bhansali
Ansh Sharma
Samarth G | Indian Institute of Technology, Kharagpur | India
43 | SUST Autodrive | Abul Bashar Raz
Md. Redwan Hasan
Ehsanul Karim Aslam
Md. Tamzid Islam Babul | Shahjalal University of Science and Technology | Bangladesh
44 | Sabeq | Adham Waleed
Abdulrahman Ahmed
Nabil Fouda
Mostafa Samy | Ain Shams University | Egypt
45 | RapidRabbits | Aryan Iyer
Siddhant Diwaker | Personal | India
46 | Orion | U Skanda Aithal
Aryan Agarwal
Aditya Gupta
Aman Kumar
Lakshmikanth Nageswar | Personal | India
47 | KOU-Mekatronom | Mehmet Baha Dursun
Muvahhid Kılıç
Can Ercan | Personal | Türkiye
48 | CLUTCH | Emmanuel Korankye
Appenteng Adjepong
Samuel Akwensivie
Kobena Enyam
Desmond Hammond | Personal | Ghana
49 | SimRacer | Vinura Wanniarachchi | Personal | Sri Lanka
50 | WaterlooF110 | Megnath Ramesh
Shaswat Garg
Avraiem Iskander
Praneeth KVK | University of Waterloo | Canada
51 | AA LAB | Taha Kocyigit
Taha Yigit Erdogan | Bogazici University | Türkiye

Note

The above table will be updated with newly registered teams within a few days of registration. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you do not see your team entry for more than 7 days after registering.

![](/../assets/images/competitions/2024 cdc roboracer sim racing league/Collage.png)

## Submission¶

Use the secure form below to make your team's submission for Phase 1 (Qualification Round) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 1 Submission Form](https://forms.gle/aYPFnWwVDzf47eXS6)

Warning

Phase 1 submission window will close on Nov 30, 2024. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

Use the secure form below to make your team's submission for Phase 2 (Final Race) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 2 Submission Form](https://forms.gle/mbrDFBU9Xww1Gp5X9)

Warning

Phase 2 submission window will close on Dec 07, 2024. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

## Results¶

**Phase 1: Qualification**

The following teams have qualified for the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 👏 VAUL | 70.30 s | 0 | 70.30 s | 6.96 s | [ YouTube](https://youtu.be/SDusD071cyk?feature=shared)
02 | 👏 Asturian Kingdom Team | 75.27 s | 0 | 75.27 s | 7.52 s | [ YouTube](https://youtu.be/MkIWWgdW_Bo?feature=shared)
03 | 👏 SoloDriver | 82.97 s | 0 | 82.97 s | 8.27 s | [ YouTube](https://youtu.be/iq6XiuYi0Tc?feature=shared)
04 | 👏 TURTLEBOT | 90.33 s | 0 | 90.33 s | 8.98 s | [ YouTube](https://youtu.be/tnDtR_BPtAY?feature=shared)
05 | 👏 Byte Benders | 85.61 s | 1 | 95.61 s | 8.29 s | [ YouTube](https://youtu.be/kcxb_3NtO-U?feature=shared)
06 | 👏 AsTenth Martin | 92.44 s | 1 | 102.44 s | 9.08 s | [ YouTube](https://youtu.be/KgV__0fcqr4?feature=shared)
07 | 👏 Pharst Laps | 93.69 s | 1 | 103.69 s | 9.24 s | [ YouTube](https://youtu.be/xDbs3ewB_f4?feature=shared)
08 | 👏 Autonomous Ground Vehicle | 111.94 s | 1 | 121.94 s | 10.55 s | [ YouTube](https://youtu.be/_itmR_8lQxE?feature=shared)
09 | 👏 Autonomous Motorsports Purdue | 122.34 s | 0 | 122.34 s | 12.22 s | [ YouTube](https://youtu.be/YnLfij6H87Q?feature=shared)
10 | 👏 Escuderia Brasileira de Veículos Autônomos | 114.19 s | 1 | 124.19 s | 11.33 s | [ YouTube](https://youtu.be/VRmLx6drMko?feature=shared)
11 | 👏 YTU AESK | 125.14 s | 0 | 125.14 s | 12.47 s | [ YouTube](https://youtu.be/so1HFp_kmOQ?feature=shared)
12 | 👏 Zancle E-Drive | 126.79 s | 0 | 126.79 s | 12.65 s | [ YouTube](https://youtu.be/-d4bYYlnBR4?feature=shared)
13 | 👏 Baby Driver | 122.66 s | 1 | 132.66 s | 12.19 s | [ YouTube](https://youtu.be/FHNaUfW21Rw?feature=shared)
14 | 👏 Pegasus | 146.82 s | 0 | 146.82 s | 14.65 s | [ YouTube](https://youtu.be/r7Ppv0hXfwE?feature=shared)
15 | 👏 MMS Autonomous | 113.15 s | 5 | 163.15 s | 10.90 s | [ YouTube](https://youtu.be/HXrgM4KHC2Q?feature=shared)
16 | 👏 WaterlooF110 | 190.31 s | 0 | 190.31 s | 18.78 s | [ YouTube](https://youtu.be/45_0Pjbd_YY?feature=shared)
17 | 👏 bracaai | 201.09 s | 0 | 201.09 s | 19.68 s | [ YouTube](https://youtu.be/Rmqrl6Qaiuc?feature=shared)
18 | 👏 Assiut Motorsport | 112.09 s | 9 | 202.09 s | 10.74 s | [ YouTube](https://youtu.be/n9zs7wRjR7s?feature=shared)
19 | 👏 SeDriCa-UMIC | 185.18 s | 2 | 205.18 s | 18.34 s | [ YouTube](https://youtu.be/1008cTF6gwM?feature=shared)
20 | 👏 Sabeq | 128.63 s | 10 | 228.63 s | 12.50 s | [ YouTube](https://youtu.be/Z8uZNGdLJ1A?feature=shared)

**Phase 2: Competition**

The following teams successfully finished the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 🥇 VAUL | 103.84 s | 0 | 103.84 s | 10.35 s | [ YouTube](https://youtu.be/9cGryPiPNTw?feature=shared)
02 | 🥈 Baby Driver | 136.63 s | 0 | 136.63 s | 13.58 s | [ YouTube](https://youtu.be/U40fX7-eqzc?feature=shared)
03 | 🥉 TURTLEBOT | 145.99 s | 0 | 145.99 s | 14.42 s | [ YouTube](https://youtu.be/jo_Nhqn-IPI?feature=shared)
04 | 👏 Asturian Kingdom Team | 150.76 s | 1 | 160.76 s | 14.91s | [ YouTube](https://youtu.be/hDVwhqrr_x8?feature=shared)
05 | 👏 Pharst Laps | 151.37 s | 3 | 181.37 s | 14.79 s | [ YouTube](https://youtu.be/lDuHt5YY2rk?feature=shared)
06 | 👏 bracaai | 167.15 s | 2 | 187.15 s | 16.34 s | [ YouTube](https://youtu.be/cAbo8uAQe6k?feature=shared)
07 | 👏 Byte Benders | 195.76 s | 2 | 215.76 s | 18.99 s | [ YouTube](https://youtu.be/1cwtYUkzGmc?feature=shared)
08 | 👏 Autonomous Motorsports Purdue | 211.76 s | 1 | 221.76 s | 20.48 s | [ YouTube](https://youtu.be/CZvvhld03B8?feature=shared)
09 | 👏 Escuderia Brasileira de Veículos Autônomos | 219.45 s | 1 | 229.45 s | 21.74 s | [ YouTube](https://youtu.be/m1v0NSuAhTQ?feature=shared)
10 | 👏 Pegasus | 227.29 s | 1 | 237.29 s | 21.72 s | [ YouTube](https://youtu.be/o7Xye3Sd2Ns?feature=shared)
11 | 👏 Zancle E-Drive | 241.64 s | 0 | 241.64 s | 24.04 s | [ YouTube](https://youtu.be/JFq6BRu7l8w?feature=shared)
12 | 👏 MMS Autonomous | 155.19 s | 9 | 245.19 s | 15.09 s | [ YouTube](https://youtu.be/nn9IYfmuXLM?feature=shared)
13 | 👏 SoloDriver | 259.23 s | 1 | 269.23 s | 24.59 s | [ YouTube](https://youtu.be/nPsR5S4T-4k?feature=shared)

**Celebration Event @ CDC 2024**

🎉 Please join us (in-person or virtually) for the [celebration event](https://css.paperplaza.net/conferences/conferences/CDC24/program/CDC24_ContentListWeb_1.html#moevsp1_01) of the 2nd RoboRacer Sim Racing League @ CDC 2024 on Monday (Dec 16, 2024) between 18:00-19:00 CET! 🏁

**🎤 _Agenda:_**

  * Introduction & Overview (15 min) – Dr. Krovi & Dr. Mangharam
  * Competition Insights (20 min) – Tanmay & Chinmay
  * Words from the Winners (15 min) – 5 min for each team
  * Concluding Remarks (10 min) – Dr. Krovi & Dr. Mangharam

**💻 _Zoom:_** <https://tinyurl.com/f1tenth-cdc24-virtual-race>

🏆 Don't miss this chance to relive the thrill of the competition and hear from the champions themselves!

  * **Celebration Event Recording**

  * **Words from the Winners!**

  * **Celebration Event Slides - Part 1**

  * **Celebration Event Slides - Part 2**

## Summary¶

Back to top
