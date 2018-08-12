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


JOKER = Card(
    name="Joker",
    description="Represent other existing card.")
