#---- CHANGE LOG ----
# Name  -  Change Comment  -  Date

#Oakley - Added change log at the top of the file - 3/22/2026
#Oakley - Changed lines for "elif event_roll == 2" in random trail events to only allow intigers 1 and 2 to progress the code - 3/22/2026
#Oakley - Added nested loops at the beginning of the code where it can call back to - 5/4/2026
#Oakley - Added save/load functionality - 5/4/2026
#Oakley - Added class system and try/except blocks - 5/4/2026

import random
import os

SAVE_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "python_trail_save.txt")

class Character:
    def __init__(self, name, prof_choice):
        self.name = name
        self.miles = 650
        self.day = 1
        self.food = 75
        self.health = 5
        
        professions = ["Banker", "Carpenter", "Farmer"]
        self.profession = professions[prof_choice - 1]
        
        if self.profession == "Banker":
            self.food += 50
        elif self.profession == "Carpenter":
            self.health += 2
        elif self.profession == "Farmer":
            self.food += 25
            self.health += 1

def save_game(name, profession, miles, food, health, day):
    with open(SAVE_FILE, "w") as f:
        f.write(f"{name}\n{profession}\n{miles}\n{food}\n{health}\n{day}\n")

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            lines = f.read().splitlines()
            name = lines[0]
            profession = lines[1]
            miles = int(lines[2])
            food = int(lines[3])
            health = int(lines[4])
            day = int(lines[5])
            return name, profession, miles, food, health, day
    except FileNotFoundError:
        print("\nNo save file found on your Desktop! Starting a new game...")
        return None
    except (IndexError, ValueError):
        print("\nSave file is corrupted! Starting a new game...")
        return None

def wolf_event(food, health):
    print("\nAs you were hunting, a PACK OF WOLVES came across you!")
    action = input("Do you (1) Fight them off or (2) Run away? ")
    
    if action == "1":
        if random.random() < 0.6:
            gain = random.randint(15, 30)
            print(f"You fought bravely and scared them off, "
                  f"grabbing {gain} lbs of meat as they fled.")
            food += gain
        else:
            print("The wolves bit you badly before you could drive them away! Health -2, Food -5.")
            health -= 2
            food -= 5
    else:
        print("You ran back to the wagon in panic, dropping supplies! Food -12.")
        food -= 12
    return food, health

def bear_event(food, health):
    print("\nYou spot a huge bear near the river.")
    action = input("Do you (1) Try to hunt the bear or (2) Stay hidden? ")
    if action == "1":
        if random.random() < 0.5:
            gain = random.randint(30, 60)
            print(f"You took down the bear! You get {gain} lbs of meat, but you got scratched. Health -1.")
            food += gain
            health -= 1
        else:
            print("The bear charged you! You escaped, but you're badly hurt. Health -2.")
            health -= 2
    else:
        print("You stayed hidden and the bear wandered off. No food gained today.")
    return food, health

def accident_event(food, health):
    print("\nYou slipped on some rocks and twisted your ankle while hunting.")
    print("You couldn't find much food, and you are hurt. Health -1, Food +5.")
    health -= 1
    food += 5
    return food, health

def normal_hunt_event(food):
    found = random.randint(10, 40)
    if random.random() < 0.75:
        print(f"\nYou had a decent hunt and brought back {found} lbs of food.")
        food += found
    else:
        print("\nYou saw a lot of tracks, but found no game today.")
    return food

def storm_event(day, food):
    print("\n>> EVENT: A heavy storm hits. You huddle in the wagon. Day +1, Food -5.")
    day += 1
    food -= 5
    return day, food

def bandit_event(health, food):
    print("\n>> EVENT: BANDITS! They attack your wagon.")
    
    while True:
        choice_bandit = input("Do you (1) Fight or (2) Surrender some supplies? ")
        
        if choice_bandit == "1":
            if random.random() < 0.5:
                print("You scared off the bandits! But you were injured. Health -1.")
                health -= 1
            else:
                print("The bandits overwhelmed you. Health -2, Food -10.")
                health -= 2
                food -= 10
            break 
            
        elif choice_bandit == "2":
            print("You gave them some food to avoid a fight. Food -15.")
            food -= 15
            break 
            
        else:
            print("Invalid choice! The bandits are drawing their weapons. Pick 1 or 2.")
    return health, food

def broken_wheel_event(day, food):
    print("\n>> EVENT: Broken wagon wheel! You lose time fixing it. Day +1, Food -5.")
    day += 1
    food -= 5
    return day, food

def trader_event(food):
    print("\n>> EVENT: A friendly trader passes by and shares supplies. Food +20.")
    food += 20
    return food

def sickness_event(health):
    print("\n>> EVENT: Someone in your party gets sick. Health -1.")
    health -= 1
    return health

print("Welcome to the Python Trail!")
print("1. Start a New Game")
print("2. Continue")

while True:
    start_choice = input("Pick 1 or 2: ")
    if start_choice == "2":
        loaded_data = load_game()
        if loaded_data:
            player_name, profession, miles_to_go, food, health, day = loaded_data
            print(f"\nWelcome back, {player_name} the {profession}!")
            break
        else:
            start_choice = "1" 
            
    if start_choice == "1":
        player_name = input("\nWhat is your name, traveler? ")
        
        professions_list = [
            "Banker (Starts with +50 extra food)", 
            "Carpenter (Starts with +2 extra health)", 
            "Farmer (Starts with +25 food and +1 health)"
        ]
        print("\nChoose your class:")
        for i, prof in enumerate(professions_list, 1):
            print(f"{i}. {prof}")
            
        while True:
            try:
                prof_choice = int(input("Pick 1-3: "))
                if 1 <= prof_choice <= 3:
                    break
                else:
                    print("Please pick a number from 1 to 3.")
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        new_player = Character(player_name, prof_choice)
        player_name = new_player.name
        profession = new_player.profession
        miles_to_go = new_player.miles
        food = new_player.food
        health = new_player.health
        day = new_player.day
        
        print(f"\nGood luck, {player_name} the {profession}! You have {miles_to_go} miles to go.")
        print("The trail is dangerous. Think carefully about your choices.\n")
        save_game(player_name, profession, miles_to_go, food, health, day)
        break

game_over = False

# --- MAIN GAME LOOP ---
while not game_over:
    print("\n----------------------------")
    print(f"Day: {day} | Miles left: {miles_to_go}")
    print(f"Food: {food} | Health: {health}")
    print("----------------------------")

    print("What do you want to do?")
    print("1. Travel")
    print("2. Rest")
    print("3. Hunt for food")
    print("4. Status")
    print("5. Save & Quit")
    choice = input("Pick 1-5: ")

    # --- ACTION 1: TRAVEL ---
    if choice == "1":
        miles_traveled = random.randint(18, 40)
        miles_to_go -= miles_traveled
        food -= 14      
        day += 1
        print(f"\nYou traveled {miles_traveled} miles along the dusty trail.")

    # --- ACTION 2: REST ---
    elif choice == "2":
        if health < 5:
            health += 1
            print("\nYou rested by the campfire. Health +1.")
        else:
            print("\nYou tried to rest, but you're already at full health.")
        food -= 8
        day += 1

    # --- ACTION 3: HUNT ---
    elif choice == "3":
        print("\nYou head into the wilderness to hunt...")
        day += 1

        hunt_roll = random.randint(1, 6)

        if hunt_roll == 1:
            food, health = wolf_event(food, health)
        elif hunt_roll == 2:
            food, health = bear_event(food, health)
        elif hunt_roll == 3:
            food, health = accident_event(food, health)
        else:
            food = normal_hunt_event(food)

    # --- ACTION 4: STATUS ---
    elif choice == "4":
        print(f"\n--- {player_name}'s Status ---")
        print(f"Class: {profession}")
        print(f"Day: {day}")
        print(f"Miles left: {miles_to_go}")
        print(f"Food: {food} lbs")
        print(f"Health: {health}")

    # --- ACTION 5: SAVE & QUIT ---
    elif choice == "5":
        print("\nSaving your game...")
        save_game(player_name, profession, miles_to_go, food, health, day)
        print("You decided to rest the oxen and end your journey for today. Safe travels!")
        game_over = True
        continue

    else:
        print("\nI didn't understand that. Please pick a number from 1 to 5.")
        continue

    # --- RANDOM TRAIL EVENTS ---
    if not game_over:
        event_roll = random.randint(1, 12)

        if event_roll == 1:
            day, food = storm_event(day, food)
        elif event_roll == 2:
            health, food = bandit_event(health, food)
        elif event_roll == 3:
            day, food = broken_wheel_event(day, food)
        elif event_roll == 4:
            food = trader_event(food)
        elif event_roll == 5:
            health = sickness_event(health)

    # --- FOOD & STARVATION CHECK ---
    if food <= 0:
        print("\nSTARVATION: You are out of food! You grow weaker. Health -1.")
        health -= 1
        food = 0

    # --- WIN / LOSE CONDITIONS ---
    if miles_to_go <= 0:
        print(f"\nVICTORY! You reached Oregon on Day {day}!")
        print(f"Congratulations, {player_name}! You survived the EXTREME trail.")
        # Optional: wipe the save file upon winning so they have to start fresh next time
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        game_over = True
    elif health <= 0:
        print(f"\nTRAGEDY: {player_name} did not survive the Oregon Trail.")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        game_over = True
