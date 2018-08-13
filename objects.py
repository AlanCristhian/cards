"""Define objects present in the card game."""

from __future__ import annotations

from typing import no_type_check
import abc
import collections
import dataclasses
import random


class Chip:
    pass


class Stack(collections.deque):
    pass


class Hand(collections.deque):
    pass


class Turn(collections.deque):
    pass


def _make_chip_stack() -> Stack:
    return Stack(Chip() for _ in range(10))


@dataclasses.dataclass
class Character:
    name: str
    life_stack: Stack = dataclasses.field(default_factory=Stack)
    chip_stack: Stack = dataclasses.field(default_factory=_make_chip_stack)
    death_stack: Stack = dataclasses.field(default_factory=Stack)
    played_stack: Stack = dataclasses.field(default_factory=Stack)
    hand: Hand = dataclasses.field(default_factory=Hand)


class Card(abc.ABC):
    @abc.abstractmethod
    def __post_init__(self) -> None:
        pass

    @abc.abstractmethod
    def play(self) -> Character:
        pass


@dataclasses.dataclass
class Heal(Card):
    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Heal"
        self.description = "Append two Health Chips on Character Chip Stack."

    def play(self) -> Character:
        self.player.chip_stack.append(Chip())
        self.player.chip_stack.append(Chip())

        # Return the instance of the opponent
        # to tell the Match who play next turn
        return self.opponent


@dataclasses.dataclass
class Match:
    player1: Character
    player2: Character
    turns: Turn = dataclasses.field(init=False)

    def initialize(self) -> None:
        self.shuffle_each_life_stack()
        self.fill_each_hand()
        self.shuffle_players()

    @no_type_check
    def shuffle_each_life_stack(self) -> None:
        random.shuffle(self.player1.life_stack)
        random.shuffle(self.player2.life_stack)

    def fill_each_hand(self) -> None:
        for _ in range(5):
            self.player1.hand.append(self.player1.life_stack.pop())
            self.player2.hand.append(self.player2.life_stack.pop())

    @no_type_check
    def shuffle_players(self) -> None:
        self.turns = Turn(maxlen=2)
        self.turns.extend((self.player1, self.player2))
        random.shuffle(self.turns)
