# test_game.py
import unittest
from game import Game, Player, Character, Weapon, Room, Card

#Finally, I used 'Claude' to review my code for errors.
class TestClueGame(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.game = Game()
        self.player1 = Player("Alice", Character.SCARLET)
        self.player2 = Player("Bob", Character.MUSTARD)
        self.player3 = Player("Charlie", Character.GREEN)
        self.game.players.extend([self.player1, self.player2, self.player3])

    def test_player_creation(self):
        """Verify player initialization."""
        player = Player("TestDude", Character.PLUM)
        self.assertEqual(player.name, "TestDude")
        self.assertEqual(player.char, Character.PLUM)
        self.assertFalse(player.wrong_guess)
        self.assertEqual(len(player.cards), 0)
        self.assertIsNone(player.room)
        self.assertEqual(len(player.notes), 0)

    def test_dice_roll(self):
        """Check dice roll range."""
        player = Player("Roller", Character.WHITE)
        for _ in range(100):
            roll = player.roll()
            self.assertTrue(2 <= roll <= 12)

    def test_game_setup(self):
        """Test game setup and card distribution."""
        self.game.players.clear()
        with self.assertRaises(ValueError):
            self.game.setup()

        self.game.players.extend([self.player1, self.player2, self.player3])
        self.game.setup()

        self.assertIsNotNone(self.game.solution)
        self.assertIn('char', self.game.solution)
        self.assertIn('weapon', self.game.solution)
        self.assertIn('room', self.game.solution)

        total_cards = sum(len(p.cards) for p in self.game.players)
        expected = len(Character) + len(Weapon) + len(Room) - 3
        self.assertEqual(total_cards, expected)

    def test_secret_passages(self):
        """Test secret passage functionality."""
        player = Player("Sneaky", Character.PEACOCK)

        player.room = Room.KITCHEN
        self.assertTrue(self.game.sneak(player))
        self.assertEqual(player.room, Room.STUDY)

        self.assertTrue(self.game.sneak(player))
        self.assertEqual(player.room, Room.KITCHEN)

        player.room = Room.HALL
        self.assertFalse(self.game.sneak(player))
        self.assertEqual(player.room, Room.HALL)

# Debugged and fixed the suggestion logic using 'Grok 3'. Cleared all player cards to avoid interference.
    def test_suggestion_mechanics(self):
        """Test suggestion mechanics."""
        self.game.setup()
        self.player1.room = Room.LIBRARY
        self.player1.cards.clear()
        self.player2.cards.clear()
        self.player3.cards.clear()
        test_card = Card("Weapon", Weapon.DAGGER)
        self.player2.cards.append(test_card)

        result = self.game.suggest(self.player1, Character.PLUM, Weapon.DAGGER, Room.LIBRARY)
        self.assertIsNotNone(result)
        self.assertEqual(result.val, Weapon.DAGGER)

        result = self.game.suggest(self.player1, Character.WHITE, Weapon.PIPE, Room.LIBRARY)
        self.assertIsNone(result)

        self.player1.room = Room.BALLROOM
        with self.assertRaises(ValueError):
            self.game.suggest(self.player1, Character.PLUM, Weapon.DAGGER, Room.LIBRARY)

    def test_accusation_mechanics(self):
        """Test accusation outcomes."""
        self.game.setup()

        result = self.game.accuse(self.player1, Character.SCARLET, Weapon.ROPE, Room.HALL)
        self.assertFalse(result)
        self.assertTrue(self.player1.wrong_guess)
        self.assertFalse(self.game.done)

        result = self.game.accuse(self.player1, Character.PLUM, Weapon.PIPE, Room.STUDY)
        self.assertFalse(result)

        real_char = self.game.solution['char']
        real_weapon = self.game.solution['weapon']
        real_room = self.game.solution['room']
        result = self.game.accuse(self.player2, real_char, real_weapon, real_room)
        self.assertTrue(result)
        self.assertTrue(self.game.done)

if __name__ == "__main__":
    unittest.main()