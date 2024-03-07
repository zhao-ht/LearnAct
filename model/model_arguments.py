import argparse


def add_learnact_agent_args(parser):
    parser.add_argument("--learner_method", type=str, default="single")
    parser.add_argument("--learner_method_no_preuse", action="store_true")
    parser.add_argument("--optimizer_parallel_learn", action="store_true")

    parser.add_argument("--user_method", type=str, default="zero_py")
    parser.add_argument("--user_model_size", type=str, default=None)

    parser.add_argument("--retrieve_model", default=None, type=str)
    parser.add_argument("--retrieve_file_path", default=None, type=str)
    parser.add_argument("--retrieve_top_k", default=2, type=int)
    return parser


def add_api_agent_args(parser):
    parser.add_argument("--max_steps", type=int)
    parser.add_argument("--memory_size", type=int)
    parser.add_argument("--check_actions", type=str, default=None)
    return parser


def add_py_agent_args(parser):
    parser.add_argument("--max_steps", type=int)
    parser.add_argument("--memory_size", type=int)
    parser.add_argument("--check_actions", type=str, default=None)
    return parser


def add_code_as_policy_args(parser):
    parser.add_argument("--hier", action="store_true")
    return parser


def add_reflexion_agent_args(parser):
    parser.add_argument("--learner_method", type=str, default="single")
    parser.add_argument("--learner_method_no_preuse", action="store_true")
    parser.add_argument("--optimizer_parallel_learn", action="store_true")

    parser.add_argument("--user_method", type=str, default="zero_py")
    parser.add_argument("--user_model_size", type=str, default=None)

    parser.add_argument("--use_plan_number", type=int, default=None)

    parser.add_argument("--retrieve_model", default=None, type=str)
    parser.add_argument("--retrieve_file_path", default=None, type=str)
    parser.add_argument("--retrieve_top_k", default=2, type=int)
    return parser


def add_learnact_user_args(parser):
    parser.add_argument("--max_steps", type=int)
    parser.add_argument("--memory_size", type=int)
    parser.add_argument("--use_hand_tool", type=str, default=None)
    parser.add_argument("--check_actions", type=str, default=None)
    parser.add_argument("--react", action="store_true")
    parser.add_argument("--example_order", type=str, default="origin_first")
    parser.add_argument("--note_position", type=str,
                        default="before_example")
    parser.add_argument("--no_tool_selfprompt", action="store_true")
    parser.add_argument("--no_tool_description", action="store_true")
    parser.add_argument("--full_tool_subprocess", action="store_true")
    return parser


def add_learnact_learner_args(parser):
    parser.add_argument("--optimizer_do_learn", action="store_true")
    parser.add_argument("--pass_optimizer", action="store_true")
    parser.add_argument("--tool_in_context_style", type=str, default="vanilla")
    parser.add_argument("--get_tool_version", type=str, default="structured")
    parser.add_argument("--get_tool_incontext_version",
                        type=str, default="toy")
    parser.add_argument("--usage_version", type=str, default="individual")
    parser.add_argument("--tool_improve_target", type=str, default="step")
    parser.add_argument("--tool_improve_version", type=str, default="both")
    parser.add_argument("--tool_improve_in_context_version",
                        type=str, default="toy")
    parser.add_argument("--tool_improve_history", type=str, default="single")
    parser.add_argument("--step_sample_number", type=int, default=1)
    parser.add_argument("--optimize_iteration_number", type=int, default=1)
    parser.add_argument("--score_type", type=str, default="step_correction")
    parser.add_argument("--same_usage", action="store_true")
    return parser


def add_reflexion_learner_args(parser):
    parser.add_argument("--optimizer_do_learn", action="store_true")
    parser.add_argument("--pass_optimizer", action="store_true")
    parser.add_argument("--optimize_iteration_number", type=int, default=1)
    return parser


def add_model_args(args, left):
    parser_new = argparse.ArgumentParser()

    if args.planning_method in ["api_agent"]:
        parser_new = add_api_agent_args(parser_new)
        args_data, _ = parser_new.parse_known_args(left)
        args.__dict__.update(args_data.__dict__)

    elif args.planning_method in ["py_agent", "react_py_agent"]:
        parser_new = add_py_agent_args(parser_new)
        args_data, _ = parser_new.parse_known_args(left)
        args.__dict__.update(args_data.__dict__)
        if args.check_actions is not None:
            args.check_actions = "check valid actions"

    elif args.planning_method in ["code_as_policy"]:
        parser_new = add_code_as_policy_args(parser_new)
        args_data, _ = parser_new.parse_known_args(left)
        args.__dict__.update(args_data.__dict__)

    elif args.planning_method in ["learnact_agent"]:
        parser_new = add_learnact_agent_args(parser_new)
        args_data, left = parser_new.parse_known_args(left)
        args.__dict__.update(args_data.__dict__)

        if args.learner_method == "learnact_learner":
            parser_new = argparse.ArgumentParser()
            parser_new = add_learnact_learner_args(parser_new)
            args_data, left = parser_new.parse_known_args(left)
            args.__dict__.update(args_data.__dict__)
        else:
            raise ValueError("model not implied yet")

        if args.user_method == "learnact_user":
            parser_new = argparse.ArgumentParser()
            parser_new = add_learnact_user_args(parser_new)
            args_data, _ = parser_new.parse_known_args(left)
            args.__dict__.update(args_data.__dict__)
            if args.check_actions is not None:
                args.check_actions = "check valid actions"
            if args.user_model_size is None:
                args.user_model_size = args.model_size
        else:
            raise ValueError("model not implied yet")
        assert not (args.optimizer_parallel_learn and args.parallel_learn)

    elif args.planning_method in ["reflexion_agent"]:
        parser_new = add_reflexion_agent_args(parser_new)
        args_data, left = parser_new.parse_known_args(left)
        args.__dict__.update(args_data.__dict__)
        if args.learner_method == "reflexion":
            parser_new = argparse.ArgumentParser()
            parser_new = add_reflexion_learner_args(parser_new)
            args_data, left = parser_new.parse_known_args(left)
            args.__dict__.update(args_data.__dict__)
        else:
            raise ValueError("model not implied yet")

        if args.user_method in ["py_agent", "react_py_agent"]:
            parser_new = argparse.ArgumentParser()
            parser_new = add_py_agent_args(parser_new)
            args_data, _ = parser_new.parse_known_args(left)
            args.__dict__.update(args_data.__dict__)
            if args.check_actions is not None:
                args.check_actions = "check valid actions"
            if args.user_model_size is None:
                args.user_model_size = args.model_size
        else:
            raise ValueError("model not implied yet")

        assert not (args.optimizer_parallel_learn and args.parallel_learn)

    else:
        raise ValueError("model not implied yet")

    return args
