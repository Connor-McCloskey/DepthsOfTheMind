# Imports --------------------------------------------------------------------------------------------------------------
import pygame
import constants
# --------------------------------------------------------------------------------------------------------------------//


class Player(pygame.sprite.Sprite):

# New - bool variables to track if the player is under the wind influence and if they've hit the end of the level ------
    player_hit_exit = False
    player_wind_influence = False
    jump_sound = pygame.mixer.Sound("jump_01.wav")

# ----------------------------------------------------------------------------------------------------------------------

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Remove all this, no longer needed
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # width = 40
        # height = 40

        # player image
        self.image = pygame.image.load("player.png").convert()

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """

        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

# NEW Checking to see if the player has hit an exit, a checkpoint, a wind trigger volume, or a wind end trigger volume -
        exit_hit_list = pygame.sprite.spritecollide(self, self.level.exit_list, False)
        for lvl_exit in exit_hit_list:
            self.player_hit_exit = True

        wind_trigger_collision_list = pygame.sprite.spritecollide(self, self.level.wind_trigger_list, False)
        for wind_trigger in wind_trigger_collision_list:
            self.player_wind_influence = True

        wind_end_collision_list = pygame.sprite.spritecollide(self, self.level.wind_end_trigger_list, False)
        for volume in wind_end_collision_list:
            self.player_wind_influence = False

        checkpoints = pygame.sprite.spritecollide(self, self.level.respawn_controller_list, False)
        for point in checkpoints:
            self.level.respawn_point = self.level.respawn_controller
# ----------------------------------------------------------------------------------------------------------------------
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. Updated to reflect their is no "floor" at the bottom of the screen """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

# NEW Wind mechanic - basically we can just take the gravity calculations and apply them to the X axis -----------------
    def calc_wind(self):
        """Calculate wind"""
        if self.change_x == 0:
            self.change_x = -0.35
        else:
            self.change_x -= 0.35
# ----------------------------------------------------------------------------------------------------------------------

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10
            self.jump_sound.play()

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
