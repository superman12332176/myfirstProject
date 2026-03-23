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

##################################################

#Insert Python code here and remember to document what you do

##########################################################################################################################################################

#22nd March, Oakley edited the Bandit event

#I totally didn't see that we had made this our change log (╥﹏╥). That being said, I edited the bandit event and added an "in code change log." Here's that
#code:

_____________________________________________________________________________________
elif event_roll == 2:
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
__________________________________________________________________________________________________________

#By changing it to a "while" statment and adding a "pick 1 or 2" we can make sure the user picks their intended choice.

#End comment

###############################################################################################################################


