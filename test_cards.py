import unittest
from unittest import mock
import collections
import uuid

import objects
import cards


life_stack = objects.Stack([cards.HARM, cards.HARM, cards.HARM, cards.HARM,
                            cards.HEAL, cards.HEAL])


class BoxSuite(unittest.TestCase):
    def test_box_instance(self):
        box = objects.Box()


class StackSuite(unittest.TestCase):
    def text_stack_instance(self):
        stack = objects.Stack()
        self.assertIsInstance(stack, objects.Stack)
        self.assertIsInstance(stack, collections.deque)


class HandSuite(unittest.TestCase):
    def test_hand_instance(self):
        hand = objects.Hand()


class PlayerSuite(unittest.TestCase):
    def test_player(self):
        player = objects.Player(name="user1", life_stack=objects.Stack())
        self.assertIsInstance(player, objects.Player)
        self.assertIsInstance(player.name, str)
        self.assertIsInstance(player.life_stack, objects.Stack)


class CardSuite(unittest.TestCase):
    def test_card_instance(self):
        card = cards.Card(name="test", description="Test 10")
        self.assertIsInstance(card, cards.Card)
        self.assertEqual(card.name, "test")
        self.assertEqual(card.description, "Test 10")


class RulesSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        player1 = objects.Player(name="player1", life_stack=objects.Stack())
        player1.life_stack.extend(life_stack)
        player2 = objects.Player(name="player2", life_stack=objects.Stack())
        player2.life_stack.extend(life_stack)
        cls.round = objects.Round(player1=player1, player2=player2)
        cls.round.shuffle_players = mock.Mock(
            side_effect=cls.round.shuffle_players)
        cls.round.initialize()

    def test_oponents(self):
        self.assertIsInstance(self.round.player1, objects.Player)
        self.assertIsInstance(self.round.player2, objects.Player)

    def test_shuffle(self):
        self.assertNotEqual(self.round.player1.life_stack, life_stack)
        self.assertNotEqual(self.round.player2.life_stack, life_stack)

    def test_hand_size(self):
        self.assertEqual(len(self.round.player1.hand), 5)
        self.assertEqual(len(self.round.player2.hand), 5)

    def test_player_order_shuffle(self):
        self.round.shuffle_players.assert_called()
        self.assertEqual(len(self.round.turns), 2)


if __name__ == '__main__':
    unittest.main()
