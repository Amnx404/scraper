Skip to content

# RoboRacer Sim Racing League @ IROS 2024¶

![RoboRacer Sim Racing League @ IROS 2024](../../assets/images/banners/RoboRacer%20Sim%20Racing%20%40%20IROS%202024.png)

## About¶

**RoboRacer Autonomous Racing** is a semi-regular competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **21st RoboRacer Autonomous Grand Prix** at [IROS 2024](https://iros2024-abudhabi.org) will write software for a 1:10 scaled autonomous race car to fulfill the objectives for the competition: **_drive fast but don’t crash!_**

This time, we are organizing the first ever **RoboRacer Sim Racing League** , which leverages [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to model and simulate the digital twin of a RoboRacer racecar within a virtual racetrack. Please see the accompanying video for a glimpse of the RoboRacer digital twins in action.

The main focus of the Sim Racing League is a virtual competition with simulated cars and environments, which is accessible to everyone across the globe. For the [IROS 2024](https://iros2024-abudhabi.org) competition, each team will be provided with a standardized simulation setup (in the form of a digital twin of the RoboRacer vehicle, and a digital twin of the Porto racetrack) within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to get started with developing their autonomy algorithms. Teams will have to develop perception, planning, and control algorithms to parse the real-time sensor data streamed from the simulator and generate control commands to be fed back to the simulated vehicle.

The competition will take place in 2 stages:

  * **Qualification Race:** Teams will demonstrate their ability to complete multiple laps around the practice track without colliding with the track bounds at run time.
  * **Time-Attack Race:** Teams will compete against the clock, on a previously unseen racetrack, to secure a position on the leaderboard.

Since the vehicle, the sensors, the simulator, and the devkit are standardized, teams must develop robust racing algorithms that can deal with the uncertainties of an unseen racetrack.

Tip

If you are interested in autonomously racing physical RoboRacer vehicles, please check out the website for [21st RoboRacer Autonomous Racing Competition](https://iros2024-race.f1tenth.org), which will be held in person at [IROS 2024](https://iros2024-abudhabi.org). You can always register and compete in both physical and virtual competitions!

## Organizers¶

![](/../assets/images/people/Rahul Mangharam.png) | ![](/../assets/images/people/Venkat Krovi.png) | ![](/../assets/images/people/Johannes Betz.png) | ![](/../assets/images/people/Chinmay Samak.png) | ![](/../assets/images/people/Tanmay Samak.png)
[**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu) | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu) | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de) | [**Chinmay Samak**](mailto:csamak@clemson.edu) | [**Tanmay Samak**](mailto:tsamak@clemson.edu)
![](/../assets/images/people/Ahmad Amine.png) | ![](/../assets/images/people/Hongrui Zeng.png) | ![](/../assets/images/people/Fabio Bonsignorio.png) | ![](/../assets/images/people/Enrica Zereik.png) | ![](/../assets/images/people/Bilal Hassan.png)
[**Ahmad Amine**](mailto:aminea@seas.upenn.edu) | [**Hongrui Zheng**](mailto:hongruiz@seas.upnn.edu) | [**Dr. Fabio Bonsignorio**](mailto:fabio.bonsignorio@fer.unizg.hr) | [**Dr. Enrica Zereik**](mailto:enrica.zereik@cnr.it) | [**Dr. Bilal Hassan**](mailto:bilal.hassan@ku.ac.ae)
![](/../assets/images/people/Bushra Alshehhi.png) | ![](/../assets/images/people/Fady Alnajjar.png) | ![](/../assets/images/people/Majd Khonji.png) | ![](/../assets/images/people/Hamad Karki.png) | ![](/../assets/images/people/Pedro Lima.png)
[**Bushra Alshehhi**](mailto:100050085@ku.ac.ae) | [**Dr. Fady Alnajjar**](mailto:fady.alnajjar@uaeu.ac.ae) | [**Dr. Majid Khonji**](mailto:majid.khonji@ku.ac.ae) | [**Dr. Hamad Karki**](mailto:hamad.karki@ku.ac.ae) | [**Dr. Pedro Lima**](mailto:tp.aobsilu.ocincet@amil.ordep)

## Timeline¶

Warning

Timeline is subject to change. Please keep checking this page for any updates.

DATE | EVENT
---|---
Jul 22, 2024 | Registration Opens
Aug 31, 2024 | Registration Closes
Sep 02, 2024 (5:30 – 6:30 PM EDT) | [Online Orientation 1](https://clemson.zoom.us/s/96939189458)
Sep 22, 2024 (5:30 – 6:30 PM EDT) | [Online Orientation 2](https://clemson.zoom.us/j/95101125213)
Sep 28 – Sep 29, 2024 | Qualification Round
Sep 30, 2024 | Qualification Results Declared
Oct 03, 2024 | Competition Track Released
Oct 05 – Oct 06, 2024 | Final Race
Oct 07, 2024 | Competition Results Declared

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

The RoboRacer Sim Racing League will be held approximately 1 week ahead of [IROS 2024](https://iros2024-abudhabi.org) and the performance metrics will be made available to the teams. Discussions are underway with the IROS organizing team to allow teams to analyze and present their approach/results in a short (~10 min) presentation in a special session at [IROS 2024](https://iros2024-abudhabi.org).

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

[ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-iros-explore/images/sha256-7c62e0f13edbb875c6328771a441366b8f7fc5e3fc1dac1ba5e37ae0c61e4505) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-iros-practice/images/sha256-79b24cb29dcf4ee6fe64f2e9ede4806fbae0e75238eec1091a25318dcc76df7d) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_sim/2024-iros-compete/images/sha256-f1d48a64e9d9f36d1637e7ff0152f95a6cd151478070c10f1739feeea7cf6b79)

[ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_f1tenth_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-iros-explore/images/sha256-2782ff06e5d0526b7ad963b334a4c7d6122bdb22c8c02b292dae45b6c23c5cfa) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-iros-practice/images/sha256-e0e66d5b9e4ba063780c7d6e3d741891c6b173ff4c5153c2b989a98a6cebc0db) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_f1tenth_api/2024-iros-compete/images/sha256-39a5ccc2cfe655bf13f3d04109f12b5382100125545191265d96d0d70320be43)

  * **Local Resources**

* * *

Get started with the competition framework locally, and worry about containerization later.

**AutoDRIVE Simulator:**

`explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_explore_macos.zip)

`practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_practice_macos.zip)

`compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_simulator_compete_macos.zip)

**AutoDRIVE Devkit:**

[ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/autodrive_devkit.zip)

  * **Orientation Resources**

* * *

Join the online orientation sessions or review what we covered there.

**Orientation 1:**

Meeting Link: [ Zoom](https://clemson.zoom.us/s/96939189458)

Review Links: [ Recording](https://youtu.be/ERgcBxQGHec?feature=shared) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/orientation_1_slides.zip)

**Orientation 2:**

Meeting Link: [ Zoom](https://clemson.zoom.us/j/95101125213)

Review Links: [ Recording](https://youtu.be/SPWGkH8k2MM?feature=shared) | [ Slides](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/releases/download/2024-iros/orientation_2_sildes.zip)

Question

You can post general questions on the [ AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace; this is the preferred modality. Technical questions can be also posted as [ GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/issues) or [ GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-F1TENTH-Sim-Racing/discussions). For any other questions or concerns that cannot be posted publicly, please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration¶

This competition is open to everyone around the world - students, researchers, hobbyists, professionals, or anyone else who is interested. A team can consist of multiple teammates. Teams with only one person are also allowed.

[ Registration Form](https://forms.gle/hBCctUaHcvFoB9zHA)

Registration for the Sim Racing League is free of cost and separate from the Physical Racing League and the conference registrations themselves. The above form signs you up only for the Sim Racing League, and for its orientation and information sessions. Although you can participate in the Sim Racing League without attending the conference, we strongly encourage all competition participants to attend the conference in person. This will help you connect with the broader AutoDRIVE and RoboRacer communities, and you can also witness/participate in the physical RoboRacer autonomous racing competition!

Registered teams are added to the following table:

SR. NO. | TEAM NAME | TEAM MEMBERS | ORGANIZATION | COUNTRY
01 | SAGOL | JoonCheol Park | Personal | United Arab Emirates (UAE)
02 | Solo | Abdul Rahman Khader | Khalifa University | United Arab Emirates (UAE)
03 | OptimusPrime | Sahruday Patti | University of Maryland, College Park | United States of America (USA)
04 | Velizar Zlatev | Velizar Zlatev | University of Bristol | United Kingdom (UK)
05 | Beryllium | Ronnie Romman | Personal | United States of America (USA)
06 | Cornell Electric Vehicles | Jason Klein
Eric Marchetti
Zach Chosed
Utku Melemetci
Sidharth Rao
Myles Pasetsky
Zephan Sanghani
Sia Chitnis
Nicole Sin | Cornell University | United States of America (USA)
07 | Robotisim Dev | Muhammad Luqman
Yusuf Butt | Robotisim | Pakistan
08 | Log Robotics | Logesh G | Bannari Amman Institute of Technology | India
09 | Lone Rider | Akshay Laddha | Indian Institute of Technology, Bombay | India
10 | Atlas 2.0 | Manav Gagvani | Purdue University | United States of America (USA)
11 | The Buttowskis | Kalash Jain | Pandit Deendayal Energy University | India
12 | Hanuman Parakram | Dheeraj Bhurewar
Vaibhav Wanere
Akash Sundar
Suryaprakash Senthil Kumar | Personal | United States of America (USA)
13 | Pallas | Haris Khan | Skoltech | Russia
14 | Gopher Speedsters | Sujeendra Ramesh | University of Minnesota, Twin Cities | United States of America (USA)
15 | Autopilots | Nouf Aljaberi
Amna Muhammad
Hajar Alnaqbi
Shouq Zanki
Sara Almessabie
| United Arab Emirates University | United Arab Emirates (UAE)
16 | i3 | Pranav Kallem | Personal | United States of America (USA)
17 | RobotX & More | Oussama Errouji
Imad-Eddine NACIRI | Euro Mediterranean University of Fez | Morocco
18 | IEEE Zagazig SB | Abdulrahman Omar
Hossam Elsherbiny
Essam Shenhab
Eman Abdelhamed
Abdullah Elmasry
Salma Swailem
Merna Atef
Amr Yasser
Mahmoud Samy
Mostafa Asaad
Menna Gamal
Ahmed Medhat | Zagazig University | Egypt
19 | AMUGAE | Kim Amugae | Personal | South Korea
20 | TURTLEBOT | Jit Ern Lim | Personal | Singapore
21 | Byte Benders | Bhajneet Singh Bedi | Personal | India
22 | KGX | Hareesh R
Raja Rajan K
Ramesh Patel D
Marudhu Paandian K
Bhuvaneshwari Kanagaraj | KGISL Institute of technology | India
23 | NaN | Hariharan Ravichandran
Siva Vignesh Krishnan Chidambaram | Personal | United States of America (USA)
24 | Vortex | Chinmay K | National Institute of Technology, Karnataka | India
25 | bracaai | Luis Bracamontes | Braca Vision | Mexico
26 | ASU Racing Team | Abdallah Ismail
Mahmoud Omar
Hussien Algendy
Serag Abdelmohsen
Ammar Ahmed
Ahmed Sallam
Malk Hany | Ain Shams University | Egypt
27 | TurboX | Dheeraj Bhogisetty | Personal | United States of America (USA)
28 | TractionX | Ameya Bagal
Ananya Das
Amizhthni PRK
Aayush Ranawat | Indian Institute of Technology, Madras | India
29 | Urban AI | Adham Fayad
Abdulrahman Ahmed
Nabil Fouda
George Welson
Muhab Muhammed
Mostafa Samy | Ain Shams University | Egypt
30 | fstMINI | José Mateus
Duarte Domingues | Instituto Superior Técnico | Portugal
31 | Buggy Coders | Cody Uehara | Personal | United States of America (USA)
32 | AutoVision | Luis Bracamontes | Personal | Mexico
33 | Autobots | Shubham Barge
Anshuman Jena | Personal | India
34 | Kyber-Kabs | Aditya Jambhale | SRM Institute of Science and Technology | India
35 | SUST AutoDrive | Abul Bashar Raz
Ad-Deen Mahbub
Shafi Abdullah
Fardeen Mosharraf
Redwan Hassan
Taj Ahmed | Shahjalal University of Science and Technology | Bangladesh
36 | VersusAI | Junior Jesus
Alisson Kolling
Pedro Pinheiro
Victor Kich | Universidade Federal do Rio Grande | Brazil
37 | vijAYAM | Adarsh Baburaj | Manipal University (MU), Dubai | United Arab Emirates (UAE)
38 | OutRunner | Nihad Jifri
Arif Sidhiequ
Midhun Manoharan | Personal | United Kingdom (UK)
39 | simracer | Vinura Wanniarachchi | Personal | Sri Lanka
40 | Phoenix | Aman Kumar Singh
Lakshmikanth Nageswar
Kandregula Abhinav
Suchi Sharma | Personal | India
41 | KU F1TENTH | Riley Anderson
Jackson Yanek
Mohammed Misbah Zarrar | The University of Kansas | United States of America (USA)
42 | Void | Gonna Yaswanth
Prajyot Jadhav | Personal | India
43 | Aztec Autonomous Racing Team (AART) | Hyunjong Choi
Pascal Reich
Hyunhee Kwak | San Diego State University | United States of America (USA)
44 | IDEA_LAB | Myeongjun Kim
Ji-hong Park
Juyoung Kim
Sunwoong Moon
Gyuhyeok Lee
Sujin Park | Gyeongsang National University | South Korea
45 | Aumechtron | Siddhant Diwaker
Aryan Iyer | SRM Institute of Science and Technology | India
46 | UJI | Enric Cervera | Universitat Jaume-I | Spain
47 | TurboTrack AI | Swapneel Dhananjay Wagholikar | Personal | United States of America (USA)
48 | InDIGo | Nikolaos Sarantinoudis | Technical University of Crete | Greece
49 | Shelby | S Srikaanth
S A Gogulnath | Sastra Deemed University | India
50 | Noyma | Roni Emad
Youssef Karam
Ahmed Khalifa
John Maged
Mina Sameh
Andrew Bahaa
Marise Nachaat
Mark Medhat | Personal | Egypt
51 | BREATH | Wonbin Lee
Sechan Park
Sunhwan Lee | Handong Global University | South Korea
52 | SNAIL | Minsu Kim
Minyoung Song
Sieun Park | Handong Global University | South Korea
53 | Shoubra Racing Team | Ahmed Elmasry
Mohamed Alaa
Hana Ahmed
Hazem Abuelanin | Benha University - Shoubra Faculty of Engineering | Egypt
54 | Kanka | Goktug Poyrazoglu
Volkan Isler
Yukang Cao
Burak Mert Gonultas
Qingyuan Jiang
Burak Susam
William Chastek | University of Minnesota | United States of America (USA)
55 | Kılavuz-Mekatronom | Mehmet Baha Dursun
Mustafa Kurban
Hüseyin Ayvacı
Cihat Kurtuluş Altıparmak | Saha Robotik | Türkiye
56 | AA Lab | Taha Kocyigit | Bogazici University | Türkiye
57 | Cognitron | Abhinav Pillai
Abid Ansari
Muhamed Shijas
Safa N
Razeen Rasheed | Indian Institute of Technology, Kharagpur | India
58 | VAUL | Tommy Bouchard-Lebrun
William Fecteau
Nicolas Lauzon | Laval University | Canada

Note

The above table will be updated with newly registered teams within a few days of registration. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you do not see your team entry for more than 7 days after registering.

![](/../assets/images/competitions/2024 iros roboracer sim racing league/Collage.png)

## Submission¶

Use the secure form below to make your team's submission for Phase 1 (Qualification Round) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 1 Submission Form](https://forms.gle/c9LzgnwVnm6jNNqt9)

Warning

Phase 1 submission window will close on Sep 28, 2024. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

Use the secure form below to make your team's submission for Phase 2 (Final Race) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 2 Submission Form](https://forms.gle/ps95hV8aBGFqACQt8)

Warning

Phase 2 submission window will close on Oct 05, 2024. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

## Results¶

**Phase 1: Qualification**

The following teams have qualified for the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 👏 KU F1TENTH | 117.05 s | 0 | 117.05 s | 11.67 s | [ YouTube](https://youtu.be/wOZ63Q4OYLE?feature=shared)
02 | 👏 IDEA_LAB | 145.89 s | 1 | 155.89 s | 14.43 s | [ YouTube](https://youtu.be/uA3r9io5lHA?feature=shared)
03 | 👏 Shoubra Racing Team | 179.57 s | 0 | 179.57 s | 17.84 s | [ YouTube](https://youtu.be/th7Gi0yOSHo?feature=shared)
04 | 👏 bracaai | 181.04 s | 0 | 181.04 s | 17.87 s | [ YouTube](https://youtu.be/4ackKDejY-s?feature=shared)
05 | 👏 TURTLEBOT | 181.33 s | 0 | 181.33 s | 17.98 s | [ YouTube](https://youtu.be/BtDTqaODmWE?feature=shared)
06 | 👏 Kanka | 177.08 s | 7 | 247.08 s | 17.37 s | [ YouTube](https://youtu.be/yEDHL6-6TqY?feature=shared)
07 | 👏 Log Robotics | 265.59 s | 1 | 275.59 s | 26.47 s | [ YouTube](https://youtu.be/SzUYifnIKxE?feature=shared)
08 | 👏 Phoenix | 411.03 s | 0 | 411.03 s | 41.05 s | [ YouTube](https://youtu.be/YLNN_68lXAE?feature=shared)
09 | 👏 Urban AI | 1284.26 s | 0 | 1284.26 s | 128.00 s | [ YouTube](https://youtu.be/Wnm7_KDCT80?feature=shared)

**Phase 2: Competition**

The following teams successfully finished the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 🥇 TURTLEBOT | 141.59 s | 0 | 141.59 s | 13.90 s | [ YouTube](https://youtu.be/fEj-bWC8bJ0?feature=shared)
02 | 🥈 IDEA_LAB | 186.58 s | 0 | 186.58 s | 17.79 s | [ YouTube](https://youtu.be/92napssQUY0?feature=shared)
03 | 🥉 KU F1TENTH | 244.88 s | 0 | 244.88 s | 24.12 s | [ YouTube](https://youtu.be/dOEyaTzgGhc?feature=shared)
04 | 👏 Shoubra Racing Team | 201.84 s | 6 | 261.84 s | 19.00 s | [ YouTube](https://youtu.be/Vf_XOZvBjdA?feature=shared)
05 | 👏 Phoenix | 282.16 s | 0 | 282.16 s | 27.97 s | [ YouTube](https://youtu.be/GAyaM3pc60c?feature=shared)

## Summary¶

Back to top
