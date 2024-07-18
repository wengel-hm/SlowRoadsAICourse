from slowroads_utils import update_config_file, open_browser, grab_screenshot, set_cruise_speed, autodrive_on, autodrive_off, save_screenshot, KeyListener
import matplotlib.pyplot as plt
from slowroads_utils import steer_left, steer_right
import time
import threading
import signal

# sim.init_control_thread()
# sim.pause_control_thread()
# sim.run_control_thread()

class SlowRoadsSimulator:
    def __init__(self):

        self.plot_initialized = False
        self.control_initialized = False
        self.key_listener_initialized = False
        self.driver_initialized = False

        # Thread event to signal exit
        self.exit_event = threading.Event()
        # Thread event to run the controller
        self.run_event = threading.Event()

        # Set up signal handling for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle SIGINT to set exit event."""
        self.exit_event.set()

    def __clear__(self):

            if self.control_initialized:
                print("Initiating shutdown of the control thread...")
                self.exit_event.set()  # Signal the control thread to exit
                self.control_thread.join()  # Wait for the control thread to exit
                print("Control thread shutdown successfully completed.")

            if self.plot_initialized:
                print("Initiating closure sequence for the plot...")
                plt.close('all')  # This ensures that all figures are closed properly.
                print("Plot closure completed.")

            if self.key_listener_initialized:
                print("Initiating shutdown of the KeyListener.")
                self.key_listener.stop_listening()
                print("KeyListener shutdown successfully completed.")

            if self.driver_initialized:
                print("Shutting down the driver...")
                self.driver.quit()
                print("Driver shutdown complete. All resources have been cleaned up successfully.")

    def init_control_thread(self):
        self.run_event.clear()  # Start in an paused state
        # Background thread to send commands periodically
        self.control_thread = threading.Thread(target=self._publish_commands)
        self.control_thread.daemon = True
        self.control_thread.start()
        self.control_initialized = True

    def run_control_thread(self):
        self.run_event.set() # Running state

    def pause_control_thread(self):
        self.run_event.clear() # Paused state

    def is_paused(self):
        return self.run_event.is_set()
    
    def _publish_commands(self):

        """Thread function to send commands at fixed intervals."""
        while not self.exit_event.is_set():
            
            if not self.run_event.is_set(): # Wait until run_event is set
                time.sleep(1)
            else:
                self.publish_commands()

    def publish_commands(self):
        print("Publishing Control commands")
        time.sleep(0.5)

    def update_plot(self, image = None, stats_dict = None):

        if not self.plot_initialized:
            self._init_plot()

        if not image is None:
            self._plot_image(image)

        if not stats_dict is None:
            self._plot_stats(stats_dict)

        plt.draw()
        plt.pause(0.01)  # Adjust pause time as needed

    def _init_plot(self):
        plt.ion()  # Turn on interactive mode
        _, self.ax = plt.subplots()
        self.display = None
        self.text_obj = None
        self.plot_initialized = True

    def _plot_image(self, image):
        """Update the image displayed on the Axes."""
        if self.display is None:
            # Create the display object if it doesn't exist
            self.display = self.ax.imshow(image)
        else:
            # Update the display object with the new image
            self.display.set_data(image)

    def _plot_stats(self, stats_dict):
        """Plot statistics on the image like a legend, using a dictionary of values."""
        # Generate the statistics text from the dictionary
        stats_text = "\n".join(f"{key}: {value}" for key, value in stats_dict.items())

        if self.text_obj is None:
            # Create the text object if it doesn't exist
            self.text_obj = self.ax.text(
                0.02, 0.95, stats_text, transform=self.ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
        else:
            # Update the text object content
            self.text_obj.set_text(stats_text)

        
    def open_brwoser(self, local_storage_path = None, size = (640, 360)):
        if not self.driver_initialized:
            # Open SlowRoads in Chrome Browser
            self.driver = open_browser(local_storage_path, size)
            self.driver_initialized = True

    def set_speed(self, speed):
        set_cruise_speed(self.driver, speed)

    def steer_left(self, t_down, t_up):
        steer_left(self.driver, t_down, t_up)

    def steer_right(self, t_down, t_up):
        steer_right(self.driver, t_down, t_up)

    def grab_screenshot(self):
        return grab_screenshot(self.driver)

    def save_screenshot(self, directory = None, prefix = None):
        save_screenshot(self.driver, directory, prefix)

    def autodrive_on(self):
        autodrive_on(self.driver)
    
    def autodrive_off(self):
        autodrive_off(self.driver)

    def rest_vehicle(self, t = 2):
        self.autodrive_on()
        time.sleep(t)
        self.autodrive_off()
        
    def add_key_action(self, key, func):
        # Unassigned keys: G,J,L,N,O,X,Y

        if not self.key_listener_initialized:
            self.key_listener = KeyListener()
            self.key_listener_initialized = True

        self.key_listener.add_key_action(key, func)

    def setup_scene(self, file_path, topography="normal", season="summer", weather="sun"):
        update_config_file(file_path, topography, season, weather)

    def run(self):

        """Main loop to capture images and update commands."""
        try:
            while not self.exit_event.is_set():
                time.sleep(0.1)
                # image = self.grab_screenshot()
        finally:
            self.__clear__()

