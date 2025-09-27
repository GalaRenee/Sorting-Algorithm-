import random
from ui.theme import FLOWERS

def make_flowers():
    # Create 4 of each flower type, then shuffle
    items = []
    keys = []
    for flower_type in range(4):
        for _ in range(4):
            items.append(FLOWERS[flower_type][1])  # flower name
            keys.append(flower_type)  # numeric key for sorting
    
    # Shuffle both lists the same way
    combined = list(zip(items, keys))
    random.shuffle(combined)
    items, keys = zip(*combined)
    return list(items), list(keys)

def initial_state(mode="garden"):
    labels, arr = make_flowers()
        
    return {
        "mode": mode,
        "algorithm": None,
        "arr": arr,
        "arr_labels": labels,
        "sorting": False,
        "stats": {"steps": 0, "comparisons": 0, "swaps": 0},
        "performance": [],
        "show_performance": False,
       
    }

def switch_mode(state, mode):
    if state.get("sorting"):
        return
    state["mode"] = mode 
    labels, arr = make_flowers()
    state["arr_labels"] = labels
    state["arr"] = arr
    _reset_stats(state)
    
def shuffle(state):
    if state.get("sorting"):
        return
    labels, arr = make_flowers()
    state["arr_labels"] = labels
    state["arr"] = arr
    _reset_stats(state)
    
def new_dataset(state):
    shuffle(state)
    
def _reset_stats(state):
    state["stats"] = {"steps": 0, "comparisons": 0, "swaps": 0}
    if "performance" in state:
        state["performance"].clear()