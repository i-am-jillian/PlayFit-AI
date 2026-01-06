import pygame
from actions import Actions

GRAVITY = 2
JUMP_VELOCITY = -30
FLOOR_TOP_Y = 310

class Fighter():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect(x, y, 130, 180)
        self.speed = 10
        self.vel_y = 0
        self.attack_type = 0  # 0: no attack, 1: punch, 2: kick
        self.attacking = False
        self.attack_timer = 0
        self.health = 100
        self.hit_applied = False
        
        #images
        self.idle_img = pygame.image.load("assets/sprites/Fighter1/Shinchan-idle.png").convert_alpha()
        self.idle_img = pygame.transform.scale(self.idle_img, (130, 180))

        self.punch_img = pygame.image.load("assets/sprites/Fighter1/Shinchan-punch.png").convert_alpha()
        self.punch_img = pygame.transform.scale(self.punch_img, (130, 180))
        
        self.kick_img = pygame.image.load("assets/sprites/Fighter1/Shinchan-kick.png").convert_alpha()
        self.kick_img = pygame.transform.scale(self.kick_img, (130, 180))



    def movey(self, actions: Actions):
        if self.attacking == False:
            # Apply gravity
            onGround = self.rect.y >= FLOOR_TOP_Y
            if actions.jump and onGround:
                self.vel_y = JUMP_VELOCITY
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            # Prevent falling below the floor
            if self.rect.y > FLOOR_TOP_Y:
                self.rect.y = FLOOR_TOP_Y
                self.vel_y = 0

    def movex(self, actions: Actions, target):
        if self.attacking == False:
            self.rect.x += actions.movex * self.speed
        
            # Keep fighter within screen bounds
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > 1000:
                self.rect.right = 1000
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > 600:
                self.rect.bottom = 600

            #ensure players face each other
            #if target.rect.centerx > self.rect.centerx:
            #    self.flip = False
            #else:
             #   self.flip = True

            if actions.movex > 0:
                self.flip = False
            elif actions.movex < 0:
                self.flip = True

    def attack(self, surface, target):
        if not self.attacking:
            return
        
        # Define attack hitbox
        hitbox_width = 2
        hitbox_height = 60

        if self.flip:
            hitbox_x = self.rect.left - hitbox_width
        else:
            hitbox_x = self.rect.right
        
        attacking_rect = pygame.Rect(
            hitbox_x,
            self.rect.y + self.rect.height // 4,
            hitbox_width,
            hitbox_height
        )
        if attacking_rect.colliderect(target.rect) and not self.hit_applied:
            target.health -= 10
            target.health = max(0, target.health)
            self.hit_applied = True

        #pygame.draw.rect(surface, (0, 255, 0), attacking_rect, 2)

    def handle_attack(self, actions: Actions):
        #if already attacking, count down
        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.attacking = True
            return
        
        #start new attack
        if actions.punch:
            self.attack_type = 1
            self.attack_timer = 12
            self.attacking = True
            self.hit_applied = False
        elif actions.kick:
            self.attack_type = 2
            self.attack_timer = 16
            self.attacking = True
            self.hit_applied = False 
        else:
            self.attack_type = 0
            self.attacking = False

    def draw(self, surface):
        if self.attacking:
            if self.attack_type == 1:
                image = self.punch_img
            elif self.attack_type == 2:
                image = self.kick_img
            else:
                image = self.idle_img
        else:
            image = self.idle_img

        if self.flip:
            image = pygame.transform.flip(image, True, False)
        
        surface.blit(image, self.rect)