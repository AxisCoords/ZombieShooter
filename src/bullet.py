import pygame
import src.globals

class Bullet():
    def __init__(self, pos) -> None:
        self.pos = pos

        self.rect = pygame.Rect(pos.x, pos.y, 10, 4)

    def Update(self, delta: float) -> None:
        SPEED: float = 480.0
        self.pos.x += SPEED * delta
        self.rect.x = self.pos.x

    def CheckCollision(self, zombieRect: pygame.Rect) -> bool:
        if self.rect.colliderect(zombieRect):
            return True
        return False

    def Draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, pygame.Color(255, 255, 255), self.rect)

        if src.globals.isDebugVisible:
            pygame.draw.rect(surface, pygame.Color(255, 0, 0), self.rect, 1)
