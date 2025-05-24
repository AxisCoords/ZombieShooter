import pygame
from math import sin
from src.sprite import Sprite
import src.globals as globals

class BulletDrop(Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pygame.image.load(globals.SPRITE_IMAGE).convert_alpha(), pos, globals.SPRITE_SIZE)
        self.frame = pygame.Rect(48, 0, 16, 16)
    
    def Update(self, delta: float) -> None:
        self.pos.y += sin(pygame.time.get_ticks() * 0.005) * 0.5
    
    def CheckCollision(self, playerRect: pygame.Rect) -> bool:
        if self.rect.colliderect(playerRect):
            return True
        return False
