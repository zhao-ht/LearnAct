import json
import os
from aux_func.aux_func import execute
from backbone.gpt import num_tokens_from_messages
from aux_func import copy

# the agent should receive goal, state and action (reward optional), then return the next state
import pandas as pd


class py_agent:

    def __init__(
        self,
        backbone_func,
        model_size,
        sys_prompt,
        dataset_prompt,
        max_steps,
        memory_size,
        init_prompt_dict,
        action_wrapper,
        parsering_func=None,
        grounding=False,
        world_model=False,
        given_plan=None,
        need_goal=True,
        check_actions="check valid actions",
        check_inventory=None,
        use_reward=False,
        use_parser=True,
        max_context_length=8192,
        only_action=True,
        use_plan=False,
        use_plan_number=None,
        plan_dir="",
    ):
        self.backbone_func = backbone_func
        self.model_size = model_size
        self.sys_prompt = sys_prompt
        self.dataset_prompt = dataset_prompt
        self.parsering_func = parsering_func
        self.max_steps = max_steps
        self.init_prompt_dict = init_prompt_dict
        self.split = {
            "example": [""],
            "text": [""],
            "rule": [""],
            "system_msg": [""],
            "instruction": [""],
            "goal": [""],
        }
        self.grounding = grounding
        self.world_model = world_model
        self.use_plan = use_plan
        self.use_plan_number = use_plan_number
        self.given_plan = given_plan
        self.plan_dir = plan_dir
        self.need_goal = need_goal
        self.check_actions = (
            "check valid actions" if check_actions is not None else None
        )
        self.check_inventory = check_inventory
        self.use_reward = use_reward
        if memory_size is None:
            self.memory_size = max_steps + 10
        else:
            self.memory_size = memory_size
        self.use_parser = use_parser
        self.action_wrapper = action_wrapper
        self.max_context_length = max_context_length
        # if only action, prompt will end with "Action:"; else not. No matter with "Action" or not, the result can be parsered.
        self.only_action = only_action

    def reset(self, goal, init_obs, init_act=None):
        self.goal = goal
        self.init_obs = init_obs
        self.memory = (
            [("Action", init_act), ("Observation", self.init_obs)]
            if init_act
            else [("Observation", self.init_obs)]
        )  # list of [('State', "xxx"), ('Action', "xxx"), ('Reward', "xxx") ...]
        self.steps = 0
        self.reward = 0
        self.same_reward_count = 0
        self.done = False

    def update_plan(self, plan_df):
        self.given_plan = plan_df

    def update(self, action_type, action, state, reward=None):
        self.steps += 1

        self.memory.append((action_type, action))
        self.memory.append(("Observation", state))

        if self.use_reward:
            # compare the current reward with the previous reward, if it is the same, concate ", it is the same as the previous reward which means you make no progress", if it is larger, concate ", it is larger than the previous reward which means you make progress". If same more than 5 times, concate ", you are stuck and should try a different plan."
            if reward == self.reward:
                self.same_reward_count += 1
                if self.same_reward_count > 5:
                    self.memory.append(
                        (
                            "Reward",
                            str(reward)
                            + ", you are stuck and should try a different plan",
                        )
                    )
                else:
                    self.memory.append(
                        (
                            "Reward",
                            str(reward)
                            + ", it is the same as the previous reward which means you make no progress",
                        )
                    )
            elif reward > self.reward:
                self.memory.append(
                    (
                        "Reward",
                        str(reward)
                        + ", it is larger than the previous reward which means you make progress",
                    )
                )
            else:
                raise ValueError("The reward should always increase!")
            # self.memory.append(("Reward", str(reward)))
            self.reward = reward

    def make_prompt(
        self,
        action_space=None,
        world_model=None,
        plan=None,
        need_goal=False,
        check_actions="check valid actions",
        check_inventory="inventory",
        system_message="",
        instruction="",
        examples=[],
        goal="",
    ):
        query = ""
        query += (
            self.split["instruction"][0] + instruction +
            self.split["instruction"][-1]
        )

        if isinstance(examples, str):
            examples = [examples]

        if len(examples) > 0:
            query += "\nHere are examples:\n" + self.split["example"][0]
            for example in examples:
                query += example + "\n"
            query += self.split["example"][-1]
        if need_goal:
            query += (
                self.split["goal"][0]
                + "You should perform actions to accomplish the goal: "
                + goal
                + "\n"
                + self.split["goal"][-1]
            )
        if check_actions is not None:
            # query += "You should use the following commands for help when your action cannot be understood: check valid actions\n"
            query += (
                "You should use the following commands for help when your action cannot be understood: "
                + check_actions
                + "\n"
            )
        if check_inventory is not None:
            query += "You should use the following commands for help when your action cannot be understood: inventory\n"
        if self.use_reward:
            query += "You should try to maximize the reward. It is a score between 0 and 1. If your score improves, it means you are making progress and on the right track. However, if your score does not change after many steps, it means you are stuck and should try a different plan.\n"
        if world_model is not None:
            query += (
                "Here are some important knowledge you should know about the environment you interact with: "
                + world_model
                + "\n"
            )
        if plan is not None:
            query += "Your action should follow this high level plan: " + plan + "\n"

        history = self.memory[-self.memory_size:]
        input_prompt = query + \
            "\n".join([item[0] + ": " + item[1] for item in history])

        if action_space is not None:
            input_prompt += (
                "\nValid actions for this step include: "
                + ", ".join(action_space)
                + "\n"
            )

        # if "codellama" in self.llm_model.model.lower():
        #     input_prompt += "\nWhat is the action for next step?"
        if self.only_action:
            input_prompt += "\nAction: "

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_prompt},
        ]
        num_of_tokens = num_tokens_from_messages(messages, self.model_size)
        while num_of_tokens > self.max_context_length:
            print("Warning! history are reduced due to length limitation")
            history = history[1:]
            input_prompt = query + "\n".join(
                [item[0] + ": " + item[1] for item in history]
            )

            if action_space is not None:
                input_prompt += (
                    "\nValid actions for this step include: "
                    + ", ".join(action_space)
                    + "\n"
                )

            input_prompt += "\nAction: "
            # input_prompt += "\nPlease enter your action:"
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": input_prompt},
            ]
            num_of_tokens = num_tokens_from_messages(messages, self.model_size)

        return input_prompt

    def action_parser_for_special_llms(self, action):
        action = action.split("\n")[0]
        action_type = "Action"
        origin_action = action
        if "action" in action.lower():
            action_temp = action.split("\n")
            for act in action_temp:
                if (
                    "next action" in act and ":" in act
                ):  # zzh: in Claude will return "Here is the next action to take:"
                    idx = action_temp.index(act)
                    while idx + 1 < len(action_temp):
                        if action_temp[idx + 1]:
                            action = action_temp[idx + 1]
                            break
                        idx += 1
                # chang: in case parse tool output
                if act.split(":")[0].lower().endswith("with action input"):
                    action = act
                    break
                if "action" in act.lower() and ":" in act:
                    action_temp = ":".join(act.split(":")[1:])
                    if action_temp != "":
                        action = action_temp
                        break
                if "action" in act.lower() and "is to" in act:
                    action_temp = act.split("is to")[1]
                    if action_temp != "":
                        action = action_temp
                        break

        elif action.split(" ")[0] in ["Think:", "think:", "Think", "think"]:
            action_type = "Think"
            action_temp = ":".join(action.split(":")[1:]).strip()
            action = action_temp

        if action.strip() == "":
            # temperary comment this line for codellama
            action = origin_action.split("\n")[0]
        action = action.strip()
        action = action.split("\n")[0]
        if action_type == "Action":
            action = action.strip(".")
        return action_type, action

    def run(self, action_space=None, world_model=None, plan=None, grounding_fn=None):
        # note that these configs are originally provided when initialized, but you can choose to override them here with parameters

        # self.init_prompt_dict = init_prompt_dict
        instruction = self.init_prompt_dict["instruction"]
        examples = self.init_prompt_dict["examples"]
        system_message = self.init_prompt_dict["system_msg"]
        input_prompt = self.make_prompt(
            action_space=action_space,
            world_model=world_model,
            plan=plan,
            need_goal=self.need_goal,
            check_actions=self.check_actions,
            check_inventory=self.check_inventory,
            system_message=system_message,
            instruction=instruction,
            examples=examples,
            goal=self.goal,
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_prompt},
        ]

        human_do = False
        if not human_do:
            action, _ = self.backbone_func(messages, stop=["\n"])

        if self.use_parser:
            action_type, action = self.action_parser_for_special_llms(action)

        return action_type, action

    def execute_code_action(self, env, action):
        code = self.action_wrapper + "\n" + action
        global_vars = {"env": env}
        res = execute(code, global_env=global_vars, time_limit_query=10000)
        env = res["env"]
        state, reward, done, infos = env._get_obs(), env.reward, env.done, env.infos
        return env, state, reward, done, infos

    def execute_action(self, env, action_type, action, raise_error=False):
        # This step should be replaced by python code execution
        if action == self.check_actions:
            state, reward, done, infos = env.step(action)
        else:

            try:
                env, state, reward, done, infos = self.execute_code_action(
                    env, action)

            except Exception as e:
                if raise_error:
                    raise e

                state, reward, done, infos = env.step(action)
                success = False
        return env, state, reward, done, infos

    def save_log(self, log_path):
        history = self.memory
        with open(log_path, "w") as f:
            for item in history:
                item_name = item[0]
                item_content = item[1]
                if item_content is None:
                    continue
                f.write(item_name + ": " + str(item_content) + "\n")

    @classmethod
    def from_config(cls, llm_model, config):
        memory_size = config.get("memory_size", 100)
        use_reward = config.get("use_reward", False)
        # goal = config.get("goal", None)
        # init_obs = config.get("init_obs", None)

        instruction = config.get("instruction", "")
        examples = config.get("examples", [])
        init_prompt_path = config.get("init_prompt_path", None)
        system_message = config.get(
            "system_message", "You are a helpful assistant.")
        need_goal = config.get("need_goal", False)
        check_actions = config.get("check_actions", None)
        check_inventory = config.get("check_inventory", None)
        use_parser = config.get("use_parser", True)
        return cls(
            llm_model,
            memory_size,
            use_reward,
            examples,
            instruction,
            init_prompt_path,
            system_message,
            need_goal,
            check_actions,
            check_inventory,
            use_parser,
        )

    def __call__(self, problem_input, **kwargs):

        env = problem_input

        game_name = env.game_name
        init_obs = env._get_obs()
        goal = env._get_goal()
        self.reset(goal, init_obs)

        env_details = {"game_name": game_name, "goal": goal}

        print("Goal: {}".format(self.goal))
        print("Init obs: {}".format(self.init_obs))

        reward = 0.0
        last_reward = 0.0
        grounding_acc_count = 0
        score_change_record = []

        last_state = init_obs
        reward = 0.0
        done = False

        history = []
        history.append({"Goal": goal, "Observation": init_obs, "id": 0})

        for step_id in range(self.max_steps):
            if self.grounding:
                action_space = env._get_action_space()
            else:
                action_space = None

            if self.world_model:
                world_model_hint = self.world_model_annotation[game_name]
                # world_model_hint += "If you repeat the same action, you will not get any new information."
            else:
                world_model_hint = None

            if self.use_plan:
                given_plan = self.given_plan
                if given_plan is None:
                    if os.path.exists(self.plan_dir):
                        given_plan = pd.read_csv(self.plan_dir)

                if given_plan is not None and len(given_plan) > 0:
                    if self.use_plan_number is None:
                        given_plan_hint = "\n".join(
                            [
                                item.strip("\n")
                                for item in given_plan["reflexion"].values.tolist()
                            ]
                        )
                    else:
                        given_plan_hint = "\n".join(
                            [
                                item.strip("\n")
                                for item in given_plan["reflexion"].values.tolist()[
                                    0: min(len(given_plan), self.use_plan_number)
                                ]
                            ]
                        )
                else:
                    given_plan_hint = None
            else:
                given_plan_hint = None

            action_type, action = self.run(
                action_space=action_space,
                world_model=world_model_hint,
                plan=given_plan_hint,
            )

            # if not success:
            #     break
            print("{} {}:{}".format(action_type, step_id, action))
            # history.append({action_type: action, "id": step_id})
            step_record = {action_type: action, "id": step_id}

            env, state, reward, done, infos = self.execute_action(
                env, action_type, action
            )

            step_record["Observation"] = state
            step_record["Reward"] = reward
            history.append(step_record)

            last_state = state

            if infos.get("action_is_valid", False):
                grounding_acc_count += 1

            if reward > last_reward:
                score_change_record.append((step_id, reward))
            last_reward = reward

            print("Step {}: State: {}".format(step_id, state))
            print(
                "Step {}: Reward: {}, Is done: {}".format(
                    step_id, round(reward, 3), done
                )
            )
            self.update(action_type, action, state, reward)
            if done:

                return {
                    "res": env.done,
                    "gen": {
                        "reward": reward,
                        "steps": step_id + 1,
                        "grounding_acc": grounding_acc_count / (step_id + 1),
                        "score_change_record": score_change_record,
                        "history": history,
                    },
                }

        return {
            "res": False,
            "gen": {
                "reward": reward,
                "steps": None,
                "grounding_acc": grounding_acc_count / (step_id + 1),
                "score_change_record": score_change_record,
                "history": history,
            },
        }
