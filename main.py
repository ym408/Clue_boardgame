# main.py
from game import Game, Character, Weapon, Room, Player


# Display options for selection
def show_options(items, title):
    print(f"\n{title}:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.value}")

# Get a valid number input from the player
def grab_num(prompt, low, high):
    while True:
        try:
            num = int(input(prompt))
            if low <= num <= high:
                return num
            print(f"Please enter a number between {low} and {high}.")
        except:
            print("Invalid input, please enter a number.")

def main():
    print("Welcome to Clue!")
    print("Be the first to identify who committed the crime, with what weapon, and where.")
    game = Game()

    # Determine number of players
    num_players = grab_num("How many players do you have?(3-6) ",3,6)
    chars = list(Character)
    
    # Select characters
    show_options(chars, "Available Characters")
    for i in range(num_players):
        name = input(f"\nPlayer {i+1}, enter your name: ").strip()
        while not name:
            name = input("Please provide a valid name: ").strip()
        char_pick = grab_num("Choose your character number: ", 1, len(chars)) - 1
        game.players.append(Player(name, chars[char_pick]))
        print(f"{name}, you are {chars[char_pick].value}.")

    # Reset the game
    try:
        game.setup()
        print("\nCards have been dealt. Let’s begin!")
    except ValueError as e:
        print(f"Error during setup: {e}")
        return

# Fixed errors in code using 'Grok 3'.
    # Main game loop
    turn = 0
    while not game.done:
        player = game.players[turn]
        
        if not player.wrong_guess:
            print(f"\n{player.name}’s turn ({player.char.value})")
            cards = ", ".join(c.val.value for c in player.cards)
            print(f"Your cards: {cards if cards else 'None'}")
            
            # Roll the dice
            input("\nPress Enter to roll the dice...")
            roll = player.roll()
            print(f"You rolled a {roll}.")
            
            # Current location
            if player.room:
                print(f"You are in the {player.room.value}.")
                if player.room in game.passages:
                    sneak = input("Use the secret passage? (y/n): ").lower()
                    if sneak == 'y':
                        game.sneak(player)
                        print(f"Moved to {player.room.value} via passage.")

            # Choose a room
            show_options(list(Room), "Select a Room")
            room_pick = grab_num("Enter room number: ", 1, len(Room)) - 1
            player.room = list(Room)[room_pick]
            print(f"You moved to {player.room.value}.")

            # Player action
            action = ""
            while action not in ['S', 'A', 'N']:
                action = input("\nMake a (S)uggestion, (A)ccusation, or (N)one? ").upper()
                if action not in ['S', 'A', 'N']:
                    print("Please enter S, A, or N.")
            
            if action in ['S', 'A']:
                show_options(list(Character), "Select a Suspect")
                who = grab_num("Choose suspect number: ", 1, len(Character)) - 1
                show_options(list(Weapon), "Select a Weapon")
                what = grab_num("Choose weapon number: ", 1, len(Weapon)) - 1
                
                suspect = list(Character)[who]
                weapon = list(Weapon)[what]
                
                try:
                    if action == 'S':
                        result = game.suggest(player, suspect, weapon, player.room)
                        if result:
                            print(f"\nAnother player showed: {result.val.value}")
                            player.notes.add(result.val.value)
                        else:
                            print("\nNo one could show a card.")
                        next_move = input("\nMake an accusation now? (y/n): ").lower()
                        if next_move == 'y':
                            action = 'A'
                    
                    if action == 'A':
                        print("\nMaking an accusation...")
                        won = game.accuse(player, suspect, weapon, player.room)
                        if won:
                            print(f"\nCongratulations! {player.name} wins!")
                            print("The solution was:")
                            print(f" - Suspect: {game.solution['char'].value}")
                            print(f" - Weapon: {game.solution['weapon'].value}")
                            print(f" - Room: {game.solution['room'].value}")
                            break
                        else:
                            print(f"\n{player.name}’s accusation was incorrect.")
                            print("You can no longer guess, but must show cards when asked.")
                except ValueError as e:
                    print(f"Error: {e}")
        else:
            print(f"\n{player.name} skips turn due to a prior incorrect accusation.")
        
        turn = (turn + 1) % len(game.players)
        
        # Check if everyone has failed
        if all(p.wrong_guess for p in game.players):
            print("\nGame over! All players made incorrect accusations.")
            print("The solution was:")
            print(f" - Suspect: {game.solution['char'].value}")
            print(f" - Weapon: {game.solution['weapon'].value}")
            print(f" - Room: {game.solution['room'].value}")
            break

if __name__ == "__main__":
    main()