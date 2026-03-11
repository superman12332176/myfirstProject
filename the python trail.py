import random

print("Welcome to the Python Trail!")
player_name = input("What is your name, traveler? ")

# --- STARTING STATS ---
miles_to_go = 650      # longer trail
food = 75              # less starting food
health = 5
day = 1
game_over = False

print(f"\nGood luck, {player_name}! You have {miles_to_go} miles to go.")
print("The trail is dangerous. Think carefully about your choices.\n")

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
    print("5. Quit")
    choice = input("Pick 1-5: ")

    # --- ACTION 1: TRAVEL ---
    if choice == "1":
        miles_traveled = random.randint(18, 40)
        miles_to_go -= miles_traveled
        food -= 14      # traveling costs more food
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

    # --- ACTION 3: HUNT (MULTIPLE EVENTS, INCLUDING WOLVES) ---
    elif choice == "3":
        print("\nYou head into the wilderness to hunt...")
        day += 1

        hunt_roll = random.randint(1, 6)

        # 1: WOLF PACK EVENT (your idea)
        if hunt_roll == 1:
            print("\nAs you were hunting, a PACK OF WOLVES came across you!")
            action = input("Do you (1) Fight them off or (2) Run away? ")
            
            if action == "1":
                # 60% chance to win the fight
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

        # 2: BEAR EVENT
        elif hunt_roll == 2:
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

        # 3: ACCIDENT
        elif hunt_roll == 3:
            print("\nYou slipped on some rocks and twisted your ankle while hunting.")
            print("You couldn't find much food, and you are hurt. Health -1, Food +5.")
            health -= 1
            food += 5

        # 4–6: NORMAL HUNTING SUCCESS/FAIL
        else:
            found = random.randint(10, 40)
            if random.random() < 0.75:
                print(f"\nYou had a decent hunt and brought back {found} lbs of food.")
                food += found
            else:
                print("\nYou saw a lot of tracks, but found no game today.")

    # --- ACTION 4: STATUS ---
    elif choice == "4":
        print(f"\n--- {player_name}'s Status ---")
        print(f"Day: {day}")
        print(f"Miles left: {miles_to_go}")
        print(f"Food: {food} lbs")
        print(f"Health: {health}/5")

    # --- ACTION 5: QUIT ---
    elif choice == "5":
        print("\nYou decided to end your journey early.")
        game_over = True
        continue

    else:
        print("\nI didn't understand that. Please pick a number from 1 to 5.")
        continue

    # --- RANDOM TRAIL EVENTS (AFTER YOUR ACTION) ---
    if not game_over:
        event_roll = random.randint(1, 12)

        if event_roll == 1:
            print("\n>> EVENT: A heavy storm hits. You huddle in the wagon. Day +1, Food -5.")
            day += 1
            food -= 5

        elif event_roll == 2:
            print("\n>> EVENT: BANDITS! They attack your wagon.")
            choice_bandit = input("Do you (1) Fight or (2) Surrender some supplies? ")
            if choice_bandit == "1":
                if random.random() < 0.5:
                    print("You scared off the bandits! But you were injured. Health -1.")
                    health -= 1
                else:
                    print("The bandits overwhelmed you. Health -2, Food -10.")
                    health -= 2
                    food -= 10
            else:
                print("You gave them some food to avoid a fight. Food -15.")
                food -= 15

        elif event_roll == 3:
            print("\n>> EVENT: Broken wagon wheel! You lose time fixing it. Day +1, Food -5.")
            day += 1
            food -= 5

        elif event_roll == 4:
            print("\n>> EVENT: A friendly trader passes by and shares supplies. Food +20.")
            food += 20

        elif event_roll == 5:
            print("\n>> EVENT: Someone in your party gets sick. Health -1.")
            health -= 1

        # else: 6–12 = no special event

    # --- FOOD & STARVATION CHECK ---
    if food <= 0:
        print("\nSTARVATION: You are out of food! You grow weaker. Health -1.")
        health -= 1
        food = 0

    # --- WIN / LOSE CONDITIONS ---
    if miles_to_go <= 0:
        print(f"\nVICTORY! You reached Oregon on Day {day}!")
        print(f"Congratulations, {player_name}! You survived the EXTREME trail.")
        game_over = True
    elif health <= 0:
        print(f"\nTRAGEDY: {player_name} did not survive the Oregon Trail.")
        game_over = True
