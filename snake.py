from tkinter import *
import random
from tkinter import messagebox

game_width = 700
game_height = 750  
speed = 80
space_size = 50
body_parts = 3
snake_color = "#FFFFFF"
food_color = "#FF0000"
bg_color = "#000000"
border_color = "#00FF00"

class Snake:
    
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tags='snakes')
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (game_width // space_size) - 1) * space_size
        y = random.randint(0, (game_height // space_size) - 1) * space_size

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tag='food')

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= space_size
    elif direction == 'down':
        y += space_size
    elif direction == 'left':
        x -= space_size
    elif direction == 'right':
        x += space_size
    
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        if score > max_score: 
            update_max_score(score)
        label.config(text="Score:{} Max Score:{}".format(score, max_score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def game_over():
    global score
    if messagebox.askyesno("Game Over", "Play again?"):
        reset_game()
    else:
        window.destroy()

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= game_width:
        return True
    elif y < 0 or y >= game_height:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def update_max_score(new_score):
    global max_score
    max_score = new_score
    try:
        with open("max_score.txt", "w") as file:
            file.write(str(max_score))
    except Exception as e:
        print("Error updating max score:", e)

def reset_game():
    global score, direction
    score = 0
    direction = 'down' 
    canvas.delete(ALL)
    snake.coordinates = []
    snake.squares = []
    for i in range(0, body_parts):
        snake.coordinates.append([0, 0])
    for x, y in snake.coordinates:
        square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tags='snakes')
        snake.squares.append(square)
    food = Food()
    next_turn(snake, food)

try:
    with open('max_score.txt', "r") as file:
        max_score = int(file.read())
except FileNotFoundError:
    max_score = 0
except Exception as e:
    print("Error reading max score:", e)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

canvas = Canvas(window, bg=bg_color, height=game_height, width=game_width, highlightbackground=border_color)
canvas.pack()

label = Label(window, text="Score:{} Max Score:{}".format(score, max_score), font=('consolas', 20), bg=bg_color, fg="grey")
label.place(relx=0.5, rely=0.05, anchor="center")

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_width()
screen_height = window.winfo_height()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_width / 2) - (window_width / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
