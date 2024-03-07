alfworld_instruction = """
Your task is to interact with a virtual household simulator to accomplish a specific task. With each interaction, you will receive an observation.
Your role is to decide on an action based on the observation. Please ensure that any objects ('obj') and receptacles ('recep') you mention in your response are present in the observation provided.

Here are the available actions you can take:
    take(obj,recep)
    put(obj,recep)
    open(recep)
    close(recep)
    toggle(obj_or_recep)
    clean(obj,recep)
    cool(obj,recep)
    heat(obj,recep)
    inventory()
    examine(obj_or_recep)
    goto(recep)
    use(obj)
"""
alfworld_sys = "You are a helpful assistant"
code_as_policy_prompt_dict = {
    "blockworld": {
        "examples": [
            """
Goal: The goal is to satisfy the following conditions: b1 is on b2., b2 is on b3.
Observation: b1 is on the table.  b2 is on the table.  B3 is on the table. Robot arm is empty. The b1 is clear. The b2 is clear. The b3 is clear. 
Action:
```python
Pickup('b2')
Stack('b2','b3')
Pickup('b3')
Pickup('b1')
Stack('b1','b2')
```
"""
        ],
        "instruction": """
The robot has four actions: Pickup, Putdown, Stack, and Unstack. The domain assumes a world where there are a set of blocks that can be stacked on top of each other, an arm that can hold one block at a time, and a table where blocks can be placed.
    The actions defined in this domain include:
    Pickup(block): allows the arm to pick up a block from the table if it is clear and the arm is empty. After the pickup action, the arm will be holding the block, and the block will no longer be on the table or clear.
    Putdown(block): allows the arm to put down a block on the table if it is holding a block. After the putdown action, the arm will be empty, and the block will be on the table and clear.
    Stack(block1,block2): allows the arm to stack a block on top of another block if the arm is holding the top block and the bottom block is clear. After the stack action, the arm will be empty, the top block will be on top of the bottom block, and the bottom block will no longer be clear.
    Unstack(block1,block2): allows the arm to unstack a block from on top of another block if the arm is empty and the top block is clear. After the unstack action, the arm will be holding the top block, the top block will no longer be on top of the bottom block, and the bottom block will be clear.
""",
        "system_msg": "You are a master in planning.",
    },
    "barman": {
        "examples": [
            """
The goal is to satisfy the following conditions: shot1 contains cocktail1. 
Observation: Cocktail1 part1 ingredient is ingredient1. Cocktail1 part2 ingredient is ingredient3. Cocktail2 part1 ingredient is ingredient2. Cocktail2 part2 ingredient is ingredient3. Cocktail3 part1 ingredient is ingredient1. Cocktail3 part2 ingredient is ingredient2. Dispenser1 dispenses ingredient1. Dispenser2 dispenses ingredient2. Dispenser3 dispenses ingredient3. Left hand is empty. Level l0 is next to level l1. Level l1 is next to level l2. Right hand is empty. Shaker1 is at empty level l0. Shaker1 is at level l0. Shaker1 is clean. Shaker1 is empty. Shaker1 is on the table. Shot1 is clean. Shot1 is empty. Shot1 is on the table. Shot2 is clean. Shot2 is empty. Shot2 is on the table. Shot3 is clean. Shot3 is empty. Shot3 is on the table. Shot4 is clean. Shot4 is empty. Shot4 is on the table.
Action:
```python
grasp('right','shot1')
fill_shot('shot1','ingredient3','right','left','dispenser3')
pour_shot_to_clean_shaker('shot1','ingredient3','shaker1','right','l0','l1')
clean_shot('shot1','ingredient3','right','left')
fill_shot('shot1','ingredient1','right','left','dispenser1')
pour_shot_to_used_shaker('shot1','ingredient1','shaker1','right','l1','l2')
clean_shot('shot1','ingredient1','right','left')
leave('right','shot1')
grasp('right','shaker1')
shake('cocktail1','ingredient1','ingredient3','shaker1','right','left')
pour_shaker_to_shot('cocktail1','shot1','right','shaker1','l2','l1')
```
"""
        ],
        "instruction": """
You are a robot barman that manipulates drink dispensers, shot glasses and a shaker. You have two hands. The goal is to find a plan that serves a desired set of drinks. Here are the actions you can do. Each valid action is a short phrase following fixed patterns:

    grasp(<hand>,<container>): Grasp a container
    leave(<hand>,<container>): Leave a container on the table
    fill_shot(<shot>,<ingredient>,<hand1>,<hand2>,<dispenser>): Fill a shot glass with an ingredient from dispenser
    refill_shot(<shot>,<ingredient>,<hand1>,<hand2>,<dispenser>): Refill a shot glass with an ingredient from dispenser
    empty_shot(<hand>,<shot>,<beverage>): Empty a shot glass
    clean_shot(<shot>,<beverage>,<hand1>,<hand2>): Clean a shot glass
    pour_shot_to_clean_shaker(<shot>,<ingredient>,<shaker>,<hand1>,<level1>,<level2>): Pour an ingredient from a shot glass to a clean shaker from level1 to level2
    pour_shot_to_used_shaker(<shot>,<ingredient>,<shaker>,<hand1>,<level1>,<level2>): Pour an ingredient from a shot glass to a used shaker from level1 to level2
    empty_shaker(<hand>,<shaker>,<cocktail>,<level1>,<level2>): Empty a shaker containing cocktail from level1 to level2
    clean_shaker(<hand1>,<hand2>,<shaker>): Clean a shaker
    shake(<cocktail>,<ingredient1>,<ingredient2>,<shaker>,<hand1>,<hand2>): Shake a cocktail in a shaker
    pour_shaker_to_shot(<beverage>,<shot>,<hand>,<shaker>,<level1>,<level2>): Pour a beverage from a shaker to a shot glass from level1 to level2

    You have the following restrictions on your actions:
    You can only grasp a container if your hand is empty and it is on the table.
    You can only leave a container if you are holding it.
    You can only fill a shot glass if you are holding the shot glass, your other hand is empty, the shot glass is empty and clean.
    You can only refill a shot glass if you are holding the shot glass, your other hand is empty, the shot glass is empty and has contained the saree ingredient before.
    You can only empty a shot glass if you are holding the shot glass and it contains a beverage.
    You can only pour from a shot glass to a clean shaker if you are holding the shot glass, the shot glass contains an ingredient, and the shaker is empty and clean.
    You can only pour from a shot glass to a used shaker if you are holding the shot glass, the shot glass contains an ingredient, the shaker is unshaked and at a level not full.
    You can only empty a shaker if you are holding the shaker and the shaker contains a shaked beverage.
    You can only clean a shaker if you are holding the shaker, your other hand is empty, and the shaker is empty.
    You can only shake a cocktail if you are holding the shaker, your other hand is empty, the shaker is unshaked, and the shaker contains two ingredients, and both ingredients are parts of a cocktail.
    You can only pour from a shaker to a shot glass if you are holding the shaker, the shaker contains the cocktail, the shaker is shaked, and the shot glass is empty and clean.

    Once you grasp a container, you are holding the container and the container is not on the table.
    Once you leave a container on the table, your hand become empty.
    Once you pour an ingredient from a shot glass to a shaker, the shaker contains the ingredient and is at one level above the previous level, and the shot glass becomes empty.
    Once you empty a shaker, the shaker is at the empty level.
    Once you shake, the two ingredients in the shaker become a cocktail.
    Once you pour from a shaker to a shot glass, the shot glass contains the beverage in the shaker, the shot glass is no longer clean and empty, and the shaker is at one level below the previous level.
""",
        "system_msg": "You are a master in planning.",
    },
    "gripper": {
        "examples": [
            """
The goal is to satisfy the following conditions: ball1 is at roomb. , ball2 is at roomb. , ball3 is at roomb. 
Observation: Ball1 is a ball. Ball1 is at rooma. Ball2 is a ball. Ball2 is at rooma. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at rooma. Room rooma Room roomb
Action:
```python
pick('ball1','rooma','right')
pick('ball2','rooma','left')
move('rooma','roomb')
drop('ball1','rooma','right')
drop('ball1','roomb','right')
drop('ball2','roomb','left')
move('roomb','rooma')
pick('ball3','rooma','right')
move('rooma','roomb')
drop('ball3','rooms','right')
```
"""
        ],
        "instruction": """
You are a robot with a gripper that can move objects between different rooms. Your name is Robby.
    There are three actions defined in this domain:
    move(<room1>,<room2>): This action allows the robot to move from one room to another.The action has a single precondition, which is that the robot is currently in a room. The effect of this action is to move the robot to another room and to remove the fact that it is in the original room.
    pick(<obj>,<room>,<gripper>): This action allows the robot to pick up an object using the gripper. The action has three preconditions: (1) the object is located in a room (2) the robot is currently in the same room and (3) the gripper is free (i.e., not holding any object). The effect of this action is to update the state of the world to show that the robot is carrying the object using the gripper, the object is no longer in the room, and the gripper is no longer free.
    drop(<obj>,<room>,<gripper>): This action allows the robot to drop an object that it is carrying. The action has two preconditions: (1) the robot is currently carrying the object using the gripper, and (2) the robot is currently in a room. The effect of this action is to update the state of the world to show that the robot is no longer carrying the object using the gripper, the object is now located in the room, and the gripper is now free.
""",
        "system_msg": "You are a master in moving objects.",
    },
    "tyreworld": {
        "examples": [
            """
The goal is to satisfy the following conditions: Wheel r1 is inflated., r1 is on the-hub1., w1 is in boot.
Observation: Boot is closed. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is tight. Wheel r1 is intact. Wheel r1 is not inflated. Wheel w1 is on hub the-hub1. Wrench is in boot.
Action:
```python
open('boot')
fetch('wrench','boot')
loosen('nuts1', 'the-hub1')
fetch('jack','boot')
jack_up('the-hub1')
undo('nuts1','the-hub1')
remove_wheel('w1','the-hub1')
put_away('w1','boot')
fetch('r1','boot')
put_on_wheel('r1','the-hub1')
do_up('nuts1','the-hub1')
fetch('pump','boot')
inflate('r1')
```
"""
        ],
        "instruction": """
Your goal is to replace flat tyres with intact tyres on the hubs. Remember to open boot first to get tools you need. Intact tyres should be inflated. The nuts should be tight on the hubs. The flat tyres, wrench, jack, and pump should be in the boot. The boot should be closed.
    There are actions defined in this domain:
    open(<container>): The precondition for this action is that the container is unlocked and closed. The effect of this action is that the container is open and not closed.
    close(<container>): The precondition for this action is that the container is open. The effect of this action is that the container is closed and not open.
    fetch(<object>,<container>): The precondition for this action is that the object is inside the container and the container is open. The effect of this action is that the object is held by the agent and not inside the container.
    put_away(<object>,<container>): The precondition for this action is that the object is held by the agent and the container is open. The effect of this action is that the object is inside the container and not held by the agent.
    loosen(<nut>,<hub>): The precondition for this action is that the agent has a wrench, the nut on hub is tight, and the hub is on the ground. The effect of this action is that the nut on hub is loose and not tight.
    tighten(<nut>,<hub>): The precondition for this action is that the agent has a wrench, the nut on hub is loose, and the hub is on the ground. The effect of this action is that the nut on hub is tight and not loose.
    jack_up(<hub>): This action represents the process of lifting a hub off the ground using a jack. It requires the agent to have a jack and for the hub to be on the ground. After performing this action, the hub will no longer be on the ground and the agent will no longer have the jack.
    jack_down(<hub>): This action represents the process of lowering a hub back to the ground from an elevated position using a jack. It requires the agent to have the hub off the ground. After performing this action, the hub will be back on the ground and the agent will have the jack.
    undo(<nut>,<hub>): This action undo the fastening of a nut on a hub. The preconditions are the hub is not on the ground (i.e., it has been jacked up), the hub is fastened, the agent has a wrench and the nut is loose. The effects are the agent has the nut, the hub is unfastened, the hub is no longer loose and the hub is not fastened anymore.
    do_up(<nut>,<hub>): This action fasten a nut on a hub. The preconditions are the agent has a wrench, the hub is unfastened, the hub is not on the ground (i.e., it has been jacked up) and the agent has the nut to be fastened. The effects are the nut is now loose on the hub, the hub is fastened, the hub is no longer unfastened and the agent no longer has the nut.
    remove_wheel(<wheel>,<hub>): This action removes a wheel from a hub. It can only be performed if the hub is not on the ground, the wheel is currently on the hub, and the hub is unfastened. After the action is performed, the agent will have the removed wheel and the hub will be free, meaning that the wheel is no longer on the hub.
    put_on_wheel(<wheel>,<hub>): This action puts a wheel onto a hub. It can only be performed if the agent has the wheel, the hub is free, the hub is unfastened, and the hub is not on the ground. After the action is performed, the wheel will be on the hub, the hub will no longer be free, and the agent will no longer have the wheel.
    inflate(<wheel>): This action inflates a wheel using a pump. It can only be performed if the agent has a pump, the wheel is not inflated, and the wheel is intact. After the action is performed, the wheel will be inflated.
""",
        "system_msg": "You are a master in car repair.",
    },
}


code_as_policy_prompt_hier_dict = {
    "blockworld": {
        "examples": [
            """
Goal: The goal is to satisfy the following conditions: b1 is on b2., b2 is on b3.
Observation: b2 is on b3. b3 is on b1. b1 is on the table.  Robot arm is empty. The b2 is clear.
Action:
```python
def Unstack_block_pillar(block_list):
    global env
    for ind in range(len(block_list)-1):
        Unstack(block_list[ind],block_list[ind+1])
        Putdown(block_list[ind])
        
Unstack_block_pillar(['b2','b3','b1'])        
Pickup('b2')
Stack('b2','b3')
Pickup('b3')
Pickup('b1')
Stack('b1','b2')
```
"""
        ],
        "instruction": """
The robot has four actions: Pickup, Putdown, Stack, and Unstack. The domain assumes a world where there are a set of blocks that can be stacked on top of each other, an arm that can hold one block at a time, and a table where blocks can be placed.
    The actions defined in this domain include:
    Pickup(block): allows the arm to pick up a block from the table if it is clear and the arm is empty. After the pickup action, the arm will be holding the block, and the block will no longer be on the table or clear.
    Putdown(block): allows the arm to put down a block on the table if it is holding a block. After the putdown action, the arm will be empty, and the block will be on the table and clear.
    Stack(block1,block2): allows the arm to stack a block on top of another block if the arm is holding the top block and the bottom block is clear. After the stack action, the arm will be empty, the top block will be on top of the bottom block, and the bottom block will no longer be clear.
    Unstack(block1,block2): allows the arm to unstack a block from on top of another block if the arm is empty and the top block is clear. After the unstack action, the arm will be holding the top block, the top block will no longer be on top of the bottom block, and the bottom block will be clear.
""",
        "system_msg": "You are a master in planning.",
    },
    "barman": {
        "examples": [
            """
The goal is to satisfy the following conditions: shot1 contains cocktail1. 
Observation: Cocktail1 part1 ingredient is ingredient1. Cocktail1 part2 ingredient is ingredient3. Cocktail2 part1 ingredient is ingredient2. Cocktail2 part2 ingredient is ingredient3. Cocktail3 part1 ingredient is ingredient1. Cocktail3 part2 ingredient is ingredient2. Dispenser1 dispenses ingredient1. Dispenser2 dispenses ingredient2. Dispenser3 dispenses ingredient3. Left hand is empty. Level l0 is next to level l1. Level l1 is next to level l2. Right hand is empty. Shaker1 is at empty level l0. Shaker1 is at level l0. Shaker1 is clean. Shaker1 is empty. Shaker1 is on the table. Shot1 is clean. Shot1 is empty. Shot1 is on the table. Shot2 is clean. Shot2 is empty. Shot2 is on the table. Shot3 is clean. Shot3 is empty. Shot3 is on the table. Shot4 is clean. Shot4 is empty. Shot4 is on the table.
Action:
```python
def fill_and_pour_to_shaker(shot, ingredient, dispenser, shaker, hand1,
    hand2, level):
    global env
    grasp(hand1, shot)
    fill_shot(shot, ingredient, hand1, hand2, dispenser)
    if level == 'l0':
        pour_shot_to_clean_shaker(shot, ingredient, shaker, hand1, level, 'l1')
    else:
        pour_shot_to_used_shaker(shot, ingredient, shaker, hand1, level, 'l2')
    clean_shot(shot, ingredient, hand1, hand2)
    leave(hand1, shot)
    
def shake_cocktail(ingredient1, ingredient2, shaker, hand1, hand2):
    grasp(hand1, shaker)
    global env
    shake('cocktail3', ingredient1, ingredient2, shaker, hand1, hand2)
    
def pour_from_shaker_to_shot(shot, shaker, hand1, level1, level2):
    grasp(hand1, shot)
    global env
    pour_shaker_to_shot('cocktail3', shot, hand1, shaker, level1, level2)
    leave(hand1, shot)
    
def prepare_cocktail(shot, ingredient1, ingredient2, shaker, hand1, hand2,
    dispenser1, dispenser2, level1, level2):
    global env
    fill_and_pour_to_shaker(shot, ingredient1, dispenser1, shaker, hand1,
        hand2, level1)
    fill_and_pour_to_shaker(shot, ingredient2, dispenser2, shaker, hand1,
        hand2, level2)
    shake_cocktail(ingredient1, ingredient2, shaker, hand1, hand2)
    
fill_and_pour_to_shaker('shot1','ingredient3','dispenser3','shaker1','right','left','l0')
fill_and_pour_to_shaker('shot1','ingredient1','dispenser1','shaker1','right','left','l1')
clean_shot('shot1','ingredient1','right','left')
leave('right','shot1')
grasp('right','shaker1')
shake('cocktail1','ingredient1','ingredient3','shaker1','right','left')
pour_shaker_to_shot('cocktail1','shot1','right','shaker1','l2','l1')
```
"""
        ],
        "instruction": """
You are a robot barman that manipulates drink dispensers, shot glasses and a shaker. You have two hands. The goal is to find a plan that serves a desired set of drinks. Here are the actions you can do. Each valid action is a short phrase following fixed patterns:

    grasp(<hand>,<container>): Grasp a container
    leave(<hand>,<container>): Leave a container on the table
    fill_shot(<shot>,<ingredient>,<hand1>,<hand2>,<dispenser>): Fill a shot glass with an ingredient from dispenser
    refill_shot(<shot>,<ingredient>,<hand1>,<hand2>,<dispenser>): Refill a shot glass with an ingredient from dispenser
    empty_shot(<hand>,<shot>,<beverage>): Empty a shot glass
    clean_shot(<shot>,<beverage>,<hand1>,<hand2>): Clean a shot glass
    pour_shot_to_clean_shaker(<shot>,<ingredient>,<shaker>,<hand1>,<level1>,<level2>): Pour an ingredient from a shot glass to a clean shaker from level1 to level2
    pour_shot_to_used_shaker(<shot>,<ingredient>,<shaker>,<hand1>,<level1>,<level2>): Pour an ingredient from a shot glass to a used shaker from level1 to level2
    empty_shaker(<hand>,<shaker>,<cocktail>,<level1>,<level2>): Empty a shaker containing cocktail from level1 to level2
    clean_shaker(<hand1>,<hand2>,<shaker>): Clean a shaker
    shake(<cocktail>,<ingredient1>,<ingredient2>,<shaker>,<hand1>,<hand2>): Shake a cocktail in a shaker
    pour_shaker_to_shot(<beverage>,<shot>,<hand>,<shaker>,<level1>,<level2>): Pour a beverage from a shaker to a shot glass from level1 to level2

    You have the following restrictions on your actions:
    You can only grasp a container if your hand is empty and it is on the table.
    You can only leave a container if you are holding it.
    You can only fill a shot glass if you are holding the shot glass, your other hand is empty, the shot glass is empty and clean.
    You can only refill a shot glass if you are holding the shot glass, your other hand is empty, the shot glass is empty and has contained the saree ingredient before.
    You can only empty a shot glass if you are holding the shot glass and it contains a beverage.
    You can only pour from a shot glass to a clean shaker if you are holding the shot glass, the shot glass contains an ingredient, and the shaker is empty and clean.
    You can only pour from a shot glass to a used shaker if you are holding the shot glass, the shot glass contains an ingredient, the shaker is unshaked and at a level not full.
    You can only empty a shaker if you are holding the shaker and the shaker contains a shaked beverage.
    You can only clean a shaker if you are holding the shaker, your other hand is empty, and the shaker is empty.
    You can only shake a cocktail if you are holding the shaker, your other hand is empty, the shaker is unshaked, and the shaker contains two ingredients, and both ingredients are parts of a cocktail.
    You can only pour from a shaker to a shot glass if you are holding the shaker, the shaker contains the cocktail, the shaker is shaked, and the shot glass is empty and clean.

    Once you grasp a container, you are holding the container and the container is not on the table.
    Once you leave a container on the table, your hand become empty.
    Once you pour an ingredient from a shot glass to a shaker, the shaker contains the ingredient and is at one level above the previous level, and the shot glass becomes empty.
    Once you empty a shaker, the shaker is at the empty level.
    Once you shake, the two ingredients in the shaker become a cocktail.
    Once you pour from a shaker to a shot glass, the shot glass contains the beverage in the shaker, the shot glass is no longer clean and empty, and the shaker is at one level below the previous level.
""",
        "system_msg": "You are a master in planning.",
    },
    "gripper": {
        "examples": [
            """
The goal is to satisfy the following conditions: ball1 is at roomb. , ball2 is at roomb. , ball3 is at roomb. 
Observation: Ball1 is a ball. Ball1 is at rooma. Ball2 is a ball. Ball2 is at rooma. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at rooma. Room rooma Room roomb
Action:
```python
def carry_to(room1,room2,obj,gripper):
    global env
    pick(obj,room1,gripper)
    move(room1,room2)
    drop(obj,room2,gripper)
carry_to('rooma','roomb','ball1','right')
move('roomb','rooma')
carry_to('rooma','roomb','ball2','right')
move('roomb','rooma')
carry_to('rooma','roomb','ball3','right')
move('roomb','rooma')
```
"""
        ],
        "instruction": """
You are a robot with a gripper that can move objects between different rooms. Your name is Robby.
    There are three actions defined in this domain:
    move(<room1>,<room2>): This action allows the robot to move from one room to another.The action has a single precondition, which is that the robot is currently in a room. The effect of this action is to move the robot to another room and to remove the fact that it is in the original room.
    pick(<obj>,<room>,<gripper>): This action allows the robot to pick up an object using the gripper. The action has three preconditions: (1) the object is located in a room (2) the robot is currently in the same room and (3) the gripper is free (i.e., not holding any object). The effect of this action is to update the state of the world to show that the robot is carrying the object using the gripper, the object is no longer in the room, and the gripper is no longer free.
    drop(<obj>,<room>,<gripper>): This action allows the robot to drop an object that it is carrying. The action has two preconditions: (1) the robot is currently carrying the object using the gripper, and (2) the robot is currently in a room. The effect of this action is to update the state of the world to show that the robot is no longer carrying the object using the gripper, the object is now located in the room, and the gripper is now free.
""",
        "system_msg": "You are a master in moving objects.",
    },
    "tyreworld": {
        "examples": [
            """
The goal is to satisfy the following conditions: Wheel r1 is inflated., r1 is on the-hub1., w1 is in boot.
Observation: Boot is closed. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is tight. Wheel r1 is intact. Wheel r1 is not inflated. Wheel w1 is on hub the-hub1. Wrench is in boot.
Action:
```python
def get_all_tools(container):
    global env
    open(container)
    fetch('wrench',container)
    fetch('jack',container)
    fetch('pump',container)

def remove_wheel_from_hub(wheel,nut,hub,container):
    global env
    loosen(nut,hub)
    jack_up(hub)
    undo(nut,hub)
    remove_wheel(wheel,hub)
    put_away(wheel,container)

def put_on_wheel_to_hub(wheel,nut,hub,container):
    global env
    fetch(wheel,container)
    put_on_wheel(wheel,hub)
    do_up(nut,hub)
    inflate(wheel)
    
get_all_tools('boot')
remove_wheel_from_hub('w1','nuts1','the-hub1','boot')
put_on_wheel_to_hub('r1','nuts1','the-hub1','boot')
```
"""
        ],
        "instruction": """
Your goal is to replace flat tyres with intact tyres on the hubs. Remember to open boot first to get tools you need. Intact tyres should be inflated. The nuts should be tight on the hubs. The flat tyres, wrench, jack, and pump should be in the boot. The boot should be closed.
    There are actions defined in this domain:
    open(<container>): The precondition for this action is that the container is unlocked and closed. The effect of this action is that the container is open and not closed.
    close(<container>): The precondition for this action is that the container is open. The effect of this action is that the container is closed and not open.
    fetch(<object>,<container>): The precondition for this action is that the object is inside the container and the container is open. The effect of this action is that the object is held by the agent and not inside the container.
    put_away(<object>,<container>): The precondition for this action is that the object is held by the agent and the container is open. The effect of this action is that the object is inside the container and not held by the agent.
    loosen(<nut>,<hub>): The precondition for this action is that the agent has a wrench, the nut on hub is tight, and the hub is on the ground. The effect of this action is that the nut on hub is loose and not tight.
    tighten(<nut>,<hub>): The precondition for this action is that the agent has a wrench, the nut on hub is loose, and the hub is on the ground. The effect of this action is that the nut on hub is tight and not loose.
    jack_up(<hub>): This action represents the process of lifting a hub off the ground using a jack. It requires the agent to have a jack and for the hub to be on the ground. After performing this action, the hub will no longer be on the ground and the agent will no longer have the jack.
    jack_down(<hub>): This action represents the process of lowering a hub back to the ground from an elevated position using a jack. It requires the agent to have the hub off the ground. After performing this action, the hub will be back on the ground and the agent will have the jack.
    undo(<nut>,<hub>): This action undo the fastening of a nut on a hub. The preconditions are the hub is not on the ground (i.e., it has been jacked up), the hub is fastened, the agent has a wrench and the nut is loose. The effects are the agent has the nut, the hub is unfastened, the hub is no longer loose and the hub is not fastened anymore.
    do_up(<nut>,<hub>): This action fasten a nut on a hub. The preconditions are the agent has a wrench, the hub is unfastened, the hub is not on the ground (i.e., it has been jacked up) and the agent has the nut to be fastened. The effects are the nut is now loose on the hub, the hub is fastened, the hub is no longer unfastened and the agent no longer has the nut.
    remove_wheel(<wheel>,<hub>): This action removes a wheel from a hub. It can only be performed if the hub is not on the ground, the wheel is currently on the hub, and the hub is unfastened. After the action is performed, the agent will have the removed wheel and the hub will be free, meaning that the wheel is no longer on the hub.
    put_on_wheel(<wheel>,<hub>): This action puts a wheel onto a hub. It can only be performed if the agent has the wheel, the hub is free, the hub is unfastened, and the hub is not on the ground. After the action is performed, the wheel will be on the hub, the hub will no longer be free, and the agent will no longer have the wheel.
    inflate(<wheel>): This action inflates a wheel using a pump. It can only be performed if the agent has a pump, the wheel is not inflated, and the wheel is intact. After the action is performed, the wheel will be inflated.
""",
        "system_msg": "You are a master in car repair.",
    },
}
