import copy
import json
import os

import numpy as np
import pandas as pd

from aux_func.aux_func import (
    pd_concat_ignore2,
)


def history_to_str(history):
    item_list = []
    for item in history:
        if (
            "Goal" not in item
            and "Reward" not in item
            and "Failed_subprocess" not in item
        ):
            for key in item.keys():
                item_list.append(key + ": " + item[key])
                break

    history_str = "\n".join(item_list)
    return history_str


class reflexion_optimizer:
    def __init__(
        self,
        backbone_func,
        learn_path,
        optimizer_do_learn=False,
        pass_optimizer=False,
        optimize_iteration_number=1,
        learn_save_path="learn_results",
        reflexion_prompt=None,
    ):
        self.backbone_func = backbone_func
        self.learn_path = learn_path
        self.anneal = True
        self.optimizer_do_learn = optimizer_do_learn

        self.learn_save_path = learn_save_path + "_dir"

        self.optimize_iteration_number = optimize_iteration_number

        self.pass_optimizer = pass_optimizer

        self.reflexion_prompt = reflexion_prompt

    def wrap_history(self, history):
        item_list = []
        for item in history:
            if "Goal" in item:
                item_list.append("Goal: " + item["Goal"])
            elif "Action" in item:
                item_list.append("Action: " + item["Action"])
            if "Observation" in item:
                item_list.append("Observation: " + item["Observation"])
        history_error_subprocess = "\n".join(item_list)
        return history_error_subprocess

    def find_failed_data_index_trace(self, score_list):
        if 0 in score_list:
            index = score_list.index(0)
            return index
        else:
            return None

    def create_reflexion(self, data_index, history, new_tool_df, tooluser, env):
        history_error = self.wrap_history(history)
        optimize_query = self.reflexion_prompt.format(
            history_error=history_error.strip("\n")
        )

        message = [{"role": "user", "content": optimize_query}]

        params = {
            "x": message,
            # "hist_messages": hist_messages
        }
        reflexion_content, _ = self.backbone_func(**params)

        print("----------------Reflexion----------------")
        print("reflexion_content: {}\n".format(reflexion_content))

        result = {
            "reflexion": reflexion_content,
            "tool_cases_list": str(data_index),
            "verification": None,
            "success": 1,
            "usable": True,
            "edited": True,
            "error": "1_create_reflection",
            "pre_version": None,
        }
        df = pd.DataFrame(
            [[result[key] for key in result.keys()]], columns=result.keys()
        )

        if new_tool_df is not None and len(new_tool_df) > 0:
            new_tool_df = pd_concat_ignore2(new_tool_df, df)
        else:
            new_tool_df = df

        return new_tool_df

    def __call__(
        self,
        train,
        val=None,
        tooluser=None,
        use_response=None,
        evaluator=None,
    ):

        tooluser.update_plan([])

        # env = copy.deepcopy(train[0]['input'])
        data_index = [data["index"] for data in train]

        tooluser.update_plan(None)

        file_name = os.path.join(self.learn_save_path, "debug_tem_{}.csv")
        if not os.path.exists(self.learn_save_path):
            os.makedirs(self.learn_save_path)

        max_step_pre = tooluser.max_steps

        new_tool_df = []

        debug_eval_file_name = os.path.join(
            self.learn_save_path, "debug_eval_{}.json")
        debug_eval_score_name = os.path.join(
            self.learn_save_path, "debug_eval_score_{}.json"
        )

        for opt_step in range(self.optimize_iteration_number+1):

            tooluser.update_plan(new_tool_df)
            tooluser.max_steps = 10

            history_list = []
            score_list = []
            for data in train:
                env = copy.deepcopy(data["input"])
                env.reset()
                use_response = tooluser(copy.deepcopy(env))
                histoty = use_response["gen"]["history"]
                history_list.append(histoty)
                score_list.append(use_response["res"])

            score_success = np.mean(score_list)

            with open(debug_eval_file_name.format(opt_step), "w") as f:
                json.dump(history_list, f)
            with open(debug_eval_score_name.format(opt_step), "w") as f:
                json.dump(score_list, f)

            tooluser.max_steps = max_step_pre

            if (
                not self.pass_optimizer
                and opt_step < self.optimize_iteration_number
            ):
                # if not pass_create:

                index = self.find_failed_data_index_trace(score_list)

                if index is not None:
                    histoty = history_list[index]
                    env = copy.deepcopy(train[index]["input"])
                    env.reset()

                    new_tool_df = self.create_reflexion(
                        data_index, histoty, new_tool_df, tooluser, env
                    )

                    new_tool_df.to_csv(file_name.format(opt_step + 1))
                else:
                    break

            else:
                break
        if len(new_tool_df) > 0:
            new_tool_df["usable"] = copy.deepcopy(new_tool_df["edited"])

        response_list = []
        if len(new_tool_df) > 0:
            for line_dict in new_tool_df.to_dict(orient="records"):
                response_list.append(
                    {
                        "func_id": (
                            line_dict["pre_version"] if line_dict["usable"] else None
                        ),
                        "response": line_dict,
                    }
                )

        tooluser.update_plan(None)

        return response_list
