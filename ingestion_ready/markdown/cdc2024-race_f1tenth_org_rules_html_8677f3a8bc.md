[F1TENTH Rules](index.html)

## F1TENTH Rules

These rules are prepared for the _22nd International F1TENTH Autonomous Racing Competition_. Rules are subject to change. The latest version can be found [here](https://cdc2024-race.f1tenth.org/rules.html).

Date: 2024-07-09

**Table of content**

  * 1\. General
  * 2\. In-person (physical) competition
    * 2.1 Vehicle classes
    * 2.2 Track & racing environment
    * 2.3 Inspection
    * 2.4 Time Trial
      * 2.4.1 Definitions
      * 2.4.2 General
      * 2.4.3 Requirements for Time Trial qualification
      * 2.4.4 Penalties
      * 2.4.5 Evaluation
    * 2.5 Head-to-Head Race
      * 2.5.1 General
      * 2.5.2 Requirements for qualification
      * 2.5.3 Penalties
      * 2.5.4 Evaluation
  * 3\. Virtual (simulation) competition
    * 3.1 General

### 1\. General

International F1TENTH Autonomous Racing Competition is a racing competition open to teams of all levels. Competing teams may consist of any number of members; however, each participant should be a member of only one team.

The competition is organized as an in-person competition.

Teams can register for the competition using a [registration form]().

The preferred communication method with the organizers is the _#CDC2024_ channel on [F1TENTH-teams Slack](https://join.slack.com/t/f1tenth-teams/shared_invite/enQtMzc3ODU2ODM1NzE3LTBjMmVkMzZjZTJiNWUzZDFhZTJiODgzMjg0MTA1MDAxZTUxMzkwMDRhNTM2NzdjNDc5MTk5YTc5YmNhNTdhMTU).

### 2\. In-person (physical) competition

  1. The competition will comprise three parts – _Inspection and Orientation_ , _Time Trials_ and _2 Vehicle Head-to-Head_ race. Every participant must pass qualification and will be automatically registered to both races.

  2. Teams registered to the in-person competition need to provide and build a F1TENTH car by themselves according to the constraints listed below. In addition, each team must have a unique vehicle (i.e., a research lab may not field six teams with one car).

  3. To increase the quality of the future F1TENTH competitions, the winner of each race is encourage to publish the code of their algorithm under an open-source license in the [F1TENTH repository](https://github.com/f1tenth) on Github.

  4. In order to better accomodate all participating teams, all teams should have at most 4 team members present at the race space (includes sideline and seating area) during the event. Teams with more than 4 members will be required to either register as separate teams or discard/cycle their members during the event.

#### 2.1 Vehicle classes

  1. The in-person competition distinguishes two vehicle classes: Restricted Class and Open Class.

  2. **Restricted Class** allows only cars that meet the following constraints:

     1. The vehicle is constructed according to the official [bill of materials](https://f1tenth.readthedocs.io/en/foxy_test/getting_started/build_car/bom.html). The teams are allowed to use components of similar or lower specifications.
     2. Each vehicle will be inspected as a part of qualification whether it meets the criteria. In case the criteria are not met, the vehicle is moved to the Open Class.
     3. **F1TENTH Competition is a battle of algorithms. Any hardware that should turn the odds in your favor is not allowed**.
     4. _Chassis_ : Any chassis listed as _1:10 scale_ car is allowed. Preferably **1:10 Traxxas** (e.g., [TRA74054](https://traxxas.com/products/models/electric/ford-fiesta-st-rally), [TRA6804R](https://traxxas.com/products/models/electric/6804Rslash4x4platinum), [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm)), but generally, any chassis with similar dimensions is allowed. Both 4WD and 2WD are permitted.
     5. _Main Computation Unit_ : Due to supply chain issues, we’re removing constraints on the main computation unit. Any suitable computing unit that physically fits on the vehicle within the size limit is allowed. Examples inlcude Nvidia Jetson Xavier NX, Nvidia Jetson Orin Nano, Nvidia Jetson TX2, Nvidia Jetson Nano, Intel NUC, Raspberry Pi, etc. In the spirit of the competition, all computation must be done onboard the vehicle.
     6. _LiDAR_ : [**Hokuyo UTM-30LX**](https://www.hokuyo-aut.jp/search/single.php?serial=169), its equivalent, or anything of lower specifications is allowed. The main observed characteristics are: detection range (30 m), scanning frequency (40 Hz), and angular resolution (0.25°).
     7. _Camera_ : Both _monocamera_ (e.g. Logitech C270, Logitech C920, Raspberry Pi Camera Module V2, Arducam) and _stereocameras_ (e.g. Intel Realsense, ZED) are allowed.
     8. _Engine_ : Only brushless DC motors are allowed. The [**Velineon 3500 kV**](https://traxxas.com/products/parts/motors/velineon3500motor), its equivalent, or anything of lower specifications regarding power and torque are allowed. The car must have **only one** DC motor driving the wheels. The motor could either be sensored or sensorless as long as it meets the specifications
     9. _Other sensors_ : Other sensors (IMUs, encoders, custom electronic speed controllers) are not restricted. Indoor GPS sensors (e.g. Marvelmind) are not allowed.
     10. _Tires_ : There are no resutrictions on the tires used by the car. Any and all tires that fit the wheels of the chassis are permitted.
     11. _Battery_ : The drive motor should be driven _at most_ by one battery rated at most **4s**. There are no limitations on the capacity of the battery. More than one battery can be used on the car as long as only one 4s battery powers the motor. Teams are encouraged to have spare batteries to allow fast replacements in case the battery gets discharged at an inconvenient time.
  3. **Open Class** allows cars that do not fit into Restricted Class. These cars may compete, but they are not eligible for prizes, their ranking is kept separate, and you might not have any peers competing in the class. In addition, the following constraints are applied:

     1. Car dimensions should be within 20% difference to the dimensions of the largest car required in the Restricted Class (in this case [TRA68086](https://traxxas.com/products/models/electric/slash-4x4-tsm?t=specs)). This is to make sure that the car can fit comfortably in the racing track and that it can compete with other cars in the Head-to-Head race.
     2. Only electric drive motors are allowed.

#### 2.2 Track & racing environment

The competition will take place inside [Milan Convention Centre](https://www.micomilano.it/en). The characteristics of the environment where the track will be built are:

  1. The surface is flat and reflective. Therefore, LiDAR beams may reflect from the ground and measure the surrounding area rather than the ground. Similarly, depth cameras have problems with proper ground detection.
  2. The track border is constructed from single height air ducts of 33 cm diameter. Keep in mind that there can be a gap between the pipes through which the LiDAR beams can pass.
  3. The track will fit into an area of around 30×10 m.
  4. The track can be mapped in either the training sessions on each day or in the qualification session of each team. We are providing dedicated time slots for each team to map the track. Although many teams are using SLAM algorithm or vision-based localization techniques, a dedicated **Map Creation** or **Mapping** session is provided for the teams.
  5. The track will be atleast 3 car widths (90cm) wide everywhere around the track to allow for overtaking.
  6. The track will contain a mix of choke points, sharp hairpins, wide straights and extra wide corners to test the algorithms of the cars.
  7. During the practice session, no humans are allowed on the track, except to repair the track or obstacles, or to remove a stopped car.
  8. Removing the car from or placing the car on the track should always be done at the border of the track from the outside.
  9. If the car is not able to drive anymore, the team has to remove the car from the track as soon as possible.

#### 2.3 Inspection

  1. The purpose of the Inspection is to check that the hardware of the autonomous cars meets the competition requirements and the cars are not dangerous for the environment, opponents, and people.

  2. The inspection of the vehicles is done on the first competition day in the morning.

  3. The inspection is done by the race referees.

  4. The inspection has to be completed before the Time Trials and after significant changes to the cars hardware or algorithms.

#### 2.4 Time Trial

##### 2.4.1 Definitions

  1. _Touching_ means moving the object by less than 5 cm. Moving by greater distance is called _Crashing_.

  2. Moving the track border by any distance is called _Crashing_.

  3. The track will contain several _checkpoints_ , marked with a line across the track. Starting line is not a checkpoint.

##### 2.4.2 General

  1. Time Trial is a race with a goal to drive through the designated track as fast as possible. The idea is to push the algorithms to their limits.

  2. The race consists of two heats. Each heat lasts for 5 minutes, and the goal is to drive a single lap in as short time as possible and/or to drive as many complete laps as possible. Crashing and stopping the car does not pause the heat timer.

  3. The heat sessions are split in two with a one one-hour practice session in between. The teams have to book a time slot in each session. The schedule of the sessions will be shared with the teams before the race.

  4. Each team is provided two dedicated time slot for their vehicle to qualify. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team. There will be 1-5 minutes of dedicated time to switch from one team to the next. If a team is not able to run the car in this dedicated time slot, the qualification phase is not passed for this team.

  5. The teams are allowed to change the configuration of their algorithms in between the heats, and even during the heat. When the configuration is changed during the heat, the car must stand still. In other words, the teams cannot update the configuration on-line while the car moves.

  6. The map (track layout) is **known** a priori and the track layout does not change over the whole competition. Keep in mind that cars crash into the walls and the layout of the track might slightly shift a little bit. Please consider this in your algorithms.

  7. The final score for the qualification is two parts: Firstly, based on the ranking of the **fastest laptimes** you receive points. E.g. with 10 teams the fastest team receives 10 points, second fastest 9 points, thrid fastest 8 points .... and so on. Secondly, based on the number of **consecutive uninterrupted laps** , a ranking of the teams is created and therefore the teams receive points. E.g. with 10 teams the team with the most laps receives 10 points, second team 9 points, thrid team 8 points .... and so on. The final score is the sum of both scores. Note that the best lap times and number of laps has to be obtained from the same uninterrupted session.

##### 2.4.3 Requirements for Time Trial qualification

  1. Each vehicle must demonstrate that it can drive autonomously through a track without crashing.

  2. The team must demonstrate that it is possible to trigger car emergency stop remotely.

  3. Each team will have two dedicated time slots of 5 minutes each to qualify, with a one-hour break in between for all teams to practice.

     1. The teams have to book a time slot in each session.
     2. No time extensions are given and after the 5 minutes we move on to the next time slot and the next team.
     3. There will be 1-5 minutes of dedicated time to switch from one team to the next.
     4. If a team is not able to run the car in either dedicated time slots, the qualification phase is not passed for this team.

##### 2.4.4 Penalties

  1. Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash.

  2. Upon crashing the track border or the static obstacle the team has to stop the car and move it (by hand or using the remote control) to the latest position before crash. After repairing the track and returning the obstacles to their appropriate locations, the race may continue. The time spent on moving the car to the checkpoint and repairing the track is considered the penalty.

##### 2.4.5 Evaluation

Each team will be evaluated based on the following criteria:

  1. _Fastest lap time_. The laptime will be measured with specific equipment by the race director.
  2. _Number of consecutive uninterrupted laps_

There will be two results tables based on these criteria.

The best result in each category from the two time slots will be used for the final ranking. The final ranking is the sum of the points from the fastest lap time and the number of consecutive uninterrupted laps.

The qualification is passed by finishing a single lap without crashing. Otherwise, the team is disqualified from the competition.

#### 2.5 Head-to-Head Race

##### 2.5.1 General

  1. The Head-to-Head race is a race with two cars on the track at the same time.

  2. The racetrack has the same layout as in the training and qualification sessions.

  3. The algorithms must not intentionally hinder the opponent or perform any damage to it. Specifically, manoeuvres such as deliberate crowding of a car beyond the edge of the track or any other abnormal change of direction are strictly prohibited. The referees will have the final say in whether a driver is in violation of the rule.

  4. The head-to-head race will be organized as a double-elimination tournament with two brackets seeded by results of the qualification.

  5. The two winners of each bracket will qualify to compete in the Final Four rafce. This final tournament will feature a single elimination bracket.

  6. Before the start of **each** head-to-head race, **both** teams will be tested for obstacle avoidance and are required to use the same code for the race. Any violations to this rule could result in disqualification of the violating team (up to the organizers).

  7. Teams that fail to pass the obstacle avoidance test will have the option to race on the condition that they do not overtake the opponent.

     1. If the team fails to pass the obstacle avoidance test and overtakes the opponent, the team will be disqualified.
     2. The team that failed the obstacle avoidance is permitted to use manual control when the car is 5 meters behind the opponent to slow down the car and avoid overtaking.
     3. The faulty team is not allowed to use manual control to speed up the car and overtake the opponent.
     4. The faulty team can only overtake the opponent if the opponent crashes.
  8. One head-to-head race consists of two teams racing against each other. One race has a dedicated timeslot of around 10 minutes. If one team is not showing up in these 10 minutes and let their car race, the other team won. If at some point along the race a car is not able to drive anymore (e.g. hardware issue, software not running etc.) and the teams are not able to restart the car withing the 10 minutes, the other team wins the race. No time extensions are given and after the 10 minutes we move on to the next time slot and the next team.

  9. Both competing cars start from the same starting line used in the qualifications.

     1. The teams will start in a staggered formation.
     2. The team that ranked higher in qualifications starts with the front bumper longitudinally at the finish line, and the center of the car is laterally 15cm to the right of the centerline.
     3. The team that ranked lower in qualifications starts with the front bumper longitudinally 114 cm behind the finish line, and the center of the car is laterally 15cm to the left of the centerline.
  10. Overtaking may be carried out on either the right or the left.

  11. As opposed to time trials, no reconfiguration is allowed during the race, except after a crash, as described below.

  12. Ultimately, organizers reserve the right to assign blame in the case of vehicle collision in the head-to-head tournament.

  13. The race stewards will utilize a system of colored flags to communicate with the teams. The flags are as follows:

     1. **Checkered flag** : The steward holds a checkered flag in each hand, one for each team. A flag is raised if the team is on the last lap. The flag is dropped and then waved when the team finishes and wins the current round.
     2. **Red flag** : The steward holds a red flag in each hand, one for each team. A flag is raised if a race-stopping car crash occurs. The flag is dropped after all cars are stopped, and the team representatives are allowed to approach the track. After the crash is resolved by the stewards, the flag is dropped and the race resumes.
     3. **Yellow flag** : The steward holds a yellow flag in each hand, one for each team. A flag is raised if the team is warned for a rule violation.
     4. **Black flag** : The steward holds the black flag in each hand, one for each team. A flag is raised if the team is disqualified. The flag is dropped after the disqualified team stops the car and leaves the track. The opponent is allowed to continue the race till completion of the set number of laps.
     5. **Green flag** : Optional - raised to signal that the race is safe to continue. The flag is dropped after the race resumes.
        * The flag assignment is done at the start based on the qualification results. The team with the higher qualification result that starts on the right side of the track is assigned the flag set in the right hand. The team with the lower qualification result that starts on the left side of the track is assigned the flag set in the left hand.
  14. Collisions are judged by the referees.

     1. Collisions with track boundaries do not stop the race. The team that crashed into the track boundary must fix the track and place the car at the location of the crash. The opponent is allowed to continue. The crashed team bears the burden of the time spent on fixing the track and placing the car.
     2. Light side-bumps and slow-speed nudges are not penalized and do not stop the race.
     3. High-impact crashes that result in the displacement of one or both cars on crash result in a stoppage of the race.
     4. If a car crashes into the opponent, the referees will judge which car is at fault.
     5. Both cars will be restarted at the location of the crash, with the at-fault car placed behind the other car by 2 meters.
     6. A crash is not considered a warning unless judged by the referees.
     7. Crashes that result in a warning include but are not limited to “malicious” crashes where the autonomous car did not attempt to slow down or steer away from the opponent.
        * Under special circumstances, the referees may decide to give a warning to a team with the option of stopping the race to address the issue. The team has a maximum of 5 minutes to fix the issue and resume the race.
     8. After 3 warnings, the team is disqualified and the opponent automatically wins.

##### 2.5.2 Requirements for qualification

  1. The team has successfully completed the Time Trial.
  2. The car must be equipped with front foam bumper, e.g., [TRA7436](https://traxxas.com/products/parts/7436) \+ [TRA7437](https://traxxas.com/products/parts/7437) \+ [TRA7415X](https://traxxas.com/products/parts/7415X). This solution is compatible with _Slash_. Model of _Ford Fiesta_ already has this bumper.
  3. The car must be equipped with a rear bumper which is at least as high as the front bumper.
  4. The car has to be easily perceivable by the opponent’s LiDAR. Therefore, the car **must occupy a space of size at least 12×12 cm at every horizontal plane between 10 to 30 cm above the ground**.
  5. The car needs to provide beforehand that is is able to avoid static and dynamic obstacles. This is evaluated by the race referess with a test:
     1. The cars need to run 1 lap around the racetrack that includes static and dynamic obstacles
     2. These obstacles contain of size up to 35×32×30 cm, made from LiDAR perceivable material (e.g., cardboard).
     3. The racecars must show their ability to avoid those obstacles
     4. Based on this results the access to the race is granted.

##### 2.5.3 Penalties

  1. Touching the border of the track or a static obstacle is not penalized. Excessive, repeated touching (up to the organizers) is considered a crash. (Same rules as for Time Trial.)

  2. Touching the opponent is not penalized unless one of the cars significantly diverges from its expected trajectory.

  3. Upon crashing the border of the track, the team has to fix the track and place the car on the side of the track at the place where the car first crashed the border. Then, the car can continue the race. During all of this, the opponent’s car must not be restricted by the team’s actions and the opponent is allowed to further race without stopping its car. The penalty is the time spent on fixing the track and placing the car.

  4. Upon crashing the opponent, these steps are applied:

     1. Refrees call the crash and signal for it by raising the red flag.
     2. Referees judge which car is at fault.
     3. Both cars are placed at the location of the crash, with the at-fault car placed behind the other car by 2 meters.
     4. The referees restart the race with a green flag.

##### 2.5.4 Evaluation

  1. The first car that completes 10 laps wins.
  2. There will be a total of three referees.
  3. One referee will be assigned to each car that is solely responsible to count laps. The third referee is tasked with enforcing penalties and rule violations.

### 3\. Virtual (simulation) competition

#### 3.1 General

  1. The virtual competition will be completely done in an simulation environment only and no hardware is involved.

  2. This simulation environment is based on the [AutoDrive Ecosystem](https://autodrive-ecosystem.github.io/). The F1TENTH virtual competition will be complete done in this environment only and teams need to submit their code in time to this platform.

  3. The virtual competition will comprise two parts – _Time Trials_ and _2 Vehicle Head-to-Head_ race. Every participant must pass the Time Trials and will be automatically registered to both races.

  4. F1TENTH reserves the right to reject any submission that we deem illegal due to circumstances such as exploiting the simulation environment. Therefore their source code submission will be examined by the race stuarts after the race.

  5. The map used for all the races (Time Trials, Head-to-Head) will be the same. In the Time Trials this map will have added obstacles for the obstacle avoidance task.

  6. All details will be posted on the official page for the virtual competition [here](https://autodrive-ecosystem.github.io/competitions/f1tenth-sim-racing-cdc-2024/#f1tenth-sim-racing-league-cdc-2024).

  * © 2024 F1TENTH Foundation All rights reserved
  * Design: [HTML5 UP](https://html5up.net)
