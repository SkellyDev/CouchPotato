

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

TREE_LST = [(7, 13), (43, 17), (38, 11), (7, 50)]
HOUSE = [(30, 30), (40, 40)]
LAKE = [(10, 20), (15, 25)]

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
    '''
    print("""
        User input Manual:\n
        Move foward: 'movenorth 1'\n
        Move backward: 'movesouth 1'\n
        Move left: 'movewest 1'\n
        Move right: 'moveeast 1'
        """)
    '''
    user_command = input("Ask your question: ")
    command_class = CommandParse(user_command)
    final_command = command_class.parse_command()

    action_class = CommandAction(agent_host)
    # Find animals in closest(in front of, next to...)
    # What is the closest entity (relative to agent)? ✅
    # Where is the closest (entity) (relative to agent) ?
    # Where is the (entity A) relative to (Block B)?  拿到block坐标，找离他最近的block，方向
    # How many (entity/Block) can you see? question: min max observationfromgrid
    # What is the clostest entity relative to a (Block)?
    # Which animal is inside the house?

    if final_command == "What is the closest animal around you?":
        # call correct action function
        # could add num parameter as return quantity
        animal = action_class.find_closest_animal("agent")
        print(''.join(animal))

    elif final_command == "What is the animal around house?":
        # where is the direction of closest sheep
        animal = action_class.find_closest_animal(HOUSE)
        print("The closet animal around house is ", ''.join(animal))

    elif final_command == "Where is closest sheep around you?":
        direction = action_class.get_direction_of_entity_relative_agent(
            "Sheep")
        print("The closest sheep around you is in", direction)

    elif final_command == "Where is closest sheep around house?":
        direction = action_class.get_direction_of_entity_relative_block(
            "Sheep", HOUSE)
        print("The cloeset sheep around you is in", direction)

    elif final_command == "Which animal is inside the house?":
        animal = action_class.find_animal_inside_house()
        print("The animal inside house is ", animal)

    elif user_command in ['move 1', 'move 0', 'turn 1', 'turn -1']:
        agent_host.sendCommand(user_command)
        time.sleep(0.2)
        agent_host.sendCommand('move 0')

        print("finished")
