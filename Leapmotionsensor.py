import Leap
import sys


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        self.results = {
            "detected": False,
            "x": 0,
            "y": 0,
            "z": 0,
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "grip": False,
        }
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):

        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)
        if numHands == 1:
            # Get the first hand
            hand = hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            numFingers = len(fingers)
            if numFingers >= 1:
                # Calculate the hand's average finger tip position
                pos = Leap.Vector()
                for finger in fingers:
                    pos += finger.tip_position

                pos = pos.__div__(numFingers)
            # Get the palm position
            palm = hand.palm_position

            normal = hand.palm_normal
            direction = hand.direction

            roll = direction.pitch * Leap.RAD_TO_DEG
            pitch = normal.roll * Leap.RAD_TO_DEG
            yaw = direction.yaw * Leap.RAD_TO_DEG
            grip = False
            if hand.grab_strength == 1:
                grip = True

            x = round(palm[0], 2)
            y = round(palm[1], 2)
            z = round(palm[2], 2)

            if y < 80:
                y = 80
            elif y > 200.0:
                y = 200.0

            if z > 140:
                z = 140
            elif z < -140:
                z = -140

            if x > 150:
                x = 150
            elif x < -150:
                x = -150

            if roll > 20:
                roll = 20
            elif roll < -20:
                roll = -20
            z_transformed = (((y - 80) / (200.0 - 80)) * (200 - 40)) + 40
            x_transformed = (((-1 * z + 140) / (140 + 140)) * (270 - 150)) + 150
            y_transformed = (((-1 * x + 150) / (150 + 150)) * (150 + 150)) - 150
            self.results = {
                "detected": True,
                "x": round(x_transformed, 3),
                "y": round(y_transformed, 3),
                "z": round(z_transformed, 3),
                "roll": round(roll, 2),
                "pitch": round(pitch, 2),
                "yaw": round(yaw, 2),
                "grip": grip,
            }
            return self.results
        else:
            self.results = {
                "detected": False,
                "x": 0,
                "y": 0,
                "z": 0,
                "roll": 0,
                "pitch": 0,
                "yaw": 0,
                "grip": False,
            }
            return self.results
