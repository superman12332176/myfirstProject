-- 3/22/2026 Oakley --
"I think our next changes from this point should be to condense the events and sequences into functions. It'll make developing the game later easier when we can just 
call the function for 'bandit_event()'. Also, I think we are at a good point to begin adding the 'classes' of characters, we can call on different functions 
for each event based on the class. Example:

def bandit_event(player_class, health, food):
    print("\n>> EVENT: BANDITS! They attack your wagon.")
    
    if player_class == "Nobleman":
        print("The bandits recognize your family crest and demand a heavy ransom! Food -20.")
        food -= 20
        
    elif player_class == "Hunter":
        print("You easily snipe the bandits from afar. They flee! No resources lost.")
        
    else:
        # Standard bandit logic goes here for everyone else
        
    # Send the updated stats back to the main game
    return health, food

--


__________________________________________________________________________________________________________
Goals:
-- (Uncompleted goals look like this [ ], and completed like this [x]) --
[ ] Agree on next development goals
