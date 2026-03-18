####PREAMBLE
#Oakley Harrison
#CSC 1019
#Make a code that tells the user if their chosen number is odd or even


####INPUT

numb=int(input("Print any number at all! I'll magically tell you if it is even or odd! \n Your number:"))


####PROCESS

if (numb%2)==0:
    even=True

else:
    even=False

####OUTPUT

if even:
    print(f"Congradulations! your number, {numb}, is even!!!")

else:
    print(f"Wowzers, you think you're so cool huh? Picking an odd number like {numb}.")
