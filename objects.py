"""Define objects present in the card game."""

from __future__ import annotations

from typing import no_type_check, Any
import abc
import collections
import dataclasses
import random


class Chip:
    pass


class Stack(collections.deque):
    def popindex(self, index: int) -> Any:
        item = self[index]
        del self[index]
        return item


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
    hand: Stack = dataclasses.field(default_factory=Stack)


class Card(abc.ABC):
    @abc.abstractmethod
    def __post_init__(self) -> None:
        pass

    @abc.abstractmethod
    def play(self, index: int=0) -> bool:
        pass


@dataclasses.dataclass
class Heal(Card):
    """Append two Health Chips on Character Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Heal"

    def play(self, index: int=0) -> bool:
        self.player.chip_stack.append(Chip())
        self.player.chip_stack.append(Chip())
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Postpone(Card):
    """Append a Turn on Player."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Postpone"

    def play(self, index: int=0) -> bool:
        """Tell the Match that will have an extra turn"""
        return True


@dataclasses.dataclass
class Harm(Card):
    """Remove two Health Chips on Opponent Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Harm"

    def play(self, index: int=0) -> bool:
        self.opponent.chip_stack.pop()
        self.opponent.chip_stack.pop()
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Drain(Card):
    """Move a Health Chip from Opponent Chip Stack to Player Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Drain"

    def play(self, index: int=0) -> bool:
        self.player.chip_stack.append(self.opponent.chip_stack.pop())
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Accumulate(Card):
    """Move a Card from Player Life Stack to Player Hand."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Accumulate"

    def play(self, index: int=0) -> bool:
        self.player.hand.append(self.player.life_stack.pop())
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Resurrect(Card):
    """Move a Card from Player Death Stack to Player Life Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Resurrect"

    def play(self, index: int=0) -> bool:
        self.player.life_stack.append(self.player.death_stack.popleft())
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Steal(Card):
    """Move a Card from Opponent Life Stack to Player Life Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Steal"

    def play(self, index: int=0) -> bool:
        self.player.life_stack.append(self.opponent.life_stack.popindex(index))
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Crop(Card):
    """Move a Card from Opponent Hand to Opponent Life Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Crop"

    def play(self, index: int=0) -> bool:
        self.opponent.life_stack.append(self.opponent.hand.popindex(index))
        return False  # Tell the Match that no extra turn


@dataclasses.dataclass
class Kill(Card):
    """Move a Card from Opponent Life Stack to Opponent Death Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Kill"

    def play(self, index: int=0) -> bool:
        self.opponent.death_stack.append(self.opponent.life_stack.pop())
        return False  # Tell the Match that no extra turn


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



DEFAULT_STACK = Stack([Heal, Heal, Postpone, Postpone, Harm, Harm, Drain,
                       Drain, Accumulate, Accumulate, Resurrect, Resurrect,
                       Steal, Steal, Crop, Crop, Kill, Kill])

CARDS = (Heal, Postpone, Harm, Drain, Accumulate, Resurrect, Steal, Crop,
         Kill)
