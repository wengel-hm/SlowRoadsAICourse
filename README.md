# SlowRoadsAICourse
Master autonomous driving in the SlowRoads game using Python &amp; Selenium. Start with OpenCV for lane detection, then advance to deep learning with YOLO for traffic sign detection and lane segmentation

Here's a streamlined Markdown guide for setting up a Python virtual environment using the built-in `venv` module, suitable for your GitHub project documentation:

## Prerequisites

Before starting work on the project, ensure you have the following tools installed and accounts set up. This checklist will guide you through each step:

- [ ] **Install Git**
  - **Description**: Git is a version control system that lets you manage and keep track of your source code history.
  - **Installation**: Download and install Git from [Git's official site](https://git-scm.com/downloads).

- [ ] **Install Google Chrome Browser**
  - **Description**: Google Chrome is required for optimal compatibility with several web-based tools and extensions.
  - **Installation**: Download and install Chrome from [Google Chrome's official site](https://www.google.com/chrome/).

- [ ] **Install Visual Studio Code (VSCode)**
  - **Description**: VSCode is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS, and Linux.
  - **Installation**: Download and install VSCode from [Visual Studio Code's official site](https://code.visualstudio.com/Download).

- [ ] **Create a Google Account**
  - **Description**: A Google account will allow you to access Google Colab, a free cloud service that supports Python scripting and machine learning libraries.
  - **Setup**: Sign up for a Google account at [Google's account creation page](https://accounts.google.com/signup).

Ensure all these components are installed and set up properly to facilitate a smooth setup and operation of your project workspace.


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

