import collections
import random
import dataclasses
import uuid


@dataclasses.dataclass
class Card:
    name: str
    description: str


HEAL = Card(
    name="Heal",
    description="Append a Health Chip on Player Chip Stack.")


ADVANCE = Card(
    name="Advance",
    description="Append a Turn on Player.")


HARM = Card(
    name="Harm",
    description="Remove a Healt Chip on Opponent Chip Stack.")


ABSORB = Card(
    name="Absorb",
    description="Move a Health Chip from Opponent "
                "Chip Stack to Player Chip Stack.")


ACCUMULATE = Card(
    name="Accumulate",
    description="Move a Card from Player Life Stack to Player Hand.")


RESURRECT = Card(
    name="Resurrect",
    description="Move a Card from Player Death Stack to Player Life Stack.")


STEAL = Card(
    name="Steal",
    description="Move a Card from Opponent Hand to Player Life Stack.")


Crop = Card(
    name="Crop",
    description="Move a Card from Opponent Hand to Opponent Life Stack.")


KILL = Card(
    name="Kill",
    description="Move a Card from Opponent Hand to Opponent Death Stack.")


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
        self.shuffle_each_life_stack()
        self.fill_each_hand()
        self.shuffle_players()

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
