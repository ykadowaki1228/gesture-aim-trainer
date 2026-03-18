import pygame, random, sys, time, math
from pygame.locals import *

pygame.init()
# fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
medium_img = pygame.image.load("medium.png")
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
TARGET_SIZE = 200
target_img = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))
DRAG_CIRCLE_RADIUS = 250          # radius for hard mode circle
dragging_target = False
target_offset_x = 0
target_offset_y = 0
FONT = pygame.font.SysFont(None, 128)
SMALL_FONT = pygame.font.SysFont(None, 82)

game_state = "home"
game_mode = None
total_targets = 0
current_round = 1
current_avg_ms = 0

clock = pygame.time.Clock()

# ------------------ LOGGING ------------------
LOG_FILE = "session_data.txt"

def reset_log():
    """Clear/create the log and reset round counter at the start of each session."""
    global current_round
    current_round = 1
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        # round = replay number, trial = target index in that round
        f.write("round,trial,reaction_ms\n")

def log_trial(trial_num, reaction_ms):
    """Append one trial: current round + trial number + reaction time in ms."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{current_round},{trial_num},{reaction_ms:.2f}\n")
    print(f"[Round {current_round}] Logged trial {trial_num} with {reaction_ms:.2f} ms")


# ------------------ Exit function ------------------
def exit_game():
    pygame.quit()
    sys.exit()

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

# ------------------ Exit Button (top-right “X”) ------------------
class ExitButton:
    def __init__(self):
        self.size = 60
        self.x = screen.get_width() - self.size - 25
        self.y = 875
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        # translucent background rectangle
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((0, 0, 0, 80))
        surface.blit(s, (self.x, self.y))
        pygame.draw.rect(surface, WHITE, self.rect, 3)
        pygame.draw.line(surface, WHITE, (self.x+10, self.y+10),
                                          (self.x+self.size-10, self.y+self.size-10), 4)
        pygame.draw.line(surface, WHITE, (self.x+self.size-10, self.y+10),
                                          (self.x+10, self.y+self.size-10), 4)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            exit_game()

# Create one global exit button
exit_button = ExitButton()

# ------------------ Particle effect ------------------
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.radius = random.randint(4, 8)
        self.color = random.choice([RED])
        self.speed = random.uniform(8, 16)
        self.angle = random.uniform(0, 360)
        self.life = random.randint(20, 40)  # lifetime in frames

    def update(self):
        v = pygame.math.Vector2(1, 0).rotate(self.angle)
        self.x += self.speed * 0.8 * v.x
        self.y += self.speed * 0.8 * v.y
        self.speed *= 0.9  # gradually slow down
        self.life -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            alpha = max(50, int(255 * (self.life / 40)))
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

# ------------------ Screens ------------------
def home_screen():
    global game_state
    reset_log()
    start_button = Button(start_img, screen.get_width()//2, int(screen.get_height()*0.8),
                          button_width, button_height, lambda: set_game_state("choice"))

    while game_state == "home":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                start_button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_home, screen.get_size()), (0,0))
        start_button.check_hover(mouse_pos)
        start_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def choice_screen():
    """Difficulty choice"""
    global game_state
    easy_button = Button(easy_img, screen.get_width()*0.20, screen.get_height()*0.6,
                         button_width, button_height, lambda: select_mode("easy"))
    medium_button = Button(medium_img, screen.get_width()*0.50, screen.get_height()*0.6,
                         button_width, button_height, lambda: select_mode("medium"))
    hard_button = Button(hard_img, screen.get_width()*0.80, screen.get_height()*0.6,
                         button_width, button_height, lambda: select_mode("hard"))

    buttons = [easy_button, medium_button, hard_button]

    while game_state == "choice":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                for b in buttons: b.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_choice, screen.get_size()), (0,0))
        for b in buttons:
            b.check_hover(mouse_pos)
            b.draw(screen)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def select_mode(mode):
    global total_targets, game_state, game_mode
    game_mode = mode
    if mode == "easy":
        total_targets = 20
        set_game_state("play_ready")
    elif mode == "medium":
        total_targets = 20
        set_game_state("play_ready")
    elif mode == "hard":
        total_targets = 20
        set_game_state("hard_game")

# ------------------ Target creation ------------------
def new_target_for_mode(mode):
    # For hard mode we spawn targets outside the circle (so user drags them into the circle).
    if mode == "hard":
        center_x, center_y = screen.get_width()//2, screen.get_height()//2
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(DRAG_CIRCLE_RADIUS + 50, DRAG_CIRCLE_RADIUS + 200)
        x = int(center_x + distance * math.cos(angle) - TARGET_SIZE//2)
        y = int(center_y + distance * math.sin(angle) - TARGET_SIZE//2)
        x = max(0, min(x, screen.get_width() - TARGET_SIZE))
        y = max(0, min(y, screen.get_height() - TARGET_SIZE))
        return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)
    else:
        x = random.randint(100, screen.get_width()-100-TARGET_SIZE)
        y = random.randint(100, screen.get_height()-100-TARGET_SIZE)
        return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)
    

def start_replay():
    """Action when Replay is pressed: go to next round and play again."""
    global current_round, game_state
    current_round += 1
    game_state = "play_ready"

def on_end_button():
    """Action when END is pressed: go to graph screen."""
    set_game_state("graph")




# ------------------ Play (easy/medium) ------------------

def play_game():
    """Main game loop (one round)"""
    global game_state
    remaining_targets = total_targets
    target_hit = 0
    start_time = None
    mouse_clicked = False

    target_rect = new_target_for_mode(game_mode)

    last_spawn_time = time.time()
    started = False   


    particles = []
    pygame.mouse.set_visible(False)

    while game_state == "play":
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()

            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)

           
                #  Medium
           
                if game_mode == "medium":

                    # 第一次点击开始计时
                    if not started:
                        started = True
                        start_time = time.time()

                    if target_rect.collidepoint(mouse_pos):
                        pygame.mixer.Channel(1).play(hitSound)

                        # 粒子效果
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))

                        remaining_targets -= 1

                        # 结束
                        if remaining_targets == 0:
                            avg_ms = (time.time() - start_time) / total_targets * 1000
                            log_trial(1, current_avg_ms)
                            set_game_state("result")
                            result_screen(avg_ms)
                            return

                        # 新目标
                        target_rect = new_target_for_mode(game_mode)

                    else:
                        pygame.mixer.Channel(0).play(missSound)  # miss

  
        # Easy
    
        if game_mode == "easy":
            if target_rect.collidepoint(mouse_pos):

                if not started:
                    started = True
                    start_time = time.time()

                pygame.mixer.Channel(1).play(hitSound)

                # 粒子效果
                for _ in range(40):
                    particles.append(Particle(target_rect.center))

                remaining_targets -= 1

                # 结束
                if remaining_targets == 0:
                    avg_ms = (time.time() - start_time) / total_targets * 1000
                    log_trial(1, current_avg_ms)
                    set_game_state("result")
                    result_screen(avg_ms)
                    return

                target_rect = new_target_for_mode(game_mode)

        # ============================
        # 绘制画面
        # ============================
        screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        screen.blit(target_img, target_rect)

        draw_text(f"{remaining_targets}",
                  (int(screen.get_width()*0.11), int(screen.get_height()*0.18)),
                  SMALL_FONT, WHITE, align="center")

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        # 自制准心
        mx, my = mouse_pos
        pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not started:
            draw_text("Click target to start",
                      (screen.get_width()//2, screen.get_height()//2),
                      SMALL_FONT, WHITE)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
   

# ------------------ Hard mode play (drag-to-circle) ------------------
def play_hard_game():
    global game_state, dragging_target, target_offset_x, target_offset_y
    remaining_targets = total_targets
    start_time = None
    mouse_clicked = False
    target_rect = new_target_for_mode("hard")
    particles = []
    pygame.mouse.set_visible(True)

    circle_center = (screen.get_width()//2, screen.get_height()//2)

    while game_state == "hard_game":
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)

                if not mouse_clicked:
                    mouse_clicked = True
                    start_time = time.time()

                if target_rect.collidepoint(mouse_pos):
                    dragging_target = True
                    target_offset_x = mouse_pos[0] - target_rect.x
                    target_offset_y = mouse_pos[1] - target_rect.y

            if event.type == MOUSEBUTTONUP:
                if dragging_target:
                    dragging_target = False
                    # check if center of target is inside the circle -> success
                    if math.dist(target_rect.center, circle_center) <= DRAG_CIRCLE_RADIUS:
                        pygame.mixer.Channel(1).play(hitSound)
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))
                        remaining_targets -= 1

                        if remaining_targets == 0:
                            avg_ms = (time.time() - start_time) / total_targets * 1000
                            set_game_state("result")
                            result_screen(avg_ms)
                            return

                        target_rect = new_target_for_mode("hard")
                    else:
                        pygame.mixer.Channel(0).play(missSound)
                        # generate a new target to avoid stuck
                        target_rect = new_target_for_mode("hard")

        # dragging movement
        if dragging_target:
            target_rect.x = mouse_pos[0] - target_offset_x
            target_rect.y = mouse_pos[1] - target_offset_y
            target_rect.x = max(0, min(target_rect.x, screen.get_width() - TARGET_SIZE))
            target_rect.y = max(0, min(target_rect.y, screen.get_height() - TARGET_SIZE))
       
        DRAG_CIRCLE_RADIUS = 150 
        CIRCLE_DIAMETER = 2 * DRAG_CIRCLE_RADIUS
        # draw background and circle
        screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        pygame.draw.circle(screen, WHITE, circle_center, DRAG_CIRCLE_RADIUS,5)
        # faint fill
        s = pygame.Surface((CIRCLE_DIAMETER, CIRCLE_DIAMETER), pygame.SRCALPHA)
        pygame.draw.circle(s, (YELLOW[0], YELLOW[1], YELLOW[2], 0), (DRAG_CIRCLE_RADIUS, DRAG_CIRCLE_RADIUS), DRAG_CIRCLE_RADIUS)
        screen.blit(s, (circle_center[0]-DRAG_CIRCLE_RADIUS, circle_center[1]-DRAG_CIRCLE_RADIUS))

        # draw target and UI
        screen.blit(target_img, target_rect)
        draw_text(f"{remaining_targets}", (int(screen.get_width()*0.11), int(screen.get_height()*0.18)), SMALL_FONT, WHITE, align="center")

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        mx,my = mouse_pos
        pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not mouse_clicked:
            draw_text("Drag targets into the circle", (screen.get_width()//2, screen.get_height()//2),
                      SMALL_FONT, WHITE)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

# ------------------ Result screen ------------------
def result_screen(avg_ms):
    """Result screen (after one round)"""
    global game_state
    pygame.mouse.set_visible(True)
    replay_button = Button(replay_img, screen.get_width()*0.35, screen.get_height()*0.8,
                           button_width, button_height, lambda: set_game_state("home"))
    end_button = Button(end_img, screen.get_width()*0.65, screen.get_height()*0.8,
                        button_width, button_height, lambda: set_game_state("graph"))
    buttons = [replay_button, end_button]

    while game_state=="result":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                for b in buttons:
                    b.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_result, screen.get_size()), (0,0))
        draw_text(f"{avg_ms:.1f}", (screen.get_width()*0.43, screen.get_height()*0.43), FONT, WHITE)

        for b in buttons:
            b.check_hover(mouse_pos)
            b.draw(screen)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def set_game_state(state):
    global game_state, dragging_target
    game_state = state
    dragging_target = False




# ------------------ Graph screen ------------------
def graph_screen():
    global game_state

    pygame.mouse.set_visible(True)

    # グラフ画像の生成（matplotlib）
    import matplotlib.pyplot as plt
    import pandas as pd

    try:
        df = pd.read_csv(LOG_FILE)
    except:
        print("Log file not found.")
        df = None

    if df is not None and len(df) > 0:
        # ラウンドごとの平均値計算
        avg_data = df.groupby("round")["reaction_ms"].mean()

        plt.figure(figsize=(6,4))
        avg_data.plot(marker="o")
        plt.title("Average Reaction Time per Round")
        plt.xlabel("Round")
        plt.ylabel("Reaction Time (ms)")
        plt.tight_layout()
        plt.savefig("reaction_graph.png")
        plt.close()

        graph_img = pygame.image.load("reaction_graph.png")
        graph_img = pygame.transform.scale(
            graph_img,
            (int(screen.get_width()*0.6), int(screen.get_height()*0.6))
        )
    else:
        graph_img = None

    back_button = Button(replay_img, screen.get_width()*0.5, screen.get_height()*0.85,
                         button_width, button_height, lambda: set_game_state("home"))

    while game_state == "graph":
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            if event.type == MOUSEBUTTONDOWN:
                back_button.check_click(mouse_pos)

        screen.fill(BLACK)

        if graph_img:
            screen.blit(
                graph_img,
                (
                    screen.get_width()//2 - graph_img.get_width()//2,
                    screen.get_height()//2 - graph_img.get_height()//2
                )
            )
        else:
            draw_text("NO DATA", (screen.get_width()//2, screen.get_height()//2),
                      FONT, WHITE)

        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

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
    elif game_state=="hard_game":
        play_hard_game()
    elif game_state=="result":
        result_screen(current_avg_ms)
    elif game_state=="graph":
        graph_screen()