alfworld_wrap = """
def take(obj,recep):
    global env
    env.step(f'take {obj} from {recep}')
    return env._get_obs()

def put(obj,recep):
    global env
    env.step(f'put {obj} in/on {recep}')
    return env._get_obs()
    
def open(recep):
    global env
    env.step(f'open {recep}')
    return env._get_obs()

def close(recep):
    global env
    env.step(f'close {recep}')
    return env._get_obs()

def toggle(obj_or_recep):
    global env
    env.step(f'toggle {obj_or_recep}')
    return env._get_obs()

def clean(obj,recep):
    global env
    env.step(f'clean {obj} with {recep}')
    return env._get_obs()

def cool(obj,recep):
    global env
    env.step(f'cool {obj} with {recep}')
    return env._get_obs()
    
def heat(obj,recep):
    global env
    env.step(f'heat {obj} with {recep}')
    return env._get_obs()

def inventory():
    global env
    env.step('inventory')
    return env._get_obs()

def examine(obj_or_recep):
    global env
    env.step(f'examine {obj_or_recep}')
    return env._get_obs()

def goto(recep):
    global env
    env.step(f'go to {recep}')
    return env._get_obs()
    
def use(obj):
    global env
    env.step(f'use {obj}')
    return env._get_obs()
"""

learnact_user_action_wrapper_dict = {
    "blockworld": """
def Pickup(block):
    global env
    env.step("Pickup {}".format(block))
    
def Putdown(block):
    global env
    env.step("Putdown {}".format(block))

def Stack(block1,block2):
    global env
    env.step("Stack {} on {}".format(block1,block2))
    
def Unstack(block1,block2):
    global env
    env.step("Unstack {} from {}".format(block1,block2))
""",
    "gripper": """
def move(room1,room2):
    global env
    env.step("Move from {} to {}".format(room1,room2))
    
def pick(obj,room,gripper):
    global env
    env.step("Pick up {} at {} with arm {}".format(obj,room,gripper))
    
def drop(obj,room,gripper):
    global env
    env.step("drop {} {} {}".format(obj,room,gripper))
""",
    "barman": """
def grasp(hand,container):
    global env
    env.step("{} grasp {}".format(hand,container))

def leave(hand,container):
    global env
    env.step("{} leave {}".format(hand,container))
    
def fill_shot(shot,ingredient,hand1,hand2,dispenser):
    global env
    env.step("fill-shot glass {} with {} with {} and {} holding {}".format(shot,ingredient,hand1,hand2,dispenser))

def refill_shot(shot,ingredient,hand1,hand2,dispenser):
    global env
    env.step("refill-shot {} with {} with {} and {} holding {}".format(shot,ingredient,hand1,hand2,dispenser))


def empty_shot(hand,shot,beverage):
    global env
    env.step("use hand {} to empty-shot glass {} with beverage {}".format(hand,shot,beverage))

def clean_shot(shot,beverage,hand1,hand2):
    global env
    env.step("clean-shot glass {} with {} with hand {} holding shot glass and {}".format(shot,beverage,hand1,hand2))

def pour_shot_to_clean_shaker(shot,ingredient,shaker,hand1,level1,level2):
    global env
    env.step("pour-shot-to-clean-shaker from a shot glass {} with {} to a clean shaker {} with hand {} from level {} to level {}".format(shot,ingredient,shaker,hand1,level1,level2))

def pour_shot_to_used_shaker(shot,ingredient,shaker,hand1,level1,level2):
    global env
    env.step("pour-shot-to-used-shaker from a shot glass {} with {} to a used shaker {} with hand {} from level {} to level {}".format(shot,ingredient,shaker,hand1,level1,level2))


def empty_shaker(hand,shaker,cocktail,level1,level2):
    global env
    env.step("use hand {} to empty-shaker {} with ingredient {} from level {} to level {}".format(hand,shaker,cocktail,level1,level2))

def clean_shaker(hand1,hand2,shaker):
    global env
    env.step("use hand {} and hand {} to clean-shaker {}".format(hand1,hand2,shaker))

def shake(cocktail,ingredient1,ingredient2,shaker,hand1,hand2):
    global env
    env.step("shake a cocktail {} with ingredient {} and ingredient {} in a shaker {} with hand {} and hand {}".format(cocktail,ingredient1,ingredient2,shaker,hand1,hand2))

def pour_shaker_to_shot(beverage,shot,hand,shaker,level1,level2):
    global env
    env.step("pour-shaker-to-shot to a shot glass {} the ingredient {} with hand {} from shaker {} from level {} to level {}".format(beverage,shot,hand,shaker,level1,level2))

""",
    "tyreworld": """
def open(container):
    global env
    env.step("open {}".format(container))

def close(container):
    global env
    env.step("close {}".format(container))

def fetch(object,container):
    global env
    env.step("fetch {} {}".format(object,container))

def put_away(object,container):
    global env
    env.step("put-away {} {}".format(object,container))


def loosen(nut,hub):
    global env
    env.step("loosen {} {}".format(nut,hub))

def tighten(nut,hub):
    global env
    env.step("tighten {} {}".format(nut,hub))

def jack_up(hub):
    global env
    env.step("jack-up {}".format(hub))

def jack_down(hub):
    global env
    env.step("jack-down {}".format(hub))


def undo(nut,hub):
    global env
    env.step("undo {} {}".format(nut,hub))

def do_up(nut,hub):
    global env
    env.step("do-up {} {}".format(nut,hub))

def remove_wheel(wheel,hub):
    global env
    env.step("remove-wheel {} {}".format(wheel,hub))

def put_on_wheel(wheel,hub):
    global env
    env.step("put-on-wheel {} {}".format(wheel,hub))

def inflate(wheel):
    global env
    env.step("inflate {}".format(wheel))
""",
    "alfworld_put": alfworld_wrap,
    "alfworld_clean": alfworld_wrap,
    "alfworld_heat": alfworld_wrap,
    "alfworld_cool": alfworld_wrap,
    "alfworld_puttwo": alfworld_wrap,
    "alfworld_examine": alfworld_wrap,
}
