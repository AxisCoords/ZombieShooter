import pygame
from src.windowManager import Display
from src import inputs as input
from src.player import Player
from src.zombie import Zombie
from src.bullet import Bullet
from src.bulletDrop import BulletDrop
from src.text import Text
from src.button import Button
import random, json
import src.text as text
import src.globals

pygame.mixer.init()
win: Display = Display()
renderSurf: pygame.Surface = win.InitDisplay(src.globals.WIDTH, src.globals.HEIGHT, src.globals.TITLE)

dataObj: dict[str, int] = {
    "highscore": 0
}

# Load highscore
try:
    with open("data.json", "r") as file:
        dataObj = json.load(file)
except:
    with open("data.json", "w") as file:
        json.dump(dataObj, file, indent=4)

# Global state variables
windowShouldClose: bool = False
paused: bool = False
score: int = 0
ZOMBIE_CROSS_LIMIT: int = 5
bulletCounter: int = 0
zombiesCrossed: int = 0

# Load sound effects
shootSound = pygame.mixer.Sound("assets/shoot.wav")
zombieHitSound = pygame.mixer.Sound("assets/hurt.wav")
bulletPickupSound = pygame.mixer.Sound("assets/pickup.wav")

# GUI Text elements
deathScreenScoreText: Text = Text(32, True)
deathScreenHighScoreText: Text = Text(32, True)
scoreText: Text = Text(25, True)
bulletCounterText: Text = Text(25, True)
zombiesCrossedText: Text = Text(25, True)

# Game objects
zombies: list[Zombie] = []
zombiesToRemove: set[Zombie] = set()
for _ in range(5):
    y = random.randint(0, src.globals.HEIGHT - 16 * src.globals.SPRITE_SIZE)
    zombies.append(Zombie(pygame.Vector2(src.globals.WIDTH, y)))

bullets: list[Bullet] = []
bulletsToRemove: set[Bullet] = set()

bulletDrops: list[BulletDrop] = []
bulletDropsToRemove: set[BulletDrop] = set()
for _ in range(5):
    x = random.randint(0, src.globals.WIDTH - 16 * src.globals.SPRITE_SIZE)
    y = random.randint(0, src.globals.HEIGHT - 16 * src.globals.SPRITE_SIZE)
    bulletDrops.append(BulletDrop(pygame.Vector2(x, y)))

player: Player = Player(pygame.Vector2(0, 0))
player.pos = pygame.Vector2((src.globals.WIDTH - player.frame.width * player.scale) / 2, (src.globals.HEIGHT - player.frame.height * player.scale) / 2)

# Game loop
while not windowShouldClose:
    win.Clear(pygame.Color(0, 0, 0))
    delta: float = win.clock.tick(120) / 1000

    if score > dataObj["highscore"]:
        dataObj["highscore"] = score

    if zombiesCrossed >= ZOMBIE_CROSS_LIMIT:
        src.globals.gameOver = True
        paused = True

    if not paused and random.randint(0, int(1 / delta)) == 0:
        y = random.randint(0, src.globals.HEIGHT - 16 * src.globals.SPRITE_SIZE)
        zombies.append(Zombie(pygame.Vector2(src.globals.WIDTH, y)))

    # Input handling
    events: list[pygame.Event] = pygame.event.get()
    if input.DefaultExitEvent(events): windowShouldClose = True
    if not src.globals.gameOver and input.KeyEventRegistered(events, pygame.KEYUP, pygame.K_ESCAPE): paused = not paused
    if input.KeyEventRegistered(events, pygame.KEYDOWN, pygame.K_F3): src.globals.isDebugVisible = not src.globals.isDebugVisible

    # Update game logic
    if not paused:
        player.Update(delta)
        # Shoot
        if player.Shoot(events) and bulletCounter > 0:
            shootSound.play()
            bulletCounter -= 1
            bullets.append(Bullet(pygame.Vector2(player.pos.x + player.GUN_OFFSET + 12 * player.scale, player.pos.y + 4 * player.scale)))

        for bullet in bullets:
            bullet.Update(delta)
            for zombie in zombies:
                # Zombie kill
                if bullet.CheckCollision(zombie.rect):
                    zombieHitSound.play()
                    zombiesToRemove.add(zombie)
                    bulletsToRemove.add(bullet)
                    score += 1

        for zombie in zombies:
            zombie.Update(delta)
            if zombie.IsGoalReached():
                zombiesCrossed += 1
                zombiesToRemove.add(zombie)

        # Add bullet
        for bulletDrop in bulletDrops:
            if bulletDrop.CheckCollision(player.rect):
                bulletPickupSound.play()
                bulletDropsToRemove.add(bulletDrop)
                bulletCounter += 1
            else:
                bulletDrop.Update(delta)

    # Remove zombies
    newZombies = []
    for z in zombies:
        if z not in zombiesToRemove:
            newZombies.append(z)
        else:
            bulletDrops.append(BulletDrop(z.pos))
    zombies = newZombies
    zombiesToRemove.clear()

    # Remove bullets
    newBullets = []
    for b in bullets:
        if b not in bulletsToRemove:
            newBullets.append(b)
    bullets = newBullets
    bulletsToRemove.clear()

    # Remove bullet drops
    newBulletDrops = []
    for bd in bulletDrops:
        if bd not in bulletDropsToRemove:
            newBulletDrops.append(bd)
    bulletDrops = newBulletDrops
    bulletDropsToRemove.clear()

    # Draw game objects
    player.Draw(renderSurf)
    
    for bullet in bullets:
        bullet.Draw(renderSurf)

    for zombie in zombies:
        zombie.Draw(renderSurf)

    for bulletDrop in bulletDrops:
        bulletDrop.Draw(renderSurf)

    # Draw UI text
    scoreText.Draw(renderSurf, f"Score: {score}", pygame.Vector2(5, 5))
    bulletCounterText.Draw(renderSurf, f"Bullets: {bulletCounter}", pygame.Vector2(5, 24))
    zombiesCrossedText.Draw(renderSurf, f"Zombies Crossed: {zombiesCrossed}/{ZOMBIE_CROSS_LIMIT}", pygame.Vector2(5, 43))

    # Debug drawing
    if src.globals.isDebugVisible:
        pygame.draw.line(renderSurf, pygame.Color(255, 0, 0), (0, src.globals.HEIGHT / 2), (src.globals.WIDTH, src.globals.HEIGHT / 2))
        pygame.draw.line(renderSurf, pygame.Color(0, 255, 0), (src.globals.WIDTH / 2, 0), (src.globals.WIDTH / 2, src.globals.HEIGHT))
        text.DrawDebugText(renderSurf, pygame.font.Font(None, 24), f"FPS: {int(win.clock.get_fps())}", pygame.Vector2(5, 64))

    # Death screen
    if src.globals.gameOver:
        pygame.draw.rect(renderSurf, pygame.Color(0, 0, 0), pygame.Rect(0, 0, src.globals.WIDTH, src.globals.HEIGHT))
        button: Button = Button("RESTART", pygame.Rect((src.globals.WIDTH - 200) / 2, (src.globals.HEIGHT - 40) / 2, 200, 40), pygame.Color(40, 40, 40), pygame.Color(110, 110, 110))
        button.Draw(renderSurf)

        deathScreenScoreText.Draw(renderSurf, f"SCORE: {score}", pygame.Vector2(src.globals.WIDTH / 2 - 80, 80))
        deathScreenHighScoreText.Draw(renderSurf, f"HIGH SCORE: {dataObj['highscore']}", pygame.Vector2(src.globals.WIDTH / 2 - 80, 120))

        if button.IsClicked(events):
            # Reset game state
            src.globals.gameOver = False
            zombies.clear()
            zombiesToRemove.clear()
            bullets.clear()
            bulletsToRemove.clear()
            bulletDrops.clear()
            bulletDropsToRemove.clear()
            zombiesCrossed = 0
            bulletCounter = 0
            score = 0
            paused = False
            player.pos = pygame.Vector2((src.globals.WIDTH - player.frame.width * player.scale) / 2, (src.globals.HEIGHT - player.frame.height * player.scale) / 2)

            for _ in range(5):
                x = random.randint(0, src.globals.WIDTH - 16 * src.globals.SPRITE_SIZE)
                y = random.randint(0, src.globals.HEIGHT - 16 * src.globals.SPRITE_SIZE)
                bulletDrops.append(BulletDrop(pygame.Vector2(x, y)))

    win.Update()

# Save highscore on exit
with open("data.json", "w") as file:
    json.dump(dataObj, file, indent=4)

win.Destroy()
