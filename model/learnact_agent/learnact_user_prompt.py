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
alfworld_instruction_with_tool = """
Your task is to interact with a virtual household simulator to accomplish a specific task. With each interaction, you will receive an observation.
Your role is to decide on an action based on the observation. Please ensure that any objects and receptacles you mention in your response are present in the observation provided.

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
{}
"""
alfworld_sys = "You are a helpful assistant"


learnact_user_prompt_dict = {
    "blockworld": {
        "examples": [
            """
Goal: The goal is to satisfy the following conditions: b1 is on b2., b2 is on b3.
Observation: b2 is on b3. b3 is on b1. b1 is on the table.  Robot arm is empty. The b2 is clear.
Action: Unstack('b2','b3')
Observation: b3 is on b1. b1 is on the table. The b3 is clear. You are holding b2.
Action: Putdown('b2')
Observation: b3 is on b1. b1 is on the table. b2 is on the table.  Robot arm is empty. The b2 is clear.
Action: Unstack('b3','b1')
Observation: b1 is on the table. b2 is on the table. The b1 is clear. The b2 is clear. Robot arm is empty. You are holding b3.
Action: Putdown('b3')
Observation: b1 is on the table.  b2 is on the table. b3 is on the table. Robot arm is empty. The b1 is clear. The b2 is clear. The b3 is clear. 
Action: Pickup('b2')
Observation: b1 is on the table.  b2 is on the table.  The b1 is clear. The b3 is clear. You are holding b2.  
Action: Stack('b2','b3')
Observation: b1 is on the table. b2 is on b3. b3 is on the table. Robot arm is empty. The b1 is clear. The b2 is clear. 
Action: Pickup('b3')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. 
Action: Pickup('b1')
Observation: b2 is on b3. b3 is on the table. The b2 is clear.  You are holding b1. 
Action: Stack('b1','b2')
Observation: b1 is on b2. b2 is on b3. b3 is on the table.  Robot arm is empty. The b1 is clear. The goal is satisfied.
"""
        ],
        "instruction": """
The domain assumes a world where there are a set of blocks that can be stacked on top of each other, an arm that can hold one block at a time, and a table where blocks can be placed.
    The actions defined in this domain include:
    Pickup(block): allows the arm to pick up a block from the table if it is clear and the arm is empty. After the pickup action, the arm will be holding the block, and the block will no longer be on the table or clear.
    Putdown(block): allows the arm to put down a block on the table if it is holding a block. After the putdown action, the arm will be empty, and the block will be on the table and clear.
    Stack(block1,block2): allows the arm to stack a block on top of another block if the arm is holding the top block and the bottom block is clear. After the stack action, the arm will be empty, the top block will be on top of the bottom block, and the bottom block will no longer be clear.
    Unstack(block1,block2): allows the arm to unstack a block from on top of another block if the arm is empty and the top block is clear. After the unstack action, the arm will be holding the top block, the top block will no longer be on top of the bottom block, and the bottom block will be clear.
{}
""",
        "system_msg": "You are a master in planning.",
    },
    "barman": {
        "examples": [
            """
The goal is to satisfy the following conditions: shot1 contains cocktail1. 
Observation: Cocktail1 part1 ingredient is ingredient1. Cocktail1 part2 ingredient is ingredient3. Cocktail2 part1 ingredient is ingredient2. Cocktail2 part2 ingredient is ingredient3. Cocktail3 part1 ingredient is ingredient1. Cocktail3 part2 ingredient is ingredient2. Dispenser1 dispenses ingredient1. Dispenser2 dispenses ingredient2. Dispenser3 dispenses ingredient3. Left hand is empty. Level l0 is next to level l1. Level l1 is next to level l2. Right hand is empty. Shaker1 is at empty level l0. Shaker1 is at level l0. Shaker1 is clean. Shaker1 is empty. Shaker1 is on the table. Shot1 is clean. Shot1 is empty. Shot1 is on the table. Shot2 is clean. Shot2 is empty. Shot2 is on the table. Shot3 is clean. Shot3 is empty. Shot3 is on the table. Shot4 is clean. Shot4 is empty. Shot4 is on the table.
Action: grasp('right','shot1')
Observation: You are holding right.
Action: fill_shot('shot1','ingredient3','right','left','dispenser3')
Observation: Shot1 contains ingredient3. 
Action: pour_shot_to_clean_shaker('shot1','ingredient3','shaker1','right','l0','l1')
Observation:  Pour shot1 from a shot glass to a used shaker ingredient3 Shaker1 contains ingredient3. 
Action: clean_shot('shot1','ingredient3','right','left')
Observation:  Shot1 is clean. 
Action: fill_shot('shot1','ingredient1','right','left','dispenser1')
Observation: Shot1 contains ingredient1.
Action: pour_shot_to_used_shaker('shot1','ingredient1','shaker1','right','l1','l2')
Observation: Pour shot1 from a shot glass to a used shaker ingredient1 Shaker1 contains ingredient1. Shaker1 contains ingredient3. Shaker1 is at empty level l0. Shaker1 is at level l2. Shaker1 is on the table. Shaker1 is unshaked.
Action: clean_shot('shot1','ingredient1','right','left')
Observation: Shot1 is clean. 
Action: leave('right','shot1')
Observation: Right hand is empty.
Action: grasp('right','shaker1')
Observation: You are holding right.
Action: shake('cocktail1','ingredient1','ingredient3','shaker1','right','left')
Observation: Shaker1 is shaked.
Action: pour_shaker_to_shot('cocktail1','shot1','right','shaker1','l2','l1')
Observation: Shot1 contains cocktail1. The task is completed.
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
{}
    
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
Action: pick('ball1','rooma','right')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is at rooma. Ball3 is a ball. Ball3 is at rooma.  Left is a gripper. Left is free. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: pick('ball2','rooma','left')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Robby is at roomb. Room rooma Room roomb
Action: drop('ball1','rooma','right')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. 
Action: drop('ball1','roomb','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb
Action: drop('ball2','roomb','left')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at rooma.Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at rooma. Room rooma Room roomb
Action: pick('ball3','rooma','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is carrying right.  Left is a gripper. Left is free. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is carrying right.  Left is a gripper. Left is free. Right is a gripper. Robby is at roomb. Room rooma Room roomb
Action: drop('ball3','rooms','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at roomb. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb. The task is completed.
"""
        ],
        "instruction": """
You are a robot with a gripper that can move objects between different rooms. Your name is Robby.
    There are actions defined in this domain:
    move(<room1>,<room2>): This action allows the robot to move from one room to another.The action has a single precondition, which is that the robot is currently in a room. The effect of this action is to move the robot to another room and to remove the fact that it is in the original room.
    pick(<obj>,<room>,<gripper>): This action allows the robot to pick up an object using the gripper. The action has three preconditions: (1) the object is located in a room (2) the robot is currently in the same room and (3) the gripper is free (i.e., not holding any object). The effect of this action is to update the state of the world to show that the robot is carrying the object using the gripper, the object is no longer in the room, and the gripper is no longer free.
    drop(<obj>,<room>,<gripper>): This action allows the robot to drop an object that it is carrying. The action has two preconditions: (1) the robot is currently carrying the object using the gripper, and (2) the robot is currently in a room. The effect of this action is to update the state of the world to show that the robot is no longer carrying the object using the gripper, the object is now located in the room, and the gripper is now free.
{}    
""",
        "system_msg": "You are a master in moving objects.",
    },
    "tyreworld": {
        "examples": [
            """
The goal is to satisfy the following conditions: w1 is in boot. (Note you need to open boot first so that you can extract tools from it.)
Observation: Boot is closed. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is tight. Wheel r1 is intact. Wheel r1 is not inflated. Wheel w1 is on hub the-hub1. Wrench is in boot.
Action: open('boot')
Observation: Boot is open. 
Action: fetch('wrench','boot')
Observation: You have wrench.
Action: loosen('nuts1', 'the-hub1')
Observation: The nut nuts1 on the hub the-hub1 is loose. 
Action: fetch('jack','boot')
Observation: You have jack. 
Action: jack_up('the-hub1')
Observation: Hub the-hub1 is not on the ground. 
Action: undo('nuts1','the-hub1')
Observation: Hub the-hub1 is unfastened. 
Action: remove_wheel('w1','the-hub1')
Observation: You have w1. 
Action: put_away('w1','boot')
Observation: W1 is in boot. Goal is completed.
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
{}
""",
        "system_msg": "You are a master in car repair.",
    },
    "alfworld_put": {
        "examples": [
            """
Your task is to: put some spraybottle on toilet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2.
Action: take("spraybottle 2", "cabinet 2")
Observation: You pick up the spraybottle 2 from the cabinet 2.
Action: goto("toilet 1")
Observation: On the toilet 1, you see a soapbottle 2.
Action: put("spraybottle 2", "toilet 1")
Observation: You put the spraybottle 2 in/on the toilet 1.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
    "alfworld_clean": {
        "examples": [
            """
Your task is to: clean some soapbar and put it in toilet.
Observation: You are in the middle of a room. Looking quickly around you, you see a bathtubbasin 1, a garbagecan 1, a handtowelholder 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
Action: goto("toilet 1")
Observation: On the toilet 1, you see a soapbar 4, and a soapbar 3.
Action: take("soapbar 4", "toilet 1")
Observation: You pick up the soapbar 4 from the toilet 1.
Action: goto("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: clean("soapbar 4", "sinkbasin 1")
Observation: You clean the soapbar 4 using the sinkbasin 1.
Action: goto("toilet 1")
Observation: On the toilet 1, you see a soapbar 3.
Action: put("soapbar 4", "toilet 1")
Observation: You put the soapbar 4 in/on the toilet 1.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
    "alfworld_heat": {
        "examples": [
            """
Your task is to: put a hot apple in fridge.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("diningtable 1")
Observation: On the diningtable 1, you see a apple 1, a bread 1, a fork 3, a fork 2, a fork 1, a mug 2, a peppershaker 3, a plate 2, a pot 1, a soapbottle 3, a spatula 1, a spoon 3, a spoon 2, a spoon 1, a winebottle 3, and a winebottle 2.
Action: take("apple 1", "diningtable 1")
Observation: You pick up the apple 1 from the diningtable 1.
Action: goto("microwave 1")
Observation: The microwave 1 is closed.
Action: heat("apple 1", "microwave 1")
Observation: You heat the apple 1 using the microwave 1.
Action: goto("fridge 1")
Observation: The fridge 1 is open. In it, you see a cup 1, and a egg 1.
Action: put("apple 1", "fridge 1")
Observation: You put the apple 1 in/on the fridge 1.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
    "alfworld_cool": {
        "examples": [
            """
Your task is to: cool some pan and put it in stoveburner.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 16, a cabinet 15, a cabinet 14, a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 2, a countertop 1, a diningtable 1, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a safe 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("stoveburner 1")
Observation: On the stoveburner 1, you see nothing.
Action: goto("stoveburner 2")
Observation: On the stoveburner 2, you see a pot 1.
Action: goto("stoveburner 3")
Observation: On the stoveburner 3, you see a pan 1.
Action: take("pan 1", "stoveburner 3")
Observation: You pick up the pan 1 from the stoveburner 3.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: cool("pan 1", "fridge 1")
Observation: You cool the pan 1 using the fridge 1.
Action: goto("stoveburner 1")
Observation: On the stoveburner 1, you see nothing.
Action: put("pan 1", "stoveburner 1")
Observation: You put the pan 1 in/on the stoveburner 1.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
    "alfworld_examine": {
        "examples": [
            """
Your task is to: look at statue under the desklamp.
Observation: You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Action: goto("dresser 1")
Observation: On the dresser 1, you see a cellphone 3, a newspaper 2, a statue 1, and a television 1.
Action: take("statue 1",  "dresser 1")
Observation: You pick up the statue 1 from the dresser 1.
Action: goto("sidetable 1")
Observation: On the sidetable 1, you see nothing.
Action: goto("sidetable 2")
Observation: On the sidetable 2, you see a desklamp 3, a newspaper 1, and a statue 2.
Action: use("desklamp 3")
Observation: You turn on the desklamp 3.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
    "alfworld_puttwo": {
        "examples": [
            """
Your task is to: put two cellphone in sofa.
Observation: You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Action: goto("coffeetable 1")
Observation: On the coffeetable 1, you see a box 1, a cellphone 3, and a plate 1.
Action: take("cellphone 3", "coffeetable 1")
Observation: You pick up the cellphone 3 from the coffeetable 1.
Action: goto("sofa 1")
Observation: On the sofa 1, you see a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.
Action: put("cellphone 3", "sofa 1")
Observation: You put the cellphone 3 in/on the sofa 1.
Action: goto("diningtable 1")
Observation: On the diningtable 1, you see a cellphone 2, a keychain 2, a laptop 1, a statue 2, and a statue 1.
Action: take("cellphone 2", "diningtable 1")
Observation: You pick up the cellphone 2 from the diningtable 1.
Action: goto("sofa 1")
Observation: On the sofa 1, you see a cellphone 3, a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.
Action: put("cellphone 2", "sofa 1")
Observation: You put the cellphone 2 in/on the sofa 1.
"""
        ],
        "instruction": alfworld_instruction_with_tool,
        "system_msg": alfworld_sys,
    },
}


learnact_user_prompt_dict_no_tool = {
    "blockworld": {
        "examples": [
            """
Goal: The goal is to satisfy the following conditions: b1 is on b2., b2 is on b3.
Observation: b2 is on b3. b3 is on b1. b1 is on the table.  Robot arm is empty. The b2 is clear.
Action: Unstack('b2','b3')
Observation: b3 is on b1. b1 is on the table. The b3 is clear. You are holding b2.
Action: Putdown('b2')
Observation: b3 is on b1. b1 is on the table. b2 is on the table.  Robot arm is empty. The b2 is clear.
Action: Unstack('b3','b1')
Observation: b1 is on the table. b2 is on the table. The b1 is clear. The b2 is clear. Robot arm is empty. You are holding b3.
Action: Putdown('b3')
Observation: b1 is on the table.  b2 is on the table. b3 is on the table. Robot arm is empty. The b1 is clear. The b2 is clear. The b3 is clear. 
Action: Pickup('b2')
Observation: b1 is on the table.  b2 is on the table.  The b1 is clear. The b3 is clear. You are holding b2.  
Action: Stack('b2','b3')
Observation: b1 is on the table. b2 is on b3. b3 is on the table. Robot arm is empty. The b1 is clear. The b2 is clear. 
Action: Pickup('b3')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. 
Action: Pickup('b1')
Observation: b2 is on b3. b3 is on the table. The b2 is clear.  You are holding b1. 
Action: Stack('b1','b2')
Observation: b1 is on b2. b2 is on b3. b3 is on the table.  Robot arm is empty. The b1 is clear. The goal is satisfied.
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
Action: grasp('right','shot1').
Observation: You are holding right.
Action: fill_shot('shot1','ingredient3','right','left','dispenser3')
Observation: Shot1 contains ingredient3. 
Action: pour_shot_to_clean_shaker('shot1','ingredient3','shaker1','right','l0','l1')
Observation:  Pour shot1 from a shot glass to a used shaker ingredient3 Shaker1 contains ingredient3. 
Action: clean_shot('shot1','ingredient3','right','left')
Observation:  Shot1 is clean. 
Action: fill_shot('shot1','ingredient1','right','left','dispenser1')
Observation: Shot1 contains ingredient1.
Action: pour_shot_to_used_shaker('shot1','ingredient1','shaker1','right','l1','l2')
Observation: Pour shot1 from a shot glass to a used shaker ingredient1 Shaker1 contains ingredient1. Shaker1 contains ingredient3. Shaker1 is at empty level l0. Shaker1 is at level l2. Shaker1 is on the table. Shaker1 is unshaked.
Action: clean_shot('shot1','ingredient1','right','left')
Observation: Shot1 is clean. 
Action: leave('right','shot1')
Observation: Right hand is empty.
Action: grasp('right','shaker1')
Observation: You are holding right.
Action: shake('cocktail1','ingredient1','ingredient3','shaker1','right','left')
Observation: Shaker1 is shaked.
Action: pour_shaker_to_shot('cocktail1','shot1','right','shaker1','l2','l1')
Observation: Shot1 contains cocktail1. The task is completed.
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
Action: pick('ball1','rooma','right')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is at rooma. Ball3 is a ball. Ball3 is at rooma.  Left is a gripper. Left is free. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: pick('ball2','rooma','left')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball. Ball1 is carrying right. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Robby is at roomb. Room rooma Room roomb
Action: drop('ball1','rooma','right')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. 
Action: drop('ball1','roomb','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is carrying left. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb
Action: drop('ball2','roomb','left')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at rooma. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at rooma.Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at rooma. Room rooma Room roomb
Action: pick('ball3','rooma','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is carrying right.  Left is a gripper. Left is free. Right is a gripper. Robby is at rooma. Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is carrying right. Ball4 is a ball. Ball4 is at rooma. Left is a gripper. Left is free. Right is a gripper. Robby is at roomb. Room rooma Room roomb
Action: drop('ball3','rooms','right')
Observation: Ball1 is a ball. Ball1 is at roomb. Ball2 is a ball. Ball2 is at roomb. Ball3 is a ball. Ball3 is at roomb. Ball4 is a ball. Ball4 is at rooma. Left is a gripper. Left is free. Right is a gripper. Right is free. Robby is at roomb. Room rooma Room roomb. The task is completed.
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
The goal is to satisfy the following conditions: Wheel r1 is inflated., r1 is on the-hub1., w1 is in boot. (Note you need to open boot first so that you can extract tools from it.)
Observation: Boot is closed. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is tight. Wheel r1 is intact. Wheel r1 is not inflated. Wheel w1 is on hub the-hub1. Wrench is in boot.
Action: open('boot').
Observation: Boot is open. 
Action: fetch('wrench','boot')
Observation: You have wrench.
Action: loosen('nuts1', 'the-hub1')
Observation: The nut nuts1 on the hub the-hub1 is loose. 
Action: fetch('jack','boot')
Observation: You have jack. 
Action: jack_up('the-hub1')
Observation: Hub the-hub1 is not on the ground. 
Action: undo('nuts1','the-hub1')
Observation: Hub the-hub1 is unfastened. 
Action: remove_wheel('w1','the-hub1')
Observation: You have w1. 
Action: put_away('w1','boot')
Observation: W1 is in boot.
Action: fetch('r1','boot')
Observation: You have r1.
Action: fetch('pump','boot')
Observation: You have pump.
Action: inflate('r1')
Observation: r1 is inflated. 
Action: put_on_wheel('r1','the-hub1')
Observation: R1 is on the-hub1.
Action: do_up('nuts1','the-hub1')
Observation: The nut nuts1 on the hub the-hub1 is loose. 
Action: jack_down('the-hub1')
Observation: Hub the-hub1 is on the ground.
Action: tighten('nuts1','the-hub1')
Observation: Hub the-hub1 is fastened. The task is completed.
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
    "alfworld_put": {
        "examples": [
            """
Your task is to: put some spraybottle on toilet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2.
Action: take("spraybottle 2", "cabinet 2")
Observation: You pick up the spraybottle 2 from the cabinet 2.
Action: goto("toilet 1")
Observation: On the toilet 1, you see a soapbottle 2.
Action: put("spraybottle 2", "toilet 1")
Observation: You put the spraybottle 2 in/on the toilet 1.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
    "alfworld_clean": {
        "examples": [
            """
Your task is to: clean some soapbar and put it in toilet.
Observation: You are in the middle of a room. Looking quickly around you, you see a bathtubbasin 1, a garbagecan 1, a handtowelholder 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
Action: goto("bathtubbasin 1")
Observation: On the bathtubbasin 1, you see a cloth 1, a soapbottle 1.
Action: goto("shelf 1")
Observation: On the shelf 1, you see a soapbar 4, and a soapbar 3.
Action: take("soapbar 4", "shelf 1")
Observation: You pick up the soapbar 4 from the shelf 1.
Action: goto("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: clean("soapbar 4", "sinkbasin 1")
Observation: You clean the soapbar 4 using the sinkbasin 1.
Action: goto("toilet 1")
Observation: On the toilet 1, you see a soapbar 3.
Action: put("soapbar 4", "toilet 1")
Observation: You put the soapbar 4 in/on the toilet 1.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
    "alfworld_heat": {
        "examples": [
            """
Your task is to: put a hot apple in countertop.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("fridge 1")
Observation: On the fridge 1, you see nothing.
Action: goto("diningtable 1")
Observation: On the diningtable 1, you see a apple 1, a bread 1, a fork 3, a fork 2, a fork 1, a mug 2, a peppershaker 3, a plate 2, a pot 1, a soapbottle 3, a spatula 1, a spoon 3, a spoon 2, a spoon 1, a winebottle 3, and a winebottle 2.
Action: take("apple 1", "diningtable 1")
Observation: You pick up the apple 1 from the diningtable 1.
Action: goto("microwave 1")
Observation: The microwave 1 is closed.
Action: heat("apple 1", "microwave 1")
Observation: You heat the apple 1 using the microwave 1.
Action: goto("countertop 1")
Observation: The countertop 1 is open. In it, you see a cup 1, and a egg 1.
Action: put("apple 1", "countertop 1")
Observation: You put the apple 1 in/on the countertop 1.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
    "alfworld_cool": {
        "examples": [
            """
Your task is to: cool some pan and put it in cabinet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 16, a cabinet 15, a cabinet 14, a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 2, a countertop 1, a diningtable 1, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a safe 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("stoveburner 1")
Observation: On the stoveburner 1, you see nothing.
Action: goto("stoveburner 2")
Observation: On the stoveburner 2, you see a pot 1.
Action: goto("stoveburner 3")
Observation: On the stoveburner 3, you see a pan 1.
Action: take("pan 1", "stoveburner 3")
Observation: You pick up the pan 1 from the stoveburner 3.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: cool("pan 1", "fridge 1")
Observation: You cool the pan 1 using the fridge 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: put("pan 1", "cabinet 1")
Observation: You put the pan 1 in/on the cabinet 1.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
    "alfworld_examine": {
        "examples": [
            """
Your task is to: look at statue under the desklamp.
Observation: You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Action: goto("diningtable 1")
Observation: On the diningtable 1, you see a pot 1.
Action: goto("dresser 1")
Observation: On the dresser 1, you see a cellphone 3, a newspaper 2, a statue 1, and a television 1.
Action: take("statue 1",  "dresser 1")
Observation: You pick up the statue 1 from the dresser 1.
Action: goto("sidetable 1")
Observation: On the sidetable 1, you see nothing.
Action: goto("sidetable 2")
Observation: On the sidetable 2, you see a desklamp 3, a newspaper 1, and a statue 2.
Action: use("desklamp 3")
Observation: You turn on the desklamp 3.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
    "alfworld_puttwo": {
        "examples": [
            """
Your task is to: put two cellphone in sofa.
Observation: You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Action: goto("sidetable 1")
Observation: On the sidetable 1, you see a pot 1.
Action: goto("coffeetable 1")
Observation: On the coffeetable 1, you see a box 1, a cellphone 3, and a plate 1.
Action: take("cellphone 3", "coffeetable 1")
Observation: You pick up the cellphone 3 from the coffeetable 1.
Action: goto("sofa 1")
Observation: On the sofa 1, you see a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.
Action: put("cellphone 3", "sofa 1")
Observation: You put the cellphone 3 in/on the sofa 1.
Action: goto("sidetable 2")
Observation: On the sidetable 2, you see nothing.
Action: goto("diningtable 1")
Observation: On the diningtable 1, you see a cellphone 2, a keychain 2, a laptop 1, a statue 2, and a statue 1.
Action: take("cellphone 2", "diningtable 1")
Observation: You pick up the cellphone 2 from the diningtable 1.
Action: goto("sofa 1")
Observation: On the sofa 1, you see a cellphone 3, a newspaper 2, a pillow 1, a remotecontrol 2, and a remotecontrol 1.
Action: put("cellphone 2", "sofa 1")
Observation: You put the cellphone 2 in/on the sofa 1.
"""
        ],
        "instruction": alfworld_instruction,
        "system_msg": alfworld_sys,
    },
}
