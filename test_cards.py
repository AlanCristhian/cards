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
    def setUp(self) -> None:
        self.player = objects.Character("Player")
        self.other = objects.Character("Opponent")

    def test_instance(self) -> None:
        self.assertIsInstance(self.player, objects.Character)

    def test_new_car_stack_method(self) -> None:
        self.player.new_card_stack(self.other)
        self.assertEqual(len(self.player.life_stack), 14)


class BaseCardSuite(unittest.TestCase):
    player: objects.Character
    opponent: objects.Character

    def setUp(self) -> None:
        self.player = objects.Character(name="Player")
        self.opponent = objects.Character(name="Opponent")


class HealSuite(BaseCardSuite):
    heal_card: objects.Heal

    def setUp(self) -> None:
        super().setUp()
        self.heal_card = objects.Heal(
            player=self.player, opponent=self.opponent)

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

    def test_kill_instance(self) -> None:
        self.assertIsInstance(self.kill_card, objects.Kill)

    def test_kill_name(self) -> None:
        self.assertEqual(self.kill_card.name, "Kill")

    def test_kill_description(self) -> None:
        self.assertEqual(self.kill_card.__doc__,
           "Move a Card from Opponent Played Stack to Opponent Death Stack.")

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


class MatchSuite(unittest.TestCase):
    match: objects.Match

    def assertStackNotEqual(self,
                            first: objects.Stack,
                            second: objects.Stack
                            ) -> None:
        if len(first) == len(second) \
        and all(type(f) == type(s) for f, s in zip(first, second)):
            raise AssertionError(f"first is equal to second")

    def setUp(self) -> None:
        player_1 = objects.Character(name="player_1")
        player_2 = objects.Character(name="player_2")
        self.match = objects.Match(player_1=player_1, player_2=player_2)

    def test_oponents(self) -> None:
        self.assertIsInstance(self.match.player_1, objects.Character)
        self.assertIsInstance(self.match.player_2, objects.Character)

    def test_life_stacks(self) -> None:
        self.assertEqual(len(self.match.player_1.life_stack), 10)
        self.assertEqual(len(self.match.player_2.life_stack), 10)

    def test_shuffle_life_stacks(self) -> None:
        self.assertStackNotEqual(self.match.player_1.hand,
                                self.match.player_2.hand)
        self.assertStackNotEqual(self.match.player_1.life_stack,
                                self.match.player_2.life_stack)

    def test_hand_size(self) -> None:
        self.assertEqual(len(self.match.player_1.hand), 4)
        self.assertEqual(len(self.match.player_2.hand), 4)

    def test_player_order_shuffle(self) -> None:
        self.match.shuffle_players = mock.Mock()
        self.match.__post_init__()
        self.match.shuffle_players.assert_called()


class MatchLoopSuite(unittest.TestCase):
    def setUp(self) -> None:
        player_1 = objects.Character(name="player_1")
        player_2 = objects.Character(name="player_2")
        self.match = objects.MatchLoop(player_1=player_1, player_2=player_2)

    def test_instance(self) -> None:
        self.assertIsInstance(self.match, objects.MatchLoop)

    def test_stwitch_player(self) -> None:
        turns = list(self.match.turns)
        self.match.switch_player()
        self.assertNotEqual(list(self.match.turns), turns)

    def test_add_card_to_current_player(self) -> None:
        self.match.switch_player()
        self.match.add_card_to_current_player()
        self.assertEqual(len(self.match.current_player.hand), 5)
        self.assertEqual(len(self.match.current_player.life_stack), 9)


HARM = 0
DRAIN = 1
KILL = 2


class MatchLoopPlayCardSuite(unittest.TestCase):
    def setUp(self) -> None:
        player_1 = objects.Character(name="player_1")
        player_2 = objects.Character(name="player_2")
        self.match = objects.MatchLoop(player_1=player_1, player_2=player_2)

        self.match.switch_player()
        self.match.current_player.life_stack.extend(
            self.match.current_player.hand)
        self.match.current_player.hand.clear()
        names = [c.name for c in self.match.current_player.life_stack]
        harm_index = names.index("Harm")
        drain_index = names.index("Drain")
        kill_index = names.index("Kill")

        self.harm_card = self.match.current_player.life_stack[harm_index]
        self.drain_card = self.match.current_player.life_stack[drain_index]
        self.kill_card = self.match.current_player.life_stack[kill_index]

        self.match.current_player.hand.append(self.harm_card)
        self.match.current_player.hand.append(self.drain_card)
        self.match.current_player.hand.append(self.kill_card)

    def test_hand_reduced(self) -> None:
        self.match.play_card(HARM)
        self.assertEqual(len(self.match.current_player.hand), 2)

    def test_card_in_played_stack(self) -> None:
        self.match.play_card(HARM)
        self.assertEqual(len(self.match.current_player.played_stack), 1)

    def test_harm_card_in_played_stack(self) -> None:
        self.match.play_card(HARM)
        self.assertIn(self.harm_card, self.match.current_player.played_stack)

    def test_two_chips_less_on_opponent(self) -> None:
        self.match.play_card(HARM)
        self.assertEqual(len(self.match.next_player.chip_stack), 8)

    def test_over_if_two_chips_on_opponent_after_harm(self) -> None:
        self.match.next_player.chip_stack.clear()
        self.match.next_player.chip_stack.extend([objects.Chip()]*2)
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(HARM)

    def test_over_if_one_chip_on_opponent_after_harm(self) -> None:
        self.match.next_player.chip_stack.clear()
        self.match.next_player.chip_stack.append(objects.Chip())
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(HARM)

    def test_over_if_no_chip_on_opponent_after_harm(self) -> None:
        self.match.next_player.chip_stack.clear()
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(HARM)

    def test_over_if_one_chip_on_opponent_after_drain(self) -> None:
        self.match.next_player.chip_stack.clear()
        self.match.next_player.chip_stack.append(objects.Chip())
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(DRAIN)

    def test_over_if_no_chip_on_opponent_after_drain(self) -> None:
        self.match.next_player.chip_stack.clear()
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(DRAIN)

    def test_over_if_no_playable_card_on_opponent_after_kill(self) -> None:
        self.match.next_player.played_stack.clear()
        self.match.next_player.life_stack.clear()
        self.match.next_player.hand.clear()
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(KILL)

    def test_over_if_one_playable_card_on_opponent_after_kill(self) -> None:
        self.match.next_player.played_stack.clear()
        self.match.next_player.life_stack.clear()
        self.match.next_player.hand.clear()
        self.match.next_player.played_stack.append(self.harm_card)
        with self.assertRaises(objects.GameOverError):
            self.match.play_card(KILL)


if __name__ == '__main__':
    unittest.main()
