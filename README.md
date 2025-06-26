```txt
   ___  _ _____         _____          __           __
  / _ \(_) ___/__ _____/ ___/__  ___  / /________  / /
 / ___/ / /__/ _ `/ __/ /__/ _ \/ _ \/ __/ __/ _ \/ / 
/_/  /_/\___/\_,_/_/  \___/\___/_//_/\__/_/  \___/_/  
```
# What the project does:
It controls a Raspberry Pi 5-powered car using servo motors, infrared and ultrasonic sensors. The collected data is visually displayed in a dashboard made with [Dash](https://dash.plotly.com/).

## Features
- Web interface using Dash
- Logging of vehicle data (JSON)
- Configurable vehicle offsets
- Data visualization
- Multiple driving modes using ultrasonic and infrared sensors

## How to use it:
### PiCarControl Installation Guide
> [!NOTE]
> Requirements you need to run the project smoothly.

- Raspberry Pi / Raspberry Pi OS
- Python 3.7.3
- Git & pip must be installed

__Clone the project__
```
git clone git@github.com:myzra/PiCarControl.git  
cd PiCarControl
```
__Install dependencies__ \
_Its recommended to use a virtual enviroment_
```
python3 -m venv venv
source venv/bin/activate
```
_Then install all required packages_
```
pip install -- upgrade pip
pip install -r requirements.txt
```
__Start the project__
```
python3 dashboard/app.py
```
### Open in your browser:
`http://0.0.0.0:4200`
