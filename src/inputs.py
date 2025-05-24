import pygame

def GetVector(positiveKeyX: int, negativeKeyX: int, positiveKeyY: int, negativeKeyY: int) -> pygame.Vector2:
    result = pygame.Vector2(KeyAxis(positiveKeyX, negativeKeyX), KeyAxis(positiveKeyY, negativeKeyY))

    if result.length() > 1: result.normalize_ip()
    
    return result

def KeyAxis(positiveKey: int, negativeKey: int) -> float:
    return GetKey(positiveKey) - GetKey(negativeKey)

def GetKey(key: int) -> bool:
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True
    
    return False

def KeyEventRegistered(events: pygame.Event, inputType: int, key : int) -> bool:
    for e in events:
        if e.type == inputType and e.key == key:
            return True
    
    return False

def DefaultExitEvent(events: pygame.Event) -> bool:
    for e in events:
        if e.type == pygame.QUIT:
            return True
    
    return False
