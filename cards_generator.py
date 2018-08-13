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
    ITEMS = ["Health Chip", "Turn"]
    OWNERS = ["Player"]
    STACKS = ["Chip Stack"]
    for item, owner, stack in product(ITEMS, OWNERS, STACKS):
        if item == "Turn":
            yield f"+Append a {item} on {owner}.\n"
        else:
            yield f"+Append a {item} on {owner} {stack}.\n"


def remove_cards():
    ITEMS = ["Health Chip"]
    OWNERS = ["Opponent"]
    STACKS = ["Chip Stack"]
    for item, owner, stack in product(ITEMS, OWNERS, STACKS):
        yield f"+Remove a {item} on {owner} {stack}.\n"


def move_cards():
    ITEMS = ["Health Chip", "Card"]
    OWNERS = ["Player", "Opponent"]
    STACKS = ["Chip Stack", "Life Stack", "Death Stack", "Hand"]
    CARD_STACKS = ["Life Stack", "Death Stack", "Hand"]
    for item, owner1, stack1, owner2, stack2 in product(ITEMS, OWNERS, STACKS, OWNERS, STACKS):
        if not (owner1 == owner2 and stack1 == stack2) \
        and not (item == "Card" and "Chip Stack" in (stack1, stack2)) \
        and not (item == "Health Chip" and stack1 in CARD_STACKS) \
        and not (item == "Health Chip" and stack2 in CARD_STACKS) \
        and not (owner1 == "Player" and stack2 == "Death Stack") \
        and not (owner1 == "Player" and stack1 == "Hand" and stack2 in CARD_STACKS) \
        and not (owner1 == "Opponent" and stack1 in ("Life Stack", "Death Stack")) \
        and not ((owner1, stack1) == ("Opponent", "Hand") and (owner2, stack2) == ("Player", "Death Stack")) \
        and not ((owner1, stack1) == ("Player", "Death Stack") and (owner2, stack2) == ("Player", "Hand")) \
        and not (owner1 == "Opponent" and (owner2, stack2) == ("Player", "Hand")) \
        and not (owner1 == "Player" and owner2 == "Opponent"):
            yield f"+Move a {item} from {owner1} {stack1} to {owner2} {stack2}.\n"
        else:
            yield f"-Move a {item} from {owner1} {stack1} to {owner2} {stack2}.\n"


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
