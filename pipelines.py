import copy
import json
import os.path
from random import seed

import numpy as np
from tqdm import tqdm

from threading import Thread, BoundedSemaphore, Lock

import pandas as pd

from aux_func.aux_func import pd_concat_ignore2


def answer_eval(response, dataset, data, evaluator=None, model_result_recoder=None):

    result = copy.copy(data)

    if response["res"] is None:
        score = 0
    else:

        if dataset in [
            "baking",
            "barman",
            "blocks",
            "block_medium",
            "blockworld",
            "doors",
            "elevator",
            "footwear",
            "fridge",
            "glibrearrangement",
            "gripper",
            "hanoi",
            "mineraft",
            "newspapers",
            "spannerlearning",
            "strage",
            "termes",
            "tireworld_test",
            "trapnewspapers",
            "tyreworld",
        ]:
            score = evaluator(response["res"], data)
            result["input"] = data["index"]
        elif dataset in [
            "alfworld_put",
            "alfworld_clean",
            "alfworld_heat",
            "alfworld_cool",
            "alfworld_examine",
            "alfworld_puttwo",
        ]:
            score = evaluator(response["res"], data)
            result["input"] = data["index"]
        else:
            print("evaluation of dataset {} not implied yet".format(dataset))
            raise ValueError

    result["score"] = score

    if model_result_recoder is None:
        # default response record items
        result["answer"] = response["res"]
        if isinstance(response["gen"], dict):
            for key in response["gen"].keys():
                result[key] = response["gen"][key]
        else:
            result["generation"] = response["gen"]
    else:
        # model specific response record
        result = model_result_recoder(response, result)

    return score, result


def save_result_jsonl(file_name, result):
    with open(file_name, "a") as f:
        f.write(json.dumps(result) + "\n")
        f.flush()


def save_result_pd(file_name, result, sort_columns=False):

    df = pd.DataFrame([[result[key]
                      for key in result.keys()]], columns=result.keys())

    # result_list = []
    if os.path.exists(file_name):
        result_per_dataset_table_permutated_all = pd_concat_ignore2(
            pd.read_csv(file_name, index_col=0), df
        )
        # result_list.append(pd.read_csv(file_name, index_col=0))
    else:
        result_per_dataset_table_permutated_all = df
    # result_list.append(df)
    # result_per_dataset_table_permutated_all = pd.concat(
    #     result_list, ignore_index=True)
    if sort_columns:
        result_per_dataset_table_permutated_all = (
            result_per_dataset_table_permutated_all.sort_index(axis=1)
        )
    if os.path.dirname(file_name) != "" and not os.path.exists(
        os.path.dirname(file_name)
    ):
        os.makedirs(os.path.dirname(file_name))
    result_per_dataset_table_permutated_all.to_csv(file_name, header=True)


def update_result_pd(file_name, result, replace_id):

    df = pd.DataFrame([[result[key]
                      for key in result.keys()]], columns=result.keys())

    # result_list = []
    if os.path.exists(file_name):
        result_df = pd.read_csv(file_name, index_col=0)
        result_df.at[replace_id, "usable"] = False  # Mark for filter
        result_per_dataset_table_permutated_all = pd_concat_ignore2(
            result_df, df)
        # result_list.append(result_df)
    else:
        result_per_dataset_table_permutated_all = df
    # result_list.append(df)
    # result_per_dataset_table_permutated_all = pd.concat(
    #     result_list, ignore_index=True)

    if os.path.dirname(file_name) != "" and not os.path.exists(
        os.path.dirname(file_name)
    ):
        os.makedirs(os.path.dirname(file_name))
    result_per_dataset_table_permutated_all.to_csv(file_name, header=True)


def resume_result_jsonl(file_name):
    lines = open(file_name).readlines()
    num_skip_exps = len(lines)
    for id, data in enumerate(map(json.loads, lines)):
        if "score" not in data:
            print(id, data)
    scores = [data["score"] for data in map(json.loads, lines)]
    return scores, num_skip_exps


def resume_result_pd(file_name, executed_column):
    resume = pd.read_csv(file_name, index_col=0)
    if "score" in resume:
        scores = resume["score"].values.tolist()
    elif "success" in resume:
        scores = (resume["success"] > 0).values.tolist()
    else:
        print("Warnning! No score or success in resumed file. No score resumed")
        scores = []
    if executed_column in resume:
        executed_samples = []
        for sample_list in resume[executed_column].values.tolist():
            if not pd.isna(sample_list):
                try:
                    samples = eval(sample_list)
                    if not isinstance(samples, list):
                        executed_samples.append(str(samples))
                    else:
                        for item in eval(sample_list):
                            executed_samples.append(str(item))
                except:
                    executed_samples.append(str(sample_list))
        executed_samples = set(executed_samples)
        num_skip_exps = len(executed_samples)
    else:
        num_skip_exps = len(resume)
        executed_samples = set()
    return scores, num_skip_exps, executed_samples


def test_single_sample(
    data, model, args, file_name, evaluator, is_parallel=False, ignore_error=False
):
    global scores, f, pbar

    if is_parallel or ignore_error:  # ignore error to release the process of parallel
        try:
            response = model(data)
        except Exception as e:
            print(e)
            response = {
                "res": None,
                "gen": None,
                "error": "0_test_single_sample_{}".format(e),
            }
    else:
        response = model(data)

    if is_parallel:
        lock.acquire()

    score, result = answer_eval(
        response, args.dataset_name, data, evaluator, model.result_recoder
    )

    scores.append(score)
    pbar.set_description(f"Total Score : {100*sum(scores) / len(scores)}")

    save_result_pd(file_name, result)

    if is_parallel:
        lock.release()
        pool.release()


def learn_single_sample(
    data, model, args, file_name, evaluator, is_parallel=False, ignore_error=False
):
    global scores, pbar

    if is_parallel or ignore_error:  # ignore error to release the process of parallel
        try:
            response_list = model.learn(data, evaluator)
        except Exception as e:
            print(e)
            response_list = [
                {
                    "tool_cases_list": [data],
                    "error": "0_learn_single_sample_{}".format(e),
                    "success": 0,
                }
            ]
    else:
        response_list = model.learn(data, evaluator)

    if is_parallel:
        lock.acquire()

    assert isinstance(response_list, list)

    score_recorded = False
    for response in response_list:
        if "func_id" in response:
            func_id, response = response["func_id"], response["response"]
            if ("pre_version" not in response) or (
                func_id is not None and response["pre_version"] is None
            ):
                response["pre_version"] = func_id
        else:
            func_id = None

        if "usable" not in response:
            response["usable"] = response["success"] > 0
        if not score_recorded:
            score = float(response["success"])
            scores.append(float(score > 0))
            score_recorded = True

        pbar.set_description(f"Total Score : {100*sum(scores) / len(scores)}")
        if func_id is not None:
            update_result_pd(file_name, response, func_id)
        else:
            save_result_pd(file_name, response)

    if is_parallel:
        lock.release()
        pool.release()


pool = BoundedSemaphore(4)
lock = Lock()


def training(dataloader, model, args):

    global scores, pbar

    train_index_key = dataloader["test_index_key"]

    OUTPUT_PATH = (
        args.learn_save_path
        if args.learn_save_path is not None
        else f"learn_results/{args.planning_method}/{args.dataset_name}_{args.split_dataset_num[0]}_split_{args.split_file}.csv"
    )

    print("Saving training to {}".format(OUTPUT_PATH))

    if args.resume and os.path.exists(OUTPUT_PATH):
        print("Resuming training from {}".format(OUTPUT_PATH))
        scores, num_skip_exps, executed_samples = resume_result_pd(
            OUTPUT_PATH, "tool_cases_list"
        )
    else:
        num_skip_exps = 0
        scores = []
        executed_samples = set()
        if os.path.exists(OUTPUT_PATH):
            raise ValueError(
                "Learned file exists. Cannot start a new learning. Please rename the learned file {} first.".format(
                    OUTPUT_PATH
                )
            )

    trial = 0
    threads = []

    pbar = tqdm(dataloader["dataset"]["train"])

    print("executed_samples: {}".format(len(executed_samples)))
    for data in pbar:
        trial += 1
        if not args.parallel_learn:
            if (
                (
                    train_index_key in data
                    and str(data[train_index_key]) in executed_samples
                )
                or (
                    isinstance(data, list)
                    and train_index_key in data[0]
                    and set([str(item[train_index_key]) for item in data]).issubset(
                        executed_samples
                    )
                )
                or (str(data) in executed_samples)
            ):
                print("skip")
                continue
            if dataloader["data_cleaner"] is not None and (
                not dataloader["data_cleaner"](data)
            ):
                print("Dirty Data! Skip")
                continue
            learn_single_sample(
                data,
                model,
                args,
                OUTPUT_PATH,
                dataloader["evaluator"],
                ignore_error=args.ignore_error,
            )
        else:
            if (
                train_index_key in data
                and str(data[train_index_key]) in executed_samples
            ) or (str(data) in executed_samples):
                print("skip")
                continue
            if dataloader["data_cleaner"] is not None and (
                not dataloader["data_cleaner"](data)
            ):
                print("Dirty Data! Skip")
                continue
            pool.acquire()
            thread = Thread(
                target=learn_single_sample,
                args=(
                    data,
                    model,
                    args,
                    OUTPUT_PATH,
                    dataloader["evaluator"],
                    True,
                    args.ignore_error,
                ),
            )
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join(300)  # 5 min for each task
        if thread.is_alive():
            print("A job didn't finish within the time limit")

    print(f"Total Score : {100*sum(scores) / len(scores)}")
    print("Training finished")


def testing(dataloader, model, args):

    global scores, pbar

    trial = 0
    test_index_key = dataloader["test_index_key"]

    OUTPUT_PATH = (
        args.eval_save_path
        if args.eval_save_path is not None
        else f"eval_results/{args.planning_method}.{args.model_name}.{args.model_size}/{args.dataset_name}.{args.split_dataset_num}_split_{args.split_file}.{args.exp_id}.csv"
    )

    print("Saving testing to {}".format(OUTPUT_PATH))

    if args.resume and os.path.exists(OUTPUT_PATH):
        print("Resuming testing from {}".format(OUTPUT_PATH))
        scores, num_skip_exps, executed_samples = resume_result_pd(
            OUTPUT_PATH, test_index_key
        )
    else:
        scores = []
        num_skip_exps = 0
        executed_samples = set()
        if os.path.exists(OUTPUT_PATH):
            raise ValueError(
                "Eval result file exists. Cannot start a new testing. Please rename the eval result file {} first.".format(
                    OUTPUT_PATH
                )
            )

    threads = []

    pbar = tqdm(dataloader["dataset"]["test"])

    print("executed_samples: {}".format(len(executed_samples)))
    for data in pbar:
        trial += 1
        if not args.parallel_test:
            if str(data[test_index_key]) in executed_samples or (
                str(data[test_index_key]).replace(
                    "\r\n", "\n") in executed_samples
            ):
                print("skip")
                continue
            if dataloader["data_cleaner"] is not None and (
                not dataloader["data_cleaner"](data)
            ):
                print("Dirty Data! Skip")
                continue
            test_single_sample(
                data,
                model,
                args,
                OUTPUT_PATH,
                dataloader["evaluator"],
                ignore_error=args.ignore_error,
            )
        else:
            if (
                str(data[test_index_key]) in executed_samples
                or (str(data[test_index_key]).replace("\r\n", "\n")) in executed_samples
            ):
                print("skip")
                continue
            if dataloader["data_cleaner"] is not None and (
                not dataloader["data_cleaner"](data)
            ):
                print("Dirty Data! Skip")
                continue
            pool.acquire()
            thread = Thread(
                target=test_single_sample,
                args=(
                    data,
                    model,
                    args,
                    OUTPUT_PATH,
                    dataloader["evaluator"],
                    True,
                    args.ignore_error,
                ),
            )
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join(300)  # 5 min for each task
        if thread.is_alive():
            print("A job didn't finish within the time limit")

    print(f"Total Score : {100*sum(scores) / len(scores)}")
    print("Testing finished")
