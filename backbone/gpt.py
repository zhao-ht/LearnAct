import openai
import time
import os
import numpy as np
from aux_func.aux_func import time_limit, run_with_timeout
import pandas as pd

import copy
import tiktoken


def call_chat_gpt(
    messages,
    hist_messages=None,
    model_size="gpt-3.5-turbo",
    stop=None,
    temperature=0.0,
    top_p=1.0,
    max_tokens=None,
    time_limit_query=200,
):
    if model_size == "gpt-3.5":
        model_size = "gpt-35-turbo"
    if model_size == "gpt-35":
        model_size = "gpt-35-turbo"
    messages = copy.deepcopy(messages)
    hist_messages = copy.deepcopy(hist_messages)
    if hist_messages is not None:
        messages = hist_messages + messages

    wait = 3
    call_time = 0
    save_message = True
    while call_time < 10000:
        try:
            ans = openai.ChatCompletion.create(
                engine=model_size,
                max_tokens=max_tokens,
                stop=stop,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                # n=1
            )
            messages.append(
                {"role": "assistant", "content": ans.choices[0]["message"]["content"]}
            )

            return ans.choices[0]["message"]["content"], messages
        except Exception as e:
            # time.sleep(min(wait, 50+10*np.random.rand()))
            time.sleep(np.random.rand())
            wait += np.random.rand()
            call_time += 1
    raise RuntimeError("Failed to call gpt")


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif (
        "gpt-3.5-turbo" in model
        or "gpt-35-turbo" in model
        or "gpt-3.5" in model
        or "gpt-35" in model
    ):
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    elif "text-davinci-003" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
