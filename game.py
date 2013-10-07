import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
from random import randrange, choice

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8



#### Put class definitions here ####
class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            if self.y > 0:
                return (self.x, self.y-1)
            return (self.x, self.y)
        elif direction == "down":
            if self.y < GAME_HEIGHT - 1:
                return (self.x, self.y+1)
            return (self.x, self.y)
        elif direction == "left":
            if self.x > 0:
                return (self.x-1, self.y)
            return (self.x, self.y)
        elif direction == "right":
            if self.x < GAME_WIDTH - 1:
                return (self.x+1, self.y)
            return (self.x, self.y)
        return None

class Obstacle(GameElement):
    SOLID = True

class Wall(Obstacle):
    IMAGE = "Wall"

class Rock(Obstacle):
    IMAGE = "Rock"

class Item(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just picked up a %s! You have %d items!" % (self.name, len(player.inventory)))
        GAME_BOARD.del_el(self.x, self.y)

class Gem(Item):
    name = "Blue Gem"
    IMAGE = "BlueGem"

class Key(Item):
    name = "Key"
    IMAGE = "Key"

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    contents = choice(["Blue Gem", "Green Gem", "Orange Gem", "Heart"])

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Key:
                player.inventory.append(self.contents)
                GAME_BOARD.draw_msg("You found a %s in the chest! You have %d items!" % (self.contents, len(player.inventory)))
                break
            else:
                GAME_BOARD.draw_msg("You need a key to open this chest.")


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

    key_pos = (randrange(0, GAME_WIDTH), randrange(0, GAME_HEIGHT))


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(5, 5, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(key_pos[0], key_pos[1], key)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(5, 6, wall)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(6, 7, chest)

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
        if existing_el:
            existing_el.interact(PLAYER)
            if not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
        elif existing_el == None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)