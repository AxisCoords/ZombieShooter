import pygame
from sys import exit

class Display:
    def __init__(self) -> None:
        pygame.init()

        self.FPS_CAP = 120

        self.clock: pygame.Clock = pygame.time.Clock()

    def InitDisplay(self, width: int, height: int, title: str) -> pygame.Surface:
        pygame.display.set_caption(title)
        self.win: pygame.Surface = pygame.display.set_mode((width, height), vsync=1)

        return self.win
    
    def Clear(self, color: pygame.Color) -> None:
        self.win.fill(color)
    
    def Update(self) -> None:
        pygame.display.update()
        self.clock.tick(self.FPS_CAP)
    
    def Destroy(self) -> None:
        pygame.quit()
        exit()
