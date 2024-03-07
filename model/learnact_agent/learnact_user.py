import copy
import os

import pandas as pd

from aux_func.aux_func import (
    execute,
    insert_global_env,
    get_func_argument_name,
)
from backbone.gpt import num_tokens_from_messages
from model.zero_py_agent import py_agent


class learnact_user(py_agent):

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
        init_prompt_dict_no_tool,
        action_wrapper_no_tool,
        parsering_func=None,
        grounding=False,
        world_model=False,
        given_plan=False,
        need_goal=True,
        check_actions="check valid actions",
        check_inventory=None,
        use_reward=False,
        use_parser=True,
        max_context_length=8192,
        tool_dir="",
        use_hand_tool=False,
        react=False,
        example_order="origin_first",
        usage_version="individual",
        note_position="before_example",
        error_action_info="not valid",
        no_tool_description=False,
        full_tool_subprocess=False,
    ):
        super().__init__(
            backbone_func=backbone_func,
            model_size=model_size,
            sys_prompt=sys_prompt,
            dataset_prompt=dataset_prompt,
            max_steps=max_steps,
            memory_size=memory_size,
            init_prompt_dict=init_prompt_dict,
            action_wrapper=action_wrapper,
            parsering_func=parsering_func,
            grounding=grounding,
            world_model=world_model,
            given_plan=given_plan,
            need_goal=need_goal,
            check_actions=check_actions,
            check_inventory=check_inventory,
            use_reward=use_reward,
            use_parser=use_parser,
            max_context_length=max_context_length,
            only_action=(not react),
        )
        self.tool_dir = tool_dir
        self.use_hand_tool = use_hand_tool
        self.init_prompt_dict_no_tool = init_prompt_dict_no_tool
        self.action_wrapper_no_tool = action_wrapper_no_tool
        self.tools = None
        self.select_success = True
        self.example_order = example_order
        self.usage_version = usage_version
        self.note_position = note_position
        self.no_tool_description = no_tool_description
        self.full_tool_subprocess = full_tool_subprocess

        assert self.note_position in [
            "before_example",
            "after_example",
            "after_goal",
            "no",
        ]

        self.error_action_info = error_action_info

    def update_tool(self, tool):
        self.tools = tool

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
        zero_shot_scene=False,
        tool_reflection=None,
    ):
        query = ""
        query += (
            self.split["instruction"][0] + instruction +
            self.split["instruction"][-1]
        )

        if (
            tool_reflection is not None
            and len(tool_reflection) > 0
            and self.note_position == "before_example"
        ):
            query += (
                "Here are the notations of the actions:\n"
                + "\n".join(tool_reflection)
                + "\n"
            )

        if isinstance(examples, str):
            examples = [examples]

        if len(examples) > 0:
            query += "\nHere are examples:\n" + self.split["example"][0]
            for example in examples:
                query += example.strip("\n") + "\n\n"
            query += self.split["example"][-1]

        if (
            tool_reflection is not None
            and len(tool_reflection) > 0
            and self.note_position == "after_example"
        ):
            query += (
                "Here are the notations of the actions:\n"
                + "\n".join(tool_reflection)
                + "\n"
            )

        if zero_shot_scene:
            return query

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

        if (
            tool_reflection is not None
            and len(tool_reflection) > 0
            and self.note_position == "after_goal"
        ):
            query += (
                "Here are the notations of the actions:\n"
                + "\n".join(tool_reflection)
                + "\n"
            )
        # ```````````````````` The modification to py_agent version

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

    def run(
        self,
        action_space=None,
        world_model=None,
        plan=None,
        grounding_fn=None,
        zero_shot_scene=False,
    ):
        # note that these configs are originally provided when initialized, but you can choose to override them here with parameters

        # self.init_prompt_dict = init_prompt_dict

        # ```````````````````` The modification to py_agent version

        tools = self.tools
        if tools is None:
            if os.path.exists(self.tool_dir):
                tools = pd.read_csv(self.tool_dir)
        if tools is not None and len(tools) > 0:
            if self.select_success:
                tools = (
                    tools[(tools["success"] > 0) & (tools["usable"])]
                    if "usable" in tools
                    else tools[(tools["success"] > 0)]
                )
            else:
                if "usable" in tools:
                    tools = tools[tools["usable"]]

        # ```````````````````` The modification to py_agent version # instruction depends on the tools
        tool_reflection = []

        if (tools is None or len(tools) == 0) and (not self.use_hand_tool):
            instruction = self.init_prompt_dict_no_tool["instruction"]
            examples = copy.deepcopy(self.init_prompt_dict_no_tool["examples"])
            system_message = self.init_prompt_dict_no_tool["system_msg"]
        else:
            instruction = self.init_prompt_dict["instruction"]
            examples = copy.deepcopy(self.init_prompt_dict["examples"])
            system_message = self.init_prompt_dict["system_msg"]

            if not self.use_hand_tool:
                tools_prompt = ""
                examples_tools = []
                for _, tool_line in tools.iterrows():
                    func_argument_name = get_func_argument_name(
                        tool_line["tool"], tool_line["func_name"]
                    )
                    tools_prompt += "    " + func_argument_name
                    if not self.no_tool_description:
                        tools_prompt += ": " + tool_line["description"] + "\n"
                    else:
                        tools_prompt += "\n"
                    if tool_line["usage"] is not None and (
                        not pd.isna(tool_line["usage"])
                    ):
                        examples_tools.append(
                            tool_line["usage"].strip("\n") + "\n")
                    if (
                        "reflection" in tool_line
                        and tool_line["reflection"] is not None
                        and (not pd.isna(tool_line["reflection"]))
                    ):
                        # assert reflection is list
                        reflection = eval(str(tool_line["reflection"]))
                        if len(reflection) > 0:
                            tool_reflection.append(
                                func_argument_name
                                + ": "
                                + " ".join(reflection).strip("\n")
                                + "\n"
                            )
                if self.usage_version != "individual":
                    examples_tools = (
                        [examples_tools[-1]] if len(examples_tools) > 0 else []
                    )  # -1 make sure to use the last update of examples in together setting
                instruction = instruction.format(tools_prompt)
                if self.example_order == "origin_first":
                    examples = examples + examples_tools
                elif self.example_order == "tool_first":
                    examples = examples_tools + examples
                elif self.example_order == "no":
                    examples = examples
                else:
                    raise ValueError(
                        "example_order {} Not implied yet".format(
                            self.example_order)
                    )

        # ```````````````````` The modification to py_agent version: zero_shot_scene
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
            zero_shot_scene=zero_shot_scene,
            tool_reflection=tool_reflection,
        )
        if zero_shot_scene:
            return None, input_prompt

        # ```````````````````` The modification to py_agent version: human play
        human_play = False
        # ```````````````````` The modification to py_agent version: human play
        if not human_play:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": input_prompt},
            ]

            action, _ = self.backbone_func(messages, stop=["\n"])

        if self.use_parser:
            action_type, action = self.action_parser_for_special_llms(action)

        return action_type, action

    def execute_code_action(self, env, action, raise_error=False):
        # ```````````````````` The modification to py_agent version
        last_histoty_length = len(env.infos["history"])
        last_states_length = len(env.infos["states"])
        state_pre_step = env._get_obs()

        tools = self.tools
        if tools is None:
            if os.path.exists(self.tool_dir):
                tools = pd.read_csv(self.tool_dir)
        if tools is not None and len(tools) > 0:
            if self.select_success:
                tools = (
                    tools[(tools["success"] > 0) & (tools["usable"])]
                    if "usable" in tools
                    else tools[(tools["success"] > 0)]
                )
            else:
                if "usable" in tools:
                    tools = tools[tools["usable"]]

        # ```````````````````` The modification to py_agent version # wrap code by defined interface
        if (tools is None or len(tools) == 0) and (not self.use_hand_tool):
            wrapper = self.action_wrapper
            # wrapper = self.action_wrapper_no_tool
        else:
            wrapper = self.action_wrapper
            if not self.use_hand_tool:
                tools_func = ""
                for _, tool_line in tools.iterrows():
                    tools_func += insert_global_env(tool_line["tool"]) + "\n"
                wrapper = wrapper + "\n" + tools_func

        code = wrapper + "\n" + action
        global_vars = {"env": env}

        try:
            res = execute(code, global_env=global_vars)
            env = res["env"]
            state, reward, done, infos = env._get_obs(), env.reward, env.done, env.infos
            success = True
        except Exception as e:
            if raise_error:
                raise e
            state, reward, done, infos = env._get_obs(), env.reward, env.done, env.infos
            state = "The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions."
            # env = env_back_up
            # state, reward, done, infos = env.step(action)
            success = False

        # ```````````````````` The modification to py_agent version
        new_states = env.infos["states"][last_states_length:]
        new_history = env.infos["history"][last_histoty_length:]
        if not self.full_tool_subprocess:
            if self.error_action_info in state:
                last_success_state = ""
                for state_pre in new_states[::-1]:
                    if self.error_action_info not in state_pre:
                        last_success_state = state_pre
                        break
                if len(last_success_state) > 0:
                    state = state + " " + last_success_state
        else:
            full_tool_subprocess = ""
            for state_pre in new_states:
                if self.error_action_info not in state_pre:
                    full_tool_subprocess += state_pre
            if len(full_tool_subprocess) > 0:
                if self.error_action_info in state:
                    state = state + " " + full_tool_subprocess
                else:
                    state = full_tool_subprocess
        infos["new_history"] = new_history

        # ```````````````````` The modification to py_agent version: return invalid action for no-change-state
        if state == state_pre_step:
            state = "The action is not valid and does not change any state. Please remember to satisfy the restriction of actions. You can also check valid actions."

        return env, state, reward, done, infos

    def execute_action(self, env, action_type, action):
        # ```````````````````` The modification to py_agent version
        if action_type in ["Think:", "think:", "Think", "think"]:
            state, reward, done, infos = env._get_obs(), env.reward, env.done, env.infos
            state = "Ok."
        else:
            env, state, reward, done, infos = self.execute_code_action(
                env, action)
        return env, state, reward, done, infos

    def __call__(self, problem_input, zero_shot_scene=False, **kwargs):

        # ```````````````````` The modification to py_agent version: variable name problem_input
        env = problem_input

        game_name = env.game_name
        init_obs = env._get_obs()
        goal = env._get_goal()
        self.reset(goal, init_obs)

        env_details = {"game_name": game_name, "goal": goal}

        print("Goal: {}".format(self.goal))
        print("Init obs: {}".format(self.init_obs))

        # max_steps = self.max_num_steps
        reward = 0.0
        last_reward = 0.0
        grounding_acc_count = 0
        score_change_record = []

        last_state = init_obs
        reward = 0.0
        done = False

        # ```````````````````` The modification to py_agent version: history record
        history = []
        history.append({"Goal": goal, "Observation": init_obs, "id": 0})

        query_zero_shot = None

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

            if self.given_plan:
                given_plan_hint = self.given_plan_annotation[id]
            else:
                given_plan_hint = None

            # ```````````````````` The modification to py_agent version: zero_shot_scene
            if query_zero_shot is None:
                _, query_zero_shot = self.run(
                    action_space=action_space,
                    world_model=world_model_hint,
                    plan=given_plan_hint,
                    zero_shot_scene=True,
                )
            if zero_shot_scene:
                return query_zero_shot
            action_type, action = self.run(
                action_space=action_space,
                world_model=world_model_hint,
                plan=given_plan_hint,
                zero_shot_scene=zero_shot_scene,
            )

            # if not success:
            #     break
            print("{} {}:{}".format(action_type, step_id, action))

            # ```````````````````` The modification to py_agent version: history record
            step_record = {action_type: action, "id": step_id}

            env, state, reward, done, infos = self.execute_action(
                env, action_type, action
            )

            step_record["Observation"] = state
            step_record["Reward"] = reward

            if "new_history" in infos:
                step_record["Failed_subprocess"] = infos["new_history"]
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
                        "query_zero_shot": query_zero_shot,
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
                "query_zero_shot": query_zero_shot,
            },
        }
