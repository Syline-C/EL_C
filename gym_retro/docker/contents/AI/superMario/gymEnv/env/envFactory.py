from .builder.marioBuilder import marioBuilder
from config.stageInfo import stageInfo

class envFactory:

    def __init__(self, game, level, stage):

        self.game = game
        self.level = level
        self.stage = stage

        self.rom = None
        self.title = None

    def build(self):
       
        self.rom = self._getRomInfo()
        self.title = self._getGameTitle()

        games = {
                "mario" : lambda: marioBuilder(self.title, self.rom) 
                #TODO
                # add Other Game Builder
        }

        return games.get(self.game)() 

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

