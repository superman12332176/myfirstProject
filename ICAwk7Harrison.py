#ICAwk7
#Oakley Harrison
#3/11/2026
#CSC1019

####PREAMBLE

#Create a program that maps out the upper limit of the fibonacci sequence based on \
#the user's input



####INITIALIZATION

#Define variables

a=0
b=1
c=0


####INPUT

print("Let's build the fibonacci sequence!")
limit=int(input("Enter a whole number for the sequences upper limit. \n Number:"))


####PROCESS

print(a)
print(b)

while c<limit:
    c=b+a
    if c>=limit: break
    a=b
    b=c
    print(c)


####FINAL OUTPUT

    c=b+a

print(f"The next sequence in the fibonacci sequence is larger than your number, {limit},")
print(f"The next number in the sequence would be", c ,"!")
