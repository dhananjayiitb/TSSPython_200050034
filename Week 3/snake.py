import pygame, sys, time, random

#initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480
bg_color = (0,0,0)
speed = 10

#Parameters for Snake
snake_pos = [100, 50]
snake_body = [[100, 50], [100-speed, 50], [100-(2*speed), 50]]
snake_color = (0,255,0)
direction = 1 # 1: right, 2: up, 3: left, 4: down
change_to = direction 

#Parameters for food
food_pos = [random.randrange(0, frame_size_x, speed), random.randrange(0, frame_size_y, speed)]
food_spawn = False

score = 0

isPaused = 1 #IGNORE!!!!, Will add pause functionality later for my learning

# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()

def check_for_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keyDown_events(event)

def check_keyDown_events(event):
    if(event.key == pygame.K_ESCAPE):
        sys.exit()
    elif(event.key == pygame.K_RIGHT):
        change_to(1)
    elif(event.key == pygame.K_LEFT):
        change_to(3)
    elif(event.key == pygame.K_UP):
        change_to(2)
    elif(event.key == pygame.K_DOWN):
        change_to(4)
    elif(event.key == pygame.K_SPACE):
        isPaused *= -1

def change_to(new_direction):
    global direction
    if(new_direction%2 == direction%2): return
    direction = new_direction


def update_snake():
    global score, food_spawn
    if(direction == 1):
        new_head = [snake_body[0][0]+speed, snake_body[0][1]]
    elif(direction == 2):
        new_head = [snake_body[0][0], snake_body[0][1]-speed]
    elif(direction == 3):
        new_head = [snake_body[0][0]-speed, snake_body[0][1]]
    elif(direction == 4):
        new_head = [snake_body[0][0], snake_body[0][1]+speed]

    if new_head in snake_body: game_over()
    snake_body.insert(0,new_head)
    tail = snake_body.pop()
    if(snake_body[0][0] == food_pos[0] and snake_body[0][1] == food_pos[1]): 
        score+=1
        snake_body.append(tail)
        food_spawn = True
        create_food()

    if(new_head[0]< 0 or new_head[0] > frame_size_x-speed or new_head[1]<0 or new_head[1]>frame_size_y-speed):
        game_over()


def create_food():
    global food_spawn, food_pos
    if not food_spawn: return False
    food_pos = [random.randrange(0, frame_size_x, speed), random.randrange(0, frame_size_y, speed)]
    food_spawn = False
    return True



def show_score(pos = [50,20], color = (240,240,240), font = None, size = 24):
    score_img = pygame.font.SysFont(font, size).render("Score : "+ str(score), True, color)
    score_rect = score_img.get_rect()
    score_rect.center = pos
    game_window.blit(score_img, score_rect)
    pygame.display.update()


def update_screen():
    game_window.fill(bg_color)
    for e in snake_body:
        pygame.draw.rect(game_window, snake_color, pygame.Rect(e[0], e[1] , speed, speed))
    pygame.draw.rect(game_window, (240,240,240), pygame.Rect(food_pos[0], food_pos[1], speed, speed))
    pygame.display.flip()
    


def game_over():
    gameover_img = pygame.font.SysFont(None, 48).render("You Died!", True, (240,240,240))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.center = [frame_size_x/2, frame_size_y/2]
    game_window.blit(gameover_img, gameover_rect)
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

# Main loop
while True:
    check_for_events()
    update_snake()
    update_screen()
    show_score()

    # To set the speed of the screen
    fps_controller.tick(25)