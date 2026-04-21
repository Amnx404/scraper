Skip to content

# RoboRacer Sim Racing League @ CDC 2025 and Techfest 2025¶

![RoboRacer Sim Racing League @ CDC Techfest 2025](../../assets/images/banners/RoboRacer%20Sim%20Racing%20%40%20CDC%20Techfest%202025.png)

## About¶

**RoboRacer Autonomous Racing** is a semi-regular competition organized by an international community of researchers, engineers, and autonomous systems enthusiasts. The teams participating in the **25th and 26th RoboRacer Autonomous Racing Competitions** at [CDC 2025](https://cdc2025.ieeecss.org) and [Techfest 2025](https://techfest.org) will write software for a 1:10 scaled autonomous racecar to fulfill the objectives of the competition: **_drive fast but don’t crash!_**

This time, we are organizing the fourth **RoboRacer Sim Racing League** , which leverages [AutoDRIVE Ecosystem](https://autodrive-ecosystem.github.io) to model and simulate the digital twin of a RoboRacer racecar within a virtual racetrack. Please see the accompanying video for a glimpse of the RoboRacer digital twins in action.

The main focus of the Sim Racing League is a virtual competition with simulated cars and environments, which is accessible to everyone across the globe. For the combined [CDC 2025](https://cdc2025.ieeecss.org) and [Techfest 2025](https://techfest.org) competition, each team will be provided with a standardized simulation setup (in the form of a digital twin of the RoboRacer vehicle, and a digital twin of the Porto racetrack) within the high-fidelity [AutoDRIVE Simulator](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator). Additionally, teams will also be provided with a working implementation of the [AutoDRIVE Devkit](https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Devkit) to get started with developing their autonomy algorithms. Teams will have to develop perception, planning, and control algorithms to parse the real-time sensor data streamed from the simulator and generate control commands to be fed back to the simulated vehicle.

The competition will take place in 2 stages:

  * **Qualification Race:** Teams will demonstrate their ability to complete multiple laps around the practice track without colliding with the track bounds at run time.
  * **Time-Attack Race:** Teams will compete against the clock, on a previously unseen racetrack, to secure a position on the leaderboard.

Since the vehicle, the sensors, the simulator, and the devkit are standardized, teams must develop robust racing algorithms that can deal with the uncertainties of an unseen racetrack.

Tip

If you are interested in autonomously racing physical RoboRacer vehicles, please check out the websites for [25th RoboRacer Autonomous Racing Competition](https://cdc2025-race.roboracer.ai) and [26th RoboRacer Autonomous Racing Competition](https://techfest.org/competitions/Roboracer), which will be held in person at [CDC 2025](https://cdc2025.ieeecss.org) and [Techfest 2025](https://techfest.org), respectively. You can always register and compete in both physical and virtual competitions!

## Organizers¶

![](/../assets/images/people/Rahul Mangharam.png) | ![](/../assets/images/people/Venkat Krovi.png) | ![](/../assets/images/people/Archak Mittal.png) | ![](/../assets/images/people/Johannes Betz.png)
[**Dr. Rahul Mangharam**](mailto:rahulm@seas.upenn.edu) | [**Dr. Venkat Krovi**](mailto:vkrovi@clemson.edu) | [**Dr. Archak Mittal**](mailto:archak@iitb.ac.in) | [**Dr. Johannes Betz**](mailto:johannes.betz@tum.de)
![](/../assets/images/people/Chinmay Samak.png) | ![](/../assets/images/people/Tanmay Samak.png) | ![](/../assets/images/people/Ahmad Amine.png) | ![](/../assets/images/people/Michael Coraluzzi.png)
[**Chinmay Samak**](mailto:csamak@clemson.edu) | [**Tanmay Samak**](mailto:tsamak@clemson.edu) | [**Ahmad Amine**](mailto:aminea@seas.upenn.edu) | [**Michael Coraluzzi**](mailto:mike.coraluzzi@roboracer.ai)

## Timeline¶

Warning

Timeline is subject to change. Please keep checking this page for any updates.

DATE | EVENT
---|---
Nov 01, 2025 | Registration Opens
Nov 28, 2025 | Registration Closes
Nov 29 – Nov 30, 2025 | Qualification Round
Dec 01, 2025 | Qualification Results Declared
Dec 02, 2025 | Competition Track Released
Dec 06 – Dec 07, 2025 | Final Race
Dec 08, 2025 | Competition Results Declared

Following is a brief summary of each event:

  * **Registration:** Interested teams will register for the Sim Racing League.
  * **Qualification Round:** Teams will demonstrate successful completion of 10 laps around the practice track provided ahead of time.
  * **Qualification Results Declared:** Standings of all the qualified teams will be released.
  * **Competition Track Released:** Organizers will release the actual "competition track", which will be used for the final race. This track may be replicated in the physical race as well.
  * **Final Race:** Organizers will collect containerized algorithms from each team and connect them with the containerized simulator. Performance metrics of each team will be recorded.
  * **Competition Results Declared:** Standings of all the teams for the final race will be released.

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

[ **AutoDRIVE Simulator:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_sim) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-explore/images/sha256-72887f78aaa12cf54913f77b41d4d057e8a98e5810b69c203b3653850b38f6c5) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-practice/images/sha256-c4cf1b17646b85036c008c5e1994e4f53a0e340a675fd05ec18c5e03c07f4c0d) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_sim/2025-cdc-tf-compete/images/sha256-0ba6cc7c7427eb7fd031bd58b86ee4c65d9ad5e1ceea6725927f7dfb165e320b)

[ **AutoDRIVE Devkit:**](https://hub.docker.com/r/autodriveecosystem/autodrive_roboracer_api) [`explore`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-explore/images/sha256-15a51f3b7b75085ff1d5a36f3c9b13343cc35c3aa3026afbce8e378c5c8c23b2) | [`practice`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-practice/images/sha256-f0e47bc1e694a366cc1e8fe7e0df9bb2ef77d1cce6b724af90f250ddeb83f395) | [`compete`](https://hub.docker.com/layers/autodriveecosystem/autodrive_roboracer_api/2025-cdc-tf-compete/images/sha256-808683287d8d46515d3a9fb26aea97807eae30b7432ec8c2fbee14d1e6d3ca69)

  * **Local Resources**

* * *

Get started with the competition framework locally, and worry about containerization later.

**AutoDRIVE Simulator:**

`explore` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_explore_macos.zip)

`practice` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_practice_macos.zip)

`compete` [ Linux](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_linux.zip) | [ Windows](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_windows.zip) | [ macOS](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_simulator_compete_macos.zip)

**AutoDRIVE Devkit:**

[ ROS 2](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/releases/download/2025-cdc-tf/autodrive_devkit.zip)

  * **Quick Links**

* * *

Links to be kept at your fingertips, for a smooth ride throughout the competition.

**Schedule:** Timeline

**Registration:** [ Form](https://forms.gle/wGQYoxS1ddevHMcu7)

**Documentation:** [ Rule Book](../roboracer-sim-racing-rules-2025) | [ Tech Guide](../roboracer-sim-racing-guide-2025)

**Communication:** [ Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw)

**Submission:** [ Phase 1](https://forms.gle/X3aaPGwkR9zQTKqm7) | [ Phase 2](https://forms.gle/Y95VyREHS2ABWUgJA)

**Results:** Phase 1 |  Phase 2

Question

You can post general questions on the [ AutoDRIVE Slack](https://join.slack.com/t/autodrive-ecosystem/shared_invite/zt-2oeg2hce8-0JvasvnBM1M_wUdDTWRuKw) workspace; this is the preferred modality. Technical questions can be also posted as [ GitHub Issues](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/issues) or [ GitHub Discussions](https://github.com/AutoDRIVE-Ecosystem/AutoDRIVE-RoboRacer-Sim-Racing/discussions). For any other questions or concerns that cannot be posted publicly, please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu).

## Registration¶

This competition is open to everyone around the world - students, researchers, hobbyists, professionals, or anyone else who is interested. A team can consist of multiple teammates. Teams with only one person are also allowed. However, a person cannot be a part of more than one team.

[ Registration Form](https://forms.gle/wGQYoxS1ddevHMcu7)

Registration for the Sim Racing League is free of cost and separate from the Physical Racing League and the conference/event registrations themselves. The above form signs you up only for the Sim Racing League. Although you can participate in the Sim Racing League without attending the conference/event, we strongly encourage all competition participants to attend the conference/event in person. This will help you connect with the broader AutoDRIVE and RoboRacer communities, and you can also witness/participate in the physical RoboRacer autonomous racing competition!

Registered teams are added to the following table:

SR. NO. | TEAM NAME | TEAM MEMBERS | ORGANIZATION | COUNTRY
01 | 魔法师大大 | Chen Zexiang | Personal | China
02 | Mamba | Hariharan Ravichandran | Personal | United States of America (USA)
03 | Finding Theta | Michael Kudlaty | Personal | United States of America (USA)
04 | Devrim | Melih Akay | Middle East Technical University | Türkiye
05 | Khepa_BobCats | MdSakifUddin Khan
KaziSifatul Islam
Rashedul Hasan
Sayan Paul | Personal | United States of America (USA)
06 | MIA | Srivardhini Veeraragavan
Krishna Vihaan Mokkapaty
Souptik Sinha
Siddarth Menon
Aparna Asokan | Personal | Malaysia
07 | Pathline | Albert Sagré | Personal | Spain
08 | MonacoF1 | Gerardo Puga
Ariel Lowy
Diego Palma
Emiliano Alban
Enrique Abramzon
Florencia Battocchia
Juan Manuel Carosella
Juan Manuel Gomez Vasquez
Michel Hidalgo
Nicolás de Lima | Ekumen | Argentina, Colombia, Ecuador, Peru
09 | ESL | Nico Martin
Christopher Flood | Stellenbosch University | South Africa
10 | bracavisionai | Luis Bracamontes | Personal | Mexico
11 | Gator Autonomous Racing | Christopher Oeltjon
Jackie Wang
Gabrielle Cammarata
Trevor Turnquist | University of Florida | United States of America (USA)
12 | E-Rally | Morad Singer
Ahmed Mohammed
Abdelhamid Raafat
Ramiz Sayed | Helwan University | Egypt
13 | IrohazakaJump | Fritz Andrew Graciano
Gede Bagus Wirayasa
Kelvin Pratama | National Dong Hwa University | Indonesia
14 | VAUL - Old but Gold | William Fecteau
Nicolas Lauzon
Tommy Bouchard-Lebrun | Laval University | Canada
15 | VAUL - Young Guns | Mohamed Billo Barry
Achy Chris Yohann Ekissi
Rahul Iyer
Jayson Poirier
Alissa Audet
Teddy Emmanuel Kana Boumkwo II | Laval University | Canada
16 | Raga Racing | VaishnavaHari Seenivasan | Personal | Germany
17 | RoboCORE | Mahdis Rabbani
Armin Abdolmohammadi
Mohammad Abtahi
Farhang Motallebiaraghi
Navid Mojahed
Shima Nazari | University of California, Davis | United States of America (USA)
18 | Element | Sree Penisetty | Personal | India
19 | RAPTOR | Jisu Lee | Hanyang University | South Korea
20 | EPIIBOTS | Leandro Henrique Vidigal Sousa
Elias José de Rezende Freitas
Christyan Ribeiro de Amorim Honorato
Raissa Rúbia Braga Gonçalves
Luciano Cunha de Araújo Pimenta | Instituto Federal de Minas Gerais | Brazil
21 | Phoenix Racing | Harun Teper
Utku Pazarci
Adem Jabri
Tim Gliemann
Louis Radtke
Nico Koltermann | TU Dortmund University | Germany
22 | RUN-RUN-ChuraTaro | Soya Aoki | Chura DATA Inc. | Japan
23 | UO Astur Martin | Pablo Suárez
Pedro Martín
Mateo Cobo
Álvaro Tamargo | University of Oviedo | Spain
24 | Assiut Motorsport | Mohamed Emadeldeen
Doaa Essam
Ahmed Nadi
Mina Waheed
Shams Sabry
Kareem Salah
Abdallah Elkashef
Habiba Sayed
Moataz Hesham
Mohamed Mostafa | Assiut University | Egypt
25 | F1tenth@UCI | Alistair Keiller
Daniel Huynh
Allen Dai
Bradley Chu
Jeffery Lee
George Rajamachvili
Arthur Chung | University Of California, Irvine | United States of America (USA)
26 | YTU AESK | Atahan Taşal
Mahmut Esat Baydaş
Rabia Hanne Akyüz
Efe Erbağ
Kubilay Kayra Kivrak
Berke Sinan Yetkin | Yildiz Technical University | Türkiye
27 | YTU-AESK-RL | Burak Hazır
Berdan Fırat Doğan
Efe Pehlivan
Selinay Dikdere
Muhammet Yusuf Oral | Yildiz Technical University | Türkiye
28 | Solo-Drive | Mohammed Ibrahim | Heriot-Watt University | United Arab Emirates (UAE)
29 | Autonomous Ground Vehicle | Akshit Goyal
Utsab Karan
Rohan Singh
Sandip Das
Ninaad Desai
Theyanesh E R
Jinansh Dalal
Tanishq Saxena
Yug Bargaway
Mahin Sanklecha
Shrey Nayakpara
Satyam Chakravorty
Aneesh Lade
Gokul Vemuri
Akshat Shukla
Netra Nandankar
Allu Gowri Sasaank | Indian Institute of Technology, Kharagpur | India
30 | Jarvis | Muhilan M
Rohit Balaji
Chaitanya Bhatia
Sujal Choudhary
Asvithh Sivakumar
Akash Kandasamy
Devanand P | SRM Institute of Science and Technology | India
31 | SART | Seyyed Ali Kakaei
Siavash Sepahi
Abdolreza Pasharavesh | Sharif University of Technology | Iran
32 | Meteoritonomous | Seif Ashraf Mohammed Hussein
Omar Mostafa
Shrouq Hamdy
Abdelbadee Yehia
Abdelrahman Talaat
Abdelrahman Ehab
Abdelrahman Hamouda
Ahmed Hazem
Ahmed M. Khalafallah
Fagr Ahmed
Hatem Safwat
Jana Mohamed
Khalid Ashraf
MIna Rushdy Rady
Mohamed Fouad
Mohamed Shaaban
Mohamed Abdelatif
Abdelrahman Hatem
Eman Mohamed
Nourhan Anter
Sajda Mohamed
Sama Ahmed
Sama Mohamed | Sohag University | Egypt
33 | Fifty Four | Anonymous | Personal | Egypt
34 | BlindRacer | Kamallesh Umasankar | Personal | India
35 | HumbleOps | Ayush David
Cyril Jacob
Basil Shaji | Karunya Institute of Technology and Sciences | India
36 | SKG | Anvesh SK
Subhash G | Personal | India
37 | Al-Jazari | Taha Koçyiğit | The Institute for Data Science & Artificial Intelligence at Boğaziçi University | Türkiye
38 | PARCar | Pranav Bhatt | University of California, Berkeley | United States of America (USA)
39 | Hero Comes Last | Omar Abdelrady | Schmalkalden Applied Science University | Germany
40 | 321GO | Ashwin Pandey | Personal | India

Note

The above table will be updated with newly registered teams within a few days of registration. Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you do not see your team entry for more than 7 days after registering.

![](/../assets/images/competitions/2025 cdc-tf roboracer sim racing league/Collage.png)

## Submission¶

Use the secure form below to make your team's submission for Phase 1 (Qualification Round) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 1 Submission Form](https://forms.gle/X3aaPGwkR9zQTKqm7)

Warning

Phase 1 submission window will close on Nov 29, 2025 (anywhere on Earth). Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

Use the secure form below to make your team's submission for Phase 2 (Final Race) of the RoboRacer Sim Racing League. Please fill in your team's name and add the link to your team's DockerHub repository containing the autonomous racing stack. If you are using a private repository, make sure to add [autodriveecosystem](https://hub.docker.com/u/autodriveecosystem) as a [collaborator to your repository](https://docs.docker.com/docker-hub/repos/access).

[ Phase 2 Submission Form](https://forms.gle/Y95VyREHS2ABWUgJA)

Warning

Phase 2 submission window will close on Dec 06, 2025 (anywhere on Earth). Please contact [ Chinmay Samak](mailto:csamak@clemson.edu) or [ Tanmay Samak](mailto:tsamak@clemson.edu) if you have any questions.

## Results¶

**Phase 1: Qualification**

The following teams have qualified for the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 👏 Mamba | 65.41 s | 0 | 65.41 s | 6.53 s | [ YouTube](https://youtu.be/pp8wH99UGVE)
02 | 👏 VAUL - Old but Gold | 65.65 s | 0 | 65.65 s | 6.49 s | [ YouTube](https://youtu.be/oYM95QmoKjg)
03 | 👏 Phoenix Racing | 70.35 s | 0 | 70.35 s | 7.00 s | [ YouTube](https://youtu.be/iJnI9B54vf8)
04 | 👏 Solo-Drive | 71.42 s | 0 | 71.42 s | 7.11 s | [ YouTube](https://youtu.be/i0yusiTkY60)
05 | 👏 Autonomous Ground Vehicle | 80.44 s | 0 | 80.44 s | 7.99 s | [ YouTube](https://youtu.be/fPZe9Gwtg_A)
06 | 👏 RUN-RUN-ChuraTaro | 84.33 s | 0 | 84.33 s | 8.37 s | [ YouTube](https://youtu.be/DinFNDFU3VY)
07 | 👏 IrohazakaJump | 85.38 s | 0 | 85.38 s | 8.51 s | [ YouTube](https://youtu.be/6duv3lrsy1U)
08 | 👏 YTU-AESK-RL | 94.96 s | 0 | 94.96 s | 8.98 s | [ YouTube](https://youtu.be/IylqRsMGc2g)
09 | 👏 MonacoF1 | 98.69 s | 0 | 98.69 s | 9.81 s | [ YouTube](https://youtu.be/xQS-xyQkqD0)
10 | 👏 PARCar | 113.30 s | 0 | 113.30 s | 11.32 s | [ YouTube](https://youtu.be/gfdK2JVEP2k)
11 | 👏 Jarvis | 118.37 s | 0 | 118.37 s | 11.83 s | [ YouTube](https://youtu.be/10cVc3KRHNs)
12 | 👏 VAUL - Young Guns | 118.40 s | 0 | 118.40 s | 11.84 s | [ YouTube](https://youtu.be/i7mi00juG2Q)
13 | 👏 Assiut Motorsport | 118.83 s | 0 | 118.83 s | 11.85 s | [ YouTube](https://youtu.be/bk6gZ97GS_4)
14 | 👏 UO Astur Martin | 120.42 s | 0 | 120.42 s | 12.04 s | [ YouTube](https://youtu.be/GFu3DErGk-k)
15 | 👏 E-Rally | 124.30 s | 0 | 124.30 s | 12.41 s | [ YouTube](https://youtu.be/SG45DjQLLcA)
16 | 👏 YTU AESK | 123.39 s | 1 | 133.39 s | 12.19 s | [ YouTube](https://youtu.be/hMxCyuJvdt4)
17 | 👏 RoboCORE | 162.99 s | 0 | 162.99 s | 16.18 s | [ YouTube](https://youtu.be/taEslu3mVU4)
18 | 👏 bracavisionai | 185.69 s | 0 | 185.69 s | 18.48 s | [ YouTube](https://youtu.be/OBVz7dLw2ag)
19 | 👏 Gator Autonomous Racing | 225.60 s | 0 | 225.60 s | 22.55 s | [ YouTube](https://youtu.be/jWXGBITw4es)
20 | 👏 Hero Comes Last | 301.73 s | 0 | 301.73 s | 30.02 s | [ YouTube](https://youtu.be/Q7VPn6YlgCA)

**Phase 2: Competition**

The following teams successfully finished the final time-attack race. Here are the official standings:

RANK | TEAM NAME | RACE TIME | COLLISION COUNT | ADJUSTED RACE TIME | BEST LAP TIME | VIDEO
01 | 🥇 VAUL - Old but Gold | 78.19 s | 0 | 78.19 s | 7.74 s | [ YouTube](https://youtu.be/A5JdND5oZts)
02 | 🥈 Mamba | 87.82 s | 0 | 87.82 s | 8.73 s | [ YouTube](https://youtu.be/yCjCcjlxnOg)
03 | 🥉 Phoenix Racing | 99.33 s | 0 | 99.33 s | 9.90 s | [ YouTube](https://youtu.be/HJqpXWUNR-4)
04 | 👏 MonacoF1 | 104.23 s | 0 | 104.23 s | 10.38 s | [ YouTube](https://youtu.be/CTjnzO3qMvQ)
05 | 👏 Assiut Motorsport | 113.13 s | 0 | 113.13 s | 11.28 s | [ YouTube](https://youtu.be/f5Fx91bhmFI)
06 | 👏 Hero Comes Last | 117.23 s | 0 | 117.23 s | 11.67 s | [ YouTube](https://youtu.be/mGndZPicWl0)
07 | 👏 Autonomous Ground Vehicle | 119.17 s | 0 | 119.17 s | 11.76 s | [ YouTube](https://youtu.be/mQSvaBFIycY)
08 | 👏 RUN-RUN-ChuraTaro | 138.86 s | 0 | 138.86 s | 13.71 s | [ YouTube](https://youtu.be/qXM7OQZmbKY)
09 | 👏 YTU AESK | 155.39 s | 0 | 155.39 s | 15.38 s | [ YouTube](https://youtu.be/ivZ-AfTFYTM)
10 | 👏 VAUL - Young Guns | 183.08 s | 0 | 183.08 s | 18.30 s | [ YouTube](https://youtu.be/0t-CkkVrlx0)
11 | 👏 bracavisionai | 208.51 s | 0 | 208.51 s | 20.73 s | [ YouTube](https://youtu.be/DISFyHiLYYM)
12 | 👏 PARCar | 255.06 s | 0 | 255.06 s | 25.32 s | [ YouTube](https://youtu.be/gE_fsHm0mlc)
13 | 👏 UO Astur Martin | 322.33 s | 1 | 332.33 s | 32.08 s | [ YouTube](https://youtu.be/CWAUidTH78I)

## Summary¶

Back to top
