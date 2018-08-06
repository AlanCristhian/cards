import unittest
from unittest import mock
import collections
import uuid

import objects
import cards
import stacks


CARD_STACK = objects.Stack([cards.HARM, cards.HARM, cards.HARM, cards.HARM,
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
        player = objects.Player(name="user1", card_stack=objects.Stack(),
                                chip_stack=stacks.INITIAL_CHIPS)
        self.assertIsInstance(player, objects.Player)
        self.assertIsInstance(player.name, str)
        self.assertIsInstance(player.card_stack, objects.Stack)
        self.assertIsInstance(player.chip_stack, objects.Stack)


class CardSuite(unittest.TestCase):
    def test_card_instance(self):
        card = objects.Card(name="test", description="Test {x}", value=10)
        self.assertIsInstance(card, objects.Card)
        self.assertEqual(card.name, "test")
        self.assertEqual(card.description, "Test 10")
        self.assertEqual(card.value, 10)
        self.assertIsInstance(card.identifier, uuid.UUID)


class RulesSuite(unittest.TestCase):
    @classmethod
    def setUp(cls):
        player1 = objects.Player(name="player1", card_stack=objects.Stack(),
                                 chip_stack=stacks.INITIAL_CHIPS)
        player1.card_stack.extend(CARD_STACK)
        player1.chip_stack.extend(stacks.INITIAL_CHIPS)
        player2 = objects.Player(name="player2", card_stack=objects.Stack(),
                                 chip_stack=stacks.INITIAL_CHIPS)
        player2.card_stack.extend(CARD_STACK)
        player2.chip_stack.extend(stacks.INITIAL_CHIPS)
        cls.round = objects.Round(player1=player1, player2=player2)
        cls.round.shuffle_players = mock.Mock(
            side_effect=cls.round.shuffle_players)
        cls.round.initialize()

    def test_oponents(self):
        self.assertIsInstance(self.round.player1, objects.Player)
        self.assertIsInstance(self.round.player2, objects.Player)

    def test_shuffle(self):
        self.assertNotEqual(self.round.player1.card_stack, CARD_STACK)
        self.assertNotEqual(self.round.player2.chip_stack, CARD_STACK)

    def test_card_hand_size(self):
        self.assertEqual(len(self.round.player1.card_hand), 5)
        self.assertEqual(len(self.round.player2.card_hand), 5)

    def test_chip_hand_size(self):
        self.assertEqual(len(self.round.player1.chip_hand), 3)
        self.assertEqual(len(self.round.player2.chip_hand), 3)

    def test_player_order_shuffle(self):
        self.round.shuffle_players.assert_called()
        self.assertEqual(len(self.round.turns), 2)


if __name__ == '__main__':
    unittest.main()
