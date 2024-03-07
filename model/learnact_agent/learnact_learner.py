import os
import json
import glob
import re
from re import findall, DOTALL, MULTILINE
from multiprocessing import Pool
from tqdm import tqdm
import torch
import openai
import itertools
import random
import pandas as pd
import copy
import numpy as np
from threading import Thread, BoundedSemaphore, Lock
import traceback

from aux_func.aux_func import (
    execute,
    extract_functions,
    extract_import_lines,
    extract_function_name,
    get_decimal_places,
    insert_docstring,
    remove_sure_reply,
    get_significant_digits,
    find_undefined_function,
    parse_ans,
    convert_res_to_ans_format,
    pd_concat_ignore2,
    to_number,
    insert_global_env,
    parse_python_func,
)
import builtins
from pipelines import save_result_pd, update_result_pd
from backbone.gpt import num_tokens_from_messages


tool_maker_decompose_combination_prompt_v2 = """Please summarize the high-level steps to complete this task. 
Each high-level step should be a general Python function encompassing multiple (at least two) basic actions. All the values used in the function should be provided as input rather than being fixed within the function to make it general and usable in similar cases.
The actions provided are Python functions and can be executed directly, for example: ```python
{action_example}
```
No additional interfaces besides the provided actions are available. check_valid_actions is not available.
All the code should be wrapped by```python
```

Here are examples:
{tool_example}

Function:
"""

tool_maker_decompose_combination_prompt_v3 = """Please summarize the high-level steps to complete this task. 
Each high-level step should be a general Python function encompassing multiple (at least two) basic actions. All the values used in the function should be given as input rather than fixed in the function.
The actions provided are Python functions and can be executed directly, for example: ```python
{action_example}
```
No additional interfaces besides the provided actions are available. check_valid_actions is not available.
All the code should be wrapped by```python
```

Here are examples:
{tool_example}

Now please write your solution:
"""

tool_maker_decompose_combination_prompt_v4 = """Please propose several high-level steps for this task. 
Each high-level step should be a Python function encompassing multiple (at least two) basic actions. All the values used in the function should be given as input rather than fixed in the function. 
The provided actions are Python functions and can be executed directly, for example: ```python
{action_example}
```
No additional interfaces besides the provided actions are available.
All the code should be wrapped by```python
```

Here are examples:
{tool_example}

Now please write your solution:
"""


def get_tool_maker_decompose_combination_prompt(version):
    if version == "structured":
        return tool_maker_decompose_combination_prompt_v2
    elif version == "free":
        return tool_maker_decompose_combination_prompt_v3
    elif version == "decompose":
        return tool_maker_decompose_combination_prompt_v4
    else:
        raise ValueError("version {} not implied".format(version))


tool_wrap_prompt_combination = """Now here are some Python function encompassing multiple basic actions to serve as high-level interface in this task. Please write interface instruction for the given Python function.

Here are examples:

{tool_explanation}

Now please write interface instruction for this high-level step {func_name}:
Function:
```python
{function}
```
Instruction:
"""

tool_in_context_prompt_combination_format_instruction = {
    "react": "The usage example should contain Observation, Think, Observation, Action, Observation.",
    "vanilla": "The usage example should contain Goal, Observation, Action, Observation.",
    "together": "The usage example should contain an initial goal, and several iterations of Observation and Action (No line breaks between them).",
    "together_complete": "The completion process should contain an initial goal, and several iterations of Observation and Action.",
}

tool_in_context_prompt_combination = """Now here are some Python function encompassing multiple basic actions to serve as high-level interface in this task. Please Write usage example for the interface following the format of the examples. {format_instruction}

Here are examples:

{tool_in_context}

Now please write interface usage example for this high-level step {func_name}:
Function:
```python
{function}
```
Example:
"""

tool_in_context_prompt_combination_together = """Now here are some Python function encompassing multiple basic actions to serve as high-level interface in this task. Please write usage example for the interface following the format of the examples. {format_instruction}

Here are examples:

{tool_in_context}

Now please write interface usage example:
Function:
```python
{function}
```
Example:
"""

tool_in_context_prompt_combination_together_complete = """Now, here are some Python functions encompassing multiple basic actions to serve as high-level interfaces in this task. Please complete the task with the interface following the format of the examples. {format_instruction}

Here are examples:

{tool_in_context}

Now, please complete the task using these interfaces:
Function:
```python
{function}
```
Example:
"""


tool_in_context_prompt_combination_together_dict = {
    "together": tool_in_context_prompt_combination_together,
    "together_complete": tool_in_context_prompt_combination_together_complete,
}


tool_optimizer_prompt_step_single = """
{query}
{goal}

The actions provided are Python functions and can be executed directly, for example: ```python
{action_example}
```
No additional actions besides the provided actions are available. check_valid_actions is not available.
All the code should be wrapped by```python
```
Now here are some high-level steps to complete this task. Each high-level step are a general Python function encompassing multiple (at least two) basic actions. All the values used in the function should be given as input rather than fixed in the function.

The high-level steps is executed but failed. {format_description}

Here are examples:

{in_context_example}

Now please analyze this case:
```python
{tools}
```
The high level action {function_name} is executed in this state:
{error_line}

But error is observed ({error_info}):
{error_subprocess}

Failed reason:"""

tool_optimizer_prompt_step_full = """
{query}
{goal}

The actions provided are Python functions and can be executed directly, for example: ```python
{action_example}
```
No additional actions besides the provided actions are available. check_valid_actions is not available.
All the code should be wrapped by```python
```
Now here are some high-level steps to complete this task. Each high-level step is a general Python function encompassing multiple (at least two) basic actions. All the values used in the function should be given as input rather than fixed in the function.

The high-level steps are executed but failed. {format_description}

Here are examples:

{in_context_example}

Now please analyze this case:
```python
{tools}
```
The agent performs this task, and the high-level action {function_name} is executed last:
{error_line}

But an error is observed in the last call ({error_info}). The detailed subprocess of this step is:
{error_subprocess}

Failed reason:"""

tool_optimizer_prompt_dict = {
    "single": tool_optimizer_prompt_step_single,
    "full": tool_optimizer_prompt_step_full,
}


def result_is_plan(response):
    return "Improve: Plan" in response


def get_tool_improve_prompt_format_description(version):
    if version == "both":
        return """Please analyze why the execution failed, and give one of the following improvement: Update, Plan.
Please respond in the following format:
Failed reason: <>
Improve: <Update or Plan: [The target function]>
Content: <>
Test case: <> (This is only for Update case, not for Plan)"""
    elif version == "plan":
        return """Please analyze why the execution failed, and give one of the following improvement: Plan.
Please respond in the following format:
Failed reason: <>
Improve: <Plan: [The target function]>
Content: <>"""
    elif version == "update":
        return """Please analyze why the execution failed, and give one of the following improvement: Update.
Please respond in the following format:
Failed reason: <>
Improve: <Update: [The target function]>
Content: <>
Test case: <>"""
    else:
        raise ValueError("{} not implied".format(version))


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


class learnact_learner:
    def __init__(
        self,
        backbone_func,
        dataset_prompt,
        learn_path,
        optimizer_do_learn=False,
        pass_optimizer=False,
        tool_in_context_style="vanilla",
        get_tool_version="structured",
        get_tool_incontext_version="toy",
        usage_version="individual",
        tool_improve_target="step",
        tool_improve_version="both",
        tool_improve_in_context_version="toy",
        tool_improve_history="single",
        step_sample_number=1,
        optimize_iteration_number=1,
        score_type="step_correction",
        error_action_info="not valid",
        same_usage=False,
        learn_save_path="learn_results",
    ):
        self.backbone_func = backbone_func
        self.dataset_prompt = dataset_prompt
        self.learn_path = learn_path
        self.anneal = True
        self.optimizer_do_learn = optimizer_do_learn
        self.tool_in_context_style = tool_in_context_style
        self.get_tool_version = get_tool_version
        self.get_tool_incontext_version = get_tool_incontext_version
        self.usage_version = usage_version
        self.learn_save_path = learn_save_path + "_dir"

        self.tool_improve_target = tool_improve_target
        self.tool_improve_version = tool_improve_version
        self.tool_improve_in_context_version = tool_improve_in_context_version
        self.tool_improve_history = tool_improve_history

        self.step_sample_number = step_sample_number
        self.optimize_iteration_number = optimize_iteration_number
        self.score_type = score_type
        self.error_action_info = error_action_info
        self.pass_optimizer = pass_optimizer
        self.same_usage = same_usage

    def wrap_tool_description(self, query, func_name, tool):

        message = [
            {
                "role": "user",
                "content": query
                + "\n"
                + tool_wrap_prompt_combination.format(
                    func_name=func_name,
                    tool_explanation=self.dataset_prompt["tool_explanation"],
                    function=tool,
                ),
            }
        ]
        params = {
            "x": message,
            # "hist_messages": hist_messages
        }
        description, _ = self.backbone_func(**params)
        description = remove_sure_reply(description).replace("\n", "")
        print("tool: {} \n{}".format(tool, description))
        return description

    def wrap_tool_usage(self, query, func_name, tool):
        tool_in_context_key = "tool_in_context_{}".format(
            self.tool_in_context_style)
        format_instruction = tool_in_context_prompt_combination_format_instruction[
            self.tool_in_context_style
        ]
        message = [
            {
                "role": "user",
                "content": query
                + "\n"
                + tool_in_context_prompt_combination.format(
                    func_name=func_name,
                    format_instruction=format_instruction,
                    tool_in_context=self.dataset_prompt[tool_in_context_key].strip(
                        "\n"
                    ),
                    function=tool,
                ),
            }
        ]
        params = {
            "x": message,
            # "hist_messages": hist_messages
        }
        in_context, _ = self.backbone_func(**params)
        # parse the in context exmaples
        in_context = remove_sure_reply(in_context)

        print("tool usage: {}".format(in_context))
        return in_context

    def wrap_tool_usage_together(self, query, tools):
        tool_in_context_key = "tool_in_context_together"
        format_instruction = tool_in_context_prompt_combination_format_instruction[
            "together"
        ]
        prompt_together = tool_in_context_prompt_combination_together_dict[
            self.usage_version
        ]
        query_usage = (
            query
            + "\n"
            + prompt_together.format(
                format_instruction=format_instruction,
                tool_in_context=self.dataset_prompt[tool_in_context_key].strip(
                    "\n"),
                function=tools,
            )
        )
        if self.same_usage:
            query_usage += self.dataset_prompt["usage_init"].strip("\n")

        message = [{"role": "user", "content": query_usage}]
        params = {
            "x": message,
            # "hist_messages": hist_messages
        }
        in_context, _ = self.backbone_func(**params)
        # parse the in context exmaples
        in_context = remove_sure_reply(in_context).replace("\n\n", "\n")

        if self.same_usage:
            in_context = (
                self.dataset_prompt["usage_init"].strip(
                    "\n") + "\n" + in_context
            )

        print("tool: {} \n{}".format(tools, in_context))
        return in_context

    def recursive_code_generation(
        self, messages, tooluser, env, no_code_condition=None
    ):
        # recurrent code generation until pass the execution

        hist_messages = None
        code = None
        for retry in range(4):
            try:
                params = {"x": messages, "hist_messages": hist_messages}
                response, hist_messages = self.backbone_func(**params)
                # enable do not generate code
                if no_code_condition is not None and no_code_condition(response):
                    return None, response
                num_tokens_from_messages(messages, "gpt-4")
                code = parse_python_func(response)
                print("Generated code: {}".format(code))
                if code == "":
                    raise ValueError(
                        """Your response has no effective Python code. Please write the code. All the code should be wrapped by
```python
```."""
                    )
                # do not use the env; just make sure the code has no error
                tooluser.execute_code_action(env, code, raise_error=True)
                break
            except Exception as e:
                print("ERROR: failed to generate code", str(e))
                traceback_str = traceback.format_exc()
                print(traceback_str)
                messages = [
                    {
                        "role": "user",
                        "content": f"Failed to execute the code due to the error: {traceback_str}. Please fix it and regenerate the whole response.",
                    }
                ]
                code = None
        return code, response

    def create_tool(self, query, data_index, tooluser, env):

        tool_query = (
            query
            + "\n"
            + get_tool_maker_decompose_combination_prompt(self.get_tool_version).format(
                action_example=self.dataset_prompt["action_example"],
                tool_example=self.dataset_prompt["tool_example"][
                    self.get_tool_version + "_" + self.get_tool_incontext_version
                ],
            )
        )

        # recurrent code generation until pass the execution
        messages = [{"role": "user", "content": tool_query}]
        code, response = self.recursive_code_generation(
            messages, tooluser, env)

        if code is None:
            return False, [
                {
                    "func_id": None,
                    "response": {
                        "tool": None,
                        "func_name": None,
                        "tool_cases_list": str(data_index),
                        "verification": None,
                        "usage": None,
                        "description": None,
                        "success": 0,
                        "usable": True,
                        "edited": True,
                        "error": "0_create_tool_subtask",
                        "reflection": "[]",
                        "pre_version": None,
                    },
                }
            ]

        tools_extracted = extract_functions(code)
        imports = extract_import_lines(code)

        if self.usage_version in ["together", "together_complete"]:
            in_context = self.wrap_tool_usage_together(
                query, "\n".join([tool for func_name, tool in tools_extracted])
            )

        response_list = []
        for func_name, tool in tools_extracted:
            description = self.wrap_tool_description(query, func_name, tool)
            if self.usage_version == "individual":
                in_context = self.wrap_tool_usage(query, func_name, tool)
            elif self.usage_version not in ["together", "together_complete"]:
                raise ValueError(
                    "in context method {} not implied".format(
                        self.usage_version)
                )

            tool_code = "\n".join(imports) + "\n" + tool
            # func_name = extract_function_name(tool_code)[-1]
            # print("tool: {} \n{}\n\n{}".format(tool_code, description, in_context))
            response_list.append(
                {
                    "func_id": None,
                    "response": {
                        "tool": tool_code,
                        "func_name": func_name,
                        "tool_cases_list": str(data_index),
                        "verification": None,
                        "usage": in_context,
                        "description": description,
                        "success": 1,
                        "usable": True,
                        "edited": True,
                        "error": "1_create_tool_subtask",
                        "reflection": "[]",
                        "pre_version": None,
                    },
                }
            )
        return True, response_list

    def find_failed_step(self, history, new_tool_df):
        failed_ind = None
        for i, item in enumerate(history):
            if (
                "Failed_subprocess" in item
                and self.error_action_info in item["Observation"]
            ):
                if "Action" in item:
                    try:
                        called_func = find_undefined_function(item["Action"])
                        assert len(called_func) == 1
                    except:
                        called_func = ["None"]

                    called_func = list(called_func)[0]
                    if called_func in new_tool_df["func_name"].values:
                        failed_ind = i
                        break
        return failed_ind

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

    def optimize_tool_step(
        self, query_zero, data_index, history, new_tool_df, tooluser, env
    ):
        new_tool_df_back = copy.deepcopy(new_tool_df)
        new_tool_df_list = [new_tool_df_back]  # keep the previous best result
        for _ in range(self.step_sample_number):
            new_tool_df = copy.deepcopy(new_tool_df_back)
            # find the step id that created tool is used and failed
            failed_ind = self.find_failed_step(history, new_tool_df)
            if failed_ind is not None:
                target_function = history[failed_ind]["Action"].split("(")[0]
                error_info = history[failed_ind]["Observation"].split(".")[0]

                if self.tool_improve_history == "single":
                    item_list = []
                    for i in range(failed_ind - 1, -1, -1):
                        observation = history[i]["Observation"]
                        if observation.split("valid actions.")[-1] != "":
                            break
                    item_list.append("Observation" + ": " + observation)
                    item_list.append("Action" + ": " +
                                     history[failed_ind]["Action"])
                    history_error = "\n".join(item_list)
                elif self.tool_improve_history == "full":
                    history_error = self.wrap_history(
                        history[0: (failed_ind + 1)])
                else:
                    raise ValueError(
                        "tool_improve_history {} not implied".format(
                            self.tool_improve_target
                        )
                    )

                item_list = []
                for item in history[failed_ind]["Failed_subprocess"]:
                    if (
                        "Goal" not in item
                        and "reward" not in item
                        and "Failed_subprocess" not in item
                    ):
                        item_list.append(
                            {"action": "Action", "state": "Observation"}[
                                item[0]]
                            + ": "
                            + str(item[1])
                        )
                history_error_subprocess = "\n".join(item_list)

                tool_improve_in_context_key = "tool_improve_in_context_{}".format(
                    self.tool_improve_in_context_version
                )
                goal = (
                    tooluser.split["goal"][0]
                    + "You should perform actions to accomplish the goal: "
                    + env._get_goal()
                    + "\n"
                    + tooluser.split["goal"][-1]
                )

                tool_optimizer_prompt = tool_optimizer_prompt_dict[
                    self.tool_improve_history
                ]

                optimize_query = tool_optimizer_prompt.format(
                    query=query_zero.strip("\n"),
                    goal=goal,
                    action_example=self.dataset_prompt["action_example"].strip(
                        "\n"),
                    format_description=get_tool_improve_prompt_format_description(
                        self.tool_improve_version
                    ),
                    in_context_example=self.dataset_prompt[
                        tool_improve_in_context_key
                    ].strip("\n"),
                    function_name=target_function,
                    tools="\n\n".join(
                        [
                            item.strip("\n")
                            for item in new_tool_df["tool"].values.tolist()
                        ]
                    ),
                    error_line=history_error.strip("\n"),
                    error_info=error_info,
                    error_subprocess=history_error_subprocess.strip("\n"),
                )
                message = [{"role": "user", "content": optimize_query}]

                tooluser.update_tool(new_tool_df)
                code, improve_response = self.recursive_code_generation(
                    message,
                    tooluser,
                    env,
                    no_code_condition=lambda x: result_is_plan(x),
                )

                print("----------------Action Revise----------------")
                print(optimize_query)
                print("----------------Action Revise Response----------------")
                print(improve_response)

                if result_is_plan(improve_response):
                    reflection = (
                        improve_response.split("Content:")[1]
                        .strip(" ")
                        .replace("\n\n", "\n")
                    )
                    print(reflection)
                    index = new_tool_df.index[
                        new_tool_df["func_name"] == target_function
                    ].values.tolist()[0]
                    new_tool_df.loc[index, "reflection"] = str(
                        eval(
                            str(new_tool_df.loc[index, "reflection"])) + [reflection]
                    )
                    new_tool_df.loc[index, "edited"] = True

                    new_tool_df_list.append(new_tool_df)

                elif code is not None:
                    tools_extracted = extract_functions(code)
                    imports = extract_import_lines(code)

                    if self.usage_version in ["together", "together_complete"]:
                        in_context = self.wrap_tool_usage_together(
                            query_zero,
                            "\n".join(
                                new_tool_df[
                                    ~new_tool_df["func_name"].isin(
                                        [
                                            func_name
                                            for func_name, tool in tools_extracted
                                        ]
                                    )
                                ]["tool"].values.tolist()
                                + [tool for func_name, tool in tools_extracted]
                            ),
                        )
                        # change usage for all the tools in the together case
                        new_tool_df["usage"] = in_context

                    for func_name, tool in tools_extracted:

                        description = self.wrap_tool_description(
                            query_zero, func_name, tool
                        )
                        if self.usage_version == "individual":
                            in_context = self.wrap_tool_usage(
                                query_zero, func_name, tool
                            )
                        elif self.usage_version not in [
                            "together",
                            "together_complete",
                        ]:
                            raise ValueError(
                                "in context method {} not implied".format(
                                    self.usage_version
                                )
                            )

                        tool_code = "\n".join(imports) + "\n" + tool
                        # func_name = extract_function_name(tool_code)[-1]
                        # print(
                        #     "tool: {} \n{}\n".format(
                        #         tool_code, description
                        #     )
                        # )
                        # edit existing tools:
                        if func_name in new_tool_df["func_name"].values:
                            index = new_tool_df.index[
                                new_tool_df["func_name"] == func_name
                            ].values.tolist()[0]
                            new_tool_df.loc[index, "tool"] = (
                                "\n".join(imports) + "\n" + tool
                            )
                            new_tool_df.loc[index, "usage"] = in_context
                            new_tool_df.loc[index, "description"] = description
                            new_tool_df.loc[index, "reflection"] = "[]"
                            new_tool_df.loc[index, "edited"] = True
                        else:
                            # add new tools:
                            result = {
                                "tool": tool_code,
                                "func_name": func_name,
                                "tool_cases_list": str(data_index),
                                "verification": None,
                                "usage": in_context,
                                "description": description,
                                "success": 1,
                                "usable": True,
                                "edited": True,
                                "error": "1_create_tool_subtask",
                                "reflection": "[]",
                                "pre_version": None,
                            }
                            df = pd.DataFrame(
                                [[result[key] for key in result.keys()]],
                                columns=result.keys(),
                            )
                            new_tool_df = pd_concat_ignore2(new_tool_df, df)

                    new_tool_df_list.append(new_tool_df)
        return new_tool_df_list

    def analyze_history(self, new_tool_df, history_list):
        func_score_df = copy.deepcopy(new_tool_df[new_tool_df["usable"]])

        func_score_df["total_step"] = 0
        func_score_df["call"] = 0
        func_score_df["success_call"] = 0
        func_score_df["failed_call"] = 0

        for id, history in enumerate(history_list):
            for step in history:
                if "Action" in step:
                    func_score_df["total_step"] += 1
                    try:
                        called_func = find_undefined_function(step["Action"])
                        assert len(called_func) == 1
                    except:
                        called_func = ["None"]

                    called_func = list(called_func)[0]
                    if called_func in func_score_df["func_name"].values:
                        # print(called_func, id)
                        func_score_df.loc[
                            func_score_df["func_name"] == called_func, "call"
                        ] += 1
                        if self.error_action_info in step["Observation"]:
                            func_score_df.loc[
                                func_score_df["func_name"] == called_func, "failed_call"
                            ] += 1
                        else:
                            func_score_df.loc[
                                func_score_df["func_name"] == called_func,
                                "success_call",
                            ] += 1

        print(func_score_df["total_step"])
        print(func_score_df["tool"])
        print(func_score_df["call"])
        print(func_score_df["success_call"])
        print(func_score_df["failed_call"])
        return func_score_df

    def select_best_tools_index(self, func_score_df_list, score_success):
        score_list = []
        full_score_list = []

        for ind, func_score_df in enumerate(func_score_df_list):
            score_step_correction = (
                func_score_df["success_call"].sum(
                ) / func_score_df["call"].sum()
                if func_score_df["call"].sum() > 0
                else 0
            )
            score_call_ratio = (
                func_score_df["success_call"].sum(
                ) / func_score_df.loc[0, "total_step"]
            )
            score_used_ratio = (
                func_score_df["call"].sum() /
                func_score_df.loc[0, "total_step"]
            )

            print(
                "step_correction: {}, call_ratio: {}, used_ratio: {}, success: {}".format(
                    score_step_correction,
                    score_call_ratio,
                    score_used_ratio,
                    np.mean(score_success[ind]),
                )
            )

            if self.score_type == "step_correction":
                score = score_step_correction
            elif self.score_type == "call_ratio_success":
                score = score_call_ratio + np.mean(score_success[ind])
            elif self.score_type == "step_correction_call_ratio_success":
                score = (
                    score_step_correction
                    + score_call_ratio
                    + np.mean(score_success[ind])
                )
            else:
                raise ValueError(
                    "score_type {} not implied".format(self.score_type))
            score_list.append(score)

            full_score_list.append(
                {
                    "step_correction": score_step_correction,
                    "call_ratio": score_call_ratio,
                    "used_ratio": score_used_ratio,
                    "success": np.mean(score_success[ind]),
                    "final_score": score,
                }
            )

        print(score_list)
        return np.argmax(score_list), full_score_list

    def find_failed_data_index_step(self, history_list, new_tool_df):
        for index, history in enumerate(history_list):
            if self.find_failed_step(history, new_tool_df) is not None:
                return index
        return None

    def __call__(
        self,
        train,
        val=None,
        tooluser=None,
        use_response=None,
        evaluator=None,
    ):

        tooluser.update_tool([])

        env = train[0]["input"]
        data_index = [data["index"] for data in train]

        query_zero = tooluser(env, zero_shot_scene=True)

        tooluser.update_tool(None)

        file_name = os.path.join(self.learn_save_path, "debug_tem_{}_{}.csv")
        if not os.path.exists(self.learn_save_path):
            os.makedirs(self.learn_save_path)

        new_tool_df_list = []

        max_step_pre = tooluser.max_steps

        for sample_step in range(self.step_sample_number):

            # create tools
            _, response_list = self.create_tool(
                query_zero, data_index=data_index, tooluser=tooluser, env=env
            )

            if not self.optimizer_do_learn:
                return response_list

            df_list = []
            for response in response_list:
                df_list.append(response["response"])
            new_tool_df = pd.DataFrame(
                df_list, columns=response["response"].keys())

            new_tool_df_list.append(new_tool_df)

            new_tool_df.to_csv(file_name.format(0, sample_step))

        debug_eval_file_name = os.path.join(
            self.learn_save_path, "debug_eval_{}_{}.json"
        )
        debug_eval_score_name = os.path.join(
            self.learn_save_path, "debug_eval_score_{}_{}.json"
        )

        for opt_step in range(self.optimize_iteration_number+1):
            func_score_df_list = []
            score_success_list = []
            history_list_all_samples = []
            for sample_step, new_tool_df in enumerate(new_tool_df_list):
                tooluser.update_tool(new_tool_df)
                tooluser.max_steps = 10

                # use the tools
                history_list = []
                score_list = []
                for data in train:
                    env = data["input"]
                    env.reset()
                    use_response = tooluser(env)
                    histoty = use_response["gen"]["history"]
                    history_list.append(histoty)
                    score_list.append(use_response["res"])

                history_list_all_samples.append(history_list)
                score_success = np.mean(score_list)

                # save the tool using response temperally for debug

                with open(debug_eval_file_name.format(opt_step, sample_step), "w") as f:
                    json.dump(history_list, f)
                with open(
                    debug_eval_score_name.format(opt_step, sample_step), "w"
                ) as f:
                    json.dump(score_list, f)

                # tool_user_result_analyze
                func_score_df = self.analyze_history(new_tool_df, history_list)
                func_score_df_list.append(func_score_df)
                score_success_list.append(score_list)

            index, full_score_list = self.select_best_tools_index(
                func_score_df_list, score_success_list
            )
            new_tool_df_best = new_tool_df_list[index]
            history_list = history_list_all_samples[index]
            score_list = score_success_list[index]
            func_score_df_best = func_score_df_list[index]
            full_score_best = full_score_list[index]

            # visualize the new tools
            print(
                "----------------------------------------iter {}----------------------------------------".format(
                    opt_step + 1
                )
            )
            for key in new_tool_df_best.keys():
                print("\n" + key + "\n")
                if key in ["tool", "func_name", "description", "reflection", "error"]:
                    print("\n".join(new_tool_df_best[key].values.tolist()))
                else:
                    print(new_tool_df_best[key].values.tolist()[0])

            print(func_score_df_best["total_step"])
            print(func_score_df_best["tool"])
            print(func_score_df_best["call"])
            print(func_score_df_best["success_call"])
            print(func_score_df_best["failed_call"])

            print(full_score_best)

            tooluser.max_steps = max_step_pre

            if (
                not self.pass_optimizer
                and opt_step < self.optimize_iteration_number
            ):
                if self.tool_improve_target == "step":
                    index = self.find_failed_data_index_step(
                        history_list, new_tool_df_best
                    )
                else:
                    raise ValueError(
                        "tool_improve_target {} not implied".format(
                            self.tool_improve_target
                        )
                    )
                if index is not None:
                    # if not pass_create:
                    histoty = history_list[index]
                    env = train[index]["input"]
                    env.reset()

                    if self.tool_improve_target == "step":
                        new_tool_df_list = self.optimize_tool_step(
                            query_zero,
                            data_index,
                            histoty,
                            new_tool_df_best,
                            tooluser,
                            env,
                        )  # env here matters
                    else:
                        raise ValueError(
                            "tool_improve_target {} not implied".format(
                                self.tool_improve_target
                            )
                        )

                    # save the new new_tool_df_list
                    for sample_step, new_tool_df in enumerate(new_tool_df_list):
                        new_tool_df.to_csv(file_name.format(
                            opt_step + 1, sample_step))

                else:
                    break
            else:
                break

        new_tool_df_best["usable"] = copy.deepcopy(new_tool_df_best["edited"])
        # select the tools again to make the saved tools concise

        response_list = []
        for line_dict in new_tool_df_best.to_dict(orient="records"):
            response_list.append(
                {
                    "func_id": (
                        line_dict["pre_version"] if line_dict["usable"] else None
                    ),
                    "response": line_dict,
                }
            )

        tooluser.update_tool(None)

        return response_list
