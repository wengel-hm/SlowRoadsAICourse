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

    def publish_control_commands(self, offset, threshold = 20, kp = 4e-3, tmax = 0.3):
        
        # If the offset is within the threshold, no steering adjustment is needed
        if abs(offset) < threshold:
            return
        
        t_down = min(abs(offset) * kp, tmax)
        t_up = 0.05

        if offset > 0:
            self.steer_right(t_down, t_up) # Steer right if offset is positive
        elif offset < 0:
            self.steer_left(t_down, t_up) # Steer left if offset is negative


    def run(self):
        self.autodrive_off()  # Turn off autodrive

        # Set up a success list to keep track of successful path findings.
        # If there are N consecutive failures, turn autodrive back on.
        N = 3
        success_list = [True] * N

        try:
            while not self.exit_event.is_set():
                time.sleep(1)
                continue
                success, image = self.grab_screenshot()

                if not success:  # If screenshot is not successful, skip to the next iteration
                    continue

                mask, resized_image = preprocess_image(image)
                success, offset, overlay, stats = find_driving_path(resized_image, mask, min_pixels = 60)
                success_list.append(success)

                # Extract relevant statistics for plotting
                stats_dict = {k: stats[k] for k in ['offset', 'lane_center']}

                if success:
                    self.update_plot(overlay, stats_dict)
                    self.publish_control_commands(offset)
                elif not True in success_list[-N:]: # If there are N consecutive failures
                    self.rest_vehicle() # Rest the vehicle as a fallback mechanism


        finally:
            self.__clear__()


if __name__ == "__main__":

    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(src_dir)
    data_dir = os.path.join(project_dir, 'data')

    local_storage_file = os.path.join(project_dir, 'config', 'slowroads_storage.json')
    window_size = (480, 480)


    sim = SlowRoadsSimulator()

    season_list = ["summer", "autumn", "spring", "winter"]
    weather_list = ["sunrise", "sun", "cloudy", "sunset", "night"]

    season = "summer"
    weather = "sunrise"

    prefix = f"{season}_{weather}"
    sim.add_key_action('g', lambda: sim.save_screenshot(data_dir, prefix))

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


    #sim.setup_scene(local_storage_file, season="spring", topography="straight", weather="night")



