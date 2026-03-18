#### ICAwk6Harrison
# Oakley Harrison
# CSC1019
# 25/2/2026

 #### PREAMBLE

# Ask a yes/no question (is it raining?), Next, ask the temprature.

#Then, determine if they need a jacket or if they need a coat, and if they need an umbrella 


#### USER INPUT

raining = input("Hello! I'll help you determine what to wear outside today.\n Does it seem to be raining outside today?\nYes or No: ")

temperature = float(input("Now, what temperature does your weather app or thermometer say it is? \n Temprature: "))


#### PROCESS & OUTPUT

if temperature > 65:
    print("\n \nIt's warm out today! You probably don't need a coat or a jacket.")
elif 50 <= temperature <= 65:
    print("\n \nIt's a tad chilly today, best to bring a light jacket with you!")
else:
    print("\n \nIt's cold out today! Bring a heavier coat with you to stay warm!")


if raining.lower() == "yes":
    print("And, it's raining as well, so make sure to bring an umbrella!")
else:
    print("And, it's not raining, so don't worry about an umbrella!")
