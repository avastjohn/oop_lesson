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
        have_gem = False
        for item in player.inventory:
            if type(item) == Gem:
                have_gem = True
        if have_gem:
            GAME_BOARD.draw_msg("The dragon spies the shiny bauble you are carrying, seizes it from you and flies away.")
            GAME_BOARD.del_el(self.x, self.y)
        else:
            GAME_BOARD.draw_msg("Dragon: Who are you to talk to me, human?? Bring me something valuable... and maybe I'll let you pass.")

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True

    def interact(self, player):
        have_star = False
        for item in player.inventory:
            if item == "Star":
                have_star = True
        if have_star:
            GAME_BOARD.draw_msg("Helpless boy: Oh, brave adventuress, you've saved me from a life of misery! I will forever be indebted to you!")
            heart = Heart()
            GAME_BOARD.register(heart)
            GAME_BOARD.set_el(7, 8, heart)
        else:
            GAME_BOARD.draw_msg("Helpless boy: Ohhh, what should I do???")


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
            GAME_BOARD.draw_msg("You built a cool little boat with the wood you gathered!")
            player.inventory["pile of wood"] = 0
        elif player.inventory.get("pile of wood") > 0:
            GAME_BOARD.draw_msg("You don't have enough wood yet!")
        else:
            GAME_BOARD.draw_msg("You need a way to cross the river. Think!")

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
            GAME_BOARD.draw_msg("You have an axe! Hit space to chop.")
            player.inventory["pile of wood"] = player.inventory.get("pile of wood", 0) + 1
            GAME_BOARD.draw_msg("You chopped down this tree and got some wood!")
            GAME_BOARD.del_el(self.x, self.y)
        else:
            GAME_BOARD.draw_msg("If you have an axe, you can chop down this tree.")
    

class Boat(GameElement):
    IMAGE = "Boat"
          
class Item(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory[self] = player.inventory.get(self, 0) + 1
        GAME_BOARD.draw_msg("You just picked up a %s! You have %d items!" % (self.name, len(player.inventory)))
        GAME_BOARD.del_el(self.x, self.y)

class Dirt_Wall(GameElement):
    IMAGE = "DirtBlock"
    SOLID = False
    
    def interact(self, player):
        pass

class Gem(Item):
    name = "Green Gem"
    IMAGE = "GreenGem"

class Star(Item):
    name = "Star"
    IMAGE = "Star"

class Heart(Item):
    name = "Heart"
    IMAGE = "Heart"

class Key(Item):
    name = "Key"
    IMAGE = "Key"

class Axe(Item):
    name = "Axe"
    IMAGE = "Axe"

class Chest(GameElement):
    CLOSED_IMAGE = pyglet.resource.image("Chest Closed.png")
    CLOSED_SPRITE = pyglet.sprite.Sprite(CLOSED_IMAGE)
    OPEN_IMAGE = pyglet.resource.image("Chest Open.png")
    OPEN_SPRITE = pyglet.sprite.Sprite(OPEN_IMAGE)
    IMAGE = "ChestClosed"
    SOLID = True
    contents = choice(["Star"])
    chest_closed = True
    timer = 0


    def update(self, dt):
        self.timer += dt
        if self.timer > 2:
            self.sprite = Chest.CLOSED_SPRITE
        self.timer = 0


    def interact(self, player):
        if self.chest_closed:
            have_key = False
            for item in player.inventory:
                if type(item) == Key:
                    have_key = True
            if have_key:
                self.sprite = Chest.OPEN_SPRITE
                player.inventory[self.contents] = player.inventory.get(self.contents, 0) + 1
                GAME_BOARD.draw_msg("You found a %s in the chest!" % self.contents)
                star = Star()
                GAME_BOARD.register(star)
                GAME_BOARD.set_el(11, 8, star)
                self.chest_closed = False
            else:
                GAME_BOARD.draw_msg("You need a key to open this chest.")
        else:
            GAME_BOARD.draw_msg("You have emptied the chest.")


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    GAME_BOARD.draw_msg("Helpless boy: I'm in trouble! I've lost the key to my master's treasure! Please help me get it back!" )

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

    dirt_wall_positions = [
        (3, 2),
        (4, 2)
    ]

    dirt_walls = []

    for pos in dirt_wall_positions:
        dirt_wall = Dirt_Wall()
        GAME_BOARD.register(dirt_wall)
        GAME_BOARD.set_el(pos[0], pos[1], dirt_wall)
        walls.append(dirt_wall)

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
            if PLAYER.y == 5:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, existing_el)
                GAME_BOARD.set_el(next_x, next_y-1, PLAYER)
            else:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, existing_el)
                GAME_BOARD.set_el(next_x, next_y+1, PLAYER)
        elif type(existing_el) == Dirt_Wall:
            if direction == "up":
                if GAME_BOARD.get_el(next_x, next_y - 1) == None:
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x, next_y - 1, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            elif direction == "right":
                if GAME_BOARD.get_el(next_x + 1, next_y) == None:
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x + 1, next_y, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            elif direction == "left":
                if GAME_BOARD.get_el(next_x - 1, next_y) == None:
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x - 1, next_y, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
        elif existing_el:
            existing_el.interact(PLAYER)
            if not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
        elif existing_el == None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)