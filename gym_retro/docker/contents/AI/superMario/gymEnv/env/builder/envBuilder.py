from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.vec_env import SubprocVecEnv

from config.model import modelConfig
from ..controller.superMarioControllerBuilder import superMarioControllerBuilder 
  

import cloudpickle

class envBuilder:

    def __init__(self, gameInstance):
        self.modelConfig = modelConfig()
        self.rawEnv = gameInstance


    def buildAiEnv(self,buildType):

        dummyEnv = DummyVecEnv([lambda: self.rawEnv])
        model = self._setModel(buildType, dummyEnv)

        return model, dummyEnv
    
    def buildAiGridEnv(self,buildType, gridBuilders ):
    
        #     env_vns = [lambda b=builder: b.rawEnv for builder in gridBuilders]
    
#        try :
#            cloudpickle.dumps(env_vns[0])
#            print("Success")
#        except Exception as e:
#            print(f"Reason : {e}")
        gridVenv = SubprocVecEnv(gridBuilders)
        print(type(gridBuilders[0]))
        #gridVenv = DummyVecEnv(env_vns)
        model = self._setModel(buildType, gridVenv)

        return model, gridVenv
    
    def _setModel(self, buildType, env):

        modelMap = {
            "PPO": lambda: PPO(**self.modelConfig.get_ppo_params(), env = env),
            "DQN": lambda: DQN(**self.mocdelConfig.get_dqn_params(), env = env)
        }
        
        return modelMap.get(buildType)()

#env = DummyVecEnv([lambda: self.controllerBuilder.gymMario.gymMarioEnv])
