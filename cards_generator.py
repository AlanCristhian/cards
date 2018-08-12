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

def append_cards():
    OBJECTS = ["Health Chip", "Turn"]
    OWNERS = ["Player"]
    PLACES = ["Chip Stack"]
    for obj, owner, place in product(OBJECTS, OWNERS, PLACES):
        if obj == "Turn":
            yield f"+Append a {obj} on {owner}.\n"
        else:
            yield f"+Append a {obj} on {owner} {place}.\n"


def remove_cards():
    OBJECTS = ["Health Chip"]
    OWNERS = ["Opponent"]
    PLACES = ["Chip Stack"]
    for obj, owner, place in product(OBJECTS, OWNERS, PLACES):
        yield f"+Remove a {obj} on {owner} {place}.\n"


def move_cards():
    OBJECTS = ["Health Chip", "Card"]
    OWNERS = ["Player", "Opponent"]
    PLACES = ["Chip Stack", "Life Stack", "Death Stack", "Hand"]
    CARD_STACKS = ["Life Stack", "Death Stack", "Hand"]
    for obj, owner1, place1, owner2, place2 in product(OBJECTS, OWNERS, PLACES, OWNERS, PLACES):
        if not (owner1 == owner2 and place1 == place2) \
        and not (obj == "Card" and "Chip Stack" in (place1, place2)) \
        and not (obj == "Health Chip" and place1 in CARD_STACKS) \
        and not (obj == "Health Chip" and place2 in CARD_STACKS) \
        and not (owner1 == "Player" and place2 == "Death Stack") \
        and not (owner1 == "Player" and place1 == "Hand" and place2 in CARD_STACKS) \
        and not (owner1 == "Opponent" and place1 in ("Life Stack", "Death Stack")) \
        and not ((owner1, place1) == ("Opponent", "Hand") and (owner2, place2) == ("Player", "Death Stack")) \
        and not ((owner1, place1) == ("Player", "Death Stack") and (owner2, place2) == ("Player", "Hand")) \
        and not (owner1 == "Opponent" and (owner2, place2) == ("Player", "Hand")) \
        and not (owner1 == "Player" and owner2 == "Opponent"):
            yield f"+Move a {obj} from {owner1} {place1} to {owner2} {place2}.\n"
        else:
            yield f"-Move a {obj} from {owner1} {place1} to {owner2} {place2}.\n"


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
