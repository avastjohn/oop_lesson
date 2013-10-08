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

GAME_WIDTH = 12
GAME_HEIGHT = 10



#### Put class definitions here ####
class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

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

class Dragon(GameElement):
    IMAGE = "Dragon"
    SOLID = True

    def interact(self, player):
        # asks player what she wants
        # burns player to crisp if player has nothing to give or tries to fight
        # flies away if player hands a gem over
        pass

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True

    def interact(self, player):
        # gives player her quest
        pass

class Obstacle(GameElement):
    SOLID = True

class Invisible(Obstacle):
    IMAGE = "Invisible"

    def interact(self, player):
        if player.inventory.get("pile of wood") >= 3:
            GAME_BOARD.del_el(self.x, self.y)
            boat = Boat()
            GAME_BOARD.register(boat)
            GAME_BOARD.set_el(self.x, self.y, boat)
            player.inventory["pile of wood"] = 0
        elif player.inventory.get("pile of wood") > 0:
            GAME_BOARD.draw_msg("You don't have enough wood yet!")
        else:
            GAME_BOARD.draw_msg("You need a boat to cross the river. Chop down some trees to get wood.")
"""
class Push_Wall(Item):
    IMAGE = "DirtBlock"
    
    def interact(self, player):
        pass
"""
class Wall(Obstacle):
    IMAGE = "Wall"

class Rock(Obstacle):
    IMAGE = "Rock"

class Tree(GameElement):
    SOLID = True

class Ugly_Tree(Tree):
    IMAGE = "UglyTree"

    def interact(self, player):
        GAME_BOARD.draw_msg("This is just a bush and can't be chopped down.")


class Tall_Tree(Tree):
    IMAGE = "TallTree"

    def interact(self, player):
        have_axe = False
        for item in player.inventory:
            if type(item) == Axe:
                have_axe = True
        if have_axe:
            GAME_BOARD.draw_msg("You have an axe! Hit space to chop down this tree.")
            player.inventory["pile of wood"] = player.inventory.get("pile of wood", 0) + 1
            GAME_BOARD.draw_msg("You chopped down this tree and got some wood!")
            GAME_BOARD.del_el(self.x, self.y)
        else:
            GAME_BOARD.draw_msg("If you acquire an axe, you can chop down this tree.")
    

class Boat(GameElement):
    IMAGE = "Boat"
          
class Item(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory[self] = player.inventory.get(self, 0) + 1
        GAME_BOARD.draw_msg("You just picked up a %s! You have %d items!" % (self.name, len(player.inventory)))
        GAME_BOARD.del_el(self.x, self.y)

class Gem(Item):
    name = "Orange Gem"
    IMAGE = "OrangeGem"

class Key(Item):
    name = "Key"
    IMAGE = "Key"

class Axe(Item):
    name = "Axe"
    IMAGE = "Axe"

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
                player.inventory[self.contents] = player.inventory.get(self.contents, 0) + 1
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

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(6, 9, PLAYER)

    HAPLESS_BOY = Boy()
    GAME_BOARD.register(HAPLESS_BOY)
    GAME_BOARD.set_el(7, 9, HAPLESS_BOY)

    DRAGON = Dragon()
    GAME_BOARD.register(DRAGON)
    GAME_BOARD.set_el(3, 1, DRAGON)

    invisible_positions = [
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (8, 4),
        (9, 4),
        (10, 4),
        (11, 4)
    ]

    invisibles = []
    for pos in invisible_positions:
        invisible = Invisible()
        GAME_BOARD.register(invisible)
        GAME_BOARD.set_el(pos[0], pos[1], invisible)
        invisibles.append(invisible)

    rock_positions = [
        (2, 9),
        (7, 1),
        (9, 7),
        (11, 0),
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    wall_positions = [
        (2, 0),
        (2, 1),
        (3, 2),
        (4, 2),
        (4, 0),
        (5, 0),
        (5, 1)
    ]

    walls = []

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

    tall_tree_positions = [
        (0, 9),
        (1, 5),
        (1, 0),
        (5, 7),
        (6, 0),
        (6, 5),
        (8, 1),
        (10, 3),
        (10, 6),
    ]

    tall_trees = []

    for pos in tall_tree_positions:
        tree = Tall_Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        tall_trees.append(tree)

    ugly_tree_positions = [
        (0, 2),
        (3, 8),
        (7, 3),
        (8, 6),
        (10, 8),
        (10, 0)
    ]

    ugly_trees = []

    for pos in ugly_tree_positions:
        tree = Ugly_Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        ugly_trees.append(tree)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(4, 7, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(3, 0, key)

    axe = Axe()
    GAME_BOARD.register(axe)
    GAME_BOARD.set_el(1, 7, axe)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(11, 9, chest)

def keyboard_handler():
    direction = None
    chopped = False
    

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
        if type(existing_el) == Boat:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, existing_el)
            GAME_BOARD.set_el(next_x, next_y - 1, PLAYER)

        elif existing_el:
            existing_el.interact(PLAYER)
            if not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
        elif existing_el == None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)