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

    def run(self):

        """Main loop to capture images and update commands."""
        try:
            while not self.exit_event.is_set():
                image = self.grab_screenshot()
                mask, resized_image = preprocess_image(image)
                success, result, offset = find_driving_path(resized_image, mask)
                if success:
                    self.update_plot(result)
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





