import os.path

import argparse
from random import seed

import numpy as np
from dataset import get_dataset
from dataset import add_dataset_args

from model import model_loader, add_model_args
from pipelines import testing, training

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--seed", type=int, default=62471893)
    parser.add_argument("--do_learn", action="store_true")
    parser.add_argument("--do_test", type=bool, default=True)
    parser.add_argument("--parallel_learn", action="store_true")
    parser.add_argument("--parallel_test", action="store_true")
    parser.add_argument("--ignore_error", action="store_true")
    parser.add_argument("--new_epoch", action="store_true")

    parser.add_argument("--eval_save_path", type=str, default=None)
    parser.add_argument("--learn_save_path", type=str, default=None)

    parser.add_argument("--model_name", type=str, default="llama")
    parser.add_argument("--gpt_request", action="store_true")
    parser.add_argument("--model_size", type=str, default="7b")
    parser.add_argument("--opt_server", type=str, default=None)
    parser.add_argument("--api_key", type=str, default=None)

    parser.add_argument(
        "--planning_method",
        type=str,
        default="cot",
        choices=[
            "learnact_agent",
            "api_agent",
            "py_agent",
            "react_py_agent",
            "reflexion_agent",
            "code_as_policy",
        ],
    )

    parser.add_argument("--dataset_name", type=str, default="prontoqa")
    parser.add_argument(
        "--split_dataset_num",
        type=float,
        nargs="+",
    )
    parser.add_argument("--batch_train", action="store_true")
    parser.add_argument("--exp_id", type=int, default=0)
    parser.add_argument("--exp_id_on_train", action="store_true")
    # parser.add_argument("--split_dataset_ratio", type=float, nargs='+',)
    parser.add_argument("--split_file", type=str, default="0")
    parser.add_argument("--test_on_train", action="store_true")
    parser.add_argument("--test_on_all", action="store_true")

    parser.add_argument("--proofs_only", action="store_true")

    args, left = parser.parse_known_args()
    print("arguments\t", args)

    args = add_dataset_args(args, left)
    args = add_model_args(args, left)

    opt_server = args.opt_server

    gpt_api_key = args.api_key

    if os.path.exists("openai_keys.txt"):
        with open("openai_keys.txt") as f:
            gpt_api_key = f.read()

    import openai

    # openai.api_type =
    # openai.api_base =
    # openai.api_version =
    openai.api_key = gpt_api_key

    seed(args.seed)
    np.random.seed(args.seed)

    dataloader = get_dataset(args)
    model = model_loader(args)

    if args.do_learn:
        training(dataloader, model, args)

    if args.do_test:
        testing(dataloader, model, args)
