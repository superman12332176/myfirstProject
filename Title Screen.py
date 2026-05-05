#Setup
import turtle
import random
turtle.bgcolor('goldenrod1')
turtle.setup(1920,1080)
turtle.hideturtle()
    
#trail
turtle.penup()
turtle.pensize(200)
turtle.speed(7)
turtle.pencolor('lightseagreen')
turtle.goto(-1920,0)
turtle.pendown()
turtle.goto(1920,0)


#words
turtle.penup()
turtle.goto(-700,0)
turtle.pencolor('black')
turtle.write("The Python Trail", font=("Verdana",150,"bold italic"))
turtle.goto(-100,-100)
turtle.pencolor('white')
turtle.write("Press Enter to Start...",font=("Courier",15,"normal"))
