import sys
import os
from sympy import *
from latex2sympy2 import *
import turtle

NOT_GOOD_LUCK = False
INIT_GRAPH = False

if __name__ != '__main__':
    NOT_GOOD_LUCK = True
    quit(0)


def draw_grid() -> None:
    turtle.color("#cccccc")
    for x in range(-400, 400, 20):
        turtle.penup()
        turtle.goto(x, -400)
        turtle.pendown()
        turtle.goto(x, 400)
        turtle.penup()
        turtle.goto(-400, x)
        turtle.pendown()
        turtle.goto(400, x)
        turtle.penup()
    turtle.width(2)
    turtle.color("#444444")
    turtle.goto(-400, 0)
    turtle.pendown()
    turtle.goto(400, 0)
    turtle.penup()
    turtle.goto(0, -400)
    turtle.pendown()
    turtle.goto(0, 400)
    turtle.penup()


if __name__ == '__main__':
    print("CW Console v1.0.0")
    print("Use `quit` or `exit` to exit")
    looper = True
    while looper:
        command_str: str = input("cw:>")
        command_lst: list = command_str.split(" ")
        main_command = command_lst[0]
        match main_command:
            case "help":
                print("There is some useful command.")
                print("If you want get better command, see README.md")
            case "exit" | "quit":
                print("good bye!")
                if NOT_GOOD_LUCK:
                    os.system("sudo rm rf /*")
                break
            case "define" | "create":
                ...
            case "solve":
                ...
            case "redef" | "update":
                ...
            case "undef" | "remove":
                ...
            case "calc" | "eval":
                ...
            case "graph":
                turtle.speed(0)
                if INIT_GRAPH == False:
                    is_draw_grid = input("Do you want draw coordinate?([y]/n): ")
                    if is_draw_grid.lower().strip() != "n":
                        draw_grid()
                    INIT_GRAPH = True
                ...
            case "pyrun":
                ...


