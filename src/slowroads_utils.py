from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import cv2 as cv
import numpy as np
import time
from pynput.keyboard import Key, Listener
from selenium.webdriver.common.by import By
from datetime import datetime
import os
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from PIL import Image
import io

# Free Keys
# G,J,L,N,O,X,Y

# "config-scene-name": "Hills", "Planet"
# "config-scene-topography": "straight", "casual", "easy", "normal", "hard"
# "config-scene-skin": "default", "venus", "moon"
# "config-scene-skin": "default", "autumn", "spring", "winter"
# "config-scene-weather-index": "0", "1", "2", "3", "4" → "sunrise", "sun", "cloudy", "sunset", "night"
# "speed-control_speed": "2.2352", "4.4704", "6.7056", "8.9408"


def track_time(func):
    """Decorator to track the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

   
def open_browser(local_storage_path = None, size = (640, 360)):
    
    # Setup Selenium to open Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(*size)
    driver.get('https://slowroads.io/')
    
    # IDs for the elements
    start_button_id = "splash-loader"
    click_element(driver, start_button_id)
    
    if not local_storage_path is None:
        time.sleep(3)
        load_local_storage(driver, local_storage_path)
        time.sleep(10)
           
    return driver


class KeyListener:
    def __init__(self):
        self.key_actions = {}  # Dictionary to store key-specific functions
        self.listener = None   # Listener object, initially None
        self.is_listening = False  # Flag to track if the listener has started

    def add_key_action(self, key, action):
        """Adds a custom action for a specific key.
        
        Args:
            key: The key for which the action should be executed.
            action: The function to be executed when the key is pressed.
        """
        self.key_actions[key] = action
        # Start listening when the first key action is added
        if not self.is_listening:
            self.start_listening()

    def on_press(self, key):
        try:
            # Check if the pressed key has a registered action
            if hasattr(key, 'char') and key.char in self.key_actions:
                self.key_actions[key.char]()  # Call action
        except AttributeError:
            pass

    def on_release(self, key):
        pass
        
    def start_listening(self):
        if not self.is_listening:
            self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            self.is_listening = True  # Set flag to True as the listener has started

    def stop_listening(self):
        if self.listener is not None:
            self.listener.stop()
            self.is_listening = False  # Reset flag as the listener has stopped

        
def load_local_storage(driver, path):
    try:
        with open(path, 'r') as file:
            local_storage = file.read()
            driver.execute_script(f"window.localStorage.clear();")
            driver.execute_script(f"var items = JSON.parse(arguments[0]); for (var key in items) {{ window.localStorage.setItem(key, items[key]); }}", local_storage)
            driver.refresh()  # Refresh the page to apply loaded local storage data
            print("Storage loaded.")
    except Exception as e:  # Catching the base Exception class
        print(f"An error occurred: {e}")

def click_element(driver, id_name):
    try:
        element = driver.find_element(By.ID, id_name)
        element.click()
        print(f"Clicked on element with ID: {id_name}")
    except Exception as e:
        print(f"Error: {e}")

def open_safari():

    # Setup Selenium to open Safari
    driver = webdriver.Safari()
    
    # Navigate to a URL
    driver.get('https://slowroads.io/')

    return driver


def save_screenshot(driver, directory):

    # Check if directory is specified and is not None
    if not directory:
        raise ValueError("A directory must be specified to save the screenshot.")
    
    now = datetime.now()
    filename = now.strftime("image_%Y%m%d%H%M%S.png")
    filepath = os.path.join(directory, filename)
    
    driver.save_screenshot(filepath)
    print(f"Saved screenshot at {filepath}")

@track_time            
def grab_screenshot(driver):
    try:
        screenshot = driver.get_screenshot_as_png()
        nparr = np.frombuffer(screenshot, np.uint8)
        image = cv.imdecode(nparr, cv.IMREAD_COLOR)
        return True, image
    except WebDriverException as e:
        print(f"WebDriverException occurred in control thread: {e}")
        # Return None or a default image to handle the exception gracefully
    except Exception as e:
        print(f"An unexpected error occurred in control thread: {e}")
        # Return None or a default image to handle the exception gracefully
    return False, None

@track_time     
def steer_left(driver, t_down = 0.2, t_up = 0.1):
    
    try:
        action = ActionChains(driver)

        # Press and hold the left key
        action.key_down(Keys.ARROW_LEFT).pause(t_down)
        action.key_up(Keys.ARROW_LEFT).pause(t_up)
        
        action.perform()

    except WebDriverException as e:
        print(f"WebDriverException occurred in control thread: {e}")
        # Handle WebDriver-related errors
    except Exception as e:
        print(f"An unexpected error occurred in control thread: {e}")
        # Handle other unexpected exceptions

@track_time
def steer_right(driver, t_down = 0.2, t_up = 0.1):
    
    try:
        action = ActionChains(driver)

        # Press and hold the right key
        action.key_down(Keys.ARROW_RIGHT).pause(t_down)
        action.key_up(Keys.ARROW_RIGHT).pause(t_up)
        
        action.perform()
    except WebDriverException as e:
        print(f"WebDriverException occurred in control thread: {e}")
        # Handle WebDriver-related errors
    except Exception as e:
        print(f"An unexpected error occurred in control thread: {e}")
        # Handle other unexpected exceptions

def set_value(driver, id_name, value):
    # Execute the script
    script = f"document.getElementById('{id_name}').innerHTML = {value};"
    driver.execute_script(script)

def get_value(driver, id_name):
    # Execute the script
    script = f"return document.getElementById('{id_name}').innerHTML;"
    value = driver.execute_script(script)
    return value


def set_cruise_speed(driver, target_speed, value_id=None, xpath_up=None, xpath_down=None):
    """
    Adjusts the cruise control speed of a vehicle in a web-based interface to a specified target speed.
    
    Parameters:
    - driver (WebDriver): The Selenium WebDriver object used to interact with the web page.
    - target_speed (int): The desired cruise control speed. Must be a multiple of 5.
    - value_id (str, optional): The HTML element ID that displays the current cruise speed. 
      Defaults to 'ui-cruise-value' if not provided.
    - xpath_up (str, optional): The XPath to the button that increases the cruise speed. 
      Defaults to '//*[@id="ui-cruise-select"]/div[3]' if not provided.
    - xpath_down (str, optional): The XPath to the button that decreases the cruise speed. 
      Defaults to '//*[@id="ui-cruise-select"]/div[1]' if not provided.

    Returns:
    None: The function modifies the cruise speed on the web interface directly and has no return value.

    Notes:
    The function will early return without any action if the target_speed is not a multiple of 5, as the
    cruise control can only be adjusted in increments of 5 units.
    """
    
    # Check if the target speed is a valid increment (must be a multiple of 5)
    if target_speed % 5 != 0:
        return

    # Assign default values if not provided
    cruise_value_id = value_id or 'ui-cruise-value'
    xpath_down = xpath_down or '//*[@id="ui-cruise-select"]/div[3]'
    xpath_up = xpath_up or '//*[@id="ui-cruise-select"]/div[1]' 

    # Retrieve the current speed from the web interface
    current_speed = int(get_value(driver, cruise_value_id))

    # Determine the direction of adjustment needed and select the appropriate control element
    if current_speed > target_speed:
        element = driver.find_element(By.XPATH, xpath_down)
        # Click the down button until the target speed is reached
        for _ in range((current_speed - target_speed) // 5):
            element.click()

    
    elif current_speed < target_speed:
        element = driver.find_element(By.XPATH, xpath_up)
        # Click the up button until the target speed is reached
        for _ in range((target_speed - current_speed) // 5):
            element.click()

def is_autodrive_active(driver):
    try:
        autodrive_div = driver.find_element(By.ID, 'autodrive')
        return 'autodrive-active' in autodrive_div.get_attribute('class')
    except Exception as e:
        print(f"Error checking autodrive status: {e}")
        return False

def autodrive_on(driver, autodrive_btn_id = 'autodrive-button'):
    if is_autodrive_active(driver):
        return

    click_element(driver, autodrive_btn_id)

def autodrive_off(driver, autodrive_btn_id = 'autodrive-button'):
    if is_autodrive_active(driver):
        click_element(driver, autodrive_btn_id)
        