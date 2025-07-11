# Data Collection Program
This module includes the program used in collecting participants' data in both the tracking and planning tasks.

## Installation

Currently, this works on Windows. To get it working on Linux, file paths will need to be handled.

### Prerequisites

Before you begin, ensure you have installed python. This code was generated with python 3.9.2 so we recommend using it.

### Installing Dependencies 

Install the project dependencies using pip (It is highly recommended to use a virtual environment to manage dependencies):

```
pip install -r requirements.txt
```

## Resources

Download the folder `Resources` from https://drive.google.com/drive/folders/1G3pT8fv4KmhhZXY0tgO4xr44FaRe3rNS?usp=sharing and add it under the CM-ExperimentTools folder.

## Login Cookies

To log in to the ground control system in Task 2, username and password are required, which are not publicly available as it is proprietary software owned by Windracers Limited. 
<!-- To automatically login to https://cloud.distributed-avionics.com/, create a file named `cookie` inside `Resources` folder. Get the value of the cookie `.DA-CC-Identity` from a logged in session from your browser and paste it into the file `cookie`. -->

## Usage

To run the code
```
python main.py
```

## PyQT Workaround
If running program on campus and you receive an error message regarding the web server, run:
```
QTWEBENGINE_DISABLE_SANDBOX=1
```
before initiating main.py
