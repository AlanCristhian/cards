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
        hand = objects.Hand()
        self.assertIsInstance(hand, collections.deque)


class TurnSuite(unittest.TestCase):
    def test_turn_instance(self) -> None:
        turn = objects.Turn()
        self.assertIsInstance(turn, collections.deque)


class CharacterSuite(unittest.TestCase):
    def test_player(self) -> None:
        player = objects.Character(name="User", life_stack=objects.Stack())


class HealSuite(unittest.TestCase):
    player: objects.Character
    opponent: objects.Character
    heal_card: objects.Heal

    def setUp(self) -> None:
        self.player = objects.Character(name="Player")
        self.opponent = objects.Character(name="Opponent")
        self.heal_card = objects.Heal(
            player=self.player, opponent=self.opponent)

    def tearDown(self) -> None:
        del self.player
        del self.opponent
        del self.heal_card

    def test_heal_instance(self) -> None:
        self.assertIsInstance(self.heal_card, objects.Heal)

    def test_larger_chip_stack_after_play(self) -> None:
        before = len(self.player.chip_stack)
        self.heal_card.play()
        after = len(self.player.chip_stack)
        self.assertEqual(after, before + 2)

    def test_opponent_returned_by_play(self) -> None:
        obtained = self.heal_card.play()
        self.assertIs(obtained, self.opponent)


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
