import pygame
import math
import os, sys
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = "."
    return base_path + "/" + path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ZONE_COLOR = (255, 0, 255) 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.init()
gun_sound = pygame.mixer.Sound(resource_path("gun.wav"))
pygame.display.set_caption("2 Player Battle Royale - Rapid Fire Mode- by Fardin Khan")
clock = pygame.time.Clock()


def load_image(file_name, width, height, fallback_color):
    try:
        img = pygame.image.load(resource_path(file_name)).convert_alpha()
        img = pygame.transform.scale(img, (width, height))
        return img, True
    except:
        surf = pygame.Surface((width, height))
        surf.fill(fallback_color)
        return surf, False


p1_img, has_p1_img = load_image('p1.png', 40, 40, BLUE)
p2_img, has_p2_img = load_image('p2.png', 40, 40, GREEN)
bullet_img, has_bullet_img = load_image('bullet.png', 10, 10, YELLOW)

#BackGround Logic
BG_IMAGE_NAME = 'bg.png'
BACKGROUND_IMG = None

try:
    if os.path.exists(resource_path(BG_IMAGE_NAME)):
        # image loading
        BACKGROUND_IMG = pygame.image.load(resource_path(BG_IMAGE_NAME)).convert_alpha()
        BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        print("Background image 'bg.png' not found. Using default color.")
except Exception as e:
    print(f"Error loading background image: {e}")
    BACKGROUND_IMG = None


class Bullet:
    def __init__(self, x, y, direction_x, direction_y, owner):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 12 
        self.dx = direction_x
        self.dy = direction_y
        self.owner = owner 

    def move(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, surface):
        if has_bullet_img:
            surface.blit(bullet_img, (self.rect.x, self.rect.y))
        else:
            pygame.draw.ellipse(surface, YELLOW, self.rect)

class Player:
    def __init__(self, x, y, player_id, img, has_img, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.player_id = player_id
        self.img = img
        self.has_img = has_img
        self.color = color
        self.speed = 5
        self.health = 100
        self.bullets = []
        self.last_shot = 0
        self.facing = 'RIGHT' 

    def move(self, keys):
        
        if self.player_id == 1:
            if keys[pygame.K_a]: 
                self.rect.x -= self.speed
                self.facing = 'LEFT'
            if keys[pygame.K_d]: 
                self.rect.x += self.speed
                self.facing = 'RIGHT'
            if keys[pygame.K_w]: 
                self.rect.y -= self.speed
                self.facing = 'UP'
            if keys[pygame.K_s]: 
                self.rect.y += self.speed
                self.facing = 'DOWN'
            
            if keys[pygame.K_SPACE]:
                self.shoot()
                gun_sound.play()

        elif self.player_id == 2:
            if keys[pygame.K_LEFT]: 
                self.rect.x -= self.speed
                self.facing = 'LEFT'
            if keys[pygame.K_RIGHT]: 
                self.rect.x += self.speed
                self.facing = 'RIGHT'
            if keys[pygame.K_UP]: 
                self.rect.y -= self.speed
                self.facing = 'UP'
            if keys[pygame.K_DOWN]: 
                self.rect.y += self.speed
                self.facing = 'DOWN'
            
            if keys[pygame.K_RETURN]: 
                self.shoot()
                gun_sound.play()

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - 40))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - 40))

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > 100: 
            self.last_shot = now
            dx, dy = 0, 0
            if self.facing == 'LEFT': dx = -1
            if self.facing == 'RIGHT': dx = 1
            if self.facing == 'UP': dy = -1
            if self.facing == 'DOWN': dy = 1
            
            if dx == 0 and dy == 0: dx = 1

            b = Bullet(self.rect.centerx, self.rect.centery, dx, dy, self.player_id)
            self.bullets.append(b)

    def draw(self, surface):
        
        current_img = self.img
        
        # if player going to left side then flip the image left
        if self.facing == 'LEFT':
            current_img = pygame.transform.flip(self.img, True, False)

        # if player going to right side then flip the image right
        if self.has_img:
            surface.blit(current_img, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        
        # Health Bar
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, 40, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, 40 * (self.health / 100), 5))

# --- Game Logic ---

p1 = Player(100, 300, 1, p1_img, has_p1_img, BLUE)
p2 = Player(650, 300, 2, p2_img, has_p2_img, GREEN)

zone_radius = 600
zone_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
zone_shrink_speed = 0.2

running = True
winner = None

while running:
    clock.tick(FPS)
    if BACKGROUND_IMG:
        screen.blit(BACKGROUND_IMG, (0, 0))
    else:
        screen.fill(BLACK) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if winner:
        font = pygame.font.Font(None, 74)
        text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
        
        sub_font = pygame.font.Font(None, 36)

        #  Press R to Restart
        sub_text = sub_font.render("Press R to Restart", True, YELLOW)
        screen.blit(sub_text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 20))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]: 
            # restart
            p1.health = 100
            p2.health = 100
            p1.rect.x, p1.rect.y = 100, 300
            p2.rect.x, p2.rect.y = 650, 300
            zone_radius = 600
            winner = None
            p1.bullets = []
            p2.bullets = []
        
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    p1.move(keys)
    p2.move(keys)

    if zone_radius > 50:
        zone_radius -= zone_shrink_speed

    dist_p1 = math.hypot(p1.rect.centerx - zone_center[0], p1.rect.centery - zone_center[1])
    if dist_p1 > zone_radius:
        p1.health -= 0.5 

    dist_p2 = math.hypot(p2.rect.centerx - zone_center[0], p2.rect.centery - zone_center[1])
    if dist_p2 > zone_radius:
        p2.health -= 0.5 

    for b in p1.bullets[:]:
        b.move()
        b.draw(screen)
        if p2.rect.colliderect(b.rect):
            p2.health -= 5 
            p1.bullets.remove(b)
        elif not screen.get_rect().colliderect(b.rect):
            p1.bullets.remove(b)

    for b in p2.bullets[:]:
        b.move()
        b.draw(screen)
        if p1.rect.colliderect(b.rect):
            p1.health -= 5 
            p2.bullets.remove(b)
        elif not screen.get_rect().colliderect(b.rect):
            p2.bullets.remove(b)

    p1.draw(screen)
    p2.draw(screen)

    pygame.draw.circle(screen, ZONE_COLOR, zone_center, int(zone_radius), 2)

    if p1.health <= 0:
        winner = "Player 2"
    if p2.health <= 0:
        winner = "Player 1"

    pygame.display.flip()

pygame.quit()