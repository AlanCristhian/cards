from itertools import product, filterfalse, chain

from utils import unique_everseen


def append_cards():
    ITEMS = ["Chip"]
    OWNERS = ["Player"]
    STACKS = ["Chip Stack"]
    for item, owner, stack in product(ITEMS, OWNERS, STACKS):
        if item == "Turn":
            yield f"+Append a {item} on {owner}.\n"
        else:
            yield f"+Append a {item} on {owner} {stack}.\n"


def remove_cards():
    ITEMS = ["Chip"]
    OWNERS = ["Opponent"]
    STACKS = ["Chip Stack"]
    for item, owner, stack in product(ITEMS, OWNERS, STACKS):
        yield f"+Remove a {item} on {owner} {stack}.\n"


def valid_cards():
    with open("append_remove_cards.txt", "w") as file:
        all_actions = chain(append_cards(), remove_cards())
        for card_description in unique_everseen(all_actions, str.lower):
            if card_description.startswith("+"):
                file.write(card_description[1:])


if __name__ == '__main__':
    valid_cards()
