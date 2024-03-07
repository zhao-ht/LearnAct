from model.zero_py_agent import py_agent


class react_py_agent(py_agent):

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
        use_plan="False",
        use_plan_number=None,
        plan_dir="",
    ):
        # only_action is specified
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
            only_action=False,
            use_plan=use_plan,
            use_plan_number=use_plan_number,
            plan_dir=plan_dir,
        )

    def execute_action(self, env, action_type, action):
        # This step should be replaced by python code execution
        if action == self.check_actions:
            state, reward, done, infos = env.step(action)
        elif action_type in ["Think:", "think:", "Think", "think"]:
            state, reward, done, infos = env._get_obs(), env.reward, env.done, env.infos
            state = "Ok."
        else:
            try:
                env, state, reward, done, infos = self.execute_code_action(env, action)
            except:
                state, reward, done, infos = env.step(action)
        return env, state, reward, done, infos
