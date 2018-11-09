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
5. Set the variables `BACKEND_ADDRESS`, `PORT`, `OBJECT_DETECTION_ADDRESS`, `OBJECT_DETECTION_PORT` (`main.py`)

## Run
```
./bootstrap.sh
```

## Backend useful urls
- List received events and available cameras.
```
<BACKEND_ADDRESS>:<PORT>/
```
- Send a test event
```
<MONITOR_ADDRESS>:<PORT>/send-test-event
```
- Monitor video received
```
<MONITOR_ADDRESS>:<PORT>/monitor-video
```