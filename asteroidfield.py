import pygame
import random
from asteroid import Asteroid
from constants import *
from hanzi_db import HANZI_DB
from hanzi import Hanzi


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity, hanzi_soul):
        asteroid = Asteroid(position.x, position.y, radius, hanzi_soul)
        asteroid.velocity = velocity

    def update(self, dt):
        # 0. The clock must tick!
        self.spawn_timer += dt

        # 1. Gatekeeper: don't count if at capacity
        if len(self.asteroids_group) >= MAX_ASTEROIDS:
            return
        
        #2. Check if time to spawn:
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # 3. Preparation: Pick the Edge and Velocity
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))

            # 4. Selection: Pick the Hanzi Soul
            char_key = random.choice(list(HANZI_DB.keys()))
            data = HANZI_DB[char_key]
            new_soul = Hanzi(char=char_key, **data)

            # 5. Action: Spawn the physical body with its soul
            # (Note: we use a fixed radius now, no more 'kind')
            self.spawn(ASTEROID_MIN_RADIUS * 2, position, velocity, new_soul)

