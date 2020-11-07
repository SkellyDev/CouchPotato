'''
This is a script for actionclass that call Malmo action
based on given command
How many pigs?
Where is the village?
What is in front of the house?
'''

import malmo.MalmoPython
import json
import math
from collections import defaultdict
import numpy as np

# What is the closest entity (relative to agent)? 
# Where is the closest (entity) (relative to agent) ?
# Where is the (entity A) relative to (Block B)?  拿到block坐标，找离他最近的entity，方向
# How many (entity/Block) can you see? question: min max observationfromgrid
# What is the clostest entity relative to a (Block)? 


class CommandAction:

    def __init__(self, agentHost):
        self.agent = agentHost
        self.observation = self.get_observation()
        self.world_state = self.get_latest_world()

    def get_latest_world(self):
        latest_world = self.agent.peekWorldState()
        return latest_world

    def get_observation(self):
        lastest_world = self.get_latest_world()
        observation = json.loads(lastest_world.observations[-1].text)
        return observation

    def get_grid_from_observation(self):
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'ground_layer', 0)
        print(grid)
        return grid
        
    def get_agent_pos(self):
        return (self.observation['XPos'], self.observation['ZPos'])

    def count(self):
        return 0

    def get_distance(self, x1, x2, z1, z2):
        """
        Get distance
        """
        return math.sqrt((x1 - x2)**2 + (z1 - z2)**2)

    def entity_angle(self, p1: tuple):
        """
        Get angle between two points
        """
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*(0, 0)[::-1])
        return -1 * int(np.rad2deg((ang1 - ang2) % (2 * np.pi)))

    def get_entity_dict(self):
        """
        return a dict: entity : [distance, coord]
        """
        entity_dict = defaultdict(list)
        for e in self.observation["Entities"][1:]:
            entity_name = e["name"]
            x = e["x"]
            z = e["z"]
            angle = self.entity_angle((x, z))
            dist = self.get_distance(self.get_agent_pos()[
                0], x, self.get_agent_pos()[1], z)
            entity_dict[entity_name].append((dist, angle))
        return entity_dict

    def get_direction_of_entity(self, type):
        '''
        Get the direction of entity correlated to where agent face
        '''
        agent_yaw = self.observation['Yaw']
        print(agent_yaw)
        entity_list = self.get_entity_dict()[type]
        # find the closet one of that entity
        entity_list = sorted(entity_list, key=lambda entity: entity[0])
        print(entity_list[0][1])
        direction_of_closet = agent_yaw-entity_list[0][1]
        print(direction_of_closet)

        direction = ""
        if direction_of_closet >= -50 and direction_of_closet <= 50:
            direction = "right in front of me"
        elif direction_of_closet < -50 and direction_of_closet >= -160:
            direction = "on my right hand"
        elif direction_of_closet > 50 and direction_of_closet < 160:
            direction = "on my left hand"
        else:
            direction = f"I cannot see any {type}, maybe it's behind me"
        return direction

    def get_entity_closest(self):
        '''
        Return list of tuple : [('Pig', 4.234), ('Cow', 5)...] For getting
        animal distances
        '''
        entity_distance_dict = []
        for e in self.observation["Entities"][1:]:
            x = e["x"]
            z = e["z"]
            dist = self.get_distance(self.get_agent_pos()[
                                     0], x, self.get_agent_pos()[1], z)
            entity_distance_dict.append((e["name"], dist))
        entity_distance_dict.sort(key=lambda x: x[1])
        # print(entity_distance_dict)
        return entity_distance_dict

    def find_closest_animal(self, num=1):
        entity_list = self.get_entity_closest()
        count = 0
        result = []
        while count < num:
            if entity_list[count][0] in ['Pig', 'Cow', 'Sheep']:
                result.append(entity_list[count][0])
                count += 1
        return result
