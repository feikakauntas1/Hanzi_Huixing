import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TONE_COLORS, PURPLE
from logger import log_state, log_event
from circleshape import CircleShape
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from assets import GAME_FONT


RULE_POSITIONS = [
    (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 300), # Middle Right
    (50, SCREEN_HEIGHT - 300),                # Middle Left
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  # Bottom Center
]
rule_pos_index = 0

def get_rule_text(rule):
    # Colors: Initials = Purple, Finals = Brown
    rule_type, value = rule
    if rule_type == "tone":
        return "射击第", f"{value}", "声的字", TONE_COLORS[value]
    if rule_type == "initial":
        return "射击声母为", f"{value}", "的字", "purple"
    if rule_type == "final":
        return "射击韵母为", f"{value}", "的字", "brown"
    return "Target:", f"{value}", "", "white"

def is_correct(hanzi, rule):
    rule_type, target_value = rule
    if rule_type == "tone":
        return hanzi.tone == target_value
    if rule_type == "initial":
        return hanzi.initial == target_value
    if rule_type == "final":
        return hanzi.final == target_value
    return False

def main():
    pygame.init()
    ui_opaque = True # Start with clean, opaque UI
    pygame.font.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    asteroid_field.asteroids_group = asteroids # Hand the group to the field
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    score = 0
    ui_opaque = True
    current_rule = ("tone", 3) # Let's start with Tone 3
    last_score = -1
    last_rule = None
    rule_pos_index = 0  # <--- Move it here!
    ui_opaque = True
    current_rule = ("tone", 3)
    score_surf = None
    rule_surf = None

    #game loop
    while True:
        # log_state()  <-- Commented out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                # Toggle UI with the 'U' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    ui_opaque = not ui_opaque
                if event.key == pygame.K_SPACE:
                    player.shoot()
        screen.fill("black")
        updatable.update(dt)
        # main.py loop
# ...
        for a in asteroids:
            if a.is_dying: continue # Skip if already popping
            
            for s in shots:
                if a.collides_with(s):
                    s.kill()
                    a.is_dying = True
                    a.death_timer = 0.6 # 600ms display
                    
                    # HARDCODED RULE TEST: TONE 3
                    if is_correct(a.hanzi, current_rule):
                        score += 100
                        a.was_correct = True
                    else:
                        score = max(0, score - 50) 
                        a.was_correct = False
        for obj in drawable:
            obj.draw(screen)


                # === UI SECTION START ===
        if score != last_score:
            # Padded 8-digit score
            score_surf = GAME_FONT.render(f"SCORE {score:08}", True, "white")
            last_score = score
            
        if current_rule != last_rule:
            prefix, val, suffix, color = get_rule_text(current_rule)
            p_surf = GAME_FONT.render(prefix, True, "white")
            v_surf = GAME_FONT.render(val, True, color)
            s_surf = GAME_FONT.render(suffix, True, "white")
            
            w = p_surf.get_width() + v_surf.get_width() + s_surf.get_width()
            h = p_surf.get_height()
            rule_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            rule_surf.blit(p_surf, (0, 0))
            rule_surf.blit(v_surf, (p_surf.get_width(), 0))
            rule_surf.blit(s_surf, (p_surf.get_width() + v_surf.get_width(), 0))
            
            rule_pos_index = (rule_pos_index + 1) % len(RULE_POSITIONS)
            last_rule = current_rule

        score_rect = score_surf.get_rect(topleft=(20, 20))
        target_pos = RULE_POSITIONS[rule_pos_index]
        
        # Safe anchoring logic
        if target_pos[0] > SCREEN_WIDTH // 2:
            rule_text_rect = rule_surf.get_rect(midright=target_pos)
        elif target_pos[0] < SCREEN_WIDTH // 2:
            rule_text_rect = rule_surf.get_rect(midleft=target_pos)
        else:
            rule_text_rect = rule_surf.get_rect(midbottom=target_pos)
            
        rule_box_rect = rule_text_rect.inflate(40, 20)

        if ui_opaque:
            pygame.draw.rect(screen, "black", score_rect.inflate(10, 5))
            pygame.draw.rect(screen, "black", rule_box_rect)
            pygame.draw.rect(screen, "white", rule_box_rect, 4)

        screen.blit(score_surf, score_rect)
        screen.blit(rule_surf, rule_text_rect)
        # === UI SECTION END ===

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
