import curses
import math
from random import randint
import sys
import time

# globals
ship = (0, 0)
score = 0
diff_threashold = 1.0
symbols = {
    'ship': '*',
    'obstacle': '-',
    'collision': 'x',
}
width = 40
height = 15
difficulty = 2
advanced_difficulty = 1
starting_location = (height - 2, int(width / 2))


# curses init
def setup_window(height, width):
    curses.initscr()
    win = curses.newwin(height, width, 0, 0)
    win.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(True)
    return win, curses
# Only AD
def move_ship(win, ship):
    event = win.getch()
    x = ship[1]
    if x > 1 and event == curses.KEY_LEFT:
        x -= 1
    if x < width - 2 and event == curses.KEY_RIGHT:
        x += 1
    new_ship = (height - 2, x)
    if new_ship != ship:
        draw_ship(win, ship, ' ')
        draw_ship(win, new_ship)
    return new_ship


def update_obstacle(obstacles, advanced_difficulty):
    global score
    new_obs = []
    integer_obs = []

    if obstacles != []:
        # no dead end
        for obs in obstacles:
            win.addch(math.floor(obs[0]), obs[1], ' ')
            if math.floor(obs[0]) != height - 2:
                new_obs.append((obs[0] + .01, obs[1]))

    if new_obs == [] or math.isclose(new_obs[0][0], int(new_obs[0][0])):
        for _ in range(advanced_difficulty):
            for i in range(num_obs):
                new_obs.insert(0, (1, randint(1, width - 2)))

    if ship[0] in [math.floor(obs[0]) for obs in new_obs]:
        score += 1
    for obs in new_obs:
        integer_obs.append((math.floor(obs[0]), obs[1]))

    return new_obs, integer_obs


def draw_obs(win, obstacles, symbol=symbols['obstacle']):
    for obs in obstacles:
        win.addch(math.floor(obs[0]), obs[1], symbol)


def draw_ship(win, ship, symbol=symbols['ship']):
    win.addch(ship[0], ship[1], symbol)


def tick(difficulty):
    time.sleep(.005 / difficulty)


def get_user_input():
    argv = sys.argv
    uwidth, uheight, udifficulty = width, height, difficulty
    for i in range(len(argv)):
        if argv[i] == '--canvas_height':
            uheight = int(argv[i + 1])
        elif argv[i] == '--canvas_width':
            uwidth = int(argv[i + 1])
        elif argv[i] == '--diff_level':
            udifficulty = int(argv[i + 1])

    return uwidth, uheight, udifficulty


def update_score(win):
    win.addstr(0, width // 4 + 5, 'Score ' + str(score) + '')

def show_collision(win, ship):
    win.addch(ship[0] - 1, ship[1], symbols['collision'])

def ending_win_messages(win):
    ending_message = 'Final Score: ' + str(score-1) + '. ' + "Diffculty: " + str(difficulty)
    win.addstr(height-1, width - len(ending_message) - 1, ending_message)
    key = curses.KEY_RIGHT
    ESC = 27
    while key != ESC:
        key = win.getch()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        width, height, difficulty = get_user_input()
    num_obs = math.ceil(width / 5 * difficulty)
    win, curses = setup_window(height, width)
    ship = starting_location
    obstacles = []
    draw_ship(win, ship, '*')
    while True:
        update_score(win)
        ship = move_ship(win, ship)
        new_obs, integer_obs = update_obstacle(obstacles, advanced_difficulty)
        if ship in integer_obs:
            draw_obs(win, obstacles)
            break

        draw_obs(win, integer_obs)
        obstacles = new_obs
        tick(difficulty)

    show_collision(win, ship)
    ending_win_messages(win)
    curses.endwin()
    #print("Final score = " + str(score) + ".")
