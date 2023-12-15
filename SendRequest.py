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

# while True:
#     # Get user input for the command
#     user_input = input("Enter a command (F/B/L/R/I/G/J/H/0-9/S to control, Q to quit): ").strip()
    
#     if user_input.upper() == 'Q':
#         break
#     print(user_input)
#     if user_input in commands:
#         # Send the command as an HTTP GET request to your NodeMCU
#         response = requests.get(f"http://{nodeMCU_ip}/?State={user_input}")
        
#         # Print the command and the NodeMCU's response
#         print(f"Sent command: {commands[user_input]}")
#         print(f"NodeMCU response: {response.text}")
#     else:
#         print("Invalid command. Please enter a valid command.")

def sendRequest(command,t):
    # response = requests.get(f"http://{nodeMCU_ip}/?State={'0'}")
    response = requests.get(f"http://{nodeMCU_ip}/?State={command}")
    time.sleep(t)
    response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
    time.sleep(0.3)
    return True


# response = requests.get(f"http://{nodeMCU_ip}/?State={'0'}")

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.3)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'R'}")
# time.sleep(0.35)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.4)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'L'}")
# time.sleep(0.29)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.5)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'L'}")
# time.sleep(0.29)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.25)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.3)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
# time.sleep(0.2)

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.25)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")

# response = requests.get(f"http://{nodeMCU_ip}/?State={'R'}")
# time.sleep(0.25)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")

# response = requests.get(f"http://{nodeMCU_ip}/?State={'F'}")
# time.sleep(0.25)
# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")

# response = requests.get(f"http://{nodeMCU_ip}/?State={'S'}")
        
        # Print the command and the NodeMCU's response
# print(f"Sent command: {commands['F']}")
# print(f"NodeMCU response: {response.text}")