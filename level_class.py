# Imports --------------------------------------------------------------------------------------------------------------
import pygame
import constants
# --------------------------------------------------------------------------------------------------------------------//


# Each type of platform will have its own class
class platform_A(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 270
        self.height = 70

        # Load art
        self.image = pygame.image.load("block_a.png").convert()

        self.rect = self.image.get_rect()


class platform_B(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 630
        self.height = 70

        # Load art
        self.image = pygame.image.load("block_b.png").convert()
        self.rect = self.image.get_rect()


class platform_C(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 100
        self.height = 70

        # Load art
        self.image = pygame.image.load("block_c.png").convert()
        self.rect = self.image.get_rect()


class platform_D(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 210
        self.height = 310

        # Load art
        self.image = pygame.image.load("block_d.png").convert()
        self.rect = self.image.get_rect()


class platform_E(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 210
        self.height = 600

        # Load art
        self.image = pygame.image.load("block_e.png").convert()
        self.rect = self.image.get_rect()


class Bush(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 60
        self.height = 60

        # Load art
        self.image = pygame.image.load("bush.png").convert()
        self.rect = self.image.get_rect()


class tree_A(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 60
        self.height = 120

        # Load art
        self.image = pygame.image.load("tree_a.png").convert()
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()


class tree_B(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 60
        self.height = 200

        # load art
        self.image = pygame.image.load("tree_b.png").convert()
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()


# Platform class - for jumping platforms
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)

        self.rect = self.image.get_rect()


# Exit class - on contact, the player will complete the level
class Exit(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.width = 70
        self.height = 70

        # art
        self.image = pygame.image.load("exit.png").convert()
        self.rect = self.image.get_rect()


# Respawn Point class - each level has a point where the player "reboots" to after a "death"
class RespawnPoint(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)

        self.rect = self.image.get_rect()


# Respawn Controller class - each level will have a checkpoint halfway through the level
# This class is a placeholder - when the player reaches this, the respawn point's coordinates are swapped to this one
class RespawnController(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.PINK)

        self.rect = self.image.get_rect()


# wind trigger volume - for levels with wind
class WindTriggerVolume(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)

        self.rect = self.image.get_rect()


class WindEndTriggerVolume(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.RED)

        self.rect = self.image.get_rect()


class Level:
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
# NEW ------------------------------------------------------------------------------------------------------------------
        self.exit_list = pygame.sprite.Group()
        self.respawn_list = pygame.sprite.Group()
        self.wind_trigger_list = pygame.sprite.Group()
        self.wind_end_trigger_list = pygame.sprite.Group()
        self.respawn_controller_list = pygame.sprite.Group()
        self.respawn_point = RespawnPoint(0, 0)
        self.respawn_controller = RespawnController(0, 0)
# ----------------------------------------------------------------------------------------------------------------------
        # How far this world has been scrolled left/right
        self.world_shift = 0

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
# NEW ------------------------------------------------------------------------------------------------------------------
        self.exit_list.update()
        self.respawn_list.update()
        self.wind_trigger_list.update()
        self.wind_end_trigger_list.update()
        self.respawn_controller_list.update()
# ----------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
# NEW ------------------------------------------------------------------------------------------------------------------
        self.exit_list.draw(screen)

        # Below are disabled - drawing for debugging only
        # self.wind_trigger_list.draw(screen)
        # self.wind_end_trigger_list.draw(screen)
        # self.respawn_controller_list.draw(screen)
# ----------------------------------------------------------------------------------------------------------------------

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
# NEW ------------------------------------------------------------------------------------------------------------------
        for lvl_exit in self.exit_list:
            lvl_exit.rect.x += shift_x

        for point in self.respawn_list:
            point.rect.x += shift_x

        for point in self.respawn_controller_list:
            point.rect.x += shift_x

        for trigger in self.wind_trigger_list:
            trigger.rect.x += shift_x

        for volume in self.wind_end_trigger_list:
            volume.rect.x += shift_x
# ----------------------------------------------------------------------------------------------------------------------


# Create platforms for the level
class Level_01(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

# NEW ------------------------------------------------------------------------------------------------------------------
        platform_A_coordinate_array = [[0, 530],
                                       [4460, 530],
                                       [5600, 350],
                                       [6000, 300],
                                       [6400, 200],
                                       [7000, 340],
                                       [7300, 200],
                                       [7700, 200],
                                       [7900, 450],
                                       [9000, 460]
                                       ]
        for coordinate in platform_A_coordinate_array:
            block = platform_A()
            block.rect.x = coordinate[0]
            block.rect.y = coordinate[1]
            block.player = self.player
            self.platform_list.add(block)

        platform_B_coordinate_array = [[500, 530],
                                       [2170, 530],
                                       [3000, 530],
                                       [3630, 530],
                                       [4870, 530],
                                       [8210, 200],
                                       [9210, 330],
                                       [10040, 530],
                                       [10870, 530]
                                       ]
        for coordinate in platform_B_coordinate_array:
            block = platform_B()
            block.rect.x = coordinate[0]
            block.rect.y = coordinate[1]
            block.player = self.player
            self.platform_list.add(block)

        platform_C_coordinate_array = [[1500, 270],
                                       [1700, 300],
                                       ]
        for coordinate in platform_C_coordinate_array:
            block = platform_C()
            block.rect.x = coordinate[0]
            block.rect.y = coordinate[1]
            block.player = self.player
            self.platform_list.add(block)

        platform_D_coordinate_array = [[1120, 290],
                                       [1960, 290],
                                       ]
        for coordinate in platform_D_coordinate_array:
            block = platform_D()
            block.rect.x = coordinate[0]
            block.rect.y = coordinate[1]
            block.player = self.player
            self.platform_list.add(block)

        platform_E_coordinate_array = [[-210, 0], [11500, 0]]
        for coordinate in platform_E_coordinate_array:
            block = platform_E()
            block.rect.x = coordinate[0]
            block.rect.y = coordinate[1]
            block.player = self.player
            self.platform_list.add(block)

        bush_coordinate_array = [[800, 470],
                                 [5440, 470],
                                 [6000, 240],
                                 [6940, 200],
                                 [7000, 280],
                                 [7900, 390],
                                 [8720, 140],
                                 ]
        for coordinate in bush_coordinate_array:
            bush = Bush()
            bush.rect.x = coordinate[0]
            bush.rect.y = coordinate[1]
            bush.player = self.player
            self.platform_list.add(bush)

        tree_A_coordinate_array = [[920, 410],
                                   [8050, 330],
                                   [10040, 410]
                                   ]
        for coordinate in tree_A_coordinate_array:
            tree = tree_A()
            tree.rect.x = coordinate[0]
            tree.rect.y = coordinate[1]
            tree.player = self.player
            self.platform_list.add(tree)

        tree_B_coordinate_array = [[1040, 330],
                                   [9000, 260]]
        for coordinate in tree_B_coordinate_array:
            tree = tree_B()
            tree.rect.x = coordinate[0]
            tree.rect.y = coordinate[1]
            tree.player = self.player
            self.platform_list.add(tree)

        # Add exit
        exit_01 = Exit()
        exit_01.rect.x = 11430
        exit_01.rect.y = 460
        self.exit_list.add(exit_01)

        # Add first respawn point
        respawn_01 = RespawnPoint(70, 70)
        respawn_01.rect.x = 0
        respawn_01.rect.y = 470
        self.respawn_point = respawn_01
        self.respawn_list.add(respawn_01)

        # Add respawn controller for when the player gets halfway through the level
        respawn_02 = RespawnController(40, 200)
        respawn_02.rect.x = 5370
        respawn_02.rect.y = 330
        self.respawn_controller = respawn_02
        self.respawn_controller_list.add(respawn_02)

        # Wind trigger volumes - pass in width, height, x, y
        wind_trigger_array = [[60, 300, 2740, 230],
                              [60, 300, 5440, 170]]
        for trigger in wind_trigger_array:
            volume = WindTriggerVolume(trigger[0], trigger[1])
            volume.rect.x = trigger[2]
            volume.rect.y = trigger[3]
            self.wind_trigger_list.add(volume)

        # Wind end volumes - pass in width, height, x, y
        wind_end_array = [[60, 300, 4870, 230],
                          [60, 300, 10550, 290]
                          ]
        for trigger in wind_end_array:
            volume = WindEndTriggerVolume(trigger[0], trigger[1])
            volume.rect.x = trigger[2]
            volume.rect.y = trigger[3]
            self.wind_end_trigger_list.add(volume)
# ----------------------------------------------------------------------------------------------------------------------


# Create platforms for the level
class Level_02(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 60, 570]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add demo exit
        exit_02 = Exit()
        exit_02.rect.x = 270
        exit_02.rect.y = 500
        self.exit_list.add(exit_02)
