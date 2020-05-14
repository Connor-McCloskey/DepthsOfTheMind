# Imports --------------------------------------------------------------------------------------------------------------
import pygame
import constants
import ptext
# --------------------------------------------------------------------------------------------------------------------//


def cutscene(screen, current_level):
    screen.fill(constants.BLACK)
    text = ""
    if current_level == 0:
        file = open('cutscene_0.txt', 'r')
        for line in file:
            text += line
        file.close()
    elif current_level == 1:
        file = open('cutscene_1.txt', 'r')
        for line in file:
            text += line
        file.close()
    elif current_level == 2:
        text = "End of demo. Press escape to quit."
    ptext.draw(text, (10, 10), color=constants.WHITE, width=750, fontsize=21)
    pygame.display.update()

    start = False
    while start is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_level == 2:
                        pygame.quit()
                        quit()
                    else:
                        return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
