from .builder.marioBuilder import marioBuilder
from .builder.envBuilder import envBuilder
from .launcher.superMarioLauncher import marioLauncher
from config.stageInfo import stageInfo

from functools import partial

class envFactory:

    def __init__(self, game, level, stage, mode):

        self.game = game
        self.level = level
        self.stage = stage
        self.mode = mode

        self.baseEnv = None
        self.builder = None
        self.facade = None

        self.rom = self._getRomInfo()
        self.title = self._getGameTitle()
        self.game = self._getGameInstance()
         

    def build(self, buildType, envType="sb3"):
       
        env = self._setEnv(self.game, envType)()
        return env.buildAiEnv(buildType)

    def gridBuild(self, gridNum, buildType, envType="sb3"):

        headBuilder = envBuilder(self.game)

        env_fns = [partial(marioLauncher.create, str(self.rom)) for _ in range(gridNum)]
        return headBuilder.buildAiGridEnv(buildType, env_fns)

    def _setEnv(self, game_instance, envType):
       
        envMap = {
                "sb3" : lambda : envBuilder(game_instance)
                #TODO
                # add Other Game Stage Info
        }

        return envMap.get(envType)

    def _getRomInfo(self):

        stageRom = {
                "mario": lambda: stageInfo.MARIO_INFO[self.level][self.stage]
                #TODO
                # add Other Game Stage Info
        }
       

        return stageRom.get(self.game)()

    def _getGameTitle(self):

        title = {
                "mario": lambda: stageInfo.GAME_TITLE[self.game]
                #TODO
                # add Other Game Stage Info
        }
        return title.get(self.game)()

    def _getGameInstance(self):

        games = {
                "mario" : lambda: marioBuilder(self.title, self.rom, self.mode) 
                #TODO
                # add Other Game Builder
        }
        self.baseEnv = games.get(self.game)().getBaseEnv()
        self.builder = games.get(self.game)()

        builder = games.get(self.game)().build()
        self.facade  = builder.getFacade()
        return builder
        #return games.get(self.game)().build()

