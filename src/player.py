import pygame
from src.sprite import Sprite
import src.inputs as inputs
from math import sin
import src.globals as globals
import src.inputs as inputs

class Player(Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        Sprite.__init__(self, pygame.image.load(globals.SPRITE_IMAGE).convert_alpha(), pos, globals.SPRITE_SIZE)
        self.frame = pygame.Rect(0, 0, 16, 16)

        self.gun: Sprite = Sprite(pygame.image.load(globals.SPRITE_IMAGE).convert_alpha(), pos, globals.SPRITE_SIZE)
        self.gun.frame = pygame.Rect(32, 0, 16, 16)

        self.GUN_OFFSET: int = 45

    def Update(self, delta: float) -> None:
        SPEED: float = 450.0
        self.inputDir1: pygame.Vector2 = inputs.GetVector(pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP)
        self.inputDir2: pygame.Vector2 = inputs.GetVector(pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_w)

        self.pos.x += sin((self.inputDir1.x + self.inputDir2.x)) * SPEED * delta
        self.pos.y += sin((self.inputDir1.y + self.inputDir2.y)) * SPEED * delta

        self._bounds()

        self.gun.pos = pygame.Vector2(self.pos.x + self.GUN_OFFSET, self.pos.y)
    
    def Shoot(self, events: pygame.Event) -> bool:
        if inputs.KeyEventRegistered(events, pygame.KEYDOWN, pygame.K_SPACE):
            return True
        return False

    def Draw(self, surf: pygame.Surface) -> None:
        Sprite.Draw(self, surf)

        self.gun.Draw(surf)

    def _bounds(self) -> None:
        self.pos.x = pygame.math.clamp(self.pos.x, 0, globals.WIDTH - self.frame.right * self.scale)
        self.pos.y = pygame.math.clamp(self.pos.y, 0, globals.HEIGHT - self.frame.bottom * self.scale)
