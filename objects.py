import dataclasses
import collections
import uuid
import random
from typing import List


@dataclasses.dataclass
class Card:
    name: str
    description: str
    identifier: int = dataclasses.field(init=False)
    value: int = 0

    def __post_init__(self):
        self.identifier = uuid.uuid4()
        self.description = self.description.format(x=self.value)


class Box:
    pass


class Stack(collections.deque):
    pass


class Hand(collections.deque):
    pass


class Turn(collections.deque):
    pass


@dataclasses.dataclass
class Player:
    name: str
    life_stack: Stack
    death_stack: Stack = dataclasses.field(init=False)
    hand: Hand = dataclasses.field(default_factory=Hand)
    health: int = 10


@dataclasses.dataclass
class Round:
    player1: Player
    player2: Player
    turns: Turn = dataclasses.field(init=False)

    def initialize(self):
        self.add_joker()
        self.shuffle_each_life_stack()
        self.fill_each_hand()
        self.shuffle_players()

    def add_joker(self):
        import cards
        self.player1.life_stack.append(cards.JOKER)
        self.player2.life_stack.append(cards.JOKER)

    def shuffle_each_life_stack(self):
        random.shuffle(self.player1.life_stack)
        random.shuffle(self.player2.life_stack)

    def fill_each_hand(self):
        for _ in range(5):
            self.player1.hand.append(self.player1.life_stack.pop())
            self.player2.hand.append(self.player2.life_stack.pop())

    def shuffle_players(self):
        self.turns = Turn(maxlen=2)
        self.turns.extend((self.player1, self.player2))
        random.shuffle(self.turns)
