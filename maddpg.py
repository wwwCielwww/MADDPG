import gym
import numpy as np
from typing import Any, Optional, Tuple, Type, Union
from stable_baselines3 import TD3
from stable_baselines3.common.type_aliases import GymEnv
from stable_baselines3.td3.policies import TD3Policy

DEFAULT_TIMESTEPS = 10000

class agents: 
    """ A iterator, successively executing the trained model in the given environment

    This class is implemented as an ITERATOR. It will iterate until the agents in the environment 
    complete their iteration thoroughouly. For each iteration step, it utilizes the input model
    to predict the desirable action, iteracts with the environment using that action and return
    the action results renderred by the environment. 

    Args: 
        model:    the trained MADDPG model. 
        min_step: once the number of iteractions exceeds the min_step AND the environment is completed
                  step the execution
        max_step: once the number of iteractions exceeds the max_step, terminate IMMEDIATELY, 
                  regardless the current status of environment. If not set or set to a negative
                  value, this mechanism will not be in effect. 
    """
    def __init__(self,
        model: "maddpg",
        min_steps: int,
        max_steps: int = -1) -> None:
        self.__model     = model
        self.__env       = self.__model.env
        self.__obs       = self.__env.reset()
        self.__min_steps = min_steps
        self.__max_steps = max_steps
        self.__count     = 0
        self.__next_time_terminate = False


    def _iteract(self) -> Tuple[Any, bool]: 
        """ Predict for the next action, and then with the action interact with the environment

        Returns: 
            The result after the iteraction, and
            A boolean to spedicify whether the environment is completed
        """
        action, _ = self.__model.predict(self.__obs)
        self.__obs, _, done, _ = self.__env.step(action)
        self._env.render(), done

    def __next__(self) -> Any:
        if self.__next_time_terminate or self.__count >= self.__max_steps > 0:
            raise StopIteration
        render_result, done = self._iteract()
        self.__count += 1
        if done: 
            self.__obs = self.__env.reset()
            if self.__count >= self.__min_steps: 
                self.__next_time_terminate = True
        return render_result
        

    def __iter__(self) -> "agents":
        self.__obs   = self.__env.reset()
        self.__count = 0
        self.__next_time_terminate = False
        return self

class maddpg:
    """ Implementation of Multi-agent DDPG (MADDPG)

    The original paper is available at #TODO#
    Here, instead of following the existing implementation at https://github.com/openai/maddpg/tree/master/maddpg
    which is basde on TensorFlow, we re-implement the model utilizing Stable-Baseline 3, constructed
    on PyTorch. Meanwhile, the underlying DDPG algorithm are replaced by TD3. 

    Args: 
        #TODO#
    """
    def __init__(self, 
        policy: Union[str, Type[TD3Policy]],
        env: Union[GymEnv, str]) -> None:
        self.__env    = env
        self.__policy = policy
        #TODO
        pass

    def learn(self, total_timesteps = 10000) -> None:
        """ Learn from the environment using the policy

        Args
            total_timesteps: learn for how many timesteps
        """
        #TODO
        pass

    @property
    def env(self) -> GymEnv:
        """ Get the underlying environment for the model

        Returns: 
            the iteractive GYM environment
        """
        if isinstance(self.__env, str):
            return gym.make(self._env)
        return self.__env

    def predict(self, observation: np.ndarray) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Get the model's action(s) from an observation

        Args
            observation:    The input observation

        Returns
            The model's action and the next state
            (used in recurrent policies)
        """
        #TODO
        pass

    def execute(self, num_of_step: int) -> agents:
        """ Execute the policy in the environment
        
        Get a iterator over the environment, which continuously instructs all the agents to
        interacts with the environment. 

        Args: 
            num_of_step: stop the execution after how many steps

        Returns: 
            An iterator over the agent
        """
        return iter(agents(self, self.__env, num_of_step, max_steps=2*num_of_step))