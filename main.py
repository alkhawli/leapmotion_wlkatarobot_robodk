import numpy as np
import time
from Leapmotionsensor import SampleListener
import Leap
import sys
import threading
from wlkata_mirobot import WlkataMirobot
from enum import Enum

from robolink import *  # API to communicate with RoboDK
from robodk import *  # basic matrix operations


class DemoRobot:
    def __init__(self, robot_available=False, simulator_available=True):

        # Demo is based on this sensor value
        self.senor_output = {
            "detected": False,
            "x": 0,
            "y": 0,
            "z": 0,
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "grip": False,
        }

        self.robot_available = robot_available
        self.simulator_available = simulator_available

        # Listening to Sensor
        self.listener = SampleListener()
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)
        self.controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
        thread = threading.Thread(target=self.estimate_hand_gesture, args=())
        thread.daemon = True
        thread.start()

        if simulator_available is True:
            self.thread_simulation = threading.Thread(
                target=self.control_simulation, args=()
            )
            self.thread_simulation.daemon = True
            RL = Robolink()
            self.robot_simulation = RL.Item("robot-wlkata")
            self.robot_simulation.setTool(RL.Item("servo-gripper"))
            self.robot_simulation.setFrame(RL.Item("base-frame"))
            self.robot_simulation.setRounding(10)
            RL.setSimulationSpeed(100)
            self.thread_simulation.start()

        if self.robot_available is True:
            self.freemove = True
            self.arm = WlkataMirobot(portname="COM5")
            self.arm.set_speed(3000)

            self.arm.home(has_slider=False)
            time.sleep(4)

            # Set Gripper Spacing
            spacing_mm = 20.0
            self.arm.set_gripper_spacing(spacing_mm)
            self.arm.gripper_open()
            time.sleep(0.01)

            self.cube_midle = {"x": 208, "y": 0, "z": 100, "a": 0, "b": 0, "c": -5}
            self.cube_left = {"x": 212, "y": 110, "z": 100, "a": 0, "b": 0, "c": -13}
            self.cube_right = {"x": 189, "y": -63, "z": 100, "a": 0, "b": 0, "c": -26}

    def control_simulation(self):
        while True:
            try:
                if self.senor_output["detected"]:
                    self.robot_simulation.MoveL(
                        xyzrpw_2_pose(
                            [
                                self.senor_output["x"],
                                self.senor_output["y"],
                                self.senor_output["z"] + 30,
                                -180.000000 + self.senor_output["pitch"],
                                self.senor_output["roll"],
                                180.000000 - 1 * self.senor_output["yaw"],
                            ]
                        )
                    )
                    time.sleep(0.01)
            except:
                self.robot_simulation.MoveJ([0, 0, 0, 0, 0, 0])

    def estimate_hand_gesture(self):
        while True:
            self.senor_output = self.listener.on_frame(self.controller)
            time.sleep(0.01)

    def run(self):
        try:
            while True:
                print(self.senor_output)
                if self.robot_available is True:
                    if self.senor_output["detected"]:

                        if self.senor_output["grip"]:
                            self.released = False
                            chosen_cube = {}

                            if abs(self.senor_output["y"]) < 30:
                                chosen_cube = self.cube_midle
                            elif (self.senor_output["y"]) < -31:
                                chosen_cube = self.cube_right
                            else:
                                chosen_cube = self.cube_left

                            self.arm.set_tool_pose(
                                chosen_cube["x"],
                                chosen_cube["y"],
                                chosen_cube["z"],
                                roll=chosen_cube["a"],
                                pitch=chosen_cube["b"],
                                yaw=chosen_cube["c"],
                                is_relative=False,
                                speed=3000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.001)
                            proceed = 75

                            self.arm.set_tool_pose(
                                z=-proceed,
                                is_relative=True,
                                speed=1000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)
                            self.arm.gripper_close()
                            time.sleep(0.1)
                            self.arm.set_tool_pose(
                                z=proceed,
                                is_relative=True,
                                speed=1000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)
                            self.arm.set_tool_pose(
                                roll=70,
                                is_relative=True,
                                speed=3000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)
                            self.arm.set_tool_pose(
                                roll=-70,
                                is_relative=True,
                                speed=3000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)
                            self.arm.set_tool_pose(
                                z=-proceed,
                                is_relative=True,
                                speed=1000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)
                            self.arm.gripper_open()
                            time.sleep(0.1)

                            self.arm.set_tool_pose(
                                z=proceed,
                                is_relative=True,
                                speed=1000,
                                mode="linear",
                                wait_ok=True,
                            )
                            time.sleep(0.1)

                            self.arm.set_tool_pose(
                                x=202,
                                y=0,
                                z=181,
                                roll=0,
                                pitch=0,
                                yaw=0,
                                is_relative=False,
                            )
                            time.sleep(0.01)
                            self.released = True

                        else:
                            self.released = True

                        #     self.arm.gripper_open()

                        if self.released is True:
                            self.arm.set_tool_pose(
                                self.senor_output["x"],
                                self.senor_output["y"],
                                self.senor_output["z"],
                                roll=-self.senor_output["pitch"],
                                pitch=-self.senor_output["roll"],
                                yaw=-1 * self.senor_output["yaw"],
                                is_relative=False,
                                speed=3000,
                                mode="p2p",
                                wait_ok=True,
                            )
                            time.sleep(0.001)
                    else:
                        pass
        except KeyboardInterrupt:
            self.controller.remove_listener(self.listener)


def main():
    demo = DemoRobot()
    demo.run()


if __name__ == "__main__":
    main()
