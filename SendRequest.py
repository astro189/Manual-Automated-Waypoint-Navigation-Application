import requests
import time

# Change this to your NodeMCU's IP address
nodeMCU_ip = "192.168.4.1"

# Define the commands to control the robot
commands = {
    "F": "Forward",
    "B": "Backward",
    "L": "Left",
    "R": "Right",
    "I": "AheadRight",
    "G": "AheadLeft",
    "J": "BackRight",
    "H": "BackLeft",
    "0": "Speed 200",
    "1": "Speed 470",
    "2": "Speed 540",
    "3": "Speed 610",
    "4": "Speed 680",
    "5": "Speed 750",
    "6": "Speed 820",
    "7": "Speed 890",
    "8": "Speed 960",
    "9": "Speed 1023",
    "S": "Stop"
}


def sendRequest(command,t):
    requests.get(f"http://{nodeMCU_ip}/?State={'0'}")
    requests.get(f"http://{nodeMCU_ip}/?State={command}")
    time.sleep(t)
    requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
    time.sleep(0.3)
    return True