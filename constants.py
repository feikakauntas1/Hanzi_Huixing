SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 500
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 1000 
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.0
MAX_ASTEROIDS = 10
# Keep the character and its specific data bound together!
TEST_HANZI = [
    {"char": "马", "pinyin": "mǎ", "tone": 3},
    {"char": "学", "pinyin": "xué", "tone": 2},
    {"char": "九", "pinyin": "jiǔ", "tone": 3},
]

# The RGB Tuples
RED    = (255, 60, 60)
ORANGE = (255, 165, 0)
GREEN  = (60, 255, 60)
BLUE   = (60, 160, 255)
PURPLE = (180, 60, 255)

# The Mapping (Your Dictionary)
TONE_COLORS = {
    1: RED,
    2: ORANGE,
    3: GREEN,
    4: BLUE,
    5: PURPLE
}
