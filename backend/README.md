## MIA Dashboard backend
Dashboard backend to receive notifications and debug videos and send to frontend.

## Setup
1. Create virtualenv `$ virtualenv --system-site-packages -p python3 venv`
2. Activate virtualenv `$ source venv/bin/activate`
3. Install requirements `$ pip install -r requirements.txt`
4. Set the variables `BROKER_ADDRESS` and `MONITOR_ADDRESS` (`main.py`)

## Run
```
./bootstrap.sh
```

## Backend Useful url
- List received events
```
<MONITOR_ADDRESS>:5000/
```
- Send a test event
```
<MONITOR_ADDRESS>:5000/send-event
```
- Debug video received
```
<MONITOR_ADDRESS>:5000/video-debug
```