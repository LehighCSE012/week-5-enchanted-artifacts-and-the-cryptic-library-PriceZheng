"""Week 5 coding assignment: Enhance the text-based
adventure game by using dictionaries to manage enchanted
artifacts and sets to handle unique clues in a cryptic
library."""
import random

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover the artifact, return player_stats and artifacts"""
    if artifact_name in artifacts:
        artifact = artifacts.pop(artifact_name) #Pop the artifact and save it
        print(f"You discover the {artifact_name}: {artifact['description']}")
        effect = artifact.get('effect') #Using get() to aviod keyError
        if effect == "increases health":
            #Using update() to update health
            player_stats.update({'health': player_stats['health'] + artifact['power']})
        elif effect == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Applied: {artifact['effect']}, +{artifact['power']}")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Checks if new_clue is already in the clues set using the in operator."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)  #Using add() to add new_clue in clues
        print(f"You discovered a new clue: {new_clue}")
    return clues

def acquire_item(inventory, item):
    """Acquire an item and print the message, update to the inventory list"""
    inventory.append(item) # Using append() to add an item to the list
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Display the player's current inventory"""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(inventory,1):
            print(f"{i}. {item}")

def display_player_status(player_health):
    """Prints the player's current health."""
    print(f"Your current health: {player_health}")

def handle_path_choice(player_health):
    """Randomly chooses a path for the player, either "left" or "right"."""
    path = random.choice(["left","right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health = min(player_health + 10, 100) #Health should not over than 100
    else:
        print("You fall into a pit and lose 15 health points.")
        player_health = max(player_health - 15, 0)
        if player_health == 0:
            print("You are barely alive!")
    return player_health

def player_attack(monster_health):
    """The player inflicts 15 damage to the monster."""
    print("You strike the monster for 15 damage!")
    monster_health = max(monster_health - 15, 0)
    return monster_health

def monster_attack(player_health):
    """Simulates the monster's attack with a chance of critical hit."""
    chance = random.random() #get a random number form 0 to 1
    if chance > 0.5:
        print("The monster hits you for 10 damage!")
        player_health = max(player_health - 10, 0)
    else:
        print( "The monster lands a critical hit for 20 damage!")
        player_health = max(player_health - 20, 0)
    return player_health

def combat_encounter(player_stats, monster_health, has_treasure):
    """Manages the combat encounter using a while loop."""
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = max(monster_health - player_stats['attack'], 0) #Player attack first
        if monster_health == 0:
            print("You defeated the monster!")
            return has_treasure
        player_stats['health'] = monster_attack(player_stats['health']) #Monster attack
        display_player_status(player_stats['health'])
        if player_stats['health']  == 0:
            print("Game Over!")
            return False
    return False #Make sure all path return the bool

def check_for_treasure(has_treasure):
    """"Check the status of treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def handle_puzzle(player_stats, challenge_outcome):
    """Handles puzzle challenges"""
    print("You encounter a puzzle!")
    choice = input("Do you want to 'solve' or 'skip' the puzzle? ").strip().lower()
    if choice == "solve":
        success = random.choice([True, False])
        if success:
            print(challenge_outcome[0])
            player_stats['health'] += challenge_outcome[2]
        else:
            print(challenge_outcome[1])
            player_stats['health'] += challenge_outcome[2]
    return player_stats

def handle_trap(player_stats, challenge_outcome):
    """Handle trap challenges"""
    print("You see a potential trap!")
    choice = input("Do you want to 'disarm' or 'bypass' the trap? ").strip().lower()
    if choice == "disarm":
        success = random.choice([True, False])
        if success:
            print(challenge_outcome[0])
        else:
            print(challenge_outcome[1])
            player_stats['health'] += challenge_outcome[2]
    return player_stats

def handle_library(inventory, clues):
    """Handle library"""
    possible_clues = [
        "The treasure is hidden where the dragon sleeps.",
        "The key lies with the gnome.",
        "Beware the shadows.",
        "The amulet unlocks the final door."
    ]
    selected_clues = random.sample(possible_clues, 2)
    for clue in selected_clues:
        clues = find_clue(clues, clue)

    if "staff_of_wisdom" in inventory:
        print("With the Staff of Wisdom, you can bypass a puzzle later.")
        return input("Enter the name of the room you want to bypass: ").strip()
    return None

def handle_challenge(player_stats, challenge_type, challenge_outcome, room_description, bypass):
    """Handle challenges for dungeon"""
    if challenge_type == "puzzle":
        if bypass and isinstance(bypass, str) and bypass in room_description:
            print("You use your wisdom to bypass the puzzle in this room!")
            if isinstance(challenge_outcome, tuple):
                player_stats['health'] += challenge_outcome[2]
        elif isinstance(challenge_outcome, tuple):
            player_stats = handle_puzzle(player_stats, challenge_outcome)

    elif challenge_type == "trap":
        if isinstance(challenge_outcome, tuple):
            player_stats = handle_trap(player_stats, challenge_outcome)

    elif challenge_type == "none":
        print("There doesn't seem to be a challenge in this room. You move on.")

    return player_stats

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Iterates through each room in dungeon_rooms."""
    for room in dungeon_rooms:
        #Tuple unpacking
        if len(room) == 4:
            room_description, item, challenge_type, challenge_outcome = room
        else:
            raise ValueError(f"Invalid room tuple: {room}")
        bypass = None
        room_description, item, challenge_type, challenge_outcome = room
        print(f"{room_description}")

        #Demonstrating tuple is immutability
        try:
            raise TypeError("Tuples are immutable and cannot be modified!")
        except TypeError as e:
            print(f"Error: {e}")

        if item: #acquire update
            print(f"You found a {item} in the room.")
            acquire_item(inventory, item)
            if len(inventory) > 10: #aviod oveflow
                inventory.pop(0) # Using remove() to remove item at the end
                inventory.insert(0, inventory.pop())  # Using insert() to add item at the beginning

        if challenge_type == "library":
            bypass = handle_library(player_stats, inventory, clues)

        player_stats = handle_challenge(player_stats, challenge_type,
                                        challenge_outcome, room_description, bypass)
        player_stats['health'] = max(player_stats['health'], 0)
        display_inventory(inventory)
        display_player_status(player_stats['health'])
        print("Player Final Stats:", list(player_stats.values()))
        return player_stats, inventory, clues

def main():
    """Initializes game variables and runs the adventure game."""
    player_stats = {'health':100, 'attack':5}
    inventory = [] #String list
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
        "description": "A glowing amulet that enhances your life force.",
        "power": 15,
        "effect": "increases health"
    },
        "ring_of_strength": {
        "description": "A powerful ring that boosts your attack damage.",
        "power": 10,
        "effect": "enhances attack"
    },
        "staff_of_wisdom": {
        "description": "A staff imbued with ancient wisdom.",
        "power": 5,
        "effect": "solves puzzles"
    }
    }


    dungeon_rooms = [

    ("Dusty library", "key", "puzzle",

     ("Solved puzzle!", "Puzzle unsolved.", -5)),

    ("Narrow passage, creaky floor", "torch", "trap",

     ("Avoided trap!", "Triggered trap!", -10)),

    ("Grand hall, shimmering pool", "healing potion", "none", None),

    ("Small room, locked chest", "treasure", "puzzle",

     ("Cracked code!", "Chest locked.", -5)),

    ("Cryptic Library", None, "library", None)

    ]
    monster_health = 55 # Initialize to a hardcoded value
    has_treasure = False #Initialize to False

    has_treasure = random.choice([True, False]) # Randomly assign treasure

    print(f"Starting Health: {player_stats['health']}, Attack: {player_stats['attack']}")
    player_stats = combat_encounter(player_stats, monster_health, has_treasure)

    if random.random() < 0.3 and artifacts:
        artifact_name = random.choice(list(artifacts.keys()))
        player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
    player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms,
                                                   clues, artifacts)
    print("\n--- Game End ---")
    print(f"Final Health: {player_stats['health']}, Attack: {player_stats['attack']}")
    print(f"Final Inventory: {inventory}")
    print("Clues:")
    for clue in clues:
        print(f"- {clue}")

if __name__ == "__main__":
    main()
    