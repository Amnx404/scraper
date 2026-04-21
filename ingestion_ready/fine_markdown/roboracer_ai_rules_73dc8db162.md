These rules are prepared for the _24th International Roboracer Autonomous Racing Competition_. Rules are subject to change. The latest version can be found [here](http://icra2025-race.roboracer.ai/rules.html).

Date: 2026-01-10

# 1. General

International Roboracer Autonomous Racing Competition is an autonomous vehicle racing competition open to teams of all levels. Competing teams may consist of any number of members; however, each participant should be a member of only one team.

The competition is organized as an in-person competition.

Teams can register for the competition using a [registration form](https://forms.gle/FdfY9sKXREdu772u6).

The preferred communication method with the organizers is the _#ICRA2025_ channel on [Roboracer-teams Slack](https://join.slack.com/t/robo-racer/shared_invite/zt-2pq4fuyjq-gTUflzeZDKDDGjuVoeZqNg).

# 2. In-person (physical) competition

1.  The competition will comprise two main stages – Online Qualification and Vehicle Head-to-Head Knockout Races.

    In the online qualification round, teams must submit a 1-minute video showing their car driving autonomously on a track without any human intervention.

    Teams that qualify will compete in-person at Techfest, IIT Bombay, where they will first get a 15-minute practice session on the track, followed by an open track trial for all teams.

    The knockout races will then determine the winners, with the fastest lap deciding each matchup. In case of a tie, the best lap time from the open track trials will be used.

2.  Teams registered for the in-person competition need to provide and build a Roboracer car by themselves according to the constraints listed below. In addition, each team must have a unique vehicle (i.e., a research lab may not field six teams with one car).

3.  To increase the quality of the future Roboracer competitions, the top 3 teams of each race are encouraged to publish the code of their algorithm under an open-source license in the [Roboracer repository](https://github.com/f1tenth) on Github.

4.  In order to better accommodate all participating teams, all teams should have **at most 10 team members** present at the race space (includes sideline and seating area) during the event. There are no restrictions on the number of team members otherwise and all members will receive certificates of participation.

5.  Teams should not display any national flags or national symbols. This competition is between peers, not nations.

## 2.1 Vehicle Specifications

Only cars that meet the following constraints will be allowed to participate:

1.  The vehicle is constructed according to the official [bill of materials](https://f1tenth.readthedocs.io/en/foxy_test/getting_started/build_car/bom.html#bill-of-materials). The teams are allowed to use components of similar or lower specifications.
2.  Each vehicle will be inspected as a part of qualification whether it meets the criteria. In case the criteria are not met, the vehicle is disqualified.
3.  _Chassis_: Any chassis listed as _1:10 scale_ car is allowed. Preferably **1:10 Traxxas** (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4platinum), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)), but generally, any chassis with similar dimensions is allowed. Both 4WD and 2WD are permitted.
4.  _Main Computation Unit_: Due to supply chain issues, we're removing constraints on the main computation unit. Any suitable computing unit that physically fits on the vehicle within the size limit is allowed. Examples include Nvidia Jetson Xavier NX, Nvidia Jetson Orin Nano, Nvidia Jetson TX2, Nvidia Jetson Nano, Intel NUC, Raspberry Pi, etc. In the spirit of the competition, all computation must be done onboard the vehicle.
5.  _LiDAR_: [**Hokuyo UTM-30LX**](https://www.hokuyo-aut.jp/search/single.php?serial=169), its equivalent, or any 2D LiDAR with similar specifications is recommended but not required. The main characteristics are detection range (30 m), scanning frequency (40 Hz), and angular resolution (~0.25°).
6.  _Camera_: The recommended camera for the competition is Intel RealSense D455 or similar; other monocameras (e.g., Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and stereocameras (e.g., ZED) are also recommended for practice, but only the Intel RealSense D455 or similar should be used during the competition runs.
7.  _Engine_: Only brushless DC motors are allowed. The [**Velineon 3500 kV**](https://traxxas.com/products/parts/motors/velineon3500motor), its equivalent, or anything of lower specifications regarding power and torque are allowed. The car must have **only one** DC motor driving the wheels. The motor could either be sensored or sensorless as long as it meets the specifications.
8.  _Other sensors_: Other sensors (IMUs, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g. Marvelmind) are not allowed.
9.  _Tires_: There are no restrictions on the tires used by the car. Any and all tires that fit the wheels of the chassis are permitted.
10. _Battery_: The drive motor should be driven _at most_ by one battery rated at most **4s**. There are no limitations on the capacity of the battery. More than one battery can be used on the car as long as only one 4s battery powers the motor. Teams are encouraged to have spare batteries to allow fast replacements in case the battery gets discharged at an inconvenient time.
11. _Transmitter Spot_: The car must have a designated spot at the front-half of the car of at least 8cm x 12cm for a transmitter. The spot should be easily accessible and nothing should be on top of the transmitter. This spot will be used for a transmitter that will be used for time-keeping.

## 2.2 Track & racing environment

The competition will take place inside [Georgia World Congress Center](https://www.gwcca.org/georgia-world-congress-center). The characteristics of the environment where the track will be built are:

1.  The surface is flat and reflective. Therefore, LiDAR beams may reflect from the ground and measure the surrounding area rather than the ground. Similarly, depth cameras have problems with proper ground detection.
2.  The track border is constructed from single height air ducts of 33 cm diameter. Keep in mind that **there will be gaps** between the pipes through which the LiDAR beams can pass.
3.  The track can be mapped in either the training sessions on each day or in the qualification session of each team. We are providing dedicated time slots for each team to map the track. Although many teams are using SLAM or vision-based localization techniques, a dedicated **Map Creation** or **Mapping** session is provided for the teams.
4.  The track will be at least 4 car widths (120cm) wide everywhere around the track to allow for and incentivize overtaking.
5.  The track will contain a mix of choke points, sharp hairpins, wide straights and extra wide corners to test the algorithms of the cars. The track borders will contain holes on parts of the track to test out the robustness of the algorithms.
6.  No humans are allowed on the track at all times, except to repair the track or obstacles, or to remove a stopped car.
7.  Removing the car from or placing the car on the track should always be done at the border of the track from the outside.
8.  If the car is not able to drive anymore, the team has to remove the car from the track as soon as possible.
9.  All days of the competition will be streamed live on twitch on the official Roboracer channel. The stream will be available for the public to watch.

## 2.3 Practice

1.  There will be two practice days for the competition. The first day will be dedicated to regulated practice sessions and the second day will be dedicated to open practice sessions.
2.  The dedicated time slots for the regulated practice sessions will be designated on a first-come-first-serve basis. The schedule of the sessions will be shared with the teams before the competition. Each session will be 10 minutes long.
3.  The second day of practice will be open practice sessions. To limit the number of teams on the track at the same time, the teams will be split into groups. Each group will have a shared time for open practice. The groups will be assigned by the organizers. The schedule of the sessions will be shared with the teams before the competition. The length of these sessions will be determined by the number of teams. Tentatively, the sessions will be 4 hours long.
4.  During shared practice sessions, if a car is stationary on the track for more than 5 minutes and the team does not remove the car, the car will be removed by the organizers and the team will be flagged for obstructing practice.
    *   Other teams are allowed to report a stationary car on the track to the organizers.
    *   If a team is flagged three times for obstructing practice, the team will be disqualified from the competition.

## 2.3 Inspection

1.  The purpose of the Inspection is to check that the hardware of the autonomous cars meets the competition requirements and the cars are not dangerous for the environment, opponents, and people.
2.  The inspection of the vehicles is done on the first day in the morning.
3.  The inspection is done by the race referees.
4.  The inspection has to be completed before the Time Trials and after any significant changes to the cars hardware or algorithms during any of the days of the event.

## 2.4 Time Trial

### 2.4.1 Definitions

1.  _Touching_ means moving the object by less than 5 cm. Moving by a greater distance is called _Crashing_.
2.  Moving the track border by any distance is called _Crashing_.

### 2.4.2 General

1.  Each team must pass the inspection to be able to participate in the Time Trial. Any team that does not pass the inspection on the first day will be disqualified from the competition.
2.  Time Trial is a race with a goal to drive through the designated track as fast as possible and as consistently as possible. The idea is to push the algorithms to their limits.
3.  The race consists of two heats. Each heat lasts for 5 minutes, and the goal is to drive a single lap in as short time as possible and to drive as many complete laps as possible. Crashing and stopping the car does not pause the heat timer.
4.  The heat sessions are split in two with a one-hour practice session in between. The teams have to book a time slot in each session. The schedule of the sessions will be shared with the teams before the race.
5.  Each team is provided two dedicated time slots for their vehicle to qualify. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team. There will be 1-5 minutes of dedicated time to switch from one team to the next. If a team is not able to run the car in this dedicated time slot, the qualification phase is not passed for this team.
6.  The teams are allowed to change the configuration of their algorithms in between the heats, and even during the heat. When the configuration is changed during the heat, the car must stand still. In other words, the teams cannot update the configuration on-line while the car moves.
7.  The map (track layout) is **known** a priori (from practice the day before) and the track layout does not change over the whole competition. Keep in mind that cars crash into the walls and the layout of the track might slightly shift a little bit. Please consider this in your algorithms.

### 2.4.3 Requirements for Time Trial qualification

1.  Each vehicle must demonstrate that it can drive autonomously one lap through the track without crashing.
2.  The team must demonstrate that it is possible to trigger car emergency stop remotely.
3.  Each team will have two dedicated time slots of 5 minutes each to qualify, with a one-hour break in between for all teams to practice.
    1.  The teams have to book a time slot in each session.
    2.  No time extensions are given and after the 5 minutes we move on to the next time slot and the next team.
    3.  There will be 1-5 minutes of dedicated time to switch from one team to the next.
    4.  If a team is not able to run the car in either dedicated time slots, the team fails the qualification phase and is disqualified from the competition.

### 2.4.4 Penalties

1.  Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash.
2.  Upon crashing the track border or the static obstacle the team has to stop the car and move it (by hand or using the remote control) to the latest position before crash. After repairing the track and returning the obstacles to their appropriate locations, the race may continue. The time spent on moving the car to the checkpoint and repairing the track is considered the penalty.

### 2.4.5 Evaluation

The competition consists of two heats: the first heat will be the trial, and the second heat will be the final. Each team will be evaluated based on the fastest lap time achieved during the competition. The final score will be cumulative, combining the results from the time trial and the head-to-head knockout races.

Fastest lap time: Teams are ranked based on their fastest lap times. In the knockout races, the car with the fastest lap wins each matchup.

Tie-breaker: If two or more teams have identical lap times in the knockout stage, the best lap time from the open track trials on Day 2 will be used to break the tie.

To pass the qualification, a team must complete at least one lap without crashing. Teams failing to do so will be disqualified from the in-person competition.

## 2.5 Head-to-Head Race

### 2.5.1 General

1.  The Head-to-Head race is a race with two cars on the track at the same time.
2.  The racetrack has the same layout as in the training and qualification sessions.
3.  The algorithms must not intentionally hinder the opponent or perform any damage to it. Specifically, maneuvers such as deliberate crowding of a car beyond the edge of the track or any other abnormal change of direction are strictly prohibited. The referees will have the final say in whether a driver is in violation of this rule.
    *   Should a team be found in violation of this rule, the referees will issue a warning in the form of a yellow flag. After three warnings, the team is disqualified.
4.  The head-to-head race will be organized as a double-elimination tournament with two brackets seeded by results of the qualification.
5.  The two winners of each bracket will qualify to compete in the Final Four race. This final tournament will feature a single elimination bracket.
6.  Before the start of **each** head-to-head race, **both** teams will be tested for obstacle avoidance and are required to use the same code for the race. Any violations to this rule could result in disqualification of the violating team (up to the organizers).
7.  Teams that fail to pass the obstacle avoidance test will have the option to race on the condition that they do not overtake the opponent.
    1.  If the team fails to pass the obstacle avoidance test and overtakes the opponent, the team will be disqualified.
    2.  The team that failed the obstacle avoidance is permitted to use manual control when the car is 5 meters behind the opponent to slow down the car and avoid overtaking.
    3.  The faulty team is not allowed to use manual control to speed up the car and overtake the opponent.
    4.  The faulty team can only overtake the opponent if the opponent crashes.
8.  One head-to-head race consists of two teams racing against each other. One race has a dedicated time slot of around 10 minutes. If one team is not showing up in these 10 minutes and let their car race, the other team won. If at some point along the race a car is not able to drive anymore (e.g. hardware issue, software not running etc.) and the teams are not able to restart the car within the 10 minutes, the other team wins the race. No time extensions are given and after the 10 minutes we move on to the next time slot and the next team.
    *   Each race consists of three rounds, the team that wins two rounds wins the race.
9.  Both competing cars start from the same starting line used in the qualifications.
    1.  The teams will start side-by-side separated by one car width (30cm) from each other.
    2.  For the first round, the team that ranked higher in qualifications chooses the starting position (left or right). The other team starts on the opposite side.
    3.  In the second round, the teams switch sides. The team that started on the left side in the first round starts on the right side in the second round.
    4.  Should a third round be necessary, a coin flip will determine the starting position. The team that ranked higher in qualifications will call the coin flip (i.e. heads or tails). The team that wins the coin flip chooses the starting position.
10. Overtaking may be carried out on either the right or the left.
11. As opposed to time trials, no reconfiguration is allowed during the race, except after a crash, as described below.
12. Ultimately, organizers reserve the right to assign blame in the case of vehicle collision in the head-to-head tournament.
13. Collisions are judged by the referees.
    1.  Collisions with track boundaries do not stop the race. The team that crashed into the track boundary must fix the track and place the car at the location of the crash. The opponent is allowed to continue. The crashed team bears the burden of the time spent on fixing the track and placing the car.
    2.  Light side-bumps and slow-speed nudges are not penalized and do not stop the race.
    3.  High-impact crashes that result in the displacement of one or both cars on crash result in a stoppage of the race.
    4.  If a car crashes into the opponent, the referees will judge which car is at fault.
    5.  Both cars will be restarted at the location of the crash, with the at-fault car placed behind the other car by 2 meters.
    6.  A crash is not considered a warning unless judged by the referees.
    7.  Crashes that result in a warning include but are not limited to "malicious" crashes where the autonomous car did not attempt to slow down or steer away from the opponent.
        *   Under special circumstances, the referees may decide to give a warning to a team with the option of stopping the race to address the issue. The team has a maximum of 5 minutes to fix the issue and resume the race.
    8.  After 3 warnings, the team is disqualified and the opponent automatically wins.
    9.  If the team that was crashed into is able to autonomously detect and recover from the crash by stopping on the side of the track, that team is granted an extra head-start of 1 meter before the restart (i.e. the at-fault car is placed 3 meters behind the other car).

### 2.5.2 Requirements for qualification

1.  The team has successfully completed the Time Trial.
2.  The car must be equipped with a front foam bumper, e.g., [TRA7436](https://traxxas.com/products/parts/7436) + [TRA7437](https://traxxas.com/products/parts/7437) + [TRA7415X](https://traxxas.com/products/parts/7415X). This solution is compatible with _Slash_. The model of _Ford Fiesta_ already has this bumper.
3.  The car must be equipped with a rear bumper which is at least as high as the front bumper.
4.  The car has to be easily perceivable by the opponent’s LiDAR. Therefore, the car **must occupy a space of size at least 12x12 cm at every horizontal plane between 10 to 30 cm above the ground**.
5.  The car needs to provide beforehand that it is able to avoid static and dynamic obstacles. This is evaluated by the race referees with a test:
    1.  The cars need to run 1 lap around the racetrack that includes static and dynamic obstacles.
    2.  These obstacles consist of size up to 35x32x30 cm, made from LiDAR perceivable material (e.g., cardboard).
    3.  The racecars must show their ability to avoid those obstacles.
    4.  Based on these results, access to the race is granted.

### 2.5.3 Penalties

Track abuse: If a team abuses the track (e.g., deliberately cutting corners, damaging the track, or violating race boundaries excessively), they will be penalized. Penalties will be decided by a group of referees, and their decisions are final.

Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash. (Same rules as for Time Trial.)

Touching the opponent is not penalized unless one of the cars significantly diverges from its expected trajectory.

Upon crashing the border of the track, the team has to fix the track and place the car on the side of the track at the place where the car first crashed the border. Then, the car can continue the race. During all of this, the opponent’s car must not be restricted by the team’s actions and the opponent is allowed to further race without stopping its car. The penalty is the time spent on fixing the track and placing the car.

Upon crashing the opponent, these steps are applied:

Referees call the crash and signal for it by raising the red flag.

Referees judge which car is at fault.

Both cars are placed at the location of the crash, with the at-fault car placed behind the other car by 2 meters.

The referees restart the race with a green flag.

### 2.5.4 Evaluation

1.  The first car that completes **20 laps** wins.
2.  There will be at least three referees.
3.  One referee will be assigned to each car and is solely responsible for calling flag raises and rule violations per team. The third referee is tasked with enforcing penalties, crash resolution, and time-keeping.
