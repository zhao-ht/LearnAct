reflexion_prompt_agent = {
    "alfworld_put": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: put some saltshaker on drawer.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a dishsponge 1, and a plate 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a plate 2.
Action: open("cabinet 3")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("cabinet 4")
Observation: On the cabinet 4, you see a bowl 1, a cup 1, and a peppershaker 1.
Action: goto("cabinet 5")
Observation: The cabinet 5 is closed.
Action: open("cabinet 5")
Observation: You open the cabinet 5. The cabinet 5 is open. In it, you see saltshaker 2.
Action: goto("cabinet 6")
Observation: The cabinet 6 is closed.
Action: open("cabinet 6")
Observation: You open the cabinet 6. The cabinet 6 is open. In it, you see a cup 3.

Short prompt for future:
After I see the obj that I need, I should take the obj.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_clean": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: clean some bowl and put it in cabinet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: examine("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: goto("countertop 1")
Observation: On the countertop 1, you see a apple 3, a egg 2, and a vase 2.
Action: goto("countertop 2")
Observation: On the countertop 2, you see a creditcard 2, a creditcard 1, a cup 3, a cup 2, a fork 2, a glassbottle 1, a knife 2, a knife 1, a lettuce 2, a lettuce 1, and a pan 2.
Action: goto("countertop 3")
Observation: On the countertop 3, you see a bread 1, a butterknife 1, a cellphone 1, a houseplant 1, a papertowelroll 1, a plate 1, a soapbottle 1, a spoon 3, a spoon 2, a statue 1, and a vase 3.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: examine("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a vase 1.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_heat": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: heat some egg and put it in garbagecan.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: open("fridge 1")
Observation: You open the fridge 1. The fridge 1 is open. In it, you see a apple 2, a bowl 2, a bowl 1, a bread 1, a lettuce 1, a plate 1, and a tomato 1.
Action: take("egg 1", "fridge 1")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: examine("fridge 1")
Observation: The fridge 1 is open. In it, you see a apple 2, a bowl 2, a bowl 1, a bread 1, a lettuce 1, a plate 1, and a tomato 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a glassbottle 1, and a vase 1.
Action: examine("cabinet 1")
Observation: On the cabinet 1, you see a glassbottle 1, and a vase 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a dishsponge 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a vase 2.
Action: examine("cabinet 3")
Observation: On the cabinet 3, you see a vase 2.

Short prompt for future:
After take the obj, I should find some place that can heat the obj.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_cool": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: cool some mug and put it in cabinet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a pan 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a mug 1.
Action: take("mug 1", "cabinet 3")
Observation: You pick up the mug 1 from the cabinet 3.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: open("fridge 1")
Observation: You open the fridge 1. The fridge 1 is open. In it, you see a apple 1, a bowl 1, a cup 2, a egg 1, a plate 2, a potato 2, a potato 1, a tomato 2, and a tomato 1.
Action: cool("mug 1", "fridge 1")
Observation: You cool the mug 1 using the fridge 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a pan 1.
Action: goto("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.

Short prompt for future:
After I goto the target place, I should put the object in there.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_examine": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: examine the book with the desklamp.
Observation: You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 2, a desk 1, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a garbagecan 1, a laundryhamper 1, a safe 1, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, and a shelf 1.
Action: goto("desk 1")
Observation: On the desk 1, you see a alarmclock 1, a creditcard 1, a desklamp 1, a laptop 3, and a mug 1.
Action: take("desklamp 1","desk 1")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("shelf 1")
Observation: On the shelf 1, you see a bowl 1.
Action: goto("shelf 2")
Observation: On the shelf 2, you see a pen 1.
Action: goto("shelf 3")
Observation: On the shelf 3, you see a creditcard 1, a desklamp 1, and a mug 1.
Action: take("desklamp 1","shelf 3")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("shelf 4")
Observation: On the shelf 4, you see a mug 2, and a pencil 1.
Action: goto("shelf 5")
Observation: On the shelf 5, you see nothing.
Action: goto("shelf 6")
Observation: On the shelf 6, you see nothing.
Action: goto("desk 2")
Observation: On the desk 2, you see a cellphone 2, a creditcard 2, a mug 3, and a pencil 2.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_puttwo": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: find two peppershaker and put them in drawer.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Action: goto("countertop 1")
Observation: On the countertop 1, you see a egg 1, and a potato 3.
Action: goto("countertop 2")
Observation: On the countertop 2, you see a apple 1, a bread 2, a bread 1, a butterknife 2, a butterknife 1, a glassbottle 2, a papertowelroll 1, a potato 1, and a soapbottle 1.
Action: goto("countertop 3")
Observation: On the countertop 3, you see a butterknife 3, a cellphone 1, a fork 1, a houseplant 1, a knife 2, a knife 1, a lettuce 2, a peppershaker 4, a pot 2, a statue 2, and a statue 1.
Action: take("peppershaker 4", "countertop 3")
Observation: You pick up the peppershaker 4 from the countertop 3.
Action: goto("drawer 1")
Observation: The drawer 1 is closed.
Action: open("drawer 1")
Observation: You open the drawer 1. The drawer 1 is open. In it, you see a creditcard 1, and a spatula 1.
Action: put("peppershaker 4", "drawer 1")
Observation: You put the peppershaker 4 in/on the drawer 1.
Action: goto("shelf 1")
Observation: On the shelf 1, you see a peppershaker 3, and a saltshaker 2.
Action: take("peppershaker 3", "shelf 1")
Observation: You pick up the peppershaker 3 from the shelf 1.
Action: goto("drawer 1")
Observation: The drawer 1 is open. In it, you see a creditcard 1, a peppershaker 4, and a spatula 1.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "gripper": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: ball1 is at rooma. , ball2 is at rooma. , ball3 is at roomb. , ball4 is at roomb. , ball5 is at rooma. , ball6 is at rooma. 
Observation: Ball1 is a ball.  Ball1 is at roomb.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball.  Ball1 is at roomb.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball1','roomb','right')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball2','roomb','left')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Robby is at rooma.  Room rooma Room roomb
Action: drop('ball1','rooma','right')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Action: drop('ball2','rooma','left')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball5','roomb','right')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball6','roomb','left')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is carrying left.  Left is a gripper.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is carrying left.  Left is a gripper.  Right is a gripper.  Robby is at rooma.  Room rooma Room roomb

Short prompt for future:
When I move across the room, I can see if there are balls I can take to the required target room.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "blockworld": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: b1 is on b2., b3 is on b5., b4 is on b1.
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. B5 is on b3. The b5 is clear. Your arm is empty.
Action: Unstack('b2', 'b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b3', 'b4')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b2','b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b5','b3')
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. The b3 is clear. You are holding b5. 
Action: Putdown('b5')
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. B5 is on the table. The b3 is clear. The b5 is clear. Your arm is empty.
Action: Unstack('b3', 'b4')
Observation: B1 is on the table. B2 is on b1. B4 is on b2. B5 is on the table. The b4 is clear. The b5 is clear. You are holding b3. 
Action: Stack('b3','b5')
Observation: B1 is on the table. B2 is on b1. B3 is on b5. B4 is on b2. B5 is on the table. The b3 is clear. The b4 is clear. Your arm is empty.
Action: Unstack('b4', 'b2')
Observation: B1 is on the table. B2 is on b1. B3 is on b5. B5 is on the table. The b2 is clear. The b3 is clear. You are holding b4. 
Action: Stack('b4','b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b2', 'b1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.

Short prompt for future:
When I call Unstack, the first block should be clear.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "barman": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: shot1 contains cocktail3. , shot2 contains cocktail2. 
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Handempty right Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table. 
Action: grasp('right','shot1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: fill_shot('shot1','ingredient2','right','left','dispenser2')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient2. Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 contains ingredient2.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: pour_shot_to_clean_shaker('shot1','ingredient2','shaker1','right','l0','l1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient2. Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: clean_shot('shot1','ingredient2','right','left')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: fill_shot('shot1','ingredient3','right','left','dispenser3')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient3. Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 contains ingredient3.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: pour_shot_to_used_shaker('shot1','ingredient3','shaker1','right','l1','l2')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient3. Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: clean_shot('shot1','ingredient3','right','left')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: leave('right','shot1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Handempty right Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table. 
Action: grasp('right','shaker1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: shake('cocktail3','ingredient2','ingredient3','shaker1','right','left')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.

Short prompt for future:
I should pay attention to the order of ingredients pf a cocktail.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "tyreworld": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: r1 is on the-hub1., w1 is in boot.
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot.
Action: fetch('r1', 'boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have r1.
Action: put_on_wheel('r1', 'the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: fetch('jack','boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have jack. You have r1.
Action: jack_up('the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is not on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have r1.
Action: undo('nuts1','the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: remove_wheel('w1','the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: fetch('wrench','boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is not on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have r1. You have wrench.
Action: undo('nuts1','the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have r1. You have wrench.
Action: remove_wheel('w1','the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. The-hub1 is free.  Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have r1. You have w1. You have wrench.
Action: put_on_wheel('r1', 'the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. R1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have w1. You have wrench.

Short prompt for future:
I should get tool wrench before I undo nuts.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
}

reflexion_prompt_react_agent = {
    "alfworld_put": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: put some saltshaker on drawer.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Think: First, I need to find a saltshaker.
Observation: Ok.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a dishsponge 1, and a plate 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a plate 2.
Action: open("cabinet 3")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("cabinet 4")
Observation: On the cabinet 4, you see a bowl 1, a cup 1, and a peppershaker 1.
Action: goto("cabinet 5")
Observation: The cabinet 5 is closed.
Action: open("cabinet 5")
Observation: You open the cabinet 5. The cabinet 5 is open. In it, you see saltshaker 2.
Action: goto("cabinet 6")
Observation: The cabinet 6 is closed.
Action: open("cabinet 6")
Observation: You open the cabinet 6. The cabinet 6 is open. In it, you see a cup 3.

Short prompt for future:
After I see the obj that I need, I should take the obj.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_clean": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: clean some bowl and put it in cabinet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Think: First, I need to find a bowl.
Observation: Ok.
Action: goto("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: examine("sinkbasin 1")
Observation: On the sinkbasin 1, you see nothing.
Action: goto("countertop 1")
Observation: On the countertop 1, you see a apple 3, a egg 2, and a vase 2.
Action: goto("countertop 2")
Observation: On the countertop 2, you see a creditcard 2, a creditcard 1, a cup 3, a cup 2, a fork 2, a glassbottle 1, a knife 2, a knife 1, a lettuce 2, a lettuce 1, and a pan 2.
Action: goto("countertop 3")
Observation: On the countertop 3, you see a bread 1, a butterknife 1, a cellphone 1, a houseplant 1, a papertowelroll 1, a plate 1, a soapbottle 1, a spoon 3, a spoon 2, a statue 1, and a vase 3.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: examine("cabinet 1")
Observation: On the cabinet 1, you see nothing.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a vase 1.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_heat": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: heat some egg and put it in garbagecan.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Think: First, I need to find an egg.
Observation: Ok.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: open("fridge 1")
Observation: You open the fridge 1. The fridge 1 is open. In it, you see a apple 2, a bowl 2, a bowl 1, a bread 1, a lettuce 1, a plate 1, and a tomato 1.
Action: take("egg 1", "fridge 1")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: examine("fridge 1")
Observation: The fridge 1 is open. In it, you see a apple 2, a bowl 2, a bowl 1, a bread 1, a lettuce 1, a plate 1, and a tomato 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a glassbottle 1, and a vase 1.
Action: examine("cabinet 1")
Observation: On the cabinet 1, you see a glassbottle 1, and a vase 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a dishsponge 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a vase 2.
Action: examine("cabinet 3")
Observation: On the cabinet 3, you see a vase 2.

Short prompt for future:
After take the obj, I should find some place that can heat the obj.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_cool": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: cool some mug and put it in cabinet.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Think: First, I need to find a mug.
Observation: Ok.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a pan 1.
Action: goto("cabinet 2")
Observation: The cabinet 2 is closed.
Action: open("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.
Action: goto("cabinet 3")
Observation: On the cabinet 3, you see a mug 1.
Action: take("mug 1", "cabinet 3")
Observation: You pick up the mug 1 from the cabinet 3.
Action: goto("fridge 1")
Observation: The fridge 1 is closed.
Action: open("fridge 1")
Observation: You open the fridge 1. The fridge 1 is open. In it, you see a apple 1, a bowl 1, a cup 2, a egg 1, a plate 2, a potato 2, a potato 1, a tomato 2, and a tomato 1.
Action: cool("mug 1", "fridge 1")
Observation: You cool the mug 1 using the fridge 1.
Action: goto("cabinet 1")
Observation: On the cabinet 1, you see a pan 1.
Action: goto("cabinet 2")
Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a saltshaker 1.

Short prompt for future:
After I goto the target place, I should put the object in there.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_examine": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: examine the book with the desklamp.
Observation: You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 2, a desk 1, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a garbagecan 1, a laundryhamper 1, a safe 1, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, and a shelf 1.
Think: First, I need to find a book.
Observation: Ok.
Action: goto("desk 1")
Observation: On the desk 1, you see a alarmclock 1, a creditcard 1, a desklamp 1, a laptop 3, and a mug 1.
Action: take("desklamp 1","desk 1")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("shelf 1")
Observation: On the shelf 1, you see a bowl 1.
Action: goto("shelf 2")
Observation: On the shelf 2, you see a pen 1.
Action: goto("shelf 3")
Observation: On the shelf 3, you see a creditcard 1, a desklamp 1, and a mug 1.
Action: take("desklamp 1","shelf 3")
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions.
Action: goto("shelf 4")
Observation: On the shelf 4, you see a mug 2, and a pencil 1.
Action: goto("shelf 5")
Observation: On the shelf 5, you see nothing.
Action: goto("shelf 6")
Observation: On the shelf 6, you see nothing.
Action: goto("desk 2")
Observation: On the desk 2, you see a cellphone 2, a creditcard 2, a mug 3, and a pencil 2.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "alfworld_puttwo": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: Your task is to: find two peppershaker and put them in drawer.
Observation: You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Think: First, I need to find a peppershaker.
Observation: Ok.
Action: goto("countertop 1")
Observation: On the countertop 1, you see a egg 1, and a potato 3.
Action: goto("countertop 2")
Observation: On the countertop 2, you see a apple 1, a bread 2, a bread 1, a butterknife 2, a butterknife 1, a glassbottle 2, a papertowelroll 1, a potato 1, and a soapbottle 1.
Action: goto("countertop 3")
Observation: On the countertop 3, you see a butterknife 3, a cellphone 1, a fork 1, a houseplant 1, a knife 2, a knife 1, a lettuce 2, a peppershaker 4, a pot 2, a statue 2, and a statue 1.
Action: take("peppershaker 4", "countertop 3")
Observation: You pick up the peppershaker 4 from the countertop 3.
Action: goto("drawer 1")
Observation: The drawer 1 is closed.
Action: open("drawer 1")
Observation: You open the drawer 1. The drawer 1 is open. In it, you see a creditcard 1, and a spatula 1.
Action: put("peppershaker 4", "drawer 1")
Observation: You put the peppershaker 4 in/on the drawer 1.
Action: goto("shelf 1")
Observation: On the shelf 1, you see a peppershaker 3, and a saltshaker 2.
Action: take("peppershaker 3", "shelf 1")
Observation: You pick up the peppershaker 3 from the shelf 1.
Action: goto("drawer 1")
Observation: The drawer 1 is open. In it, you see a creditcard 1, a peppershaker 4, and a spatula 1.

Short prompt for future:
To find the object I need, I should explore different receptacles.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "gripper": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: ball1 is at rooma. , ball2 is at rooma. , ball3 is at roomb. , ball4 is at roomb. , ball5 is at rooma. , ball6 is at rooma. 
Observation: Ball1 is a ball.  Ball1 is at roomb.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Think: I can move ball1 and ball2 from roomb to rooma first.
Observation: Ok.
Action: move('rooma','roomb')
Observation: Ball1 is a ball.  Ball1 is at roomb.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball1','roomb','right')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is at roomb.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball2','roomb','left')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball.  Ball1 is carrying right.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Robby is at rooma.  Room rooma Room roomb
Action: drop('ball1','rooma','right')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is carrying left.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Action: drop('ball2','rooma','left')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at rooma.  Room rooma Room roomb
Action: move('rooma','roomb')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is at roomb.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Right is free.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball5','roomb','right')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is at roomb.  Left is a gripper.  Left is free.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: pick('ball6','roomb','left')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is carrying left.  Left is a gripper.  Right is a gripper.  Robby is at roomb.  Room rooma Room roomb
Action: move('roomb','rooma')
Observation: Ball1 is a ball.  Ball1 is at rooma.  Ball2 is a ball.  Ball2 is at rooma.  Ball3 is a ball.  Ball3 is at rooma.  Ball4 is a ball.  Ball4 is at rooma.  Ball5 is a ball.  Ball5 is carrying right.  Ball6 is a ball.  Ball6 is carrying left.  Left is a gripper.  Right is a gripper.  Robby is at rooma.  Room rooma Room roomb

Short prompt for future:
When I move across the room, I can see if there are balls I can take to the required target room.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "blockworld": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: b1 is on b2., b3 is on b5., b4 is on b1.
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. B5 is on b3. The b5 is clear. Your arm is empty.
Think: I can unstack b5, b3, b2, b1, and b4 first.
Observation: Ok.
Action: Unstack('b2', 'b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b3', 'b4')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b2','b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b5','b3')
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. The b3 is clear. You are holding b5. 
Action: Putdown('b5')
Observation: B1 is on the table. B2 is on b1. B3 is on b4. B4 is on b2. B5 is on the table. The b3 is clear. The b5 is clear. Your arm is empty.
Action: Unstack('b3', 'b4')
Observation: B1 is on the table. B2 is on b1. B4 is on b2. B5 is on the table. The b4 is clear. The b5 is clear. You are holding b3. 
Action: Stack('b3','b5')
Observation: B1 is on the table. B2 is on b1. B3 is on b5. B4 is on b2. B5 is on the table. The b3 is clear. The b4 is clear. Your arm is empty.
Action: Unstack('b4', 'b2')
Observation: B1 is on the table. B2 is on b1. B3 is on b5. B5 is on the table. The b2 is clear. The b3 is clear. You are holding b4. 
Action: Stack('b4','b1')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.
Action: Unstack('b2', 'b1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.

Short prompt for future:
When I call Unstack, the first block should be clear.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "barman": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: shot1 contains cocktail3. , shot2 contains cocktail2. 
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Handempty right Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table. 
Think: I can get ingredient3 and ingredient2 to shaker1 first.
Observation: Ok.
Action: grasp('right','shot1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: fill_shot('shot1','ingredient2','right','left','dispenser2')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient2. Shaker1 is at empty level l0.  Shaker1 is at level l0.  Shaker1 is clean.  Shaker1 is empty.  Shaker1 is on the table.  Shot1 contains ingredient2.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: pour_shot_to_clean_shaker('shot1','ingredient2','shaker1','right','l0','l1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient2. Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: clean_shot('shot1','ingredient2','right','left')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: fill_shot('shot1','ingredient3','right','left','dispenser3')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient3. Shaker1 contains ingredient2.  Shaker1 is at empty level l0.  Shaker1 is at level l1.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 contains ingredient3.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: pour_shot_to_used_shaker('shot1','ingredient3','shaker1','right','l1','l2')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Pour shot1 from a shot glass to a used shaker ingredient3. Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: clean_shot('shot1','ingredient3','right','left')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: leave('right','shot1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Handempty right Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is on the table.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table. 
Action: grasp('right','shaker1')
Observation: Cocktail1 part1 ingredient is ingredient2.  Cocktail1 part2 ingredient is ingredient3.  Cocktail2 part1 ingredient is ingredient1.  Cocktail2 part2 ingredient is ingredient3.  Cocktail3 part1 ingredient is ingredient3.  Cocktail3 part2 ingredient is ingredient2.  Cocktail4 part1 ingredient is ingredient2.  Cocktail4 part2 ingredient is ingredient1.  Dispenser1 dispenses ingredient1.  Dispenser2 dispenses ingredient2.  Dispenser3 dispenses ingredient3.  Handempty left Level l0 is next to level l1.  Level l1 is next to level l2.  Shaker1 contains ingredient2.  Shaker1 contains ingredient3.  Shaker1 is at empty level l0.  Shaker1 is at level l2.  Shaker1 is unshaked.  Shot1 is clean.  Shot1 is empty.  Shot1 is on the table.  Shot2 is clean.  Shot2 is empty.  Shot2 is on the table.  Shot3 is clean.  Shot3 is empty.  Shot3 is on the table.  Shot4 is clean.  Shot4 is empty.  Shot4 is on the table.  Shot5 is clean.  Shot5 is empty.  Shot5 is on the table.  You are holding right. 
Action: shake('cocktail3','ingredient2','ingredient3','shaker1','right','left')
Observation: The action is not valid and therefore takes no effect. Please remember to satisfy the restriction of actions. You can also check valid actions.

Short prompt for future:
I should pay attention to the order of ingredients pf a cocktail.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
    "tyreworld": """
You will be given the history of a past experience in which you were placed in an environment and given a task to complete. 
You were unsuccessful in completing the task. 
Write a short prompt to help yourself in completing similar tasks in the future. Use abstract names like object and receptacle instead of concrete names to make the prompt more general.

Here is an example:
Goal: The goal is to satisfy the following conditions: r1 is on the-hub1., w1 is in boot.
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. R1 is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot.
Think: I can remove w1 from the-hub1 first.
Observation: Ok.
Action: fetch('r1', 'boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Jack is in boot. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have r1.
Action: put_on_wheel('r1', 'the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: fetch('jack','boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have jack. You have r1.
Action: jack_up('the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is not on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. Wrench is in boot. You have r1.
Action: undo('nuts1','the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: remove_wheel('w1','the-hub1')
Observation: The action is not valid and therefore takes no effect. Please check valid actions.
Action: fetch('wrench','boot')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is fastened. Hub the-hub1 is not on the ground. Pump is in boot. The nut nuts1 on the hub the-hub1 is loose. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have r1. You have wrench.
Action: undo('nuts1','the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. W1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have r1. You have wrench.
Action: remove_wheel('w1','the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. The-hub1 is free.  Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have r1. You have w1. You have wrench.
Action: put_on_wheel('r1', 'the-hub1')
Observation: Boot is open. Boot is unlocked. Hub the-hub1 is not on the ground. Hub the-hub1 is unfastened. Pump is in boot. R1 is on the-hub1. Wheel r1 is inflated. Wheel r1 is intact. You have nuts1. You have w1. You have wrench.

Short prompt for future:
I should get tool wrench before I undo nuts.

Now write a short answer for this case in similar form:
{history_error}

Short prompt for future:
""",
}

reflexion_prompt = {
    "py_agent": reflexion_prompt_agent,
    "react_py_agent": reflexion_prompt_react_agent,
}
