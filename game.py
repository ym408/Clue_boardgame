# game.py
from enum import Enum
import random

class Character(Enum):
    SCARLET = "Miss Scarlet"
    MUSTARD = "Colonel Mustard"
    WHITE = "Mrs. White"
    GREEN = "Mr. Green"
    PEACOCK = "Mrs. Peacock"
    PLUM = "Professor Plum"

class Weapon(Enum):
    ROPE = "Rope"
    DAGGER = "Dagger"
    WRENCH = "Wrench"
    PISTOL = "Pistol"
    CANDLESTICK = "Candlestick"
    PIPE = "Lead Pipe"

class Room(Enum):
    HALL = "Hall"
    LOUNGE = "Lounge"
    DINING = "Dining Room"
    KITCHEN = "Kitchen"
    BALLROOM = "Ballroom"
    CONSERVATORY = "Conservatory"
    BILLIARD = "Billiard Room"
    LIBRARY = "Library"
    STUDY = "Study"

class Card:
    """Just a card"""
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val

class Player:
    """Player stuff"""
    def __init__(self, name, char):
        self.name = name
        self.char = char
        self.cards = []
        self.room = None
        self.wrong_guess = False
        self.notes = set()

    def roll(self):
        """Roll some dice"""
        try:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            if d2 == 6:
                print("Magnifying glass!")
                d2 = 1
            return d1 + d2
        except:
            print("Dice roll messed up!")
            return 2

    def show(self, guess):
        """Pick a card to show"""
        for c in self.cards:
            if c.val in guess.values():
                return c
        return None

class Game:
    """The whole game"""
    def __init__(self):
        self.players = []
        self.solution = None
        self.done = False
        self.passages = {
            Room.KITCHEN: Room.STUDY,
            Room.STUDY: Room.KITCHEN,
            Room.CONSERVATORY: Room.LOUNGE,
            Room.LOUNGE: Room.CONSERVATORY
        }
# Used ChatGPT to optimize this feature for better efficiency.
    def setup(self):
        """Get things going"""
        if len(self.players) < 3:
            raise ValueError("Need more players!")
        chars = [Card("Character", c) for c in Character]
        weapons = [Card("Weapon", w) for w in Weapon]
        rooms = [Card("Room", r) for r in Room]

        self.solution = {
            'char': random.choice(chars).val,
            'weapon': random.choice(weapons).val,
            'room': random.choice(rooms).val
        }

        chars = [c for c in chars if c.val != self.solution['char']]
        weapons = [w for w in weapons if w.val != self.solution['weapon']]
        rooms = [r for r in rooms if r.val != self.solution['room']]

        pile = chars + weapons + rooms
        random.shuffle(pile)

        # Equal cards for everyone first
        cards_per_player = len(pile) // len(self.players)
        for p in self.players:
            for _ in range(cards_per_player):
                p.cards.append(pile.pop())

        # The remaining cards are dealt out one by one
        player_idx = 0
        while pile:
            self.players[player_idx].cards.append(pile.pop())
            player_idx = (player_idx + 1) % len(self.players)

    def suggest(self, player, char, weapon, room):
        """Guess time"""
        if player.room != room:
            raise ValueError("Wrong room, buddy!")
        guess = {'char': char, 'weapon': weapon, 'room': room}
        me = self.players.index(player)
        for i in range(1, len(self.players)):
            next_guy = self.players[(me + i) % len(self.players)]
            card = next_guy.show(guess)
            if card:
                return card
        return None

    def accuse(self, player, char, weapon, room):
        """Big guess"""
        if player.wrong_guess:
            return False
        guess = {'char': char, 'weapon': weapon, 'room': room}
        if guess == self.solution:
            self.done = True
            return True
        player.wrong_guess = True
        return False

    def sneak(self, player):
        """Use a secret path"""
        if player.room in self.passages:
            player.room = self.passages[player.room]
            return True
        return False