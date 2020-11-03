'''
script for xml environment
'''
import random


class Mission:
    def __init__(self):
        self._SIZE = 60
        self._DENSITY = 0.001

    def spawn_type(self, type):
        result_xml = ""
        for _ in range(int((self._SIZE*2)**2*self._DENSITY)):
            xd, zd = random.randint(
                0, self._SIZE), random.randint(0, self._SIZE)
            result_xml += "<DrawEntity x='{}' y='4' z='{}' type='{}'/>".format(
                xd, zd, type)
        return result_xml
    '''
    def draw_lake(self,type):
        result_xml = ""
        #Layer One
        "<DrawBlock x='{}'  y='3' z='{}' type='water' />"
        #Layer Two
        "<DrawBlock x='{}'  y='2' z='{}' type='water' />"
    '''

    def draw_house(self, x1, x2, z1, z2):
        result_xml = "<DrawCuboid x1='{}' x2='{}' y1='3' y2='3' z1='{}' z2='{}' type='sand'/>".format(
            x1, x2, z1, z2)
        for l in range(4, 8):
            for i in range(x1, x2+1):
                result_xml += f"<DrawBlock x='{i}'  y='{l}' z='{z1}' type='gold_ore' />"
                result_xml += f"<DrawBlock x='{i}'  y='{l}' z='{z2}' type='gold_ore' />"
            for j in range(z1, z2+1):
                result_xml += f"<DrawBlock x='{x1}'  y='{l}' z='{j}' type='gold_ore' />"
                result_xml += f"<DrawBlock x='{x2}'  y='{l}' z='{j}' type='gold_ore' />"
        result_xml += f"<DrawBlock x='{(x1+x2)//2}'  y='{l}' z='{z1}' type='dark_oak_door' />"
        result_xml += f"<DrawBlock x='{(x1+x2)//2+1}'  y='{l}' z='{z1}' type='dark_oak_door' />"
        return result_xml

    def draw_wall(self, x1, x2, z1, z2):
        result_xml = ""
        for l in range(4, 7):
            for i in range(x1, x2+1):
                result_xml += f"<DrawBlock x='{i}'  y='{l}' z='{z1}' type='dark_oak_fence' />"
                result_xml += f"<DrawBlock x='{i}'  y='{l}' z='{z2}' type='dark_oak_fence' />"

            for j in range(z1, z2+1):
                result_xml += f"<DrawBlock x='{x1}'  y='{l}' z='{j}' type='dark_oak_fence' />"
                result_xml += f"<DrawBlock x='{x2}'  y='{l}' z='{j}' type='dark_oak_fence' />"

        return result_xml

    def GetMission(self):

        return '''
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

        <About>
            <Summary>Environment Description</Summary>
        </About>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>true</AllowPassageOfTime>
                </Time>
                <Weather>normal</Weather>
                <AllowSpawning>false</AllowSpawing>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,2*3,1;1;biome_1,village,lake,lava_lake"/>
                <DrawingDecorator>''' +  \
            "<DrawCuboid x1='{}' x2='{}' y1='4' y2='4' z1='{}' z2='{}' type='air'/>".format(0, self._SIZE, 0, self._SIZE) + \
            "<DrawCuboid x1='{}' x2='{}' y1='3' y2='3' z1='{}' z2='{}' type='grass'/>".format(0, self._SIZE, 0, self._SIZE) + \
            "<DrawCuboid x1='{}' x2='{}' y1='3' y2='3' z1='{}' z2='{}' type='water'/>".format(10, 20, 10, 20) + \
            self.spawn_type('Pig') + self.draw_wall(0, self._SIZE, 0, self._SIZE) + self.draw_house(30, 40, 30, 40) + \
            '''</DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes/>
            </ServerHandlers>
        </ServerSection>
        
         <AgentSection mode="Creative">
            <Name>Environment Description</Name>
            <AgentStart>
                <Placement x="5" y="4" z="5" yaw="0"/>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullStats/>
                    <ContinuousMovementCommands turnSpeedDegs="180"/>
            </AgentHandlers>
        </AgentSection>
        </Mission>
        '''
