from constants import SHOT_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
import pygame

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y, SHOT_RADIUS)
        self.max_radius=10
        
    def draw(self, screen):
        pygame.draw.circle(screen, "purple", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        if (self.position.x < 0 or self.position.x > SCREEN_WIDTH or 
            self.position.y < 0 or self.position.y > SCREEN_HEIGHT):
            self.kill()

        #increase size after shooting
        if self.radius < self.max_radius:
            growth_speed = 40 
            self.radius += growth_speed * dt
