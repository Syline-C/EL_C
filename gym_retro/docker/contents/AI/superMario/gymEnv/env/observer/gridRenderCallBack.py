from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class gridRenderCallBack(BaseCallback):
    def __init__(self, facade, verbose=0):
        super().__init__(verbose)
        self.facade = facade

    def _on_step(self) -> bool:
        frames = self.training_env.get_images()
        #print(f"Frames Type: {type(frames)}")
        if frames is not None:
            if isinstance(frames, list):
                frames = np.array(frames)
            #self.facade.render_grid(frames)
            #print(f"Frames Shape: {frames.shape}")
            #print(type(self.facade))
            self.facade.render(data=frames)
            
        return True
