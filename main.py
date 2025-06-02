import turtle
import time
import random

# Set up screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Invaders")
screen.setup(width=600, height=600)
screen.tracer(0)

# Register shapes (optional)
# screen.register_shape("invader.gif")
# screen.register_shape("player.gif")

# Player setup
player = turtle.Turtle()
player.shape("triangle")  # Or use "player.gif"
player.color("white")
player.penup()
player.goto(0, -250)
player.setheading(90)

player_speed = 15

# Bullet setup
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(0.3, 1)
bullet.penup()
bullet.hideturtle()
bullet.setheading(90)

bullet_speed = 20
bullet_state = "ready"

# Create enemies
enemies = []
num_enemies = 5

for i in range(num_enemies):
    enemy = turtle.Turtle()
    enemy.shape("circle")  # Or use "invader.gif"
    enemy.color("red")
    enemy.penup()

    x = random.randint(-200, 200)
    y = random.randint(100, 250)

    enemy.goto(x, y)
    enemies.append(enemy)

enemy_speed = 2

# Scoreboard setup
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-280, 260)
score_pen.write(f"Score: {score}", align="left", font=("Courier", 18, "normal"))

def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="left", font=("Courier", 18, "normal"))

# Movement functions
def move_left():
    x = player.xcor()
    x -= player_speed

    if x < -280:
        x = -280

    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed

    if x > 280:
        x = 280

    player.setx(x)

def fire_bullet():
    global bullet_state

    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

def is_collision(t1, t2):
    return t1.distance(t2) < 20

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Main game loop
game_over = False

while not game_over:
    screen.update()

    for enemy in enemies:
        # Move enemy
        x = enemy.xcor()
        x += enemy_speed

        enemy.setx(x)

        # Reverse direction
        if x > 280 or x < -280:
            enemy_speed *= -1

            for e in enemies:
                e.sety(e.ycor() - 20)

        # Check collision with player
        if enemy.ycor() < -230:
            player.hideturtle()

            print("GAME OVER!")

            # Show GAME OVER! on the screen
            game_over_pen = turtle.Turtle()
            game_over_pen.hideturtle()
            game_over_pen.color("white")
            game_over_pen.penup()
            game_over_pen.goto(0, 0)
            game_over_pen.write("GAME OVER!", align="center", font=("Courier", 36, "bold"))

            game_over = True

        # Check collision with bullet
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)

            enemy.goto(random.randint(-200, 200), random.randint(150, 250))

            # Update score
            score += 1
            update_score()

            # Add a new enemy
            new_enemy = turtle.Turtle()
            new_enemy.shape("circle")
            new_enemy.color("red")
            new_enemy.penup()
            new_enemy.goto(random.randint(-200, 200), random.randint(150, 250))
            enemies.append(new_enemy)

    # Move bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed

        bullet.sety(y)

        # Bullet off screen
        if y > 275:
            bullet.hideturtle()
            bullet_state = "ready"

    time.sleep(0.02)

screen.mainloop()
