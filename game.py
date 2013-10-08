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

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

    def interact(self, player):
        pass

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

class Axe(Item):
    name = "Axe"
    IMAGE = "Star"

class Chest(GameElement):
    IMAGE = "ChestClosed"
    SOLID = True
    contents = choice(["Blue Gem", "Green Gem", "Orange Gem", "Heart"])
    chest_closed = True

    def interact(self, player):
        if self.chest_closed:
            have_key = False
            for item in player.inventory:
                if type(item) == Key:
                    have_key = True
            if have_key:
                player.inventory.append(self.contents)
                GAME_BOARD.draw_msg("You found a %s in the chest! You have %d items!" % (self.contents, len(player.inventory)))
                
                for item in player.inventory:
                    if type(item) == Key:
                        player.inventory.remove(item)
    #            IMAGE = "ChestOpen"
    #            GAME_BOARD.del_el(self.x,self.y)
    #            GAME_BOARD.set_el(self.x, self.y, self)
                self.chest_closed = False
            else:
                GAME_BOARD.draw_msg("You need a key to open this chest.")
        else:
            GAME_BOARD.draw_msg("You have emptied the chest.")

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (7, 0)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    trees = []

    tree_positions = [
        (3, 4),
        (5, 4),
        (6, 5),
        (5, 7)
    ]

    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(3, 7, PLAYER)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(4, 5, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0, 0, key)

    axe = Axe()
    GAME_BOARD.register(axe)
    GAME_BOARD.set_el(1, 7, axe)

#    wall = Wall()
#    GAME_BOARD.register(wall)
#    GAME_BOARD.set_el(5, 6, wall)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(7, 7, chest)

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