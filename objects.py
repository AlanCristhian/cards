import dataclasses
import collections
import uuid
import random
from typing import List


@dataclasses.dataclass
class Card:
    name: str
    description: str
    value: int = 0
    identifier: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.identifier = uuid.uuid4()
        self.description = self.description.format(x=self.value)


class Chip(Card):
    pass


class Box:
    pass


class Stack(collections.deque):
    pass


class Hand(collections.deque):
    pass


@dataclasses.dataclass
class Player:
    name: str
    card_stack: Stack
    chip_stack: Stack
    card_hand: Hand = dataclasses.field(default_factory=Hand)
    chip_hand: Hand = dataclasses.field(default_factory=Hand)


@dataclasses.dataclass
class Round:
    player1: Player
    player2: Player

    def initialize(self):
        self.shuffle_each_card_stack()
        self.fill_each_hand()
        self.turns = collections.deque(maxlen=2)
        self.turns.extend((self.player1, self.player2))
        self.shuffle_players()

    def shuffle_each_card_stack(self):
        random.shuffle(self.player1.card_stack)
        random.shuffle(self.player2.card_stack)

    def fill_each_hand(self):
        for _ in range(5):
            self.player1.card_hand.append(self.player1.card_stack.pop())
            self.player2.card_hand.append(self.player2.card_stack.pop())
        for _ in range(3):
            self.player1.chip_hand.append(self.player1.chip_stack.pop())
            self.player2.chip_hand.append(self.player2.chip_stack.pop())

    def shuffle_players(self):
        random.shuffle(self.turns)
