"""Define objects present in the card game."""

from __future__ import annotations

from typing import no_type_check, Any, Iterable, Optional
import abc
import collections
import dataclasses
import random


class Item:
    def __repr__(self) -> str:
        return type(self).__name__


class Chip(Item):
    pass


class Stack(collections.deque):
    def pop_from(self, index: int) -> Any:
        item = self[index]
        del self[index]
        return item


class ChipStack(Stack):
    def __init__(self,
                 iterable: Iterable[Chip],
                 maxlen: Optional[int] = None
                 ) -> None:
        if maxlen is None:
            super().__init__(iterable)
        else:
            super().__init__(iterable, maxlen)

    def append(self, x: Chip) -> None:
        super().append(x)

    def extend(self, iterable: Iterable) -> None:
        super().extend(iterable)


class CardStack(Stack):
    def __init__(self,
                 iterable: Iterable[Card] = [],
                 maxlen: Optional[int] = None
                 ) -> None:

        if maxlen is None:
            super().__init__(iterable)
        else:
            super().__init__(iterable, maxlen)

    def append(self, x: Card) -> None:
        super().append(x)

    def extend(self, iterable: Iterable) -> None:
        super().extend(iterable)


class Turn(collections.deque):
    pass


def new_chip_stack() -> ChipStack:
    return ChipStack(Chip() for _ in range(10))


@dataclasses.dataclass(repr=False, frozen=True)
class Character:
    name: str
    life_stack: CardStack = dataclasses.field(default_factory=CardStack)
    chip_stack: ChipStack = dataclasses.field(default_factory=new_chip_stack)
    death_stack: CardStack = dataclasses.field(default_factory=CardStack)
    played_stack: CardStack = dataclasses.field(default_factory=CardStack)
    hand: CardStack = dataclasses.field(default_factory=CardStack)

    @no_type_check
    def new_card_stack(self, other: Character) -> None:
        classes = [Heal, Harm, Drain, Revive, Expand, Kill, Crop]*2
        self.life_stack.extend([card(self, other) for card in classes])


class Card(abc.ABC):
    @abc.abstractmethod
    def __post_init__(self) -> None:
        pass

    @abc.abstractmethod
    def play(self, index: int=0) -> None:
        pass


@dataclasses.dataclass
class Heal(Card):
    """Append two Chips on Character Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Heal"

    def play(self, index: int=0) -> None:
        self.player.chip_stack.append(Chip())
        self.player.chip_stack.append(Chip())


@dataclasses.dataclass
class Harm(Card):
    """Remove two Chips on Opponent Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Harm"

    def play(self, index: int=0) -> None:
        self.opponent.chip_stack.pop()
        self.opponent.chip_stack.pop()


@dataclasses.dataclass
class Drain(Card):
    """Move a Chip from Opponent Chip Stack to Player Chip Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Drain"

    def play(self, index: int=0) -> None:
        self.player.chip_stack.append(self.opponent.chip_stack.pop())


@dataclasses.dataclass
class Revive(Card):
    """Move a Card from Player Death Stack to Player Life Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Revive"

    def play(self, index: int=0) -> None:
        self.player.life_stack.append(self.player.death_stack.popleft())


@dataclasses.dataclass
class Expand(Card):
    """Move a Card from Player Life Stack to Player Hand."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Expand"

    def play(self, index: int=0) -> None:
        self.player.hand.append(self.player.life_stack.pop())


@dataclasses.dataclass
class Kill(Card):
    """Move a Card from Opponent Played Stack to Opponent Death Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Kill"

    def play(self, index: int=0) -> None:
        self.opponent.death_stack.append(self.opponent.life_stack.pop())


@dataclasses.dataclass
class Crop(Card):
    """Move a Card from Opponent Hand to Opponent Life Stack."""

    player: Character
    opponent: Character

    def __post_init__(self) -> None:
        self.name = "Crop"

    def play(self, index: int=0) -> None:
        self.opponent.life_stack.append(self.opponent.hand.pop_from(index))


@dataclasses.dataclass
class Match:
    player_1: Character
    player_2: Character
    turns: Turn = dataclasses.field(init=False)
    current_player: Character = dataclasses.field(init=False)
    next_player: Character = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.fill_players_life_stack()
        self.shuffle_life_stacks()
        self.fill_hands()
        self.shuffle_players()

    def fill_players_life_stack(self) -> None:
        self.player_1.new_card_stack(self.player_2)
        self.player_2.new_card_stack(self.player_1)

    @no_type_check
    def shuffle_life_stacks(self) -> None:
        random.shuffle(self.player_1.life_stack)
        random.shuffle(self.player_2.life_stack)

    def fill_hands(self) -> None:
        for _ in range(4):
            self.player_1.hand.append(self.player_1.life_stack.pop())
            self.player_2.hand.append(self.player_2.life_stack.pop())

    @no_type_check
    def shuffle_players(self) -> None:
        self.turns = Turn([self.player_1, self.player_2], maxlen=2)
        random.shuffle(self.turns)


class MatchLoop(Match):
    def switch_player(self) -> None:
        self.current_player = self.turns[0]
        self.next_player = self.turns[1]
        self.turns.reverse()

    def add_card_to_current_player(self) -> None:
        if self.current_player.life_stack:
            self.current_player.hand.append(
                self.current_player.life_stack.pop())
        elif self.current_player.played_stack:
            self.current_player.played_stack.reverse()
            self.current_player.life_stack.extend(
                self.current_player.played_stack)
            self.current_player.played_stack.clear()
            self.current_player.hand.append(
                self.current_player.life_stack.pop())

    def play_card(self, index: int) -> None:
        card = self.current_player.hand.pop_from(index)

        if (isinstance(card, Harm) and len(self.next_player.chip_stack) <= 2) \
        or (isinstance(card, Drain) and len(self.next_player.chip_stack) <= 1):
            raise GameOverError()
        elif isinstance(card, Kill) \
        and len(self.next_player.played_stack) <= 1 \
        and len(self.next_player.hand) == 0 \
        and len(self.next_player.life_stack) == 0:
            raise GameOverError()

        card.play()
        self.current_player.played_stack.append(card)


class GameOverError(RuntimeError):
    pass
