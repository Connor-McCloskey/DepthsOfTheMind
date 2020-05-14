"""
Connor McCloskey
CSC 200
Final Project
"""

# Imports --------------------------------------------------------------------------------------------------------------
import pygame
from pygame_functions import *
import constants
import player_class
import level_class
import cutscenes
import main_menu
# --------------------------------------------------------------------------------------------------------------------//


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    pygame.display.set_caption("Depths of the Mind")
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

# New material ---------------------------------------------------------------------------------------------------------
    # New - ambient music
    pygame.mixer.music.load("RPG Ambient 3.mp3")
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()

    # New - main menu
    player_save_level = main_menu.main_menu(screen)
    if player_save_level == 0:
        cutscenes.cutscene(screen, 0)
# ----------------------------------------------------------------------------------------------------------------------

    # Create the player
    player = player_class.Player()

    # New - Load the background-----------------------------------------------------------------------------------------
    background = pygame.image.load("background.png").convert()
    # ------------------------------------------------------------------------------------------------------------------

    # Create all the levels
    level_list = []
    level_list.append(level_class.Level_01(player))
    level_list.append(level_class.Level_02(player))

    # Set the current level
    current_level_no = player_save_level
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 60
    player.rect.y = 490

    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

# New material ---------------------------------------------------------------------------------------------------------
    # NEW - wind tick
    wind_tick_default = 180
    wind_tick = wind_tick_default

    # New - wind timer
    wind_timer_default = 300
    wind_timer = wind_timer_default

    # New - load sound effects
    exit_sound = pygame.mixer.Sound("exit.wav")
    reboot_sound = pygame.mixer.Sound("reboot.wav")
    wind_sound = pygame.mixer.Sound("wind.wav")
# ----------------------------------------------------------------------------------------------------------------------
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        """
        Wind mechanic
        If player_wind_influence is True, the player has collided with a trigger volume to start the wind
        So, we need to start the wind in that gameplay section, as well as two timers - time between gusts, and
        how long the wind itself should last
        """
        if player.player_wind_influence is True:
            wind_timer -= 1
            if wind_timer == 60:
                wind_sound.play()
            if wind_timer <= 0:
                player.calc_wind()
                wind_tick -= 1
                if wind_tick == 0:
                    wind_tick = 180
                    wind_timer = 300
                    wind_sound.fadeout(1000)
        if player.player_wind_influence is False:
            wind_timer = wind_timer_default
            wind_tick = wind_tick_default

        # New - draw the background
        screen.blit(background, [0, 0])

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # NEW / adapted
        # If the player gets to the level exit, go to the next level
        if player.player_hit_exit is True:
            exit_sound.play()
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                file = open('save file.txt', 'w')
                file.write(str(current_level_no))
                file.close()
                player.rect.x = 60
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                current_level_no = 2

        # New - "respawning" player from a fall. Check if rect.y coordinate of player sprite
        # exceeds screen height
        if player.rect.y > 600:
            reboot_sound.play()
            player.rect.x = current_level.respawn_point.rect.x
            player.rect.y = current_level.respawn_point.rect.y
            player.player_wind_influence = False
            player.stop()
            wind_sound.fadeout(1000)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # New - check to see if player has hit the exit. If so, play a cutscene. Otherwise, draw as normal.
        if player.player_hit_exit is True:
            player.stop()
            pygame.event.clear()
            player.player_hit_exit = False
            cutscenes.cutscene(screen, current_level_no)
        else:
            current_level.draw(screen)
            active_sprite_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()
