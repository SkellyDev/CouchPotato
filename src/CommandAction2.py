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

# What is the closest entity (relative to agent)? ✅
# Where is the closest (entity) (relative to agent) ?
# Where is the (entity A) relative to (Block B)?  拿到block坐标，找离他最近的block，方向
# How many (entity/Block) can you see? question: min max observationfromgrid
# What is the clostest entity relative to a (Block)?
# ------- after status -------
# Where are you? / Describe your location

# direction, nearest, color,
# train model to have multiple tags?


#### GLOABL #####
TREE_LIST = [(7, 13), (43, 17), (38, 11), (7, 50)]
HOUSE = [(30, 30), (40, 40)]
LAKE = [(10, 20), (15, 25)]
###############


class CommandAction:

    def __init__(self, agentHost):
        self.agent = agentHost
        self.observation = self.get_observation()
        self.world_state = self.get_latest_world()

    ####### --------------------------- HELPER FUNCTION ------------------------------------- ########
    def get_latest_world(self):
        latest_world = self.agent.peekWorldState()
        return latest_world

    def get_observation(self):
        lastest_world = self.get_latest_world()
        observation = json.loads(lastest_world.observations[-1].text)
        print(observation)
        return observation

    def get_grid_from_observation(self):
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'ground_layer', 0)
        return grid

    def get_agent_pos(self):
        return (self.observation['XPos'], self.observation['ZPos'])

    def get_distance(self, x1, x2, z1, z2):
        """
        Get distance of two coordinate
        """
        return math.sqrt((x1 - x2)**2 + (z1 - z2)**2)

    def entity_angle(self, p1: tuple):
        """
        Get angle between two points p1 coordinate of the entity/agent
        """
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*(0, 0)[::-1])
        return -1 * int(np.rad2deg((ang1 - ang2) % (2 * np.pi)))

    def find_closest_block_relative_agent(self, block_type: [tuple]):
        '''
        根据agent找最近的block
        Find the closest block(e.g. tree) relative to agent
        input: a block type --- list of tuple
        output: the cloest block coordinate --- tuple
        '''
        if block_type == TREE_LIST:
            dist_list = []
            for cor in block_type:
                dist_list.append(self.get_distance(cor[0], self.get_agent_pos()[
                    0], cor[1], self.get_agent_pos()[1]))
            return block_type[dist_list.index(min(dist_list))]
        elif block_type == HOUSE:
            return (35, 35)
        elif block_type == LAKE:
            return (12.5, 22.5)

    def find_closest_entity_relative_agent(self, entity_type):
        '''
        根据agent找最近的entity
        return the coordinate of closest entity (tuple)
        '''
        entity_dict = defaultdict(list)

        x = self.get_agent_pos()[0]
        z = self.get_agent_pos()[1]

        for e in self.observation["Entities"][1:]:
            entity_x = e["x"]
            entity_z = e["z"]
            entity_name = e["name"]
            dist = self.get_distance(x, entity_x, z, entity_z)
            entity_dict[entity_name].append(
                (dist, (entity_x, entity_z)))

        for k in entity_dict:
            entity_dict[k].sort(key=lambda item: item[0])
        return entity_dict[entity_type][0][1]

    def get_object_dict(self, ob):
        """
        input: "agent"/block/entity
        return a dict : [distance, angle, coord]
        """
        object_dict = defaultdict(list)
        if ob == "agent":  # agent
            x = self.get_agent_pos()[0]
            z = self.get_agent_pos()[1]
        elif ob in ["HOUSE", "TREE", "LAKE"]:  # block
            x = self.find_closest_block_relative_agent(ob)[0]
            z = self.find_closest_block_relative_agent(ob)[1]
        else:  # entity
            x = self.find_closest_entity_relative_agent(ob)[0]
            z = self.find_closest_entity_relative_agent(ob)[1]

        # add entities into list
        for e in self.observation["Entities"][1:]:
            entity_x = e["x"]
            entity_z = e["z"]
            entity_name = e["name"]
            angle = self.entity_angle((x, z))
            dist = self.get_distance(x, entity_x, z, entity_z)
            object_dict[entity_name].append(
                (dist, angle, (entity_x, entity_z)))

        return object_dict

    ####### --------------------------- END OF HELPER FUNCTION ------------------------------------- ########

    ####### --------------------------- ACTION FUNCTION ------------------------------------- #############
    def nearest(self, block_type, num=1):
        '''
        purpose: use to find the nearest object relative to an object
        input: "agent"/block/entity
        output: "agent"/block/entity
        '''
        entity_list = self.get_entity_closest_relative_block(block_type)
        # print(entity_list)
        count = 0
        result = []
        index = 0
        while count < num:
            if entity_list[index][0] in ['Pig', 'Cow', 'Sheep']:
                result.append(entity_list[index][0])
                count += 1
            index += 1
        return result

        def direction(self, original, target):
            '''
             purpose: use to find the direction of one object relative to another object
             input: original---"agent"/block  target---"agent"/block/entity
             output: direction string
             Assume agent <--- block/entity; block <--- "agent"/block/entity
             '''
               if original == "agent":
                    agent_pos = self.get_agent_pos()
                    if target in ['Pig', 'Cow', 'Sheep']:

                    else:  # block

                else if type(original) == list:
