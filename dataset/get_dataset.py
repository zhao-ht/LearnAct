import math
import pandas as pd
import os

import numpy as np
import torch

from torch.utils.data import Dataset, Subset
import json

try:
    import sys

    sys.path.append("dataset/agent_environments")
except:
    pass
from dataset.agent_environments.environment.pddl_env.pddl_env import PDDL
from dataset.agent_environments.environment.alfworld.alfworld_env_mine import (
    AlfWorld,
    AlfWorld_PREFIXES,
    AlfWorld_Reverse_PREFIXES,
)

dataset_file_map = {
    "gsm": "gsm",
    "penguin": "penguins_in_a_table",
    "colored_object": "reasoning_about_colored_objects",
    "date_understanding": "date_understanding",
    "penguin_h": "penguins_in_a_table",
    "colored_object_h": "reasoning_about_colored_objects",
    "date_understanding_h": "date_understanding",
}


class PDDLDataset(Dataset):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        directory_path = (
            "dataset/agent_environments/environment/pddl_env/pddlgym/pddl/{}".format(
                dataset_name
            )
        )
        file_count = len(
            [
                name
                for name in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, name))
            ]
        )
        self.data = list(range(file_count))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        env = PDDL(problem_index=index, game_name=self.dataset_name)
        item = {"input": env, "target": None, "index": index}
        return item


class AlfWorldDataset(Dataset):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        directory_path = "dataset/alfworld/json_2.1.1/valid_unseen"
        env_full = AlfWorld(
            "eval_out_of_distribution",
            base_config="dataset/agent_environments/environment/alfworld/base_config.yaml",
            batch_size=1,
            seed=1,
        )
        type_files = []
        for file in env_full.env.gamefiles:
            # the file form is xxx/pick_cool_then_place_in_recepxxx/trial_xxx/game.tw-pddl
            if file.split("/")[-3].startswith(dataset_name):
                type_files.append(file)
        if len(type_files) == 0:
            raise ValueError("task type {} not found in file".format(dataset_name))

        self.data = type_files

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        env = AlfWorld(
            "eval_out_of_distribution",
            base_config="dataset/agent_environments/environment/alfworld/base_config.yaml",
            batch_size=1,
            seed=1,
            task_type=self.dataset_name,
            id=index,
        )
        item = {"input": env, "target": None, "index": index}
        return item


def PDDLEvaluator(model_output, data):
    return float(model_output)


def AlfWorldEvaluator(model_output, data):
    return float(model_output)


class Batch_dataset(Dataset):
    def __init__(self, dataset, batch_size=None):
        self.dataset = dataset
        self.batch_size = batch_size

    def __len__(self):
        if self.batch_size is None:
            return 1
        else:
            return math.ceil(len(self.dataset) / self.batch_size)

    def __getitem__(self, index):
        if index >= self.__len__():
            raise StopIteration
        if self.batch_size is None:
            item_list = [item for item in self.dataset]
        else:
            item_list = [
                item
                for item in self.dataset[
                    (index * self.batch_size) : (
                        min(len(self.dataset), (index + 1) * self.batch_size)
                    )
                ]
            ]
        return item_list


def get_dataset(args):
    data_cleaner = None
    test_index_key = "input"

    if args.dataset_name in [
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
        dataset = PDDLDataset(args.dataset_name)
        evaluator = PDDLEvaluator
        test_index_key = "index"
    elif args.dataset_name in [
        "alfworld_put",
        "alfworld_clean",
        "alfworld_heat",
        "alfworld_cool",
        "alfworld_examine",
        "alfworld_puttwo",
    ]:
        dataset = AlfWorldDataset(
            AlfWorld_Reverse_PREFIXES[args.dataset_name.replace("alfworld_", "")]
        )
        evaluator = AlfWorldEvaluator
        test_index_key = "index"
    else:
        raise ValueError("dataset not implied yet")

    if not isinstance(dataset, dict):  # split is not specified

        if args.split_dataset_num is not None:
            if args.split_dataset_num[0] < 1:
                # if args.split_dataset_num is not None:
                #     print(
                #         'Warning! Both split_dataset_num and split_dataset_ratio specified. Using split_dataset_ratio.')
                args.split_dataset_num = [
                    int(len(dataset) * ratio) for ratio in args.split_dataset_num
                ]
            else:
                args.split_dataset_num = [int(num) for num in args.split_dataset_num]
            # Add the dataset size of remaining data
            if len(args.split_dataset_num) < 3:
                args.split_dataset_num.append(
                    len(dataset) - np.sum(args.split_dataset_num)
                )

            split_file_path = os.path.join(
                "dataset",
                "split",
                "{}_{}_split_{}.csv".format(
                    args.dataset_name, args.split_dataset_num, args.split_file
                ),
            )
            if not os.path.exists(os.path.join("dataset", "split")):
                os.mkdir(os.path.join("dataset", "split"))

            # The case of train-val-test split
            if len(args.split_dataset_num) == 3:

                if os.path.exists(split_file_path):
                    print("Loading existing split file {}".format(split_file_path))
                    split_pd = pd.read_csv(split_file_path, index_col=0)
                    train_ind = split_pd[split_pd["split"] == "train"][
                        "ind"
                    ].values.tolist()
                    val_ind = split_pd[split_pd["split"] == "val"][
                        "ind"
                    ].values.tolist()
                    test_ind = split_pd[split_pd["split"] == "test"][
                        "ind"
                    ].values.tolist()
                else:
                    train_ind, val_ind, test_ind = torch.utils.data.random_split(
                        list(range(len(dataset))), args.split_dataset_num
                    )

                    train_ind = train_ind.indices
                    val_ind = val_ind.indices
                    test_ind = test_ind.indices
                    split_list = []
                    for ind in train_ind:
                        split_list.append([ind, "train"])
                    for ind in val_ind:
                        split_list.append([ind, "val"])
                    for ind in test_ind:
                        split_list.append([ind, "test"])
                    split_pd = pd.DataFrame(split_list, columns=["ind", "split"])
                    split_pd.to_csv(split_file_path, header=True)

                train_set = Subset(dataset, train_ind)
                val_set = Subset(dataset, val_ind)
                test_set = Subset(dataset, test_ind)

                if args.batch_train:
                    train_set = Batch_dataset(train_set)

                if args.test_on_train:
                    dataset = {"train": train_set, "val": val_set, "test": train_set}
                elif args.test_on_all:
                    dataset = {"train": train_set, "val": val_set, "test": dataset}
                dataset = {"train": train_set, "val": val_set, "test": test_set}

            else:
                assert len(args.split_dataset_num) == 2

                if os.path.exists(split_file_path):
                    print("Loading existing split file {}".format(split_file_path))
                    split_pd = pd.read_csv(split_file_path, index_col=0)
                    train_ind = split_pd[split_pd["split"] == "train"][
                        "ind"
                    ].values.tolist()
                    test_ind = split_pd[split_pd["split"] == "test"][
                        "ind"
                    ].values.tolist()
                else:
                    train_ind, test_ind = torch.utils.data.random_split(
                        list(range(len(dataset))), args.split_dataset_num
                    )

                    train_ind = train_ind.indices
                    test_ind = test_ind.indices

                    split_list = []
                    for ind in train_ind:
                        split_list.append([ind, "train"])
                    for ind in test_ind:
                        split_list.append([ind, "test"])
                    split_pd = pd.DataFrame(split_list, columns=["ind", "split"])
                    split_pd.to_csv(split_file_path, header=True)

                train_set = Subset(dataset, train_ind)
                test_set = Subset(dataset, test_ind)

                if args.batch_train:
                    train_set = Batch_dataset(train_set)

                if args.test_on_train:
                    dataset = {"train": train_set, "val": None, "test": train_set}
                elif args.test_on_all:
                    dataset = {"train": train_set, "val": None, "test": dataset}
                else:
                    dataset = {"train": train_set, "val": None, "test": test_set}

        else:
            dataset = {"train": None, "val": None, "test": dataset}

    return {
        "dataset": dataset,
        "evaluator": evaluator,
        "data_cleaner": data_cleaner,
        "test_index_key": test_index_key,
    }
