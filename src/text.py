import pygame

class Text:
    def __init__(self, fontSize: int, shadow: bool = False):
        self.font: pygame.font.Font = pygame.font.Font(None, fontSize)
        self.shadow: bool = shadow
    
    def Draw(self, surface: pygame.Surface, text: str, position: pygame.Vector2, color: pygame.Color = pygame.Color(255, 255, 255)):
        if self.shadow:
            textSurfaceShadow: pygame.Surface = self.font.render(text, False, (30, 30, 30))
            SHADOW_OFFSET: int = 2
            surface.blit(textSurfaceShadow, pygame.Vector2(position.x + SHADOW_OFFSET, position.y + SHADOW_OFFSET))

        textSurface: pygame.Surface = self.font.render(text, False, color)
        surface.blit(textSurface, position)

def DrawDebugText(surface: pygame.Surface, font: pygame.font.Font, text: str, position: pygame.Vector2):
    textSurface: pygame.Surface = font.render(text, False, pygame.Color(255, 255, 255))
    surface.blit(textSurface, position)
