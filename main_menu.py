# Imports --------------------------------------------------------------------------------------------------------------
import pygame
import constants
import ptext
# --------------------------------------------------------------------------------------------------------------------//

menu_text = """
Depths of the Mind

Main Menu:
W - New Game
Space - Resume game from file

Instructions:
Left/right arrows - move character
Tap right arrow - fight against the wind
Up arrow - jump
Escape key - quit game
"""


def main_menu(screen):
    background = pygame.image.load("background.png").convert()
    screen.blit(background, [0, 0])
    ptext.draw(menu_text, (250, 180), color=constants.WHITE, align="center")
    pygame.display.update()

    # Check the player's save file
    file = open('save file.txt', 'r')
    level = int(file.readline())
    file.close()

    start = False
    while start is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    level = 0
                    file = open('save file.txt', 'w')
                    file.write(str(level))
                    file.close()
                    return level
                if event.key == pygame.K_SPACE:
                    return level
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play()
        pygame.display.update()
