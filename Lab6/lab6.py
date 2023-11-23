import time

class SlidingDoorsAutomaton:
    def __init__(self):
        self.state = "DoorsClosed"
        self.timestamp = time.time()

    def transition(self, event):
        current_time = time.time()
        time_elapsed = current_time - self.timestamp

        if self.state == "DoorsClosed":
            if event == "MotionDetected":
                print("Motor rolling to open...")
                time.sleep(1)  # Simulate motor rolling time
                self.state = "MotorRollingToOpen"
                self.timestamp = current_time
        elif self.state == "MotorRollingToOpen":
            if event == "DoorsOpened" and time_elapsed >= 1:
                print("Doors are open.")
                self.state = "DoorsOpen"
                self.timestamp = current_time
        elif self.state == "DoorsOpen":
            if event == "MotionDetected":
                print("Motor rolling to close...")
                time.sleep(1)  # Simulate motor rolling time
                self.state = "MotorRollingToClose"
                self.timestamp = current_time
        elif self.state == "MotorRollingToClose":
            if event == "DoorsClosed" and time_elapsed >= 1:
                print("Doors are closed.")
                self.state = "DoorsClosed"
                self.timestamp = current_time

# Example simulation
automaton = SlidingDoorsAutomaton()

automaton.transition("MotionDetected")
automaton.transition("DoorsOpened")
automaton.transition("MotionDetected")
automaton.transition("DoorsClosed")