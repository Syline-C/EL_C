"""
@file       builder.py
@author     Suyong Choi
@brief      Declaring the Super Mario environment builder class
@version    1.0
@date       2024.05.01
"""

import gym_super_mario_bros
import gymnasium as gym
#from shimmy import GymV21CompatibilityV0

#from gym import Wrapper
#from gym import Env

from gymnasium import Wrapper
from gymnasium import Env

from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace

from env.facade.marioFacade import marioFacade

#from logger.logger import logger
from config.define import DEFINE


class gymMario:
    def __init__(self, level):
        """ 
        @brief          :   Function to create a Mario environment in openAI
        @param level    :   The Super Mario stage level you want to run
        @return         :   None
        """

        self.rawGymMarioEnv    = gym_super_mario_bros.make(level)

        if hasattr(self.rawGymMarioEnv, 'unwrapped'):
            self.rawGymMarioEnv = self.rawGymMarioEnv.unwrapped

        self.rawGymMarioEnv    = JoypadSpace(self.rawGymMarioEnv, SIMPLE_MOVEMENT)

        try:
            from gymnasium.wrappers.compatibility import EnvCompatibility
        except ImportError:
            from shimmy.openai_gym_compatibility import GymV26CompatibilityV0 as EnvCompatibility

        self.gymMarioEnv = EnvCompatibility(env=self.rawGymMarioEnv)

    def getMarioEnv(self):
        return self.gymMarioEnv
        #return self.rawGymMarioEnv

#class superMario(Wrapper):
class superMario(Env):
   
    def __init__(self, gymMario:Env, title, mode):
        """ 
        @brief              :   Function to create a customized Super Mario environment from Facade Class
        @param gymMario     :   openAI's Super Mario environment created from the gymMario class
        @param title        :   Super Mario screen title
        @return             :   None
        """
        #super().__init__(gymMario.gymMarioEnv)
        super().__init__()

        self.mode           =   mode
        self.env            =   gymMario.gymMarioEnv
        self.baseMario      =   gymMario.rawGymMarioEnv
        self.marioFacade    =   marioFacade(gymMario, title, mode)

        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        self.render_mode = "rgb_array"

        self.metadata = getattr(self.env, "metadata", {}).copy()
        self.metadata.update({"render_modes": ["rgb_array", "human"]})

#        if self.marioFacade is DEFINE._DEFINE_NULL:
#           logger.instanceEmptyAssertLog('Facade') 


    def step(self, action=None):
        """ 
        @brief              :   Returns the result of Mario's decision
        @return state       :   Mario's state according to decision making as an Integer
        @return reward      :   Reward value based on decision-making as an Float
        @return done        :   True if decision-making is in progress, False otherwisee as an Boolean
        """
        result =  self.marioFacade.step(action)

        if len(result) == 4:
            ons, reward, done, info = result
            terminated = done
            truncated = False
        else :
            obs, reward, terminated, truncated, info = result
        
        #print(f"reward : {reward}")
        return obs, reward, terminated, truncated, info


    def reset(self, seed=None, options=None):
        """ 
        @brief              :   Use openAI’s Windows data reset function
        @return             :   None
		"""
        #print("builder Reset")
        #print(seed)
        if seed is not None:
            try:
                self.env.unwrapped.seed(seed)
            except AttributeError:
                pass

        try : 
            obs, info = self.env.reset(seed=seed, options=options)
            print("success")
        except (TypeError, ValueError):
            obs = self.baseMario.reset()
            info = {}

        self.marioFacade.reset(obs)
        print("builder Reset")
        print(seed)
        #print(obs)
        print(info)
        return obs, info

    #def render(self, reward):
    def render(self ):
        """ 
        @brief              :   Function to render Mario's game data to a window
        @return             :   None
		"""
        #print("----")
        #print(self.mode)
        if self.mode == 'command':
            #return self.marioFacade.render(self.mode)
            data =  self.marioFacade.render(self.mode)
            #print("com")
            return data
        elif self.mode == 'rgb_array':
            data =  self.marioFacade.render(self.mode)
            print("===")
            print(data)
            return data
        elif self.mode == 'interactive':
            window = self.marioFacade.render(self.mode)
            return window

    def getFacade(self):
        return self.marioFacade

class marioBuilder:

    def __init__(self, title, level, mode ):
        """ 
        @brief              :   Initialize the class that builds the customized Super Mario environment and openAI's Mario environment.
        @param title        :   Super Mario screen title
        @param level        :   Super Mariio game level
        @return             :   None
        """
        self.title          = title
        self.builder        = None
        self.facade         = None
        self.baseMario      = gymMario(level)

        self.mode           = mode

    def build(self):
        """ 
        @brief              :   Build a customized Super Mario environment and openAI’s Mario environment
        @return  builder    :   Built Super Mario environment as superMario Class Instance
        """

        self.builder     = superMario(self.baseMario, self.title, self.mode)
        self.facade      = self.builder.marioFacade

#        if self.builder is DEFINE._DEFINE_NULL:
#           logger.instanceEmptyAssertLog('builder') 

        return self.builder

    def getBaseEnv(self):
        return self.baseMario

    def getFacade(self):
        return self.facade
