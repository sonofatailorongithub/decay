from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random


def computeLiftandDecay(Model):
    return

#Lift and decay for the 9 categories of agents
Dict = {1: {'Lift': 1.0, 'Decay': 0.3},2: {'Lift': 1.9, 'Decay': 0.27}, 3:{'Lift': 2.7, 'Decay': 0.24},
        4: {'Lift': 3.4, 'Decay': 0.21},5: {'Lift': 4.0, 'Decay': 0.18}, 6:{'Lift': 4.5, 'Decay': 0.16},
        7: {'Lift': 4.7, 'Decay': 0.14},8: {'Lift': 4.75, 'Decay': 0.12}, 9:{'Lift': 5.1, 'Decay': 0.11}}

#Create a random number and then map to a media consumption quintile
#50/50 chance that the frequency is the lower half or upper half of quintile consumption
class Consumer(Agent):
    """An agent with fixed initial media consumption."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.awareness = 0
        quintRandom = random.random()
        freqRandom = random.random()
        if 0.0 < quintRandom <= 0.2:
            self.quintile = 1
            if 0.0 < freqRandom <= 0.5:
                self.freq = 0
            else:
                self.freq = 1
        elif 0.2 < quintRandom <= 0.4:
            self.quintile = 2
            if 0.0 < freqRandom <= 0.5:
                self.freq = 2
            else:
                self.freq = 3
        elif 0.4 < quintRandom <= 0.6:
            self.quintile = 3
            if 0.0 < freqRandom <= 0.5:
                self.freq = 4
            else:
                self.freq = 5
        elif 0.6 < quintRandom <= 0.8:
            self.quintile = 4
            if 0.0 < freqRandom <= 0.5:
                self.freq = 6
            else:
                self.freq = 7
        elif 0.8 < quintRandom:
            self.quintile = 5
            if 0.0 < freqRandom <= 0.5:
                self.freq = 8
            else:
                self.freq = 9

#14 is number of daily steps in 2 weeks
    def calc_Awareness(self):
        exposure_Random = random.random()
        if self.freq/14 > exposure_Random:
            self.awareness = self.awareness + Dict[self.quintile]['Lift']
        else:
            if self.awareness - Dict[self.quintile]['Decay'] < 0:
                self.awareness = 0
            else:
                self.awareness = self.awareness - Dict[self.quintile]['Decay']

    def step(self):
        # The agent's step will go here.
        self.awareness = self.calc_Awareness()

class ExposureDecay(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = BaseScheduler(self)
        # Create agents
        for i in range(self.num_agents):
            a = Consumer(i, self)
            self.schedule.add(a)

        self.datacollector = DataCollector(model_reporters={"Awareness": computeLiftandDecay}, agent_reporters={"Quintile": "quintile"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

#Set number of agents
exposure_decay = ExposureDecay(5000)
for i in range(14):
    exposure_decay.step()

#Collect the output of the agents from Mesa
myfreq = exposure_decay.datacollector.get_agent_vars_dataframe()
yes = myfreq.head()
print(yes)

