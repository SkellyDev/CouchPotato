

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import sys
import time
import json
import random
from tqdm import tqdm
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from Mission import Mission
from CommandParse import CommandParse
from CommandAction import CommandAction

# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)


my_mission = MalmoPython.MissionSpec(Mission().GetMission(), True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_mission.requestVideo(800, 500)
my_mission.setViewpoint(1)

# Attempt to start a mission:
max_retries = 3

for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break

    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission", e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ")
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:

    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

action_index = 0
while world_state.is_mission_running:

    time.sleep(0.1)

    # agent_host.sendCommand("move 1")  # Get new command

    world_state = agent_host.getWorldState()

    for error in world_state.errors:
        print("Error:", error.text)

    # parse
    user_command = input("Ask your question: ")
    command_class = CommandParse(user_command)
    final_command = command_class.parse()

    # call correct action function
    action_class = CommandAction(agent_host)
    action_class.find_obj()
    # give output from agent
