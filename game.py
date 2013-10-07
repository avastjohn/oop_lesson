import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    rock_positions = [
        (2, 1),
        (1, 2),
        (4, 2),
        (2, 4)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(5, 5, gem)

#    GAME_BOARD.draw_msg("Jia Yi and Ava are amazing!")

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el == None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)