

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import sys
import time
import json
import random
import numpy
from tqdm import tqdm
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from Mission import Mission
from CommandParse2 import TreeNode
from CommandParse2 import TreeVisitor
from allennlp.predictors.predictor import Predictor
import allennlp_models.structured_prediction
PREDICTOR = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz")

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

#action_index = 0
'''
CP = CommandParse("")
model = CP.save_model()

words = CP.get_words()
labels = CP.get_labels()

model.load("model.tflearn")
'''
##### Model build finished ####

print("Usage: Type any question or 'Perform action' to move and 'Finish' to stop.")
while world_state.is_mission_running:

    time.sleep(0.1)

    # agent_host.sendCommand("move 1")  # Get new command

    world_state = agent_host.getWorldState()

    for error in world_state.errors:
        print("Error:", error.text)

    user_command = input("Ask your question: ")
    if user_command.lower() == "quit":
        break
    if user_command == "Perform action":
        while user_command == "Perform action":
            print('''Action command usage:
            1)Move forward: "move {#steps}"
            2)Move backward: "move -{#steps}"
            3)Turn right: "turn 1"
            4)Turn left: "turn -1"''')
            move_command = input("Give your move command: ")

            if move_command.startswith('move'):
                step = int(move_command.split(' ')[1])
                # print(step)
                if step > 0:
                    for i in range(abs(step)):
                        print(i)
                        agent_host.sendCommand('move 1')
                        time.sleep(0.3)
                        agent_host.sendCommand('move 0')
                else:
                    for i in range(abs(step)):
                        print(i)
                        agent_host.sendCommand('move -1')
                        time.sleep(0.3)
                        agent_host.sendCommand('move 0')

            elif move_command in ['turn 1', 'turn -1']:
                agent_host.sendCommand(move_command)
                time.sleep(0.3)
                agent_host.sendCommand('turn 0')

            elif move_command == 'Finish':
                break
            else:
                print('Invalid move command')
    else:
        user_command = user_command.strip()
        if user_command.endswith('.') or user_command.endswith(',') or user_command.endswith('?'):
            user_command = user_command[:-1]
        tree_string = PREDICTOR.predict(user_command)["trees"]
        TN = TreeNode(tree_string)
        TV = TreeVisitor(TN, agent_host)

        '''
        # Get question tag returned from NN model
        CP = CommandParse(user_command)
        tag = CP.return_tag(model, words, labels)
        print("question tag is this ========= ", tag)

        # Match Command with correct describing function
        action_class = CommandAction(agent_host)
        action_class.get_observation()

        if user_command == "What is the closest animal around the closest animal of you?":
            animal1 = action_class.find_closest_animal("agent")
            print(animal1)
            animal2 = action_class.find_closest_animal(animal1)
            print(animal2)
        
        if tag == 'find_closest_animal':
            CT = CommandTagger(user_command)
            block = CT.get_full_tag_list(tag)
            animal = action_class.find_closest_animal(block)
            print(f"The closest animal near {block} is {animal}")

        elif tag == 'get_direction_of_entity_relative_agent':
            CT = CommandTagger(user_command)
            animal = CT.get_full_tag_list(tag)
            direction = action_class.get_direction_of_entity_relative(
                animal, "agent")
            print(f"The closest {animal} is {direction}")

        elif tag == 'get_direction_of_entity_relative_block':
            CT = CommandTagger(user_command)
            animal, block = CT.get_full_tag_list(tag)
            direction = action_class.get_direction_of_entity_relative(
                animal, block)
            print(
                f"The closest {animal} is {direction} relative to the {block}")

        elif tag == 'find_animal_inside_block':
            CT = CommandTagger(user_command)
            block = CT.get_full_tag_list(tag)
            animal = action_class.find_animal_inside_block(block)
            animal = list(set(animal))
            animal_result = " ".join(set(animal))
            print(f"I can see {animal_result} inside the {block}")

        elif tag == 'count_quantity':
            CT = CommandTagger(user_command)
            animal, block = CT.get_full_tag_list(tag)
            num = action_class.count_quantity(animal, block)
            print(f"There are {num} {animal} inside the {block}.")

        elif tag == 'describe_environment':
            print(action_class.describe_agent_location())
        '''
