# SlowRoadsAICourse
Master autonomous driving in the SlowRoads game using Python &amp; Selenium. Start with OpenCV for lane detection, then advance to deep learning with YOLO for traffic sign detection and lane segmentation

Here's a streamlined Markdown guide for setting up a Python virtual environment using the built-in `venv` module, suitable for your GitHub project documentation:

## Set Up Your Workspace

### Creating and Activating a Virtual Environment

To isolate the dependencies of this project from your global Python environment, create a virtual environment using Python's built-in `venv` module:

```bash
# Create a virtual environment named 'env' in your project directory
python -m venv env
```

To activate the virtual environment, use the following commands based on your operating system:

#### On Windows:
```bash
env\Scripts\activate
```

#### On macOS and Linux:
```bash
source env/bin/activate
```

### Installing Required Packages

With the virtual environment activated, install the required Python packages for this project:

```bash
pip install selenium opencv-python numpy matplotlib pynput
```

