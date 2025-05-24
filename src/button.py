import pygame

class Button:
    def __init__(self, text: str, rect: pygame.Rect, color: pygame.Color, hoverColor: pygame.Color) -> None:
        self.text: str = text
        self.rect: pygame.Rect = rect
        self.color: pygame.Color = color
        self.hoverColor: pygame.Color = hoverColor

    def Draw(self, surface: pygame.Surface) -> None:
        currColor: pygame.Color = (0, 0, 0)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            currColor = self.hoverColor
        else:
            currColor = self.color

        pygame.draw.rect(surface, currColor, self.rect)

        FONT = pygame.font.Font(None, 32)
        textSurf = FONT.render(self.text, False, (255, 255, 255))
        textRect = textSurf.get_rect(center=self.rect.center)
        surface.blit(textSurf, textRect)

    def IsClicked(self, events: pygame.event.Event) -> bool:
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    return True
                
        return False
