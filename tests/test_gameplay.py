import unittest

from ventura_game import GameState, is_game_over, replay, step


class GameplayTests(unittest.TestCase):
    def test_replay_is_deterministic(self):
        commands = ["right", "right", "up", "collect", "wait"]
        first = replay(commands)
        second = replay(commands)
        self.assertEqual(first, second)
        self.assertEqual((first.x, first.y, first.score, first.ticks), (2, -1, 10, 5))

    def test_health_clamps_at_zero(self):
        state = replay(["damage", "damage", "damage", "damage"])
        self.assertEqual(state.health, 0)
        self.assertTrue(is_game_over(state))

    def test_invalid_command_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported command"):
            step(GameState(), "teleport")


if __name__ == "__main__":
    unittest.main()
