import pygame, random, sys, time, math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Very Very Serious Game")

# ------------------ Colors ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 50)

# ------------------ Load images ------------------
bg_home = pygame.image.load("home.png")
bg_choice = pygame.image.load("choice.png")
bg_game = pygame.image.load("game.png")
bg_result = pygame.image.load("result.png")
target_img = pygame.image.load("target.png")
start_img = pygame.image.load("start.png")
easy_img = pygame.image.load("easy.png")
hard_img = pygame.image.load("hard.png")
replay_img = pygame.image.load("replay.png")
end_img = pygame.image.load("end.png")

# ------------------ Sounds ------------------
hitSound = pygame.mixer.Sound("hitsound.wav")
missSound = pygame.mixer.Sound("misssound.wav")
hitSound.set_volume(1)
missSound.set_volume(1)

# ------------------ Parameters ------------------
button_width = int(screen.get_width() * 0.25)
button_height = int(button_width / 4)
TARGET_SIZE = 175
target_img = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))
DRAG_CIRCLE_RADIUS = 150
dragging_target = False
target_offset_x = 0
target_offset_y = 0
FONT = pygame.font.SysFont(None, 96)
SMALL_FONT = pygame.font.SysFont(None, 64)

game_state = "home"
game_mode = None
total_targets = 0

clock = pygame.time.Clock()

# ------------------ Text drawing ------------------
def draw_text(text, pos, font=FONT, color=RED, align="center"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if align == "center":
        rect.center = pos
    elif align == "topleft":
        rect.topleft = pos
    screen.blit(surface, rect)

# ------------------ Button class ------------------
class Button:
    def __init__(self, image, x, y, width, height, action=None):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            temp_image = pygame.transform.scale(self.image,
                                                (int(self.rect.width*1.05), int(self.rect.height*1.05)))
            temp_rect = temp_image.get_rect(center=self.rect.center)
            surface.blit(temp_image, temp_rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

# ------------------ Particle effect class ------------------
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.radius = random.randint(4, 8)
        self.color = random.choice([RED])
        self.speed = random.uniform(8, 16)
        self.angle = random.uniform(0, 360)
        self.life = random.randint(20, 40)  # lifetime in frames

    def update(self):
        self.x += self.speed * 0.8 * pygame.math.Vector2(1, 0).rotate(self.angle).x
        self.y += self.speed * 0.8 * pygame.math.Vector2(1, 0).rotate(self.angle).y
        self.speed *= 0.9  # gradually slow down
        self.life -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = max(50, int(255 * (self.life / 40)))
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.radius, self.radius), int(self.radius))
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

# ------------------ Screen functions ------------------
def home_screen():
    """Home screen"""
    global game_state
    start_button = Button(start_img, screen.get_width()//2, int(screen.get_height()*0.8),
                          button_width, button_height, lambda: set_game_state("choice"))

    while game_state == "home":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                start_button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_home, screen.get_size()), (0,0))
        start_button.check_hover(mouse_pos)
        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def choice_screen():
    """Difficulty choice screen"""
    global game_state, game_mode, total_targets
    easy_button = Button(easy_img, screen.get_width()*0.35, screen.get_height()*0.6,
                         button_width, button_height, lambda: select_mode("easy"))
    hard_button = Button(hard_img, screen.get_width()*0.65, screen.get_height()*0.6,
                         button_width, button_height, lambda: select_mode("hard"))
    buttons = [easy_button, hard_button]

    while game_state == "choice":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_choice, screen.get_size()), (0,0))
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def select_mode(mode):
    """Set game mode and total targets"""
    global game_mode, total_targets, game_state
    game_mode = mode
    total_targets = 20 if mode=="easy" else 30
    set_game_state("play_ready")

# ------------------ New target ------------------
def new_target():
    if game_mode == "hard":
        center_x, center_y = screen.get_width()//2, screen.get_height()//2
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.randint(DRAG_CIRCLE_RADIUS + 50, DRAG_CIRCLE_RADIUS + 200)
        
        x = center_x + distance * math.cos(angle) - TARGET_SIZE//2
        y = center_y + distance * math.sin(angle) - TARGET_SIZE//2
        
        x = max(0, min(x, screen.get_width() - TARGET_SIZE))
        y = max(0, min(y, screen.get_height() - TARGET_SIZE))
        
        return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)
    else:
        x = random.randint(100, screen.get_width()-100-TARGET_SIZE)
        y = random.randint(100, screen.get_height()-100-TARGET_SIZE)
        return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)

# ------------------ Main game logic ------------------
def play_game():
    global game_state, dragging_target, target_offset_x, target_offset_y
    
    remaining_targets = total_targets
    targets_hit = 0
    start_time = None
    mouse_clicked = False
    target_rect = new_target()
    particles = []
    pygame.mouse.set_visible(False)

    circle_center = (screen.get_width()//2, screen.get_height()//2)
    
    while game_state=="play":
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if not mouse_clicked:
                    mouse_clicked = True
                    start_time = time.time()
                
                if game_mode == "hard":
                    if target_rect.collidepoint(mouse_pos):
                        dragging_target = True
                        target_offset_x = mouse_pos[0] - target_rect.x
                        target_offset_y = mouse_pos[1] - target_rect.y
                else:
                    if target_rect.collidepoint(mouse_pos):
                        pygame.mixer.Channel(1).play(hitSound)
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))
                        targets_hit += 1
                        remaining_targets -= 1

                        if remaining_targets == 0:
                            avg_ms = (time.time()-start_time)/total_targets*1000
                            set_game_state("result")
                            result_screen(avg_ms)
                            return

                        target_rect = new_target()
                    else:
                        pygame.mixer.Channel(0).play(missSound)
                    
            if event.type == MOUSEBUTTONUP:
                if dragging_target and game_mode == "hard":
                    dragging_target = False
                    
                    circle_rect = pygame.Rect(circle_center[0]-DRAG_CIRCLE_RADIUS, 
                                            circle_center[1]-DRAG_CIRCLE_RADIUS,
                                            DRAG_CIRCLE_RADIUS*2, DRAG_CIRCLE_RADIUS*2)
                    
                    if circle_rect.collidepoint(target_rect.center):

                        pygame.mixer.Channel(1).play(hitSound)
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))
                        targets_hit += 1
                        remaining_targets -= 1

                        if remaining_targets == 0:
                            avg_ms = (time.time()-start_time)/total_targets*1000
                            set_game_state("result")
                            result_screen(avg_ms)
                            return

                        target_rect = new_target()
                    else:
                        pygame.mixer.Channel(0).play(missSound)

                        target_rect = new_target()
        
        if dragging_target and game_mode == "hard":
            target_rect.x = mouse_pos[0] - target_offset_x
            target_rect.y = mouse_pos[1] - target_offset_y
            
            target_rect.x = max(0, min(target_rect.x, screen.get_width() - TARGET_SIZE))
            target_rect.y = max(0, min(target_rect.y, screen.get_height() - TARGET_SIZE))

        screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        
        if game_mode == "hard":
            pygame.draw.circle(screen, YELLOW, circle_center, DRAG_CIRCLE_RADIUS, 3)
            pygame.draw.circle(screen, (*YELLOW, 50), circle_center, DRAG_CIRCLE_RADIUS)
        
        screen.blit(target_img, target_rect)
        draw_text(f"{remaining_targets}", (142,130), SMALL_FONT, WHITE, align="center")

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        mx,my = mouse_pos
        pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not mouse_clicked:
            if game_mode == "hard":
                draw_text("Drag targets to the circle", (screen.get_width()//2, screen.get_height()//2),
                          SMALL_FONT, WHITE)
            else:
                draw_text("Click target to start", (screen.get_width()//2, screen.get_height()//2),
                          SMALL_FONT, WHITE)

        pygame.display.flip()
        clock.tick(60)

# ------------------ Result screen ------------------
def result_screen(avg_ms):
    global game_state
    pygame.mouse.set_visible(True)
    replay_button = Button(replay_img, screen.get_width()*0.35, screen.get_height()*0.8,
                           button_width, button_height, lambda: set_game_state("play_ready"))
    end_button = Button(end_img, screen.get_width()*0.65, screen.get_height()*0.8,
                        button_width, button_height, lambda: set_game_state("home"))
    buttons = [replay_button, end_button]

    while game_state=="result":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_result, screen.get_size()), (0,0))
        draw_text(f"{avg_ms:.1f}", (screen.get_width()*0.45, screen.get_height()*0.43), FONT, WHITE)
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def set_game_state(state):
    global game_state, dragging_target
    game_state = state
    dragging_target = False 

# ------------------ Main loop ------------------
while True:
    if game_state=="home":
        home_screen()
    elif game_state=="choice":
        choice_screen()
    elif game_state=="play_ready":
        set_game_state("play")
        play_game()
    elif game_state=="play":
        play_game()
    elif game_state=="result":
        result_screen(0)