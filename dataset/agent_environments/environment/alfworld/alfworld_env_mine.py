from common.registry import registry
import alfworld
import alfworld.agents.environment
import pdb
import yaml
import random
import jsonlines
import re
from aux_func import copy
import os

AlfWorld_PREFIXES = {
    'pick_and_place': 'put',
    'pick_clean_then_place': 'clean',
    'pick_heat_then_place': 'heat',
    'pick_cool_then_place': 'cool',
    'look_at_obj': 'examine',
    'pick_two_obj': 'puttwo'
}

AlfWorld_Reverse_PREFIXES = {
    'put': 'pick_and_place',
    'clean': 'pick_clean_then_place',
    'heat': 'pick_heat_then_place',
    'cool': 'pick_cool_then_place',
    'examine': 'look_at_obj',
    'puttwo': 'pick_two_obj'
}


@registry.register_environment("alfworld")
class AlfWorld:
    def __init__(self,
                 split,
                 base_config,
                 batch_size,
                 seed,
                 task_type=None,
                 id=None,
                 file_path=None
                 ):
        self.split = split
        self.base_config = base_config
        self.batch_size = batch_size
        self.seed = seed
        self.task_type = task_type
        self.id = id

        with open(base_config) as reader:
            config = yaml.safe_load(reader)

        # given the file path, directly use the path as the environment;
        if file_path is not None:
            config_copy = copy.deepcopy(config)
            config_copy['dataset']['eval_ood_data_path'] = os.path.split(file_path)[
                0]
            env = getattr(alfworld.agents.environment, config["env"]["type"])(
                config_copy, train_eval=split)
            self.file_path = file_path
        else:
            env = getattr(alfworld.agents.environment, config["env"]["type"])(
                config, train_eval=split)
            env.game_files.sort()
            if task_type is not None:
                type_files = []
                for file in env.game_files:
                    # the file form is xxx/pick_cool_then_place_in_recepxxx/trial_xxx/game.tw-pddl
                    if file.split('/')[-3].startswith(task_type):
                        type_files.append(file)
                if len(type_files) == 0:
                    raise ValueError(
                        "task type {} not found in file".format(task_type))
            # set the environment to certain id one
            if id is not None:
                file_path = type_files[id]
                env.game_files = [file_path]

            self.file_path = file_path

        self.env = env.init_env(batch_size)

        self.valid_actions = []
        self.init_obs = ''
        self.done = False
        self.env_ob = self.init_obs
        self.finished_sub_goal = []
        self.labeled_data = {}
        self.sub_goal = []
        self.planning = ''
        self.world_model = ''
        # with open(label_path, 'r+', encoding='utf-8') as f:
        #     for item in jsonlines.Reader(f):
        #         self.labeled_data[item["name"]] = item
        random.seed(seed)
        self.cur_task_name = ""
        self.reward = 0.
        self.game_name = task_type

        self.reset()

        # self.env.batch_env.env_fns[0].args[2][0]._wrapped_env._wrapped_env.state = dict(
        #     self.env.batch_env.env_fns[0].args[2][0]._wrapped_env._wrapped_env.state)

    def reset(self):

        ob, info = self.env.reset()
        # self.env.batch_env.env_fns[0].args[2][0]._wrapped_env._wrapped_env.state = dict(
        #     self.env.batch_env.env_fns[0].args[2][0]._wrapped_env._wrapped_env.state)

        self.valid_actions = info["admissible_commands"][0]

        # self.init_obs = ob[0]
        # ob = '\n'.join(ob[0].split('\n\n')[1:])

        self.init_obs = ('\n'.join(ob[0].split('\n\n')[1:])).split('\n')[0]
        self.goal = ('\n'.join(ob[0].split('\n\n')[1:])).split('\n')[1]
        self.env_ob = self.init_obs
        self.cur_task_name = '/'.join(info['extra.gamefile']
                                      [0].split('/')[-3:-1])
        # self.sub_goal = self.labeled_data[self.cur_task_name]["label"]
        # self.planning = self.labeled_data[self.cur_task_name]["planning"]
        # self.world_model = self.labeled_data[self.cur_task_name]["world_model"]
        self.finished_sub_goal = [0 for i in range(len(self.sub_goal) + 1)]

        self.reward = 0
        self.done = False

        self.infos = dict()  # record last step info
        self.states = [self.init_obs]  # record a stream of states
        # record a stream of s0, a0, r0, s1, a1, r1, ...
        self.history = [("state", self.init_obs)]
        self.steps = 0

        self.infos["goal"] = self.goal
        self.infos["states"] = self.states
        self.infos["history"] = self.history
        self.infos["steps"] = self.steps
        self.infos["state"] = self.states[-1]

        return ob, info

    def step(self, action):
        info = None
        done = self.done
        if action.endswith('.'):
            action = action[:-1]
        if action == "look":
            observation, _, done, info = self.env.step([action])
            observation = [self.env_ob]
            done = done[0]
        elif action == "check valid actions":
            valid_actions = ", ".join(self.valid_actions)
            observation = [
                f"Choose an action from these valid actions: {valid_actions}"]
      #  elif action not in self.valid_actions:
      #      observation = "Your action is invalid. Please change a new one."
      #      return observation, self.reward, done, info
        else:
            observation, _, done, info = self.env.step([action])
            done = done[0]
        if "go to" in action or "open" in action:
            if "Nothing happens" not in observation[0]:
                self.env_ob = observation[0]
        if info:
            self.valid_actions = info["admissible_commands"][0]
        observation = self._process_ob(observation[0])
        self.done = done
        self._check_temperature_string(
            s=observation, selected_obs=self.sub_goal)
        self.reward = self._get_reward()

        self.update_info(action, observation)

        return observation, self.reward, done, self.infos

    def GetPlanning(self):
        return self.planning

    def GetWorldModel(self):
        return self.world_model

    def _process_ob(self, ob):
        if ob.startswith('You arrive at loc '):
            ob = ob[ob.find('. ') + 2:]
        if "Nothing happens" in ob:
            ob = 'The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.'
        return ob

    def _get_reward(self):
        if self.done:
            return 1.0
        else:
            return sum(self.finished_sub_goal) * 1.0 / len(self.finished_sub_goal)

    def _get_action_space(self):
        if "look" not in self.valid_actions:
            self.valid_actions.append("look")
        if "check valid actions" not in self.valid_actions:
            self.valid_actions.append("check valid actions")

        return self.valid_actions

    def _check_temperature_string(self, s, selected_obs):
        for i, pattern in enumerate(selected_obs):
            # if self.finished_sub_goal[i] == 1.:
            #    continue
            match = re.search(pattern, s)
            if match:
                self.finished_sub_goal[i] = 1.

    def GetValidActions(self):
        if "look" not in self.valid_actions:
            self.valid_actions.append("look")
        if "check valid actions" not in self.valid_actions:
            self.valid_actions.append("check valid actions")

        return self.valid_actions

    @classmethod
    def from_config(cls, cfg):
        split = cfg.get("split", "eval_out_of_distribution")
        base_config = cfg.get("base_config", "base_config.yaml")
        batch_size = cfg.get("batch_size", 1)
        seed = cfg.get("seed", 0)
        label_path = cfg.get(
            "label_path", "data/alfworld/alfworld_label.jsonl")
        env = cls(split=split,
                  base_config=base_config,
                  batch_size=batch_size,
                  seed=seed,
                  label_path=label_path)
        return env

    def _get_info(self):
        return self.infos

    def _get_obs(self):
        return self.states[-1]

    def _get_goal(self):
        return self.goal

    def _get_history(self):
        return self.history

        # update the environment after taking an action
    def update(self, action, obs, reward, done, infos):
        for k, v in infos.items():
            self.infos[k] = v

        # check if won by checking if the goal is satisfied
        goal_literals = self.infos["goal_literal"].literals
        obs_literals = self.last_obs.literals
        self.won = True
        for literal in goal_literals:
            if literal not in obs_literals:
                self.won = False
                break

        self.steps += 1

        self.reward = reward
        self.done = done

        if self.won:
            obs += " The goal is satisfied."

        self.history.append(("action", action))
        self.history.append(("reward", reward))
        self.history.append(("state", obs))
        self.states.append(obs)

        self.infos["goal"] = self.goal
        self.infos["states"] = self.states
        self.infos["history"] = self.history
        self.infos["steps"] = self.steps
        self.infos["state"] = self.states[-1]

    def update_info(self, action, info):
        self.history.append(("action", action))
        self.history.append(("reward", self.reward))
        self.history.append(("state", info))
        self.states.append(info)

        self.steps += 1

        self.infos["goal"] = self.goal
        self.infos["states"] = self.states
        self.infos["history"] = self.history
        self.infos["steps"] = self.steps
        self.infos["state"] = self.states[-1]

    def __deepcopy__(self, memo):
        # Create a new instance with a deeply copied state

        new_instance = AlfWorld(self.split,
                                self.base_config,
                                self.batch_size,
                                self.seed,
                                self.task_type,
                                self.id,
                                self.file_path)
        for item in self.history:
            if item[0] == 'action':
                new_instance.step(item[1])

        return new_instance
