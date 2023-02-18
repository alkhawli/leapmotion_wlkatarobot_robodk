# leapmotion_wlkatarobot_robodk

This code was generated as to play around with wlkata robotic arm with a servo gripper and a leap motion sensor.  I have generated a small [demo](https://www.linkedin.com/posts/toufikkhawli_robotics-computervision-data-activity-7030564124828819456-_4Mk?utm_source=share&utm_medium=member_desktop) on linkedin. 

## Requirement 

* python 3.7: The leap motion sdk was developed on python 2.7. In order to develop on python 3, the provided libraries were compiled and added to the repo. It was test on python 3.7.7. 
* CH340 driver for a USB serial communication.
* WlkataStudio: Tested on V1.015.
* Leap Motion Control Panel & Visualizer.

## Steps
* Using conda create a virutal environment based on python 3.7.7

```bash
conda conda create --name myenv python=3.7.7
conda activate myenv
pip install -r requirements.txt 
```