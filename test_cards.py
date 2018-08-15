from typing import List
from unittest import mock
import collections
import unittest

import objects


class ChipSuite(unittest.TestCase):
    def test_chip_instance(self) -> None:
        chip = objects.Chip()


class StackSuite(unittest.TestCase):
    def test_stack_instance(self) -> None:
        stack = objects.Stack()
        self.assertIsInstance(stack, objects.Stack)
        self.assertIsInstance(stack, collections.deque)


class HandSuite(unittest.TestCase):
    def test_hand_instance(self) -> None:
        hand = objects.Stack()
        self.assertIsInstance(hand, collections.deque)


class TurnSuite(unittest.TestCase):
    def test_turn_instance(self) -> None:
        turn = objects.Turn()
        self.assertIsInstance(turn, collections.deque)


class CharacterSuite(unittest.TestCase):
    def test_player(self) -> None:
        player = objects.Character(name="User")


class BaseCardSuite(unittest.TestCase):
    player: objects.Character
    opponent: objects.Character

    def setUp(self) -> None:
        self.player = objects.Character(name="Player")
        self.opponent = objects.Character(name="Opponent")

    def tearDown(self) -> None:
        del self.player
        del self.opponent


class HealSuite(BaseCardSuite):
    heal_card: objects.Heal

    def setUp(self) -> None:
        super().setUp()
        self.heal_card = objects.Heal(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.heal_card

    def test_heal_instance(self) -> None:
        self.assertIsInstance(self.heal_card, objects.Heal)

    def test_heal_name(self) -> None:
        self.assertEqual(self.heal_card.name, "Heal")

    def test_heal_description(self) -> None:
        self.assertEqual(self.heal_card.__doc__,
            "Append two Chips on Character Chip Stack.")

    def test_more_chips_in_player_chip_stack_after_play(self) -> None:
        before = len(self.player.chip_stack)
        self.heal_card.play()
        after = len(self.player.chip_stack)
        self.assertEqual(after, before + 2)


class HarmSuite(BaseCardSuite):
    harm_card: objects.Harm

    def setUp(self) -> None:
        super().setUp()
        self.harm_card = objects.Harm(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.harm_card

    def test_harm_instance(self) -> None:
        self.assertIsInstance(self.harm_card, objects.Harm)

    def test_harm_name(self) -> None:
        self.assertEqual(self.harm_card.name, "Harm")

    def test_harm_description(self) -> None:
        self.assertEqual(self.harm_card.__doc__,
            "Remove two Chips on Opponent Chip Stack.")

    def test_less_chips_in_opponent_chip_stack_after_play(self) -> None:
        before = len(self.opponent.chip_stack)
        self.harm_card.play()
        after = len(self.opponent.chip_stack)
        self.assertEqual(after, before - 2)


class DrainSuite(BaseCardSuite):
    drain_card: objects.Drain

    def setUp(self) -> None:
        super().setUp()
        self.drain_card = objects.Drain(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.drain_card

    def test_absorb_instance(self) -> None:
        self.assertIsInstance(self.drain_card, objects.Drain)

    def test_absorb_name(self) -> None:
        self.assertEqual(self.drain_card.name, "Drain")

    def test_absorb_description(self) -> None:
        self.assertEqual(self.drain_card.__doc__,
           "Move a Chip from Opponent Chip Stack to Player Chip Stack.")

    def test_move_a_chip_from_opponent_to_player(self) -> None:
        opponent_before = len(self.opponent.chip_stack)
        player_before = len(self.player.chip_stack)
        self.drain_card.play()
        opponent_after = len(self.opponent.chip_stack)
        player_after = len(self.player.chip_stack)
        self.assertEqual(opponent_after, opponent_before - 1)
        self.assertEqual(player_after, player_before + 1)


class ExpandSuite(BaseCardSuite):
    expand_card: objects.Expand

    def setUp(self) -> None:
        super().setUp()
        self.expand_card = objects.Expand(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.expand_card

    def test_expand_instance(self) -> None:
        self.assertIsInstance(self.expand_card, objects.Expand)

    def test_expand_name(self) -> None:
        self.assertEqual(self.expand_card.name, "Expand")

    def test_expand_description(self) -> None:
        self.assertEqual(self.expand_card.__doc__,
           "Move a Card from Player Life Stack to Player Hand.")

    def test_move_a_card_from_life_stack_to_hand(self) -> None:
        card = objects.Heal(player=self.player, opponent=self.opponent)
        self.player.life_stack.append(card)
        len_life_stack = len(self.player.life_stack)
        len_hand = len(self.player.hand)
        self.expand_card.play()
        self.assertEqual(len(self.player.life_stack), len_life_stack - 1)
        self.assertEqual(len(self.player.hand), len_hand + 1)


class ReviveSuite(BaseCardSuite):
    revive_card: objects.Revive

    def setUp(self) -> None:
        super().setUp()
        self.revive_card = objects.Revive(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.revive_card

    def test_revive_instance(self) -> None:
        self.assertIsInstance(self.revive_card, objects.Revive)

    def test_revive_name(self) -> None:
        self.assertEqual(self.revive_card.name, "Revive")

    def test_revive_description(self) -> None:
        self.assertEqual(self.revive_card.__doc__,
           "Move a Card from Player Death Stack to Player Life Stack.")

    def test_move_a_card_from_death_stack_to_life_stack(self) -> None:
        heal = objects.Heal(player=self.player, opponent=self.opponent)
        harm = objects.Harm(player=self.player, opponent=self.opponent)
        self.player.death_stack.append(heal)
        self.player.death_stack.append(harm)
        len_death_stack = len(self.player.death_stack)
        len_life_stack = len(self.player.life_stack)
        self.revive_card.play()
        self.assertEqual(len(self.player.death_stack), len_death_stack - 1)
        self.assertEqual(len(self.player.life_stack), len_life_stack + 1)
        self.assertEqual(self.player.life_stack.pop(), heal)


class CropSuite(BaseCardSuite):
    crop_card: objects.Crop

    def setUp(self) -> None:
        super().setUp()
        self.crop_card = objects.Crop(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.crop_card

    def test_crop_instance(self) -> None:
        self.assertIsInstance(self.crop_card, objects.Crop)

    def test_crop_name(self) -> None:
        self.assertEqual(self.crop_card.name, "Crop")

    def test_crop_description(self) -> None:
        self.assertEqual(self.crop_card.__doc__,
           "Move a Card from Opponent Hand to Opponent Life Stack.")

    def test_crop_a_card_from_opponent(self) -> None:
        card = objects.Harm(player=self.player, opponent=self.opponent)
        self.opponent.hand.append(card)
        len_opponent_hand = len(self.opponent.hand)
        len_opponent_life_stack = len(self.opponent.life_stack)
        self.crop_card.play()
        self.assertEqual(len(self.opponent.hand),
                         len_opponent_hand - 1)
        self.assertEqual(len(self.opponent.life_stack),
                         len_opponent_life_stack + 1)


class KillSuite(BaseCardSuite):
    kill_card: objects.Kill

    def setUp(self) -> None:
        super().setUp()
        self.kill_card = objects.Kill(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        super().tearDown()
        del self.kill_card

    def test_kill_instance(self) -> None:
        self.assertIsInstance(self.kill_card, objects.Kill)

    def test_kill_name(self) -> None:
        self.assertEqual(self.kill_card.name, "Kill")

    def test_kill_description(self) -> None:
        self.assertEqual(self.kill_card.__doc__,
           "Move a Card from Opponent Life Stack to Opponent Death Stack.")

    def test_kill_a_card_from_opponent(self) -> None:
        card = objects.Harm(player=self.player, opponent=self.opponent)
        self.opponent.life_stack.append(card)
        len_opponent_life_stack = len(self.opponent.life_stack)
        len_opponent_death_stack = len(self.opponent.death_stack)
        self.kill_card.play()
        self.assertEqual(len(self.opponent.life_stack),
                         len_opponent_life_stack - 1)
        self.assertEqual(len(self.opponent.death_stack),
                         len_opponent_death_stack + 1)


@unittest.skip("Not implemented yet")
class MatchSuite(unittest.TestCase):
    match: objects.Match

    @classmethod
    def setUpClass(cls) -> None:
        player1 = objects.Character(name="player1")
        player2 = objects.Character(name="player2")
        cls.match = objects.Match(player1=player1, player2=player2)
        cls.match.shuffle_players = mock.Mock(
            side_effect=cls.match.shuffle_players)
        cls.match.shuffle_each_life_stack = mock.Mock(
            side_effect=cls.match.shuffle_each_life_stack)
        cls.match.initialize()

    def test_oponents(self) -> None:
        self.assertIsInstance(self.match.player1, objects.Character)
        self.assertIsInstance(self.match.player2, objects.Character)

    def test_shuffle_each_card(self) -> None:
        self.match.shuffle_each_life_stack.assert_called()

    def test_hand_size(self) -> None:
        self.assertEqual(len(self.match.player1.hand), 5)
        self.assertEqual(len(self.match.player2.hand), 5)

    def test_player_order_shuffle(self) -> None:
        self.match.shuffle_players.assert_called()
        self.assertEqual(len(self.match.turns), 2)


if __name__ == '__main__':
    unittest.main()
