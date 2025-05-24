import pygame
import src.globals

class Sprite:
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, scale: float = 1, alpha: float = 255) -> None:
        self.image = image
        self.pos = pos
        self.frame = image.get_rect()
        self.scale = scale
        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self.image.set_alpha(alpha)

    def Draw(self, surface: pygame.Surface, color: pygame.Color = pygame.Color(255, 255, 255, 255)) -> None:
        self.rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, self.frame.width * self.scale, self.frame.height * self.scale)

        framedImage: pygame.Surface = self.image.subsurface(self.frame)
        transformedImage: pygame.Surface = pygame.transform.scale_by(framedImage, self.scale)
        transformedImage.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        
        surface.blit(transformedImage, self.pos)

        if src.globals.isDebugVisible:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
