## MIA Dashboard backend
Dashboard backend to receive notifications and debug videos and send to frontend.

## Requirements
1. Python3
2. Virtualenv

## Setup
1. Install OpenCV library `$ sudo apt-get install libopencv-dev python-opencv`
2. Create virtualenv `$ virtualenv --system-site-packages -p python3 venv`
3. Activate virtualenv `$ source venv/bin/activate`
4. Install requirements `$ pip install -r requirements.txt`
5. Set the variables `BROKER_ADDRESS` and `MONITOR_ADDRESS` (`main.py`)

## Run
```
./bootstrap.sh
```

## Backend useful urls
- List received events
```
<MONITOR_ADDRESS>:5000/
```
- Send a test event
```
<MONITOR_ADDRESS>:5000/send-test-event
```
- Debug video received
```
<MONITOR_ADDRESS>:5000/monitor-video
```