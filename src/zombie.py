import pygame
from src.sprite import Sprite
import src.globals as globals

class Zombie(Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pygame.image.load(globals.SPRITE_IMAGE).convert_alpha(), pos, globals.SPRITE_SIZE)
        self.frame = pygame.Rect(16, 0, 16, 16)

    def Update(self, delta: float) -> None:
        SPEED: float = 130.0
        self.pos.x -= SPEED * delta
    
    def IsGoalReached(self) -> bool:
        if self.rect.right < 0:
            return True
        return False

    def Draw(self, surface):
        return super().Draw(surface, (255, 0, 0))
