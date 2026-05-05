# Team Name: The Pioneers
# Teammates: Marcus, Oakley, Ruben, Nathan
# Course: PPSC CSC 1019
# Project Topic and Description:Project Criteria
#   1. Give the user information on what input is needed
#   2. Use well named variables
#   3. Prompt the user to enter the needed information
#   4. Print and describe the information (user feedback)
#   5. Comment as appropriate
#   6. Be creative
# Change Log:
# DATE Programmer Description
# ----------------------------------------------------------
# 11 Mar 2026 Marcus Created the initial text file for the Semester Team Project Single Input Code
# I dont think that the ammount of comments that im using is necessary but I think more context is always better than not enough.

#1: Give the user information on what input is needed.
#   So basically any input prompt must print "Please provide your...(insert desired info)" and cant just be unprompted

#2. Use well named variables
#   Self explainitory but I personaly like to use camelCase

#3. Prompt the user to enter the needed information
#   required to use the input function (i guess)

#4. Print and describe the information (user feedback)
#   Add extra context upon the output for example instead of a program printing "22" it should print "The box has 22 items inside"

#5. Comment as appropriate
#   self explainitory (oops lol)

#6. Be creative
#   XD

#11 mar 2026 Marcus end comment

##########################################################################################################################################################

# ---- CHANGE LOG ----
# Project by Marcus, Oakley, Ecko, Ruben, Nathan
# Includes: functions, class system, file I/O, error handling, lists, modular design
#Oakley - 22nd March, Oakley edited the Bandit event
#Oakley - I totally didn't see that we had made this our change log (╥﹏╥). That being said, I edited the bandit event and added an "in code change log." Here's that
#code:
#Oakley - Added change log at the top of the file - 3/22/2026
#Oakley - Changed lines for "elif event_roll == 2" in random trail events to only allow intigers 1 and 2 to progress the code - 3/22/2026
#Marcus - Added extra documetation to identify lines that meet the criteria of the program.
#Marcus - Made final logical edits, project is up to standard for a grade. Time to begin the UI/graphical phase.

import random
import os


SAVE_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "python_trail_save.txt")

# ==========================================================
# CLASS (Object-Oriented Requirement)
# ==========================================================
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


# ==========================================================
# FILE HANDLING (Read/Write Requirement)
# ==========================================================
def save_game(name, profession, miles, food, health, day):
    with open(SAVE_FILE, "w") as f:
        f.write(f"{name}\n{profession}\n{miles}\n{food}\n{health}\n{day}\n")


def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            lines = f.read().splitlines()
            return lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5])
    except:
        print("\nNo valid save file found. Starting new game...")
        return None


# ==========================================================
# FUNCTIONS (Modular Design Requirement)
# ==========================================================

def show_menu(day, miles, food, health):
    print("\n----------------------------")
    print(f"Day: {day} | Miles left: {miles}")
    print(f"Food: {food} | Health: {health}")
    print("----------------------------")
    print("1. Travel")
    print("2. Rest")
    print("3. Hunt")
    print("4. Status")
    print("5. Save & Quit")


def wolf_event(food, health):
    print("\nA PACK OF WOLVES surrounds you!")
    action = input("1) Fight  2) Run: ")

    if action == "1":
        if random.random() < 0.6:
            gain = random.randint(15, 30)
            print(f"You win and gain {gain} food.")
            food += gain
        else:
            print("You are injured! Health -2")
            health -= 2
    else:
        print("You flee and lose supplies! Food -10")
        food -= 10

    return food, health


def bear_event(food, health):
    print("\nA massive bear appears...")
    action = input("1) Hunt  2) Hide: ")

    if action == "1":
        if random.random() < 0.5:
            gain = random.randint(30, 60)
            print(f"You succeed! Food +{gain}, Health -1")
            food += gain
            health -= 1
        else:
            print("The bear injures you! Health -2")
            health -= 2
    else:
        print("You stay hidden.")

    return food, health


def normal_hunt(food):
    if random.random() < 0.75:
        gain = random.randint(10, 40)
        print(f"You hunted successfully! Food +{gain}")
        food += gain
    else:
        print("No luck hunting.")
    return food


def bandit_event(food, health):
    print("\nBANDITS ATTACK!")
    while True:
        choice = input("1) Fight  2) Surrender: ")
        if choice == "1":
            if random.random() < 0.5:
                print("You win but are hurt. Health -1")
                health -= 1
            else:
                print("You lose badly. Health -2, Food -10")
                health -= 2
                food -= 10
            break
        elif choice == "2":
            print("You surrender food. -15 food")
            food -= 15
            break
        else:
            print("Invalid input!")

    return food, health
import turtle

def show_intro():
    screen = turtle.Screen()
    screen.bgcolor('goldenrod1')
    screen.setup(1920, 1080)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # --- TRAIL LINE ---
    t.penup()
    t.pensize(200)
    t.pencolor('lightseagreen')
    t.goto(-1920, 0)
    t.pendown()
    t.goto(1920, 0)

    # --- TITLE ---
    t.penup()
    t.goto(-700, 0)
    t.pencolor('black')
    t.write("The Python Trail", font=("Verdana", 150, "bold italic"))

    # --- SUBTEXT ---
    t.goto(-100, -150)
    t.pencolor('white')
    t.write("Press ENTER to Start...", font=("Courier", 20, "normal"))

    # Wait for Enter key
    def start_game():
        turtle.bye()  # closes turtle window

    screen.listen()
    screen.onkey(start_game, "Return")

    screen.mainloop()

# ==========================================================
# GAME START (User Input + Error Handling)
# ==========================================================

print("Welcome to THE PYTHON TRAIL")
show_intro()

print("1. New Game")
print("2. Load Game")

while True:
    start = input("Choose: ")

    if start == "2":
        data = load_game()
        if data:
            player_name, profession, miles, food, health, day = data
            print(f'Welcome back, {player_name}')
            break
    elif start == "1":
        player_name = input("Enter your name: ")

        professions = [
            "Banker (+50 food)",
            "Carpenter (+2 health)",
            "Farmer (+25 food, +1 health)"
        ]

        print("\nChoose a profession:")
        for i, p in enumerate(professions, 1):
            print(f"{i}. {p}")

        while True:
            try:
                prof_choice = int(input("Pick 1-3: "))
                if 1 <= prof_choice <= 3:
                    break
            except:
                pass
            print("Invalid input!")

        player = Character(player_name, prof_choice)
        player_name = player.name
        profession = player.profession
        miles = player.miles
        food = player.food
        health = player.health
        day = player.day

        break


# ==========================================================
# MAIN GAME LOOP (Repetition + Decision Structures)
# ==========================================================

game_over = False

while not game_over:

    show_menu(day, miles, food, health)

    try:
        choice = int(input("Pick 1-5: "))
    except:
        print("Invalid input!")
        continue

    if choice == 1:
        travel = random.randint(20, 40)
        miles -= travel
        food -= 10
        day += 1
        print(f"You traveled {travel} miles.")

    elif choice == 2:
        if health < 5:
            health += 1
        food -= 5
        day += 1
        print("You rest.")

    elif choice == 3:
        roll = random.randint(1, 3)
        if roll == 1:
            food, health = wolf_event(food, health)
        elif roll == 2:
            food, health = bear_event(food, health)
        else:
            food = normal_hunt(food)

        day += 1

    elif choice == 4:
        print(f"{player_name} | {profession}")

    elif choice == 5:
        save_game(player_name, profession, miles, food, health, day)
        print("Game saved.")
        break

    else:
        print("Invalid choice.")
        continue

    # RANDOM EVENT
    if random.randint(1, 6) == 1:
        food, health = bandit_event(food, health)

    # STARVATION
    if food <= 0:
        print("You are starving! Health -1")
        health -= 1
        food = 0

    # END CONDITIONS
    if miles <= 0:
        print(f"YOU WIN! You reached your destination in {day} days.")
        game_over = True
    elif health <= 0:
        print("You died on the trail...")
        game_over = True
