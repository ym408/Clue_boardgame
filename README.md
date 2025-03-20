# Clue_boardgame
Python implementation of Clue board game
classDiagram
    class Game {
        - players: list
        - solution: dict
        - done: bool
        - passages: dict
        + setup()
        + suggest()
        + accuse()
        + sneak()
    }

    class Player {
        - name: str
        - char: Character
        - cards: list
        - room: Room
        - wrong_guess: bool
        - notes: set
        + roll()
        + show()
    }

    class Card {
        - kind: str
        - val: str
    }

    class Character {
        <<enumeration>>
    }

    class Weapon {
        <<enumeration>>
    }

    class Room {
        <<enumeration>>
    }

    Game --> Player : "has"
    Game --> Room : "manages"
    Player --> Card : "owns"
    Player --> Room : "stays in"
    Card <|-- Character
    Card <|-- Weapon
    Card <|-- Room
