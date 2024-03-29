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
import math

# What is the closest entity (relative to agent)? ✅
# Where is the closest (entity) (relative to agent) ?
# Where is the (entity A) relative to (Block B)?  拿到block坐标，找离他最近的block，方向
# How many (entity/Block) can you see? question: min max observationfromgrid
# What is the clostest entity relative to a (Block)?
# ------- after status -------
# Where are you? / Describe your location

#direction, nearest, color,
# train model to have multiple tags?


#### GLOABL #####
TREE_LIST = [(7, 13), (43, 17), (38, 11), (8, 35),
             (17, 59), (22, 53), (24, 57), (46, 14)]
HOUSE = [(30, 30), (40, 40)]
LAKE = [(15, 10), (25, 20)]
HILL = [(1, 44), (16, 59)]
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

    def get_entity_dict(self, block_type):
        """
        input: block type include agent and others "agent"/global variable
        return a dict of all types of entities : [distance, angle, coord]
        """
        # print(block_type)
        entity_dict = {}
        if block_type == "agent":
            x = self.get_agent_pos()[0]
            z = self.get_agent_pos()[1]
        else:

            x = self.find_closest_block_relative_agent(block_type)[0]
            z = self.find_closest_block_relative_agent(block_type)[1]

        for e in self.observation["Entities"][1:]:
            entity_x = e["x"]
            entity_z = e["z"]
            entity_name = e["name"]
            angle = self.entity_angle((entity_x, entity_z))
            dist = self.get_distance(x, entity_x, z, entity_z)
            if entity_name not in entity_dict.keys():
                entity_dict[entity_name] = []
            entity_dict[entity_name].append(
                (dist, angle, (entity_x, entity_z)))
        # print(entity_dict)
        return entity_dict

    def get_entity_closest_relative_block(self, block_type):
        '''
        input: "agent"/global variable(block type)
        '''
        if block_type == "agent":
            x = self.get_agent_pos()[0]
            z = self.get_agent_pos()[1]

        elif type(block_type) == tuple:
            x = block_type[0]
            z = block_type[1]
            #print(x, z)

        else:
            x = self.find_closest_block_relative_agent(block_type)[0]
            z = self.find_closest_block_relative_agent(block_type)[1]

        entity_distance_dict = []
        for e in self.observation["Entities"][1:]:
            entity_x = e["x"]
            entity_z = e["z"]
            dist = self.get_distance(x, entity_x, z, entity_z)
            entity_distance_dict.append(
                (e["name"], dist, (entity_x, entity_z)))
        entity_distance_dict.sort(key=lambda x: x[1])
        # print(entity_distance_dict)
        return entity_distance_dict

    def find_closest_block_relative_agent(self, block_type: [tuple]):
        '''
        根据agent找最近的block
        Find the closest bloack(e.g. tree) relative to agent
        input: a block type --- list of tuple 
        output: the cloest block coordinate --- tuple
        '''
        # print(block_type)
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
        elif block_type == HILL:
            return (9, 51)

    def find_closest_entity_relative_to_block(self, block_type, entity_type: str):
        '''
        Find the closest entity(type) relative to agent
        input: an entity type : string
        output: a list [distance, angle, coord] of closest entity(type)
        '''
        entity_list = self.get_entity_dict(
            block_type)[entity_type.capitalize()]
        entity_list = sorted(entity_list, key=lambda entity: entity[0])
        # print(entity_list)
        return entity_list[0]

    def block_type_convert(self, block_type):
        #block_type = block_type.strip()
        if block_type.strip().lower() == "tree":
            return TREE_LIST
        elif block_type.strip().lower() == "house":
            return HOUSE
        elif block_type.strip().lower() == "lake":
            return LAKE
        elif block_type.strip().lower() == "hill":
            return HILL
        elif block_type.strip().capitalize() in ['Pig', 'Sheep', 'Cow']:
            closest_entity = self.find_closest_entity_relative_to_block(
                "agent", block_type)
            return closest_entity[2]
        else:
            return block_type

    ####### --------------------------- END OF HELPER FUNCTION ------------------------------------- ########

    ####### --------------------------- ACTION FUNCTION ------------------------------------- #############

    def getDirection(self, entity_type, target="agent"):
        '''
        Get the direction of entity correlated to the agent or an architect
        '''
        # print(entity_type)
        block_loc = target
        target = self.block_type_convert(target)
        closest_entity = self.find_closest_entity_relative_to_block(
            target, entity_type)
        # print(closest_entity)
        direction = ""
        if target == "agent":
            agent_yaw = self.observation['Yaw']
            if agent_yaw > 180:
                agent_yaw = -(360-agent_yaw)
            elif agent_yaw < -180:
                agent_yaw = 360-agent_yaw
            # print(agent_yaw)
            entity_x = closest_entity[2][0]
            entity_y = closest_entity[2][1]
            agent_x = self.get_agent_pos()[0]
            agent_y = self.get_agent_pos()[1]

            entity_agent_degree = math.atan(
                (float)(agent_y-entity_y)/(-agent_x-(-entity_x))) * 180 / math.pi
            degree_diff = entity_agent_degree + agent_yaw
            #entity_dist = self.get_distance(entity_x, 0, entity_y, 0)
            #agent_dist = self.get_distance(agent_x, 0, agent_y, 0)

            if entity_y > agent_y:
                if entity_x < agent_x:
                    if degree_diff < 110 and degree_diff > 70:
                        direction = f"I can see the {entity_type} is right in front of me"
                    elif degree_diff > 0 and degree_diff <= 70:
                        direction = f"I can see the {entity_type} is on my right hand side"
                    elif degree_diff >= 110 and degree_diff < 180:
                        direction = f"I can see the {entity_type} is on my left hand side"
                    else:
                        direction = f"I cannot see any {entity_type}, maybe it's behind me."
                else:  # entity_x > agent_x
                    if degree_diff < -70 and degree_diff > -110:
                        direction = f"I can see the {entity_type} is right in front of me"
                    elif degree_diff < 0 and degree_diff >= -70:
                        direction = f"I can see the {entity_type} is on my left hand side"
                    elif degree_diff <= -110 and degree_diff > -180:
                        direction = f"I can see the {entity_type} is on my right hand side"
                    else:
                        direction = f"I cannot see any {entity_type}, maybe it's behind me."
            else:  # entity_y < agent_y
                if entity_x > agent_x:
                    if degree_diff >= 0 and degree_diff <= 180:
                        direction = f"I cannot see any {entity_type}, maybe it's behind me."
                    elif degree_diff < 0 and degree_diff > -70:
                        direction = f"I can see the {entity_type} is on my left hand side"
                    elif degree_diff <= -70 and degree_diff >= -110:
                        direction = f"I can see the {entity_type} is right in front of me"
                    else:
                        direction = f"I can see the {entity_type} is on my right hand side"

                else:  # entity_x < agent_x
                    if degree_diff >= 70 and degree_diff <= 110:
                        direction = f"I can see the {entity_type} is right in front of me"
                    elif degree_diff <= 0 and degree_diff >= -180:
                        direction = f"I cannot see any {entity_type}, maybe it's behind me."
                    elif degree_diff > 0 and degree_diff < 70:
                        direction = f"I can see the {entity_type} is on my right hand side"

                    else:
                        direction = f"I can see the {entity_type} is on my left hand side"
        else:
            cor1 = closest_entity[2]
            if target == HOUSE:
                cor2 = HOUSE
            elif target == LAKE:
                cor2 = LAKE
            elif target == HILL:
                cor2 = HILL
            else:  # Tree
                cor2 = [self.find_closest_block_relative_agent(target)]
            if len(cor2) != 1:
                cor2_x1 = cor2[0][0]
                cor2_z1 = cor2[0][1]
                cor2_x2 = cor2[1][0]
                cor2_z2 = cor2[1][1]
                center_x = cor2_x1+(cor2_x2-cor2_x1)//2
                center_y = cor2_z1+(cor2_z2-cor2_z1)//2

                if cor1[0] < center_x + 20 and cor1[0] > center_x - 20 and cor1[1] < center_y + 20 and cor1[1] > center_y - 20:
                    if cor1[1] > cor2_z2:
                        if cor1[0] > cor2_x2:
                            direction = f"It's in the top left corner of the {block_loc}"
                        elif cor1[0] > cor2_x1 and cor1[0] < cor2_x2:
                            direction = f"It's behind the {block_loc}"
                        else:
                            direction = f"It's in the top right corner of the {block_loc}"
                    elif cor1[1] > cor2_z1 and cor1[1] < cor2_z2:
                        if cor1[0] > cor2_x2:
                            direction = f"It's on the left side of the {block_loc}"
                        elif cor1[0] > cor2_x1 and cor1[0] < cor2_x2:
                            direction = f"It's inside the {block_loc}"
                            if block_loc.lower() == "hill":
                                direction = f"It's on the {block_loc}"
                        else:
                            direction = f"It's on the right side of the {block_loc}"
                    else:
                        if cor1[0] > cor2_x2:
                            direction = f"It's in the bottom left corner of the {block_loc}"
                        elif cor1[0] > cor2_x1 and cor1[0] < cor2_x2:
                            direction = f"It's in front of the {block_loc}"
                        else:
                            direction = f"It's in the bottom right corner of the {block_loc}"
                else:
                    direction = "This entity is not in the range of the {block_loc}."
            else:  # Tree
                cor2_x = cor2[0][0]
                cor2_z = cor2[0][1]
                if cor1[0] < cor2_x + 4 and cor1[0] > cor2_x - 4 and cor1[1] < cor2_z + 4 and cor1[1] > cor2_z - 4:
                    direction = "This entity is around the tree."
                else:
                    direction = "This entity is not in the range."
        # print(direction)
        return direction

    def closest(self, block_type="agent", num=1):
        '''
        input block type: "agent"/global variable(block type)/animal type
        output name of closest animal
        '''
        #print('block_type', block_type)
        block_type = self.block_type_convert(block_type)
        #print('self.block_type_convert(block_type)', block_type)
        entity_list = self.get_entity_closest_relative_block(block_type)
        if type(block_type) == tuple:
            entity_list = entity_list[1:]
        # print(entity_list)
        count = 0
        result = []
        index = 0
        while count < num:
            if entity_list[index][0] in ['Pig', 'Cow', 'Sheep']:
                if block_type == "agent" or block_type == TREE_LIST or type(block_type) == tuple:
                    result.append(
                        (entity_list[index][0], entity_list[index][2]))
                    count += 1
                else:
                    x1 = block_type[0][0]
                    x2 = block_type[1][0]
                    z1 = block_type[0][1]
                    z2 = block_type[1][1]
                    animal_cor = entity_list[index][2]
                    if not (animal_cor[0] > x1 and animal_cor[0] < x2 and animal_cor[1] > z1 and animal_cor[1] < z2):
                        result.append(
                            (entity_list[index][0], entity_list[index][2]))
                        count += 1
            index += 1
        result_list = [i[0] for i in result]
        result = ''.join(result_list)
        # print(result)

        return result

    def inside(self, block: str):
        inside = []
        block_loc = block
        block = self.block_type_convert(block)
        entity_dict = self.get_entity_dict(block)
        x1 = block[0][0]
        x2 = block[1][0]
        z1 = block[0][1]
        z2 = block[1][1]
        for key in entity_dict.keys():
            for each in entity_dict[key]:
                if key in ['Pig', 'Cow', 'Sheep'] and each[2][0] > x1 and each[2][0] < x2 and each[2][1] > z1 and each[2][1] < z2:
                    inside.append(key)
        p = ""
        if len(inside) == 1:
            p = 'is'
        else:
            p = 'are'
        result = ' and '.join(list(set(inside))) + \
            f" {p} inside the {block_loc}"
        return inside, result

    def count(self, animal, block):
        inside = self.inside(block)[0]
        if animal != 'animals':
            num = inside.count(animal[:-1].capitalize())
            if num == 1:
                print(f'There is {num} {animal[:-1]} inside the {block}.')
            else:
                print(f'There are {num} {animal} inside the {block}.')
        else:
            num = len(inside)
            print(f'There are total {num} animals inside the {block}')
        return num

    def describe_agent_location(self):
        x = self.get_agent_pos()[0]
        z = self.get_agent_pos()[1]
        #print(x, z)
        stand = ""
        if x > 1 and x < 16 and z > 44 and z < 59:
            stand = "hill"
        elif x > 17 and x < 20 and z >= 9 and z <= 21:
            stand = "bridge"
        else:
            stand = "grass"
        sight = ""
        position = "in front of"
        if z < 9:
            sight = "a lake, a house and a hill"
        elif z > 9 and z < 30:
            sight = "a house and a hill"
        elif stand == "hill":
            sight = "a house and a lake"
            position = "below"
        else:
            sight = "a hill"

        result = f"I am standing on the {stand} in a village, and I can see there is {sight} {position} me"
        print(result)
        return result
