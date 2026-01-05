import gymnasium as gym

class finalWrapper(gym.Wrapper):
    def reset(self, **kwargs):
        obs = self.env.reset()
        return obs, {}

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return obs, reward, done, False, info

class marioLauncher:

    @staticmethod
    def create(level):
        from env.builder.marioBuilder import marioBuilder
        builder = marioBuilder(title="MarioGrid", level=level, mode="command")
        return builder.build()
