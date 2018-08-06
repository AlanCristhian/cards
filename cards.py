import objects


HARM = objects.Card(
    name="Harm",
    description="Removes {x} health points on enemy.",
    value=2)


HEAL = objects.Card(
    name="Heal",
    description="Restores {x} health point.",
    value=1)


NULL = objects.Card(
    name="Null",
    description="Does nothing.",
    value=0)
