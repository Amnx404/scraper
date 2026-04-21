[F1TENTH Rules](index.html)

## F1TENTH Rules

These rules are prepared for the _14th International F1TENTH Autonomous Racing Competition_. Rules are subject to change. The latest version can be found [here](https://iros2023-race.f1tenth.org/rules.html).

Date: 2023-6-14

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

### 1. General

International F1TENTH Autonomous Racing Competition is a racing competition open to teams of all levels. Competing teams may consist of any number of members; however, each participant should be a member of only one team.

The competition is organized as an in-person competition.

Teams can register for the competition using a [registration form](https://iros2023-race.f1tenth.org/registration.html), where they select a single variant of the competition.

The preferred communication method with the organizers is the _#IROS2023_ channel on [F1TENTH-teams Slack](https://join.slack.com/t/f1tenth-teams/shared_invite/enQtMzc3ODU2ODM1NzE3LTBjMmVkMzZjZTJiNWUzZDFhZTJiODgzMjg0MTA1MDAxZTUxMzkwMDRhNTM2NzdjNDc5MTk5YTc5YmNhNTdhMTU).

### 2. In-person (physical) competition

1.  The competition will comprise three parts – _Inspection and Orientation_ , _Time Trials_ and _2 Vehicle Head-to-Head_ race. Every participant must pass qualification and will be automatically registered to both races.
2.  Teams registered to the in-person competition need to provide and build a F1TENTH car by themselves according to the constraints listed below. In addition, each team must have a unique vehicle (i.e., a research lab may not field six teams with one car).
3.  To increase the quality of the future F1TENTH competitions, the winner of each race is encourage to publish the code of their algorithm under an open-source license in the [F1TENTH repository](https://github.com/f1tenth) on Github.

#### 2.1 Vehicle classes

1.  The in-person competition distinguishes two vehicle classes: Restricted Class and Open Class.
2.  **Restricted Class** allows only cars that meet the following constraints:
    *   The vehicle is constructed according to the official [bill of materials](https://f1tenth.readthedocs.io/en/foxy_test/getting_started/build_car/bom.html). The teams are allowed to use components of similar or lower specifications.
    *   Each vehicle will be inspected as a part of qualification whether it meets the criteria. In case the criteria are not met, the vehicle is moved to the Open Class.
    *   **F1TENTH Competition is a battle of algorithms. Any hardware that should turn the odds in your favor is not allowed**.
    *   _Chassis_ : Any chassis listed as _1:10 scale_ car is allowed. Preferably **1:10 Traxxas** (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4platinum), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)), but generally, any chassis with similar dimensions is allowed. Both 4WD and 2WD are permitted.
    *   _Main Computation Unit_ : Due to supply chain issues, we’re removing constraints on the main computation unit. Any suitable computing unit that physically fits on the vehicle within the size limit is allowed. Examples include Nvidia Jetson Xavier NX, Nvidia Jetson Orin Nano, Nvidia Jetson TX2, Nvidia Jetson Nano, Intel NUC, Raspberry Pi, etc. In the spirit of the competition, all computation must be done onboard the vehicle.
    *   _LiDAR_ : [**Hokuyo UTM-30LX**](https://www.hokuyo-aut.jp/search/single.php?serial=169), its equivalent, or anything of lower specifications is allowed. The main observed characteristics are: detection range (30 m), scanning frequency (40 Hz), and angular resolution (0.25°).
    *   _Camera_ : Both _monocamera_ (e.g. Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and _stereocameras_ (e.g. Intel Realsense, ZED) are allowed.
    *   _Engine_ : Only brushless DC motors are allowed. The [**Velineon 3500 kV**](https://traxxas.com/products/parts/motors/velineon3500motor), its equivalent, or anything of lower specifications regarding power and torque are allowed.
    *   _Other sensors_ : Other sensors (IMUs, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g. Marvelmind) are not allowed.
3.  **Open Class** allows cars that do not fit into Restricted Class. These cars may compete, but they are not eligible for prizes, their ranking is kept separate, and you might not have any peers competing in the class. In addition, the following constraints are applied:
    *   Car dimensions should be within 20% difference to the dimensions of the car required in the Restricted Class. This is to make sure that the car can fit comfortably in the racing track and that it can compete with other cars in the Head-to-Head race.
    *   Only electric drive motors are allowed.

#### 2.2 Track & racing environment

The competition will take place inside [Huntington Place Detroit](https://www.huntingtonplacedetroit.com/). The characteristics of the environment where the track will be built are:

1.  The surface is flat and reflective. Therefore, LiDAR beams may reflect from the ground and measure the surrounding area rather than the ground. Similarly, depth cameras have problems with proper ground detection.
2.  The track border is constructed from single height air ducts of 33 cm diameter. Keep in mind that there can be a gap between the pipes through which the LiDAR beams can pass.
3.  The track will fit into an area of around 30×10 m.
4.  The track can be mapped in either the training sessions on each day or in the qualification session of each team. We are not providing dedicated time slots for each team to map the track. Although many teams are using SLAM algorithm or vision-based localization techniques, a dedicated **Map Creation** or **Mapping** session is not provided for the teams.

#### 2.3 Inspection

1.  The purpose of the Inspection is to check that the hardware of the autonomous cars meets the competition requirements and the cars are not dangerous for the environment, opponents, and people.
2.  The inspection of the vehicles is done on the first competition day in the morning.
3.  The inspection is done by the race referees.
4.  The inspection has to be completed before the Time Trials and after significant changes to the cars hardware or algorithms.

#### 2.4 Time Trial

##### 2.4.1 Definitions

1.  _Touching_ means moving the object by less than 5 cm. Moving by greater distance is called _Crashing_.
2.  Moving the track border by any distance is called _Crashing_.

##### 2.4.2 General

1.  Time Trial is a race with a goal to drive through the designated track as fast as possible. The idea is to push the algorithms to their limits.
2.  The race consists of two heats. Each heat lasts for 5 minutes, and the goal is to drive a single lap in as short time as possible and/or to drive as many complete laps as possible. Crashing and stopping the car does not pause the heat timer.
3.  Each team is provided two dedicated time slots for their vehicle to qualify. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team. If a team is not able to run the car in this dedicated time slot, the qualification phase is not passed for this team.
4.  The teams are allowed to change the configuration of their algorithms in between the heats, and even during the heat. When the configuration is changed during the heat, the car must stand still. In other words, the teams cannot update the configuration on-line while the car moves.
5.  The map (track layout) is **known** a priori and the track layout does not change over the whole competition. Keep in mind that cars crash into the walls and the layout of the track might slightly shift a little bit. Please consider this in your algorithms.
6.  The final score for the qualification is two parts: Firstly, based on the ranking of the **fastest laptimes** you receive points. E.g. with 10 teams the fastest team receives 10 points, second fastest 9 points, thrid fastest 8 points .... and so on. Secondly, based on the number of **consecutive uninterrupted laps** , a ranking of the teams is created and therefore the teams receive points. E.g. with 10 teams the team with the most laps receives 10 points, second team 9 points, thrid team 8 points .... and so on. The final score is the sum of both scores. Note that the best lap times and number of laps has to be obtained from the same uninterrupted session.

##### 2.4.3 Requirements for Time Trial qualification

1.  Each vehicle must demonstrate that it can drive autonomously through a track without crashing.
2.  The team must demonstrate that it is possible to trigger car emergency stop remotely.

##### 2.4.4 Penalties

1.  Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash.
2.  Upon crashing the track border or the static obstacle the team has to stop the car and move it (by hands) to the latest position before crash. After repairing the track and returning the obstacles to their appropriate locations, the race may continue. The time spent on moving the car to the checkpoint and repairing the track is considered the penalty.

##### 2.4.5 Evaluation

Each team will be evaluated based on the following criteria:

1.  _Fastest lap time_. The laptime will be measured with specific equipment by the race director.
2.  _Number of consecutive uninterrupted laps_

There will be two results tables based on these criteria.

#### 2.5 Head-to-Head Race

##### 2.5.1 General

1.  The Head-to-Head race is a race with two cars on the track at the same time.
2.  The racetrack has the same layout as in the training and qualification sessions.
3.  The algorithms must not intentionally hinder the opponent or perform any damage to it. Specifically, manoeuvres such as deliberate crowding of a car beyond the edge of the track or any other abnormal change of direction are strictly prohibited. The referees will have the final say in whether a driver is in violation of the rule.
4.  The head-to-head race will be organized as a knockout tournament with brackets seeded by results of the qualification. For example, with 8 teams, the bracket of the first round will be (#1 vs. #8, #2 vs. #7, #3 vs. #6, and #4 vs. #5).
5.  One head-to-head race consists of two teams racing against each other. One race has a dedicated timeslot of around 10 minutes. If one team is not showing up in these 10 minutes and let their car race, the other team won. If at some point along the race a car is not able to drive anymore (e.g. hardware issue, software not running etc.) and the teams are not able to restart the car withing the 10 minutes, the other team one the race. No time extensions are given and after the 10 minutes we move on to the next time slot and the next team.
6.  Each of the competing cars starts at its own starting line. Starting lines will be located at the opposite parts of the track.
7.  Overtaking may be carried out on either the right or the left.
8.  As opposed to time trials, no reconfiguration is allowed during the race, except after the crash, as described below.
9.  Ultimately, organizers reserve the right to assign blame in the case of vehicle collision in the head-to-head tournament.

##### 2.5.2 Requirements for qualification

1.  The team has successfully completed the Time Trial.
2.  The car must be equipped with front foam bumper, e.g., [TRA7436](https://traxxas.com/products/parts/7436) \+ [TRA7437](https://traxxas.com/products/parts/7437) \+ [TRA7415X](https://traxxas.com/products/parts/7415X). This solution is compatible with _Slash_. Model of _Ford Fiesta_ already has this bumper.
3.  The car has to be easily perceivable by the opponent’s LiDAR. Therefore, the car **must occupy a space of size at least 12×12 cm at every horizontal plane between 10 to 30 cm above the ground**.
4.  The car needs to provide beforehand that it is able to avoid static and dynamic obstacles. This is evaluated by the race referees with a test:
    *   The cars need to run 1 lap around the racetrack that includes static and dynamic obstacles
    *   These obstacles contain of size up to 35×32×30 cm, made from LiDAR perceivable material (e.g., cardboard).
    *   The racecars must show their ability to avoid those obstacles
    *   Based on this results the access to the race is granted.

##### 2.5.3 Penalties

1.  Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash. (Same rules as for Time Trial.)
2.  Touching the opponent is not penalized unless one of the cars significantly diverges from its expected trajectory.
3.  Upon crashing the border of the track, the team has to fix the track and place the car on the side of the track at the place where the car first crashed the border. Then, the car can continue the race. During all of this, the opponent’s car must not be restricted by the team’s actions and the opponent is allowed to further race without stopping its car. The penalty is the time spent on fixing the track and placing the car.
4.  Upon crashing the opponent, these steps are applied:
    *   Referees judge which car is at fault.
    *   Both cars are placed next to each other at the place decided by the referees
    *   The referees restart the race.

##### 2.5.4 Evaluation

1.  The first car that completes the designated number of laps (announced at the race) wins.
2.  There will be three referees.
3.  Two referees count the laps for each car, and the third is responsible for identifying the crashes.
