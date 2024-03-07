import gym
import subprocess
import os
import re
import numpy as np


class BaseEnvironment(gym.Env):
    def __init__(self):
        super().__init__()

    def _get_info(self):
        pass

    def _get_obs(self):
        pass

    def _get_goal(self):
        pass

    def _get_history(self):
        pass

    def _get_action_space(self):
        pass

    def _is_done(self):
        pass

    def update(self, action, obs, reward, done, infos):
        pass

    def reset(self):
        pass

    def step(self, action):
        pass

    def save_log(self, log_path):
        pass

    @classmethod
    def from_config(cls, config):
        pass