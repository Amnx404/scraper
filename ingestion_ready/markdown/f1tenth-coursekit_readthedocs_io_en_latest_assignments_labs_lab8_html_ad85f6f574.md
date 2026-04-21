# Lab 8 - Perception and Planning¶

Tip

Before starting this lab, review the [Lecture 17](../../lectures/ModuleF/lecture17.html#doc-lecture17) and [Lecture 18](../../lectures/ModuleF/lecture18.html#doc-lecture18) to ensure you are familiar with the material.

**Goals:**

Most racing series feature multiple vehicles competing simultaneously on a single track. As such, safely overtaking and navigating in the presence of other vehicles is paramount to performing well. Since the strategy and decisions of of other vehicles cannot be known ahead of time and may, in fact, be stochastic it is necessary for your car to react to new constraints imposed by other vehicles online. Thus, the goal of this lab is to track and predict the pose of an opponent vehicle.

**Learning Outcomes:**

The following fundamental should be understood by the students upon completion of this lab:

>   * Vision and Perception
>
>>     * _Camera model and parameters:_ You should be able to understand how the real camera model and the pin hole camera model are related and what assumptions are made while going from the former to the latter.
>>
>>     * _Transformations:_ You should be able to understand 3 dimensional transformations and know the representations of transformations.
>>
>>     * _Single View Geometry:_ You should be able to understand and work with single view geometry and how world coordinate frame points translate to camera coordinate frame points.
>>
>>     * _Homography:_ You should be able to work with homography and how it can be used to calculate pose of the camera given the world coordinate correspondances.
>
>   * Programming skills
>
>>     * Working with images on ROS
>>
>>     * Transformations using tf and implementation of AprilTags and similar libraries.
>>
>>     * Implementing nodelets in ROS and their advantages.
>
>

**Required Skills:** ROS, Python/C++

**Allotted Time:** 1 week

**Repository:** [Github Repository](https://github.com/f1tenth/f1tenth_labs/tree/master/lab8/latex)

The repository contains the latex source files as well as any skeleton code. Compile the latex source files to view the most up to date handout.
