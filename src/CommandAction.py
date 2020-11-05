'''
This is a script for actionclass that call Malmo action
based on given command
How many pigs?
Where is the village?
What is in front of the house? 
'''

import malmo.MalmoPython
import json


class CommandAction:

    def __init__(self, agentHost):
        self.agent = agentHost

    def get_latest_world(self):
        latest_world = self.agent.peekWorldState()
        return latest_world

    def find_obj(self):
        lastest_world = self.get_latest_world()

        observation = json.loads(lastest_world.observations[-1].text)

        # one whole string
        # TimestampedString: 2020-Nov-03 08:52:32.833486,
        # {"DistanceTravelled":0,"TimeAlive":138,"MobsKilled":0,"PlayersKilled":0,
        # "DamageTaken":0,"DamageDealt":0,"Life":20.0,"Score":0,"Food":20,"XP":0,"IsAlive":true,
        # "Air":300,"Name":"Environment Description","XPos":5.0,"YPos":4.0,"ZPos":5.0,"Pitch":0.0,"Yaw":0.0,"WorldTime":6072,"TotalTime":152}
        print(observation)

    def count(self):
        return 0

    def find_obj_direction(self):
        return 0
