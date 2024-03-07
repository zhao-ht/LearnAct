import argparse


def add_dataset_args(args, left):
    parser_new = argparse.ArgumentParser()

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
        pass
    elif args.dataset_name in [
        "alfworld_put",
        "alfworld_clean",
        "alfworld_heat",
        "alfworld_cool",
        "alfworld_examine",
        "alfworld_puttwo",
    ]:
        pass
    else:
        raise ValueError("dataset not implied yet")

    return args
