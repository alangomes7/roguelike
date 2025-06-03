import pgzrun
import random
from pygame import Rect

# === Configurações do Game ===
WIDTH = 1280
HEIGHT = 720
TITLE = "Roguelike Adventure"
TILE_SIZE = 64

# === Estados do Game ===
MENU = 0
GAME = 1
game_state = MENU
game_win = False

# === Configurações de audio ===
music_on = False
sound_on = False

# === Cores ===
BACKGROUND_COLOR = (30, 30, 60)
TITLE_COLOR = (255, 215, 0)  # Gold
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)
GAME_BG_COLOR = (20, 20, 40)

# === Classe de botões ===
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = Rect((x - width/2, y - height/2), (width, height))
        self.text = text
        self.action = action
        self.is_hovered = False
    
    def draw(self):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color=TEXT_COLOR)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def click(self):
        if self.action:
            self.action()

# === Classe Herói (Hero) ===
class Hero:
    def __init__(self):
        self.actor = Actor('kenney_tiny-dungeon/tiles/tile_0085')
        self.sword = Actor('kenney_tiny-dungeon/tiles/tile_0104')
        self.actor.pos = (WIDTH // 2, HEIGHT // 2)
        self.sword.pos = (self.actor.x + 20, self.actor.y)
        self.sword_angle = 0
        self.health = 100
        self.attack = 10
        self.defense = 5
    
    def draw(self):
        self.actor.draw()
        self.sword.angle = self.sword_angle
        self.sword.draw()

        # Barra de saúde
        screen.draw.filled_rect(Rect((self.actor.x - 32, self.actor.y - 50), (64, 10)), (255, 0, 0))
        screen.draw.filled_rect(Rect((self.actor.x - 32, self.actor.y - 50), (64 * (self.health / 100), 10)), (0, 255, 0))

    def draw_info(self):
        screen.draw.text(f"Health: {self.health}", topleft=(20, 20), fontsize=30, color="white")

# === Botões ===
buttons = [
    Button(WIDTH/2, HEIGHT/2 - 60, 300, 60, "Start Game", lambda: start_game()),
    Button(WIDTH/2, HEIGHT/2 + 30, 300, 60, f"Music: {'ON' if music_on else 'OFF'}", lambda: toggle_music()),
    Button(WIDTH/2, HEIGHT/2 + 120, 300, 60, f"Sound: {'ON' if sound_on else 'OFF'}", lambda: toggle_sounds()),
    Button(WIDTH/2, HEIGHT/2 + 210, 300, 60, "Quit", lambda: exit_game())
]

# === Objetos do Game ===
hero = None
enemies = []
walls = []
life_chargers = []
crubs = []
crub_speed = 0.2
enemy_speed = 0.1
hero_speed = 0.9
sword_direction = "right"

# === Estado do Game ===
def start_game():
    global game_state
    game_state = GAME
    init_game()

def toggle_music():
    global music_on
    music_on = not music_on
    buttons[1].text = f"Music: {'ON' if music_on else 'OFF'}"

def toggle_sounds():
    global sound_on
    sound_on = not sound_on
    buttons[2].text = f"Sound: {'ON' if sound_on else 'OFF'}"

def exit_game():
    print("Quitting game...")
    exit()

# === Iniciatilização do Game ===
def init_game():
    global hero, enemies, walls, life_chargers, crubs
    hero = Hero()

    # Gerador aleatório de elementos
    walls = [Actor('kenney_tiny-dungeon/tiles/tile_0031', (random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(20)]
    enemies = [Actor('kenney_tiny-dungeon/tiles/tile_0121', (random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(5)]
    life_chargers = [Actor('kenney_tiny-dungeon/tiles/tile_0115', (random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(5)]
    crubs = [Actor('kenney_tiny-dungeon/tiles/tile_0110', (random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(10)]

# === Funções de desenho ===
def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    screen.draw.text("ROGUELIKE", center=(WIDTH/2 + 5, HEIGHT/4 + 5), fontsize=100, color=(0, 0, 0))
    screen.draw.text("ROGUELIKE", center=(WIDTH/2, HEIGHT/4), fontsize=100, color=TITLE_COLOR)
    for button in buttons:
        button.draw()

def draw_game():
    screen.fill(GAME_BG_COLOR)
    for wall in walls: wall.draw()
    for enemy in enemies: enemy.draw()
    for life_charger in life_chargers: life_charger.draw()
    for crub in crubs: crub.draw()
    hero.draw()
    hero.draw_info()

# === Comandos de entrada ===
def on_mouse_move(pos):
    if game_state == MENU:
        for button in buttons:
            button.check_hover(pos)

def on_mouse_down(pos):
    if game_state == MENU:
        for button in buttons:
            if button.is_hovered:
                button.click()

def on_key_down(key):
    if game_state == GAME:
        speed = 15
        if key == keys.UP: hero.actor.y -= speed
        if key == keys.DOWN: hero.actor.y += speed
        if key == keys.LEFT: hero.actor.x -= speed
        if key == keys.RIGHT: hero.actor.x += speed
        hero.actor.x = max(32, min(WIDTH - 32, hero.actor.x))
        hero.actor.y = max(32, min(HEIGHT - 32, hero.actor.y))

# === Lógica de atualização ===
def update():
    global game_win, crub_speed, enemy_speed, hero_speed, sword_direction

    if game_state == GAME:
        # Enemy movement (persiga o heroi)
        if not game_win:
            for enemy in enemies:
                if enemy.x < hero.actor.x:
                    enemy.x += enemy_speed
                elif enemy.x > hero.actor.x:
                    enemy.x -= enemy_speed
                if enemy.y < hero.actor.y:
                    enemy.y += enemy_speed
                elif enemy.y > hero.actor.y:
                    enemy.y -= enemy_speed

            # Crab movement (fuja do heroi)
            for crub in crubs:
                dx = crub.x - hero.actor.x
                dy = crub.y - hero.actor.y
                
                distance = max(1, (dx**2 + dy**2)**0.5)
                dx /= distance
                dy /= distance
                
                crub.x += dx * crub_speed
                crub.y += dy * crub_speed
                
                # Manter nos limites da tela
                crub.x = max(32, min(WIDTH - 32, crub.x))
                crub.y = max(32, min(HEIGHT - 32, crub.y))
        else:
            # Depois da vitória
            for enemy in enemies:
                enemy.x += random.randint(-1, 1)
                enemy.y += random.randint(-1, 1)
                
                # Manter nos limites da tela
                enemy.x = max(32, min(WIDTH - 32, enemy.x))
                enemy.y = max(32, min(HEIGHT - 32, enemy.y))
        
        if keyboard.left: hero.actor.x -= hero_speed; sword_direction = "left"
        elif keyboard.right: hero.actor.x += hero_speed; sword_direction = "right"
        elif keyboard.up: hero.actor.y -= hero_speed; sword_direction = "up"
        elif keyboard.down: hero.actor.y += hero_speed; sword_direction = "down"

        # Position sword relative to movement
        if sword_direction == "right": hero.sword.pos = (hero.actor.x + 20, hero.actor.y)
        elif sword_direction == "left": hero.sword.pos = (hero.actor.x - 20, hero.actor.y)
        elif sword_direction == "up": hero.sword.pos = (hero.actor.x, hero.actor.y - 20)
        elif sword_direction == "down": hero.sword.pos = (hero.actor.x, hero.actor.y + 20)
        hero.sword_angle = (hero.sword_angle + 5) % 360

        check_collisions()

# === Colisões ===
def check_collisions():
    global game_state, game_win, crub_speed, enemy_speed

    for enemy in enemies:
        if abs(enemy.x - hero.actor.x) < 32 and abs(enemy.y - hero.actor.y) < 32:
            hero.health -= 0.1
            if hero.health <= 0:
                game_state = MENU

    for life_charger in life_chargers:
        if abs(life_charger.x - hero.actor.x) < 32 and abs(life_charger.y - hero.actor.y) < 32:
            hero.health = min(hero.health + 0.1, 100)

    crubs_to_remove = []
    for crub in crubs:
        if abs(crub.x - hero.actor.x) < 32 and abs(crub.y - hero.actor.y) < 32:
            crubs_to_remove.append(crub)
            crub_speed += 0.02
            enemy_speed += 0.01

    for crub in crubs_to_remove:
        crubs.remove(crub)

    if len(crubs) == 0 and not game_win:
        game_win = True
        for i in range(len(enemies)):
            enemies[i] = Actor('kenney_tiny-dungeon/tiles/tile_0099')
            enemies[i].pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

# === Main Game Loop ===
def draw():
    if game_state == MENU:
        draw_menu()
    else:
        draw_game()

# === Executa o Game ===
pgzrun.go()
