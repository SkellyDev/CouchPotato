'''
This is a script for actionclass that call Malmo action
based on given command
How many pigs?
Where is the village?
What is in front of the house? 
'''

import malmo.MalmoPython

class CommandAction:

    def __init__(self, agentHost):
        self.agent = agentHost
    
    def get_latest_world(self):
        latest_world = self.agent.peekWorldState()
        return latest_world 

    def find_obj(self):
        lastest_world = self.get_latest_world()
        observation = lastest_world.observations
        print(observation)


    def count(self):
        return 0

    def find_obj_direction(self):
        return 0


    

    

