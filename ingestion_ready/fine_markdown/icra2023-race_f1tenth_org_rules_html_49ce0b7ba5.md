[F1TENTH Rules](index.html)

## F1TENTH Rules

These rules are prepared for the _10th International F1TENTH Autonomous Racing Competition_. Rules can be modified overtime. The latest version can be found [here](https://icra2022-race.f1tenth.org/rules.html).

Date: 2021-12-17

**Table of content**

*   1. General
*   2. In-person (physical) competition
    *   2.1 Vehicle classes
    *   2.2 Track & racing environment
    *   2.3 Inspection
    *   2.4 Time Trial
        *   2.4.1 Definitions
        *   2.4.2 General
        *   2.4.3 Requirements for Time Trial qualification
        *   2.4.4 Penalties
        *   2.4.5 Evaluation
    *   2.5 Head-to-Head Race
        *   2.5.1 General
        *   2.5.2 Requirements for qualification
        *   2.5.3 Penalties
        *   2.5.4 Evaluation
*   3. Virtual (simulation) competition
    *   3.1 General
    *   3.2 Registration, Training, Code Submission.
    *   3.3 Time Trials
    *   3.4 Head To Head Race

### 1. General

International F1TENTH Autonomous Racing Competition is a racing competition open to teams of all levels. Competing teams may consist of any number of members; however, each participant should be a member of only one team.

The competition is organized in two variants:

*   In-Person competition, and
*   Virtual competition.

Teams can register for the competition using a [registration form](https://icra2022-race.f1tenth.org/registration.html), where they select a single variant of the competition. Registration is open until April 11, 2022.

_Note: If the in-person competition gets canceled due to the ongoing pandemic situation, registered teams may compete in the virtual competition instead._

The preferred communication method with the organizers is the _#ICRA2022_ channel on [F1TENTH-teams Slack](https://join.slack.com/t/f1tenth-teams/shared_invite/enQtMzc3ODU2ODM1NzE3LTBjMmVkMzZjZTJiNWUzZDFhZTJiODgzMjg0MTA1MDAxZTUxMzkwMDRhNTM2NzdjNDc5MTk5YTc5YmNhNTdhMTU).

### 2. In-person (physical) competition

1.  The competition will comprise three parts – _Inspection_ , _Time Trials_ and _2 Vehicle Head-to-Head_ race. Every participant must pass qualification and will be automatically registered to both races.
2.  Teams registered to the in-person competition need to provide and build a F1TENTH car by themselves according to the constraints listed below. In addition, each team must have a unique vehicle (i.e., a research lab may not field six teams with one car).
3.  To increase the quality of the future F1TENTH competitions, the winner of each race is encourage to publish the code of their algorithm under an open-source license in the [F1TENTH repository](https://github.com/f1tenth) on Github.

#### 2.1 Vehicle classes

1.  The in-person competition distinguishes two vehicle classes: Restricted Class and Open Class.
2.  **Restricted Class** allows only cars that meet the following constraints:
    *   The vehicle is constructed according to the official [bill of materials](https://f1tenth.readthedocs.io/en/stable/getting_started/build_car/bom.html). The teams are allowed to use components of similar or lower specifications.
    *   Each vehicle will be inspected as a part of qualification whether it meets the criteria. In case the criteria are not met, the vehicle is moved to the Open Class.
    *   **F1TENTH Competition is a battle of algorithms. Any hardware that should turn the odds in your favor is not allowed**.
    *   _Chassis_ : Any chassis listed as _1:10 scale_ car is allowed. Preferably **1:10 Traxxas** (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)), but generally, any chassis with similar dimensions is allowed. Both 4WD and 2WD are permitted.
    *   _Main Computation Unit_ : **Nvidia Jetson Xavier NX** , Equivalents to the Nvidia Jetson NX (e.g. Nvidia Jetson TX2, Nvidia Jetson Nano), or anything of equal or lower GPU and CPU specification is allowed. Examples of possible computation units could be: Raspberry Pi, Arduino, Beaglebone.
    *   _LiDAR_ : [**Hokuyo UST-10LX**](https://www.hokuyo-aut.jp/search/single.php?serial=167), its equivalent, or anything of lower specifications is allowed. The main observed characteristics are: detection range (10 m), scanning frequency (40 Hz), and angular resolution (0.25°).
    *   _Camera_ : Both _monocamera_ (e.g. Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and _stereokameras_ (e.g. Intel Realsense, ZED) are allowed.
    *   _Engine_ : Only brushless DC motors are allowed. The [**Velineon 3500 kV**](https://traxxas.com/products/parts/motors/velineon3500motor), its equivalent, or anything of lower specifications regarding power and torque are allowed.
    *   _Other sensors_ : Other sensors (IMUs, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g. Marvelmind) are not allowed. In addition, in the spirit of the competition, components with significant internal computation power are prohibited.
3.  **Open Class** allows cars that do not fit into Restricted Class. These cars may compete, but they
