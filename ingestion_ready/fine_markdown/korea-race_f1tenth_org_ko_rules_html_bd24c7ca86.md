[F1TENTH Rules](../index.html)

## F1TENTH Rules

_Last Updated: 2022-10-15_

**Table of Contents**

*   1. General Competition
*   2. In-Person (Real) Competition
    *   2.1 Vehicle Class
    *   2.2 Track and Racing Environment
    *   2.3 Vehicle Inspection
    *   2.4 Time Trial
        *   2.4.1 Definitions
        *   2.4.2 General
        *   2.4.3 Time Trial Qualification Requirements
        *   2.4.4 Penalties
        *   2.4.5 Evaluation
    *   2.5 One-on-One Race
        *   2.5.1 General
        *   2.5.2 Evaluation Requirements
        *   2.5.3 Penalties
        *   2.5.4 Evaluation

### 1. General Competition

The International F1TENTH Autonomous Racing Competition is a race that all levels of teams can participate in. While competing teams can consist of a few members, each participant can only belong to one team.

The competition will be held as an in-person competition:

*   In-person competition

Each team can register for the race using the registration form. Registration is open until November 11, 2022.

The preferred communication method with the organizers is the _KSMTE2022_ channel on [F1TENTH Team Slack](https://f1tenthxkorea.slack.com/archives/C0484BSEJ2D).

### 2. In-Person (Real) Competition

1.  The competition consists of three parts: inspection, time trial, and one-on-one races. All participants must pass the inspection stage to be automatically registered for the two races (time trial and one-on-one race).
2.  Teams registered for the in-person competition must provide and build their F1TENTH vehicles according to the constraints listed below. Each team must also have a unique vehicle (i.e., six teams cannot be formed with one vehicle).
3.  To improve the quality of future F1TENTH competitions, winners of each race are encouraged to publish their algorithmic code under an open-source license in the [F1TENTH repository](https://github.com/f1tenth) on Github.

#### 2.1 Vehicle Class

1.  For the in-person competition, the **Vehicle Class** allows only vehicles that meet the following constraints:
    *   The vehicle is built according to the official [BOM](https://f1tenth.readthedocs.io/en/stable/getting_started/build_car/bom.html). Teams may use components of similar or lower specifications.
    *   Each vehicle will be inspected to ensure it meets the criteria. If the criteria are not met, the vehicle will be moved to the open class.
    *   **F1TENTH races are about algorithms. Hardware advantages for racing are not allowed.**
    *   _Car Chassis_: Any chassis listed for 1:10 scale vehicles is allowed. Good examples include **Traxxas 1:10 cars** (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4platinum), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)), but generally, any chassis with similar dimensions is acceptable. Both 4WD and 2WD are allowed.
    *   _Main Computing Unit_: **Nvidia Jetson Xavier NX**, Nvidia Jetson NX, or anything with equivalent or lower GPU and CPU specifications is allowed. Other examples include Raspberry Pi, Arduino, and Beaglebone.
    *   _LiDAR_: [**Hokuyo UST-10LX**](https://www.hokuyo-aut.jp/search/single.php?serial=167), or any LiDAR with equivalent or lower specifications is allowed. Key observed characteristics are detection range (10m), scan frequency (40Hz), and angular resolution (0.25°).
    *   _Camera_: Both mono cameras (e.g., Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and stereo cameras (e.g., Intel Realsense, ZED) are allowed.
    *   _Drivetrain_: Only brushless DC motors are allowed. [**Velineon 3500 kV**](https://traxxas.com/products/parts/motors/velineon3500motor), or anything with equivalent or lower specifications regarding power and torque is allowed.
    *   _Other Sensors_: Other sensors (IMU, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g., Marvelmind) are not allowed. Additionally, parts that rapidly accelerate the internal computation for racing are prohibited.

#### 2.2 Track and Racing Environment

The race will be held at [Ramada Plaza Jeju](). The track environment is as follows:

1.  The surface is flat and reflective. Therefore, LiDAR beams may reflect off the ground and measure the surrounding area instead of the ground. Similarly, depth cameras have issues with proper ground detection.
2.  The room is surrounded by windows and "glass walls," making it bright and sunny. Therefore, the windows are covered with opaque material up to 50cm from the ground to enhance perception.
3.  The track boundary consists of a single 33cm diameter air pipe made of aluminum and metal, secured by plastic/wooden holders. There may be gaps between the pipes through which LiDAR beams can pass.
4.  The track will fit within an area of approximately 28.5×11 m.
5.  The track can be mapped during daily training sessions or each team's qualifying sessions. Dedicated time slots for teams to map the track are not provided. As many teams use SLAM algorithms or vision-based localization techniques, **dedicated map creation** or **mapping sessions** are not provided for them.

#### 2.3 Vehicle Inspection

1.  The purpose of the vehicle inspection is to ensure that the autonomous car's hardware meets the race requirements and that the car is not dangerous to the environment, opponents, or people.
2.  Vehicle inspection will take place on the morning of the first race day.
3.  Vehicle inspection will be conducted by the race officials.
4.  Vehicle inspection must be completed before the time trial and after any significant changes to the car's hardware or algorithms.

#### 2.4 Time Trial

##### 2.4.1 Definitions

1.  Contact is defined as moving an obstacle less than 5cm. Moving it further is considered a collision.
2.  Moving the track boundary by any distance is considered a collision.
3.  The track includes several checkpoints marked by lines across the track. The start line is not a checkpoint.

##### 2.4.2 General

1.  The Time Trial is a race where the goal is to drive as fast as possible around a designated track, pushing the limits of the algorithm.
2.  Qualifying is evaluated based on two criteria. Each qualifying run is a 5-minute attempt to complete as many laps as possible as quickly as possible. The timer does not stop even if the car collides or stops.
3.  Each team is given two opportunities to run their qualifying session. Time will not be extended, and each team will be allocated 5 minutes. If a team cannot get their car moving within 5 minutes, they will be disqualified from qualifying.
4.  Each team can change their algorithm between qualifying runs, or even during a run. If the algorithm is changed during a qualifying run, the car must be stationary. This means teams cannot modify their algorithms online while the car is moving.
5.  The track will be announced in advance, and the track layout will not change throughout the race. Be aware that the car may collide with walls, and the track layout might change slightly. Consider this in your algorithm.
6.  The final qualifying score consists of two parts. First, teams receive points based on their rank in the fastest lap times (e.g., in a field of 10 teams, 1st place gets 10 points, 2nd place gets 9 points, 3rd place gets 8 points). Second, teams receive points based on their rank in the number of consecutive laps completed, creating a ranking for each team (e.g., in a field of 10 teams, the team with the most laps gets 10 points, the second most gets 9 points, the third most gets 8 points). The final score is the sum of these two scores.

##### 2.4.3 Time Trial Qualification Requirements

1.  Each vehicle must demonstrate its ability to autonomously navigate the track without collisions.
2.  Teams must demonstrate the ability to remotely execute an emergency stop for the car.

##### 2.4.4 Penalties

1.  Contacting the track edge or static obstacles will not incur a penalty. However, excessive and repeated contact may be considered a collision.
2.  In case of a collision with the track boundary or a stationary obstacle, the team must stop their car and use their hands to move it to the most recently passed checkpoint. The race can be resumed after the track and obstacle are restored to their original state. The time taken to move the car to the checkpoint and repair the track is considered a penalty.

##### 2.4.5 Evaluation

Each team will be evaluated based on the following criteria:

1.  Fastest lap time. Lap times will be measured by race officials using specific equipment.
2.  Number of laps completed in each qualifying run.

Two result tables will be generated based on these criteria.

#### 2.5 One-on-One Race

##### 2.5.1 General

1.  A one-on-one race is a race where two cars compete on the same track at the same time.
2.  The race track will be the same as the track used for practice and qualifying.
3.  Algorithms must not intentionally interfere with the opposing vehicle or cause any damage. Specifically, movements such as intentionally going off the track edge to cause confusion or other abnormal directional changes are strictly prohibited. The judges will have the final decision on whether a driver has violated the rules.
4.  One-on-one races will be conducted as a tournament based on the seeds assigned according to the qualifying results. For example, if there are 8 teams, the first round matchups will be (#1 vs #8, #2 vs #7, #3 vs #6, #4 vs #5).
5.  A single one-on-one race involves two teams competing against each other. Each race has a time slot of approximately 10 minutes. If one team does not appear within 10 minutes and the race proceeds, the opposing team wins. If at any point during the race a vehicle can no longer drive (e.g., due to hardware issues, software malfunction, etc.) and cannot be restarted within 10 minutes, the opposing team wins. No separate time extensions will be given, and after 10 minutes, the next pair of teams will race.
6.  Competing cars will start from their respective starting lines. The starting line for each car will be positioned opposite each other within the track.
7.  Overtaking can be performed from the right or left side.
8.  Unlike the Time Trial race, vehicle reconfiguration during the race is not possible, except after a collision as described below.
9.  Ultimately, the organizers reserve the right to hold vehicles responsible in case of collisions during the one-on-one races.

##### 2.5.2 Evaluation Requirements

1.  Teams must have successfully passed the Time Trial race.
2.  The car must be equipped with a front bumper (e.g., [TRA7436](https://traxxas.com/products/parts/7436) + [TRA7437](https://traxxas.com/products/parts/7437) + [TRA7415X](https://traxxas.com/products/parts/7415X) which mitigates impact and vehicle damage. The 'Ford Fiesta' model already has this bumper).
3.  The car must be easily recognizable by the opponent's LiDAR. Therefore, the car must occupy a space of at least 12x12cm on any horizontal plane between 10cm and 30cm from the ground. (Attach a LiDAR-recognizable plate to the rear of the vehicle).
4.  The car must be able to avoid dynamic and static obstacles. This will be evaluated by the judges with the following test:
    *   The car must complete one lap of the race track containing static and dynamic obstacles.
    *   These obstacles will be up to 35x32x30 cm in size and made of LiDAR-detectable material (e.g., cardboard).
    *   The race car must demonstrate its ability to avoid such obstacles.
    *   Based on this result, participation in the race will be permitted.

##### 2.5.3 Penalties

1.  Contacting the track edge or static obstacles will not incur a penalty, but excessive and repeated contact will be considered a collision (same as Time Trial race rules).
2.  Contact with the opposing vehicle will not incur a penalty, as long as one of the vehicles does not deviate significantly from its intended path.
3.  Immediately after hitting the track boundary, the team must restore the track to its original state and position their car on the side of the track relative to where it first hit. The car can then continue the race. During this action, the opposing team's car, which was racing, must not be obstructed by the team whose car collided, and the opposing team can continue racing without stopping their car. The penalty is the time taken to fix the track and position the car.
4.  Colliding with an opponent will result in the following steps:
    *   The judge will determine which car is at fault.
    *   Both cars will be placed side-by-side at a location determined by the judge.
    *   The judge will restart the race.

##### 2.5.4 Evaluation

1.  The car that completes 10 laps of the track first wins.
2.  There will be a total of two judges, one for each car.
3.  Each judge must count the number of laps completed by their assigned car and verify collision situations.

*   © 2022 F1TENTH Foundation All rights reserved
*   Design: [HTML5 UP](https://html5up.net)
