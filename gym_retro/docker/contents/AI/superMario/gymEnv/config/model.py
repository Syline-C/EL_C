class modelConfig:

    @staticmethod
    def get_ppo_params():
        return {
            "policy": "CnnPolicy",
            "learning_rate": 0.01,
            "n_steps": 10000,
            "batch_size": 64,
            "n_epochs": 10,
            "gamma": 0.99,
            "verbose": 1,
        }

    @staticmethod
    def get_dqn_params():
        return {
            "policy": "MlpPolicy",
            "buffer_size": 10000,
            "learning_rate": 1e-4,
        }
