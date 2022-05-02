# aqmConfigurator
## Configurator and Builder for the AQM project
---
## Requirements:
- Python3
- pip
- PlatformIO Core
---
## Installation:
### 1. Download the latest [Python installer](https://www.python.org/downloads/)
   1. Open the installer file
   2. __Make sure you check the "Add Python 3.x to PATH" box__
   3. Press the "Install Now" Button (administrator privileges required)
   4. Allow changes through python
   5. Press the "Disable Path length limit" Button
   6. Close the Installer
   7. __Python is now installed. To make sure everything works properly, please reboot your system.__
### 2. Download the latest version aqmConfigurator
   1. Go to the [latest release](https://github.com/felixslama/aqmConfigurator/releases/latest) and press Sourcecode (zip)
   2. After the download is finished, extract the zip-archive to your desktop
### 3. Install the required packages using pip
   1. Open a new powershell or terminal window. (on windows type "powershell" in search)
   2. Navigate to the extracted folder using the "cd" command.
   3. Once you are in the correct directory run ```pip install -r requirements.txt```

## Usage:
### 1. Using the Configurator
   1. If you already closed the powershell window from the installation process, open a new one and navigate to the aqmConfigurator folder
   2. Once you are in the folder, run ``` python aqmConf.py``` this should bring up a small window looking like the screenshot below
      ![image](https://user-images.githubusercontent.com/79058712/164645347-f467bc17-8681-4dae-a66c-7934d30538e6.png)
   3. Connect your ESP32 to your machine using the micro-usb cable.
   4. Once you have the ESP32 connected, press the "Build" button. The application might seem frozen. The first flash can take up to 2 minutes.

## ToDo:
- write detailed install/usage guide
- add screenshots to every step
