from model.zero_py_agent import (
    py_agent,
    py_agent_action_wrapper_dict,
    py_agent_prompt_dict,
)
from model.react_py_agent import (
    react_py_agent,
    react_py_agent_prompt_dict,
)
from model.learnact_agent import (
    learnact_user,
    learnact_learner,
    learnact_user_action_wrapper_dict,
    learnact_user_prompt_dict,
    learnact_learner_dataset_prompt,
    learnact_user_prompt_dict_no_tool,
)

from model.learnable_agent import learnable_agent

from model.reflexion_py_agent import reflexion_optimizer, reflexion_prompt
from model.code_as_policy import (
    code_as_policy,
    code_as_policy_prompt_dict,
    code_as_policy_prompt_hier_dict,
)


prompt_map = {}


def load_backbone(model_name, model_size, gpt_request=False):

    if model_name == "gpt":
        from backbone import gpt
    elif model_name == "llama":
        from backbone import llama
    elif model_name == "llama-2":
        from backbone import llama2
    else:
        raise ValueError('Unrecognized model_name "' + model_name + '"')

    if model_name == "gpt":
        if gpt_request:
            backbone_func = lambda x, **kwargs: gpt.call_chat_gpt_request(
                x, model_size=model_size, **kwargs
            )
        else:
            backbone_func = lambda x, **kwargs: gpt.call_chat_gpt(
                x, model_size=model_size, **kwargs
            )
    elif model_name == "llama":
        backbone_func = lambda x, **kwargs: llama.predict(
            x, model_size=model_size, **kwargs
        )
    elif model_name == "llama-2":
        backbone_func = lambda x, **kwargs: llama2.predict(
            x, model_size=model_size, **kwargs
        )
    else:
        raise ValueError("Unimplied base model name {}".format(model_name))

    return backbone_func


def get_max_context_length(model_name, model_size):
    if model_name == "gpt":
        if model_size == 'gpt-4':
            return 8192
        elif model_size in ["gpt-35", "gpt-3.5", "gpt-35-turbo", "gpt-3.5-turbo"]:
            # set the value according to your api type
            # return 8192
            return 4096
        else:
            raise ValueError(
                "Unimplied max length for model size {}".format(model_size))
    else:
        raise ValueError(
            "Unimplied max length for base model name {}".format(model_name))


class model_loader:
    def __init__(self, args):
        self.planning_method = args.planning_method
        self.dataset_name = args.dataset_name

        # load backbone function
        self.backbone_func = load_backbone(
            args.model_name, args.model_size, args.gpt_request
        )

        # default result recoder
        self.result_recoder = None

        if args.planning_method in ["py_agent"]:
            if args.eval_save_path is None:
                args.eval_save_path = f'eval_results/{args.planning_method}.{args.model_name}.{args.model_size}.{str(args.check_actions).replace(" ","_")}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'

            init_prompt_dict = py_agent_prompt_dict
            self.itf = py_agent(
                backbone_func=self.backbone_func,
                model_size=args.model_size,
                dataset_prompt="",
                sys_prompt="",
                max_steps=args.max_steps,
                memory_size=args.memory_size,
                check_actions=args.check_actions,
                init_prompt_dict=init_prompt_dict[args.dataset_name],
                action_wrapper=py_agent_action_wrapper_dict[args.dataset_name],
                max_context_length=get_max_context_length(
                    args.model_name, args.model_size)
            )

        elif args.planning_method in ["code_as_policy"]:
            if args.eval_save_path is None:
                args.eval_save_path = f'eval_results/{args.planning_method}.{args.model_name}.{args.model_size}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}.{args.hier}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'
            init_prompt_dict = (
                code_as_policy_prompt_hier_dict
                if args.hier
                else code_as_policy_prompt_dict
            )
            self.itf = code_as_policy(
                backbone_func=self.backbone_func,
                model_size=args.model_size,
                dataset_prompt="",
                sys_prompt="",
                init_prompt_dict=init_prompt_dict[args.dataset_name],
                action_wrapper=py_agent_action_wrapper_dict[args.dataset_name],
                hier=args.hier,
            )

        elif args.planning_method in ["react_py_agent"]:
            if args.eval_save_path is None:
                args.eval_save_path = f'eval_results/{args.planning_method}.{args.model_name}.{args.model_size}.{str(args.check_actions).replace(" ","_")}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'

            init_prompt_dict = react_py_agent_prompt_dict
            self.itf = react_py_agent(
                backbone_func=self.backbone_func,
                model_size=args.model_size,
                dataset_prompt="",
                sys_prompt="",
                max_steps=args.max_steps,
                memory_size=args.memory_size,
                check_actions=args.check_actions,
                init_prompt_dict=init_prompt_dict[args.dataset_name],
                action_wrapper=py_agent_action_wrapper_dict[args.dataset_name],
                max_context_length=get_max_context_length(
                    args.model_name, args.model_size)
            )

        elif args.planning_method in ["learnact_agent"]:
            # Set file path for learn, retrieve and eval
            if args.learner_method in ["learnact_learner"] and args.user_method in [
                "learnact_user"
            ]:
                if args.eval_save_path is None:
                    args.eval_save_path = f'eval_results/{args.planning_method}.{args.model_name}.{args.model_size}.{args.user_model_size}.{"hand" if args.use_hand_tool is not None else ""}.{str(args.check_actions).replace(" ","_")}.{args.react}.{args.optimizer_do_learn}.{args.tool_in_context_style}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}{"_hand_{}".format(args.use_hand_tool) if args.use_hand_tool is not None else ""}.{args.example_order}.{args.no_tool_description}.{args.full_tool_subprocess}.{args.no_tool_selfprompt}.{args.get_tool_version}.{args.get_tool_incontext_version}.{args.usage_version}.{args.same_usage}.{args.note_position}.{args.pass_optimizer}.{args.tool_improve_target}.{args.tool_improve_version}.{args.tool_improve_in_context_version}.{args.tool_improve_history}.{args.step_sample_number}.{args.optimize_iteration_number}.{args.score_type}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'
                if args.retrieve_file_path is None:
                    args.retrieve_file_path = f"learn_results/{args.planning_method}_{args.optimizer_do_learn}_{str(args.check_actions).replace(' ','_')}_{args.react}_{args.tool_in_context_style}_{args.model_size}.{args.user_model_size}/{args.dataset_name}_{args.example_order}_{args.no_tool_description}_{args.full_tool_subprocess}_{args.no_tool_selfprompt}_{args.get_tool_version}_{args.get_tool_incontext_version}_{args.usage_version}_{args.same_usage}_{args.note_position}_{args.pass_optimizer}_{args.tool_improve_target}_{args.tool_improve_version}_{args.tool_improve_in_context_version}_{args.tool_improve_history}_{args.step_sample_number}_{args.optimize_iteration_number}_{args.score_type}_{args.split_dataset_num[0]}_split_{args.split_file}.csv"
                    if args.exp_id_on_train:
                        args.retrieve_file_path = args.retrieve_file_path.rstrip(
                            ".csv"
                        ) + "_{}.csv".format(args.exp_id)
                args.learn_save_path = args.retrieve_file_path
            else:
                raise ValueError(
                    "Not supported combination {} and {}".format(
                        args.learner_method, args.user_method
                    )
                )

            if args.learner_method == "learnact_learner":
                learner_model = learnact_learner(
                    backbone_func=self.backbone_func,
                    dataset_prompt=learnact_learner_dataset_prompt[args.dataset_name],
                    learn_path=args.retrieve_file_path,
                    optimizer_do_learn=args.optimizer_do_learn,
                    pass_optimizer=args.pass_optimizer,
                    tool_in_context_style=args.tool_in_context_style,
                    get_tool_version=args.get_tool_version,
                    get_tool_incontext_version=args.get_tool_incontext_version,
                    usage_version=args.usage_version,
                    tool_improve_target=args.tool_improve_target,
                    tool_improve_version=args.tool_improve_version,
                    tool_improve_in_context_version=args.tool_improve_in_context_version,
                    tool_improve_history=args.tool_improve_history,
                    step_sample_number=args.step_sample_number,
                    optimize_iteration_number=args.optimize_iteration_number,
                    score_type=args.score_type,
                    same_usage=args.same_usage,
                    learn_save_path=args.learn_save_path,
                )
            else:
                raise ValueError(
                    "Not supported learner method {}".format(
                        args.learner_method)
                )

            if args.user_method == "learnact_user":

                init_prompt_dict = learnact_user_prompt_dict
                init_prompt_dict_no_tool = (
                    learnact_user_prompt_dict_no_tool
                    if args.no_tool_selfprompt
                    else py_agent_prompt_dict
                )

                action_wrapper_dict = learnact_user_action_wrapper_dict

                user_model = learnact_user(
                    backbone_func=load_backbone(
                        args.model_name, args.user_model_size, args.gpt_request
                    ),
                    model_size=args.user_model_size,
                    dataset_prompt="",
                    sys_prompt="",
                    max_steps=args.max_steps,
                    memory_size=args.memory_size,
                    init_prompt_dict_no_tool=init_prompt_dict_no_tool[
                        args.dataset_name
                    ],
                    action_wrapper_no_tool=py_agent_action_wrapper_dict[
                        args.dataset_name
                    ],
                    check_actions=args.check_actions,
                    init_prompt_dict=init_prompt_dict[
                        (
                            args.dataset_name
                            if args.use_hand_tool is None
                            else args.use_hand_tool
                        )
                    ],
                    action_wrapper=action_wrapper_dict[
                        (
                            args.dataset_name
                            if args.use_hand_tool is None
                            else args.use_hand_tool
                        )
                    ],
                    max_context_length=get_max_context_length(
                        args.model_name, args.user_model_size),
                    tool_dir=args.retrieve_file_path,
                    use_hand_tool=(args.use_hand_tool is not None),
                    react=args.react,
                    example_order=args.example_order,
                    usage_version=args.usage_version,
                    note_position=args.note_position,
                    no_tool_description=args.no_tool_description,
                    full_tool_subprocess=args.full_tool_subprocess,
                )

            else:
                raise ValueError(
                    "Not supported learner method {}".format(
                        args.learner_method)
                )

            self.itf = learnable_agent(
                user_model=user_model, learner_model=learner_model)
            # self.result_recoder = tool_agent_result_recoder

        elif args.planning_method in ["reflexion_agent"]:
            # Set file path for learn, retrieve and eval

            if args.learner_method in ["reflexion"]:
                if args.eval_save_path is None:
                    args.eval_save_path = f'eval_results/{args.planning_method}.{args.learner_method}.{args.user_method}.{args.model_name}.{args.model_size}.{args.user_model_size}.{str(args.check_actions).replace(" ","_")}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}.{args.optimize_iteration_number}.{args.use_plan_number}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'
                if args.retrieve_file_path is None:
                    args.retrieve_file_path = f'learn_results/{args.planning_method}.{args.learner_method}.{args.user_method}.{args.model_name}.{args.model_size}.{args.user_model_size}.{str(args.check_actions).replace(" ","_")}/{args.dataset_name+"train" if args.test_on_train else args.dataset_name}.{args.optimize_iteration_number}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv'
                    if args.exp_id_on_train:
                        args.retrieve_file_path = args.retrieve_file_path.rstrip(
                            ".csv"
                        ) + "_{}.csv".format(args.exp_id)
                args.learn_save_path = args.retrieve_file_path
            else:
                raise ValueError(
                    "Not supported combination {} and {}".format(
                        args.learner_method, args.user_method
                    )
                )

            if args.learner_method == "reflexion":
                learner_model = reflexion_optimizer(
                    backbone_func=self.backbone_func,
                    learn_path=args.retrieve_file_path,
                    optimizer_do_learn=args.optimizer_do_learn,
                    pass_optimizer=args.pass_optimizer,
                    optimize_iteration_number=args.optimize_iteration_number,
                    learn_save_path=args.learn_save_path,
                    reflexion_prompt=reflexion_prompt[args.user_method][
                        args.dataset_name
                    ],
                )
            else:
                raise ValueError(
                    "Not supported learner method {}".format(
                        args.learner_method)
                )

            if args.user_method in ["py_agent"]:
                init_prompt_dict = py_agent_prompt_dict
                user_model = py_agent(
                    backbone_func=load_backbone(
                        args.model_name, args.user_model_size, args.gpt_request
                    ),
                    model_size=args.model_size,
                    dataset_prompt="",
                    sys_prompt="",
                    max_steps=args.max_steps,
                    memory_size=args.memory_size,
                    check_actions=args.check_actions,
                    init_prompt_dict=init_prompt_dict[args.dataset_name],
                    action_wrapper=py_agent_action_wrapper_dict[args.dataset_name],
                    max_context_length=get_max_context_length(
                        args.model_name, args.user_model_size),
                    use_plan="True",
                    use_plan_number=args.use_plan_number,
                    plan_dir=args.retrieve_file_path,
                )
            elif args.user_method in ["react_py_agent"]:
                init_prompt_dict = react_py_agent_prompt_dict
                user_model = react_py_agent(
                    backbone_func=load_backbone(
                        args.model_name, args.user_model_size, args.gpt_request
                    ),
                    model_size=args.model_size,
                    dataset_prompt="",
                    sys_prompt="",
                    max_steps=args.max_steps,
                    memory_size=args.memory_size,
                    check_actions=args.check_actions,
                    init_prompt_dict=init_prompt_dict[args.dataset_name],
                    action_wrapper=py_agent_action_wrapper_dict[args.dataset_name],
                    max_context_length=get_max_context_length(
                        args.model_name, args.user_model_size),
                    use_plan="True",
                    use_plan_number=args.use_plan_number,
                    plan_dir=args.retrieve_file_path,
                )

            else:
                raise ValueError(
                    "Not supported learner method {}".format(
                        args.learner_method)
                )

            self.itf = learnable_agent(
                user_model=user_model, learner_model=learner_model)

        else:
            raise ValueError(
                "Unimplied method name {}".format(args.planning_method))

    def learn(self, data, evaluator):

        if self.planning_method == "learnact_agent":
            if isinstance(data, list):
                return self.itf.learn(train=data, evaluator=evaluator)
            else:
                return self.itf.learn(train=[data], evaluator=evaluator)
        elif self.planning_method == "reflexion_agent":
            if isinstance(data, list):
                return self.itf.learn(train=data, evaluator=evaluator)
            else:
                return self.itf.learn(train=[data], evaluator=evaluator)
        else:
            raise ValueError(
                "Calling learning of unimplied method name {}".format(
                    self.planning_method
                )
            )

    def __call__(self, data):

        if self.planning_method in [
            "api_agent",
            "py_agent",
            "code_as_policy",
            "react_py_agent",
            "learnact_agent",
            "reflexion_agent",
        ]:
            return self.itf(data["input"])

        else:
            raise ValueError(
                "Calling unimplied method name {}".format(self.planning_method)
            )
