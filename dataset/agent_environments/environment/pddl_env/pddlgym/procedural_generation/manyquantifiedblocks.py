from pddlgym.parser import PDDLDomainParser, PDDLProblemParser
from pddlgym.structs import LiteralConjunction
import pddlgym
import os
import numpy as np
from itertools import count
np.random.seed(0)


PDDLDIR = os.path.join(os.path.dirname(pddlgym.__file__), "pddl")

def sample_blocks(domain, pile_heights):
    block_type = domain.types['block']
    ontable = domain.predicates['ontable']
    on = domain.predicates['on']

    blocks = set()
    blocks_state = set()

    block_idx = count()
    for pile_height in pile_heights:
        assert pile_height >= 1
        blocks_in_pile = [block_type("b{}".format(next(block_idx))) \
            for _ in range(pile_height)]
        blocks.update(blocks_in_pile)
        # left is top
        if pile_height > 1:
            for b1, b2 in zip(blocks_in_pile[:-1], blocks_in_pile[1:]):
                blocks_state.add(on(b1, b2))
        blocks_state.add(ontable(blocks_in_pile[-1]))

    return blocks, blocks_state

def create_goal(domain, objects, pile_heights):
    on = domain.predicates['on']
    ontable = domain.predicates['ontable']

    remaining_blocks = sorted(objects)

    goal_lits = []

    for pile_height in pile_heights:
        assert pile_height >= 1
        if len(remaining_blocks) == 0:
            break
        pile_height = min(len(remaining_blocks), pile_height)
        block_idxs = np.random.choice(len(remaining_blocks), size=pile_height, replace=False)
        blocks_in_pile = []
        for idx in block_idxs:
            blocks_in_pile.append(remaining_blocks[idx])
        remaining_blocks = [b for i, b in enumerate(remaining_blocks) if i not in block_idxs]
        # left is top
        if pile_height > 1:
            for b1, b2 in zip(blocks_in_pile[:-1], blocks_in_pile[1:]):
                goal_lits.append(on(b1, b2))
        goal_lits.append(ontable(blocks_in_pile[-1]))

    return LiteralConjunction(goal_lits)

def sample_problem(domain, problem_dir, problem_outfile, 
                   min_num_piles=30, max_num_piles=50,
                   min_num_piles_goal=1, max_num_piles_goal=2,
                   max_num_blocks=1000):
    
    while True:
        blocks, block_state = sample_blocks(domain, 
            pile_heights=np.random.randint(1, 3, 
                size=np.random.randint(min_num_piles, max_num_piles+1)),
        )
        if len(blocks) <= max_num_blocks:
            break

    while True:
        goal = create_goal(domain, blocks, 
            pile_heights=np.random.randint(2, 4, 
                size=np.random.randint(min_num_piles_goal, max_num_piles_goal+1)))

        if not goal.holds(block_state):
            break

    objects = blocks
    initial_state = block_state

    filepath = os.path.join(PDDLDIR, problem_dir, problem_outfile)

    PDDLProblemParser.create_pddl_file(
        filepath,
        objects=objects,
        initial_state=initial_state,
        problem_name="manyquantifiedblocks",
        domain_name=domain.domain_name,
        goal=goal,
        fast_downward_order=True,
    )
    print("Wrote out to {}.".format(filepath))

def generate_problems():
    domain = PDDLDomainParser(os.path.join(PDDLDIR, "manyblockssmallpiles.pddl"),
        expect_action_preds=False,
        operators_as_actions=True)

    for problem_idx in range(50):
        if problem_idx < 40:
            problem_dir = "manyquantifiedblocks"
        else:
            problem_dir = "manyquantifiedblocks_test"
        problem_outfile = "problem{}.pddl".format(problem_idx)

        if problem_idx < 40:
            sample_problem(domain, problem_dir, problem_outfile, 
                   min_num_piles=2, max_num_piles=3,
                   min_num_piles_goal=1, max_num_piles_goal=1,
                   max_num_blocks=5)
        else:
            sample_problem(domain, problem_dir, problem_outfile, 
                   min_num_piles=5, max_num_piles=8,
                   min_num_piles_goal=1, max_num_piles_goal=1)

if __name__ == "__main__":
    generate_problems()
