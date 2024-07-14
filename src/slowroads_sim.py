from slowroads_utils import open_browser, grab_screenshot, set_cruise_speed, autodrive_on, autodrive_off
import matplotlib.pyplot as plt
from slowroads_utils import steer_left, steer_right

class SlowRoadsSimulator:
    def __init__(self):
        self.init_plot()

    def init_plot(self):
        plt.ion()  # Turn on interactive mode
        _, self.ax = plt.subplots()
        self.display = None
        self.text_obj = None

    def update_plot(self, image = None, stats_dict = None):

        if not image is None:
            self.plot_image(image)

        if not stats_dict is None:
            self.plot_stats(stats_dict)

        plt.draw()
        plt.pause(0.01)  # Adjust pause time as needed
    
    def plot_image(self, image):
        """Update the image displayed on the Axes."""
        if self.display is None:
            # Create the display object if it doesn't exist
            self.display = self.ax.imshow(image)
        else:
            # Update the display object with the new image
            self.display.set_data(image)

    def plot_stats(self, stats_dict):
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
        # Open SlowRoads in Chrome Browser
        self.driver = open_browser(local_storage_path, size)

    def set_speed(self, speed):
        set_cruise_speed(self.driver, speed)

    def steer_left(self, t_down, t_up):
        steer_left(self.driver, t_down, t_up)

    def steer_right(self, t_down, t_up):
        steer_right(self.driver, t_down, t_up)

    def grab_screenshot(self):
        return grab_screenshot(self.driver)

    def autodrive_on(self):
        autodrive_on(self.driver)
    
    def autodrive_off(self):
        autodrive_off(self.driver)

    def run(self):

        """Main loop to capture images and update commands."""
        try:
            while True:
                image = self.grab_screenshot()

        except KeyboardInterrupt:
            print("Operation terminated: Request received from user.")
        finally:
            print("Initiating closure sequence for the plot...")
            plt.close('all')  # This ensures that all figures are closed properly.
            print("Plot closure completed.")

            print("Shutting down the driver...")
            self.driver.quit()
            print("Driver shutdown complete. All resources have been cleaned up successfully.")

