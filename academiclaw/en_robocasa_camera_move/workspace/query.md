# Robocasa Camera Movement Implementation

## Task Objective

Implement camera movement functionality in the Robocasa simulation environment, supporting setting different poses for the same camera at each timestep, in order to collect training data for next best view selection models in robot manipulation.

Please work on the current main branch of Robocasa and provide a method for setting camera poses using absolute coordinates in the robot base frame within the Robomimic framework.

## Background

Robocasa is a robot simulation environment based on Robosuite / MuJoCo, designed for robot manipulation tasks in kitchen scenes. This task requires you to understand the camera system in Robocasa/Robosuite and implement the ability to dynamically control camera poses through code.

Camera poses need to be set using absolute coordinates in the robot base frame, rather than the world frame, to facilitate alignment with robot manipulation data.

## Deliverables

Please complete the following three deliverables and save them in the current directory:

1. **Python example script (*.py)** -- A minimal portable solution that can be easily integrated into existing data collection pipelines. The script should demonstrate how to dynamically set camera poses at each timestep and perform offscreen rendering.

2. **Functionality documentation (*.md)** -- A concise document describing the key interfaces needed to implement this feature, including:
   - How to set camera poses (position + orientation)
   - How to perform offscreen rendering
   - Usage examples within the Robomimic framework
   - Notes (coordinate frame conventions, quaternion format, etc.)

3. **Camera trajectory video (*.mp4)** -- Continuous smooth camera trajectory movement in a kitchen scene (e.g., PnPCounterToSink), rendered offscreen as a human-readable video.

## Technical Requirements

- Use Robocasa / Robosuite MuJoCo simulation interfaces
- Camera poses expressed in absolute coordinates of the robot base frame
- Support setting different poses for the same camera at each timestep
- Use offscreen rendering to generate video
- Code should be a minimal portable solution with clear structure
