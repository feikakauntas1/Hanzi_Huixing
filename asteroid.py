from circleshape import CircleShape
import pygame
import random
from logger import log_event
from assets import GAME_FONT
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS, TONE_COLORS

# asteroid.py

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, hanzi_soul):
        super().__init__(x, y, radius)
        self.hanzi = hanzi_soul
        self.wraps_remaining = 2  # Two full passes allowed
        self.is_dying = False
        self.death_timer = 0
        self.was_correct = True

    def update(self, dt):
        # 1. If we are in the "Pinyin Pop" state, just count down
        if self.is_dying:
            self.velocity *= 0.98 # Slows down every frame
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.kill()
            #return? should stop moving

        # 2. Standard movement
        self.position += self.velocity * dt

        # 3. Wrapping Logic
        # We check if the asteroid has gone completely off-screen
        wrapped = False
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
            wrapped = True
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            wrapped = True
            
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
            wrapped = True
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
            wrapped = True

        # 4. Count the wrap!
        if wrapped:
            self.wraps_remaining -= 1
            if self.wraps_remaining < 0:
                # Goodbye! Making room for new spawns.
                self.kill()


    # asteroid.py draw method
    def draw(self, screen):
            if self.is_dying:
            # Show Pinyin in tone color
                color = TONE_COLORS[self.hanzi.tone]
                text_surf = GAME_FONT.render(self.hanzi.pinyin, True, color)
                
                # If it was a mistake, draw a red "Danger" border
                if not self.was_correct:
                    # We use a thick red circle to show it was wrong 
                    # without changing the text color
                    pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius + 5, 4)
            else:
                # Normal Hanzi state
                pygame.draw.circle(screen, "white", self.position, self.radius, 2)
                text_surf = GAME_FONT.render(self.hanzi.char, True, "white")

            rect = text_surf.get_rect(center=self.position)
            screen.blit(text_surf, rect)

    
    def split(self):
        self.kill()
        # For now, just kill it. We will add splitting logic 
        # for radicals in the next hour!
        log_event("asteroid_popped")