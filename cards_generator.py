from itertools import product, filterfalse, chain
import datetime


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


[
    "Null Card",
    "Joker",
    "Card",
    "Life Stack",
    "Death Stack",
    "Hand",
    "Turn",
    "Health Chip"]

OBJECTS = [
    "Null Card",
    "Joker",
    "Card",
    "Turn",
    "Health Chip"]

PLACES = [
    "Life Stack",
    "Death Stack",
    "Hand"]

ACTIONS = [
    "Append",
    "Remove",
    "Move"]

TIMES = [
    "actual Turn",
    "next Turn"
]

TARGETS = [
    "Player",
    "Opponent"]

CURRENCIES = [
    "Card",
    "Turn",
    "Health Chip"
]


def append_cards():
    for obj, target, place in product(OBJECTS, TARGETS, PLACES):
        if  not (obj == "Null Card" and target == "Player" and place != "Death Stack") \
        and not (target == "Player" and place != "Life Stack") \
        and not (obj != "Null Card" and target == "Opponent") \
        and not (target == "Opponent" and place != "Life Stack"):
            if obj in ("Turn", "Health Chip"):
                yield f"+Append a {obj} on {target}.\n"
                continue
            yield f"+Append a {obj} on {target} {place}.\n"
        else:
            yield f"-Append a {obj} on {target} {place}.\n"


def remove_cards():
    for obj, target, place in product(OBJECTS, TARGETS, PLACES):
        if  not (obj != "Null Card" and target == "Player") \
        and not (obj != "Health Chip") \
        and not (place == "Death Stack") \
        and not (obj in ("Null Card", "Turn") and target == "Opponent"):
            if obj == "Health Chip":
                yield f"+Remove a {obj} on {target}.\n"
                continue
            yield f"+Remove a {obj} on {target} {place}.\n"
        else:
            yield f"-Remove a {obj} on {target} {place}.\n"


def move_cards():
    for obj, target1, place1, target2, place2 in product(OBJECTS, TARGETS, PLACES, TARGETS, PLACES):
        if  not (obj == "Turn") \
        and not (place1 == "Life Stack") \
        and not (obj != "Null Card" and target1 == "Player" and target2 == "Opponent") \
        and not (target1 == "Player" and place1 == "Death Stack" and place2 != "Life Stack") \
        and not (target1 == "Player" and place1 == "Death Stack" and target2 == "Opponent") \
        and not (target1 == target2 and place1 == "Hand" and place2 == "Life Stack") \
        and not (target1 == "Opponent" and place1 == "Death Stack") \
        and not (obj == "Null Card" and target1 == "Opponent" and target2 == "Player") \
        and not (target1 == "Opponent" and target2 == "Player" and place2 == "Death Stack") \
        and not (target1 == "Player" and target2 == "Opponent" and place2 == "Death Stack") \
        and not (obj in ("Null Card", "Joker")) \
        and not (target1 == target2 and place1 == place2):
            if obj == "Health Chip":
                if target1 == "Opponent" and target2 == "Player":
                    yield f"+Move a {obj} from {target1} to {target2}.\n"
                continue
            yield f"+Move a {obj} from {target1} {place1} to {target2} {place2}.\n"
        else:
            yield f"-Move a {obj} from {target1} {place1} to {target2} {place2}.\n"


def all_cards():
    with open(f"all_cards.diff", "w") as file:
        all_actions = chain(append_cards(), remove_cards(), move_cards())
        for card_description in unique_everseen(all_actions, str.lower):
            file.write(card_description)


def valid_cards(timestamp=False):
    if timestamp:
        _, _, _, h, m, s, *_ = tuple(datetime.datetime.now().timetuple())
        filename = f"valid_cards_{h}_{m}_{s}.txt"
    else:
        filename = "valid_cards.txt"
    with open(filename, "w") as file:
        all_actions = chain(append_cards(), remove_cards(), move_cards())
        for card_description in unique_everseen(all_actions, str.lower):
            if card_description.startswith("+"):
                file.write(card_description[1:])


if __name__ == '__main__':
    all_cards()
    valid_cards(timestamp=0)
