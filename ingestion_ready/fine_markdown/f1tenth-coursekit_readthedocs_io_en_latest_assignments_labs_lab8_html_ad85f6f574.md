# Lab 8 - Perception and Planning

**Prerequisites:**
Review [Lecture 17](../../lectures/ModuleF/lecture17.html#doc-lecture17) and [Lecture 18](../../lectures/ModuleF/lecture18.html#doc-lecture18).

**Goals:**
Safely overtaking and navigating in the presence of other vehicles is crucial in racing. Since the strategies of other vehicles are unknown and potentially stochastic, your car must react to dynamic constraints. This lab focuses on tracking and predicting the pose of an opponent vehicle.

**Learning Outcomes:**
Upon completion of this lab, students should understand:

*   **Vision and Perception:**
    *   **Camera Model and Parameters:** The relationship between the real camera model and the pinhole camera model, including assumptions made in the simplification.
    *   **Transformations:** 3D transformations and their representations.
    *   **Single View Geometry:** How world coordinate points translate to camera coordinate points.
    *   **Homography:** How to use homography to calculate camera pose given world coordinate correspondences.
*   **Programming Skills:**
    *   Working with images in ROS.
    *   Transformations using `tf` and implementing libraries like AprilTags.
    *   Implementing ROS nodelets and understanding their advantages.

**Required Skills:** ROS, Python/C++
**Allotted Time:** 1 week

**Repository:** [Github Repository](https://github.com/f1tenth/f1tenth_labs/tree/master/lab8/latex)

The repository contains LaTeX source files and skeleton code. Compile the LaTeX files for the most up-to-date handout.
