import os
import time
from slowroads_sim import SlowRoadsSimulator as BaseSlowRoadsSimulator
from lane_detection_utils import preprocess_image, find_driving_path
import matplotlib.pyplot as plt
import numpy as np
from slowroads_utils import steer_left, steer_right
import cv2 as cv

class SlowRoadsSimulator(BaseSlowRoadsSimulator):
    def __init__(self):
        super().__init__()  # Initialize the base class   

    def publish_control_commands(self, offset, threshold = 20, kp = 5e-3, tmax = 0.3):

        if abs(offset) < threshold:
            return
        
        t = min(abs(offset) * kp, tmax)

        if offset > 0:
            self.steer_right(t, 0.05)
            print(f"{offset=}, {t=}, steer_right")
        elif offset < 0:
            self.steer_left(t, 0.05)
            print(f"{offset=}, {t=}, steer_left")


    def run(self):
        self.autodrive_off()

        """Main loop to capture images and update commands."""
        try:
            while not self.exit_event.is_set():
                image = self.grab_screenshot()
                mask, resized_image = preprocess_image(image)
                success, result, offset, total_pixels = find_driving_path(resized_image, mask)
                stats_dict = {'offset': offset, 'total_pixels': total_pixels}
                if success:
                    self.update_plot(result, stats_dict)
                    self.publish_control_commands(offset)
                else:
                    pass

        finally:
            self.__clear__()


if __name__ == "__main__":

    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(src_dir)

    local_storage_file = os.path.join(project_dir, 'config', 'slowroads_storage.json')
    window_size = (480, 480)


    sim = SlowRoadsSimulator()

    # Load local storage
    sim.open_brwoser(local_storage_file, window_size)

    sim.run()

    # sim.set_speed(10)
    # time.sleep(5)
    # sim.set_speed(20)
    # time.sleep(5)
    # sim.autodrive_on()
    # time.sleep(5)
    # sim.autodrive_off()
    # time.sleep(5)
    # sim.autodrive_on()
    # time.sleep(5)

    # for _ in range(5):
    #     sim.steer_left(0.5, 0.5)
    #     sim.steer_right(0.5, 0.5)

    # sim.rest_vehicle()





