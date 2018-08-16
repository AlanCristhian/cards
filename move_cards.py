import collections
import itertools


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. "
    "Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


class Card:
    pass


class Character:
    def __init__(self):
        self.life = collections.deque(Card() for _ in range(5))
        self.hand = collections.deque(Card() for _ in range(5))
        self.death = collections.deque(Card() for _ in range(5))
        self.played = collections.deque(Card() for _ in range(5))


def create_characters(owner1, owner2):
    characters = {"Player": {}, "Opponent": {}}

    character1 = Character()
    characters[owner1]["Life"] = character1.life
    characters[owner1]["Hand"] = character1.hand
    characters[owner1]["Death"] = character1.death
    characters[owner1]["Played"] = character1.played

    if owner2 == owner1:
        owner2 = "Player" if not characters["Player"] else "Opponent"

    character2 = Character()
    characters[owner2]["Life"] = character2.life
    characters[owner2]["Hand"] = character2.hand
    characters[owner2]["Death"] = character2.death
    characters[owner2]["Played"] = character2.played

    return characters


def new_move_card(owner1, stack1, owner2, stack2):
    characters = create_characters(owner1, owner2)
    player = characters["Player"]
    opponent = characters["Opponent"]

    li_player_life = len(player["Life"])
    li_player_hand = len(player["Hand"])
    li_player_death = len(player["Death"])
    li_player_played = len(player["Played"])
    li_opponent_life = len(opponent["Life"])
    li_opponent_hand = len(opponent["Hand"])
    li_opponent_death = len(opponent["Death"])
    li_opponent_played = len(opponent["Played"])

    # Play the card
    player["Played"].append(player["Hand"].pop())
    # Do what the car tell me to do
    characters[owner2][stack2].append(characters[owner1][stack1].pop())
    # Get a card and end the turn
    player["Hand"].append(player["Life"].pop())

    l_player_life = len(player["Life"])
    l_player_hand = len(player["Hand"])
    l_player_death = len(player["Death"])
    l_player_played = len(player["Played"])
    l_opponent_life = len(opponent["Life"])
    l_opponent_hand = len(opponent["Hand"])
    l_opponent_death = len(opponent["Death"])
    l_opponent_played = len(opponent["Played"])

    d_player_life = l_player_life - li_player_life
    d_player_hand = l_player_hand - li_player_hand
    d_player_death = l_player_death - li_player_death
    d_player_played = l_player_played - li_player_played
    d_opponent_life = l_opponent_life - li_opponent_life
    d_opponent_hand = l_opponent_hand - li_opponent_hand
    d_opponent_death = l_opponent_death - li_opponent_death
    d_opponent_played = l_opponent_played - li_opponent_played

    power = 0

    # Hand size
    # =========

    if d_player_hand > 0:
        power += 1
    elif d_player_hand < 0:
        power -= 1

    if d_opponent_hand > 0:
        power -= 1
    elif d_opponent_hand < 0:
        power += 1

    # Total amount of cards
    # =====================

    sum_d_player = d_player_life + d_player_hand + d_player_death \
                 + d_player_played
    if sum_d_player > 0:
        power += 1
    elif sum_d_player < 0:
        power -= 1

    sum_d_opponent = d_opponent_life + d_opponent_hand + d_opponent_death \
                   + d_opponent_played
    if sum_d_opponent > 0:
        power -= 1
    elif sum_d_opponent < 0:
        power += 1

    # Playable amount of cards
    # ========================

    playable_d_player = d_player_life + d_player_hand + d_player_played
    if playable_d_player > 0:
        power += 1
    elif playable_d_player < 0:
        power -= 1

    playable_d_opponent = d_opponent_life + d_opponent_hand + d_opponent_played
    if playable_d_opponent > 0:
        power -= 1
    elif playable_d_opponent < 0:
        power += 1

    description = f"{owner1:>8} {stack1:<6} -> {owner2:>8} {stack2:<6}\n"
    return power, description


def move_cards():
    OWNERS = ["Player", "Opponent"]
    STACKS = ["Death", "Life", "Hand", "Played"]
    PRODUCT = itertools.product(OWNERS, STACKS, OWNERS, STACKS)
    for owner1, stack1, owner2, stack2 in PRODUCT:
        power, description = new_move_card(owner1, stack1, owner2, stack2)
        if power == 1 \
        and not (stack1 == "Played" and stack2 == "Hand") \
        and not (stack1 == "Hand" and stack2 == "Played") \
        and not (stack1 == "Life" and stack2 == "Death") \
        and not (stack1 == "Death" and stack2 == "Played"):
            yield f"{power:<+3} {description}"


def main():
    with open("cards.txt", "w") as file:
        for card in unique_everseen(move_cards()):
            file.write(card)


if __name__ == '__main__':
    main()
