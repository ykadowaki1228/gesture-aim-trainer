# import pygame, random, sys, time, math
# from pygame.locals import *

# pygame.init()
# # fullscreen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# pygame.display.set_caption("Very Very Serious Game")

# # ------------------ Colors ------------------
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 200, 50)

# # Extra colors for graph
# GREY = (40, 40, 40)
# LIGHT_GREY = (180, 180, 180)

# # Colors for graph lines (cycled per round)
# ROUND_COLORS = [
#     (255, 99, 132),
#     (54, 162, 235),
#     (255, 206, 86),
#     (75, 192, 192),
#     (153, 102, 255),
#     (255, 159, 64),
# ]

# # ------------------ Load images ------------------
# bg_home = pygame.image.load("home.png")
# bg_choice = pygame.image.load("choice.png")
# bg_game = pygame.image.load("game.png")
# bg_result = pygame.image.load("result.png")

# target_img = pygame.image.load("target.png")
# start_img = pygame.image.load("start.png")
# easy_img = pygame.image.load("easy.png")
# medium_img = pygame.image.load("medium.png")
# hard_img = pygame.image.load("hard.png")
# replay_img = pygame.image.load("replay.png")
# end_img = pygame.image.load("end.png")

# # ------------------ Sounds ------------------
# hitSound = pygame.mixer.Sound("hitsound.wav")
# missSound = pygame.mixer.Sound("misssound.wav")
# hitSound.set_volume(1)
# missSound.set_volume(1)

# # ------------------ Parameters ------------------
# button_width = int(screen.get_width() * 0.25)
# button_height = int(button_width / 4)
# TARGET_SIZE = 200
# target_img = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))
# DRAG_CIRCLE_RADIUS = 250          # radius for hard mode circle
# dragging_target = False
# target_offset_x = 0
# target_offset_y = 0
# FONT = pygame.font.SysFont(None, 128)
# SMALL_FONT = pygame.font.SysFont(None, 82)
# TINY_FONT = pygame.font.SysFont(None, 32)

# game_state = "home"
# game_mode = None
# total_targets = 0

# # For multi-round logging
# current_round = 1

# clock = pygame.time.Clock()

# # ------------------ Logging ------------------
# LOG_FILE = "session_data.txt"

# def reset_log():
#     """Clear/create the log and reset round counter at the start of each session."""
#     global current_round
#     current_round = 1
#     with open(LOG_FILE, "w", encoding="utf-8") as f:
#         f.write("round,trial,reaction_ms\n")

# def log_trial(trial_num, reaction_ms):
#     """Append one trial: current round + trial number + reaction time in ms."""
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"{current_round},{trial_num},{reaction_ms:.2f}\n")
#     print(f"[Round {current_round}] Logged trial {trial_num} with {reaction_ms:.2f} ms")

# # ------------------ Exit function ------------------
# def exit_game():
#     pygame.quit()
#     sys.exit()

# # ------------------ Text drawing ------------------
# def draw_text(text, pos, font=FONT, color=RED, align="center"):
#     surface = font.render(text, True, color)
#     rect = surface.get_rect()
#     if align == "center":
#         rect.center = pos
#     elif align == "topleft":
#         rect.topleft = pos
#     screen.blit(surface, rect)

# # ------------------ Button class ------------------
# class Button:
#     def __init__(self, image, x, y, width, height, action=None):
#         self.image = pygame.transform.scale(image, (width, height))
#         self.rect = self.image.get_rect(center=(x, y))
#         self.action = action
#         self.hovered = False

#     def draw(self, surface):
#         if self.hovered:
#             temp_image = pygame.transform.scale(self.image,
#                                                 (int(self.rect.width*1.05), int(self.rect.height*1.05)))
#             temp_rect = temp_image.get_rect(center=self.rect.center)
#             surface.blit(temp_image, temp_rect.topleft)
#         else:
#             surface.blit(self.image, self.rect.topleft)

#     def check_hover(self, mouse_pos):
#         self.hovered = self.rect.collidepoint(mouse_pos)

#     def check_click(self, mouse_pos):
#         if self.rect.collidepoint(mouse_pos) and self.action:
#             self.action()

# # ------------------ Exit Button (top-right “X”) ------------------
# class ExitButton:
#     def __init__(self):
#         self.size = 60
#         self.x = screen.get_width() - self.size - 25
#         self.y = 875
#         self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

#     def draw(self, surface):
#         # translucent background rectangle
#         s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
#         s.fill((0, 0, 0, 80))
#         surface.blit(s, (self.x, self.y))
#         pygame.draw.rect(surface, WHITE, self.rect, 3)
#         pygame.draw.line(surface, WHITE, (self.x+10, self.y+10),
#                                           (self.x+self.size-10, self.y+self.size-10), 4)
#         pygame.draw.line(surface, WHITE, (self.x+self.size-10, self.y+10),
#                                           (self.x+10, self.y+self.size-10), 4)

#     def check_click(self, pos):
#         if self.rect.collidepoint(pos):
#             exit_game()

# # Create one global exit button
# exit_button = ExitButton()

# # ------------------ Particle effect ------------------
# class Particle:
#     def __init__(self, pos):
#         self.x, self.y = pos
#         self.radius = random.randint(4, 8)
#         self.color = random.choice([RED])
#         self.speed = random.uniform(8, 16)
#         self.angle = random.uniform(0, 360)
#         self.life = random.randint(20, 40)  # lifetime in frames

#     def update(self):
#         v = pygame.math.Vector2(1, 0).rotate(self.angle)
#         self.x += self.speed * 0.8 * v.x
#         self.y += self.speed * 0.8 * v.y
#         self.speed *= 0.9  # gradually slow down
#         self.life -= 1
#         self.radius = max(0, self.radius - 0.1)

#     def draw(self, surface):
#         if self.life > 0 and self.radius > 0:
#             alpha = max(50, int(255 * (self.life / 40)))
#             s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
#             pygame.draw.circle(s, (*self.color, alpha), (int(self.radius), int(self.radius)), int(self.radius))
#             surface.blit(s, (self.x - self.radius, self.y - self.radius))

# # ------------------ Screens ------------------
# def home_screen():
#     global game_state
#     # New overall session -> reset file + round counter
#     reset_log()

#     start_button = Button(start_img, screen.get_width()//2, int(screen.get_height()*0.8),
#                           button_width, button_height, lambda: set_game_state("choice"))

#     while game_state == "home":
#         mouse_pos = pygame.mouse.get_pos()
#         for event in pygame.event.get():
#             if event.type == QUIT: exit_game()
#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)
#                 start_button.check_click(mouse_pos)

#         screen.blit(pygame.transform.scale(bg_home, screen.get_size()), (0,0))
#         start_button.check_hover(mouse_pos)
#         start_button.draw(screen)
#         exit_button.draw(screen)

#         pygame.display.flip()
#         clock.tick(60)

# def choice_screen():
#     global game_state
#     easy_button = Button(easy_img, screen.get_width()*0.20, screen.get_height()*0.6,
#                          button_width, button_height, lambda: select_mode("easy"))
#     medium_button = Button(medium_img, screen.get_width()*0.50, screen.get_height()*0.6,
#                          button_width, button_height, lambda: select_mode("medium"))
#     hard_button = Button(hard_img, screen.get_width()*0.80, screen.get_height()*0.6,
#                          button_width, button_height, lambda: select_mode("hard"))

#     buttons = [easy_button, medium_button, hard_button]

#     while game_state == "choice":
#         mouse_pos = pygame.mouse.get_pos()
#         for event in pygame.event.get():
#             if event.type == QUIT: exit_game()
#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)
#                 for b in buttons: b.check_click(mouse_pos)

#         screen.blit(pygame.transform.scale(bg_choice, screen.get_size()), (0,0))
#         for b in buttons:
#             b.check_hover(mouse_pos)
#             b.draw(screen)

#         exit_button.draw(screen)
#         pygame.display.flip()
#         clock.tick(60)

# def select_mode(mode):
#     global total_targets, game_state, game_mode
#     game_mode = mode
#     if mode == "easy":
#         total_targets = 20
#         set_game_state("play_ready")
#     elif mode == "medium":
#         total_targets = 20
#         set_game_state("play_ready")
#     elif mode == "hard":
#         total_targets = 20
#         set_game_state("hard_game")

# # ------------------ Target creation ------------------
# def new_target_for_mode(mode):
#     # For hard mode we spawn targets outside the circle (so user drags them into the circle).
#     if mode == "hard":
#         center_x, center_y = screen.get_width()//2, screen.get_height()//2
#         angle = random.uniform(0, 2 * math.pi)
#         distance = random.randint(DRAG_CIRCLE_RADIUS + 50, DRAG_CIRCLE_RADIUS + 200)
#         x = int(center_x + distance * math.cos(angle) - TARGET_SIZE//2)
#         y = int(center_y + distance * math.sin(angle) - TARGET_SIZE//2)
#         x = max(0, min(x, screen.get_width() - TARGET_SIZE))
#         y = max(0, min(y, screen.get_height() - TARGET_SIZE))
#         return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)
#     else:
#         x = random.randint(100, screen.get_width()-100-TARGET_SIZE)
#         y = random.randint(100, screen.get_height()-100-TARGET_SIZE)
#         return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)

# # ------------------ Play (easy/medium) ------------------
# def play_game():
#     global game_state
#     remaining_targets = total_targets
#     start_time = None
#     started = False   

#     target_rect = new_target_for_mode(game_mode)
#     last_spawn_time = time.time()  # for per-target reaction time
#     particles = []
#     pygame.mouse.set_visible(False)

#     while game_state == "play":
#         mouse_pos = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 exit_game()

#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)

#                 #  Medium
#                 if game_mode == "medium":

#                     # 第一次点击开始计时 (first successful hit starts timing)
#                     if not started and target_rect.collidepoint(mouse_pos):
#                         started = True
#                         start_time = time.time()

#                     if target_rect.collidepoint(mouse_pos):
#                         pygame.mixer.Channel(1).play(hitSound)

#                         # per-target reaction time (ms)
#                         reaction_ms = (time.time() - last_spawn_time) * 1000.0
#                         trial_num = (total_targets - remaining_targets) + 1
#                         log_trial(trial_num, reaction_ms)

#                         # 粒子效果
#                         for _ in range(40):
#                             particles.append(Particle(target_rect.center))

#                         remaining_targets -= 1

#                         # 结束
#                         if remaining_targets == 0 and started:
#                             avg_ms = (time.time() - start_time) / total_targets * 1000
#                             set_game_state("result")
#                             result_screen(avg_ms)
#                             return

#                         # 新目标
#                         target_rect = new_target_for_mode(game_mode)
#                         last_spawn_time = time.time()

#                     else:
#                         pygame.mixer.Channel(0).play(missSound)  # miss

#         # Easy
#         if game_mode == "easy":
#             if target_rect.collidepoint(mouse_pos):

#                 if not started:
#                     started = True
#                     start_time = time.time()

#                 pygame.mixer.Channel(1).play(hitSound)

#                 # per-target reaction time (ms)
#                 reaction_ms = (time.time() - last_spawn_time) * 1000.0
#                 trial_num = (total_targets - remaining_targets) + 1
#                 log_trial(trial_num, reaction_ms)

#                 # 粒子效果
#                 for _ in range(40):
#                     particles.append(Particle(target_rect.center))

#                 remaining_targets -= 1

#                 # 结束
#                 if remaining_targets == 0 and started:
#                     avg_ms = (time.time() - start_time) / total_targets * 1000
#                     set_game_state("result")
#                     result_screen(avg_ms)
#                     return

#                 target_rect = new_target_for_mode(game_mode)
#                 last_spawn_time = time.time()

#         # ============================
#         # 绘制画面
#         # ============================
#         screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
#         screen.blit(target_img, target_rect)

#         draw_text(f"{remaining_targets}",
#                   (int(screen.get_width()*0.11), int(screen.get_height()*0.18)),
#                   SMALL_FONT, WHITE, align="center")

#         for p in particles[:]:
#             p.update()
#             p.draw(screen)
#             if p.life <= 0:
#                 particles.remove(p)

#         # 自制准心
#         mx, my = mouse_pos
#         pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
#         pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

#         if not started:
#             draw_text("Click target to start" if game_mode=="medium" else "Move over target to start",
#                       (screen.get_width()//2, screen.get_height()//2),
#                       SMALL_FONT, WHITE)

#         exit_button.draw(screen)
#         pygame.display.flip()
#         clock.tick(60)

# # ------------------ Hard mode play (drag-to-circle) ------------------
# def play_hard_game():
#     global game_state, dragging_target, target_offset_x, target_offset_y
#     remaining_targets = total_targets
#     start_time = None
#     mouse_clicked = False
#     target_rect = new_target_for_mode("hard")
#     drag_start_pos = target_rect.topleft  # 初期化
    
#     last_spawn_time = time.time()   # for per-target reaction time
#     particles = []
#     pygame.mouse.set_visible(True)

#     circle_center = (screen.get_width()//2, screen.get_height()//2)

#     while game_state == "hard_game":
#         mouse_pos = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == QUIT: exit_game()
#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)

#                 if not mouse_clicked:
#                     mouse_clicked = True
#                     start_time = time.time()

#                 if target_rect.collidepoint(mouse_pos):
#                     dragging_target = True
#                     target_offset_x = mouse_pos[0] - target_rect.x
#                     target_offset_y = mouse_pos[1] - target_rect.y
#                     drag_start_pos = target_rect.topleft  # ドラッグ開始位置を記録

#             if event.type == MOUSEBUTTONUP:
#                 if dragging_target:
#                     dragging_target = False
#                     # check if center of target is inside the circle -> success
#                     if math.dist(target_rect.center, circle_center) <= DRAG_CIRCLE_RADIUS:
#                         pygame.mixer.Channel(1).play(hitSound)
#                         for _ in range(40):
#                             particles.append(Particle(target_rect.center))

#                         # per-target reaction time (ms)
#                         reaction_ms = (time.time() - last_spawn_time) * 1000.0
#                         trial_num = (total_targets - remaining_targets) + 1
#                         log_trial(trial_num, reaction_ms)

#                         remaining_targets -= 1

#                         if remaining_targets == 0 and start_time is not None:
#                             avg_ms = (time.time() - start_time) / total_targets * 1000
#                             set_game_state("result")
#                             result_screen(avg_ms)
#                             return

#                         target_rect = new_target_for_mode("hard")
#                         last_spawn_time = time.time()
#                     else:
#                         pygame.mixer.Channel(0).play(missSound)
#                         target_rect.topleft = drag_start_pos  # 失敗時は元の位置に戻す

#         # dragging movement
#         if dragging_target:
#             target_rect.x = mouse_pos[0] - target_offset_x
#             target_rect.y = mouse_pos[1] - target_offset_y
#             target_rect.x = max(0, min(target_rect.x, screen.get_width() - TARGET_SIZE))
#             target_rect.y = max(0, min(target_rect.y, screen.get_height() - TARGET_SIZE))
       
#         DRAG_CIRCLE_RADIUS_DRAW = 150 
#         CIRCLE_DIAMETER = 2 * DRAG_CIRCLE_RADIUS_DRAW
#         # draw background and circle
#         screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
#         pygame.draw.circle(screen, WHITE, circle_center, DRAG_CIRCLE_RADIUS_DRAW,5)
#         # faint fill
#         s = pygame.Surface((CIRCLE_DIAMETER, CIRCLE_DIAMETER), pygame.SRCALPHA)
#         pygame.draw.circle(s, (YELLOW[0], YELLOW[1], YELLOW[2], 0), (DRAG_CIRCLE_RADIUS_DRAW, DRAG_CIRCLE_RADIUS_DRAW), DRAG_CIRCLE_RADIUS_DRAW)
#         screen.blit(s, (circle_center[0]-DRAG_CIRCLE_RADIUS_DRAW, circle_center[1]-DRAG_CIRCLE_RADIUS_DRAW))

#         # draw target and UI
#         screen.blit(target_img, target_rect)
#         draw_text(f"{remaining_targets}", (int(screen.get_width()*0.11), int(screen.get_height()*0.18)), SMALL_FONT, WHITE, align="center")

#         for p in particles[:]:
#             p.update()
#             p.draw(screen)
#             if p.life <= 0:
#                 particles.remove(p)

#         mx,my = mouse_pos
#         pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
#         pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

#         if not mouse_clicked:
#             draw_text("Drag targets into the circle", (screen.get_width()//2, screen.get_height()//2),
#                       SMALL_FONT, WHITE)

#         exit_button.draw(screen)
#         pygame.display.flip()
#         clock.tick(60)

# # ------------------ Round / result handling ------------------
# def start_replay():
#     """Action when Replay is pressed: go to next round and play again in same mode."""
#     global current_round, game_state
#     current_round += 1
#     # For hard we go back to hard_game directly, for others we use play_ready
#     if game_mode == "hard":
#         set_game_state("hard_game")
#     else:
#         set_game_state("play_ready")

# def on_end_button():
#     """Action when END is pressed: go to graph screen."""
#     set_game_state("graph")

# # ------------------ Result screen ------------------
# def result_screen(avg_ms):
#     global game_state
#     pygame.mouse.set_visible(True)
#     replay_button = Button(replay_img, screen.get_width()*0.35, screen.get_height()*0.8,
#                            button_width, button_height, start_replay)
#     end_button = Button(end_img, screen.get_width()*0.65, screen.get_height()*0.8,
#                         button_width, button_height, on_end_button)
#     buttons = [replay_button, end_button]

#     # local state for this screen (prevent NameError on click)
#     mouse_clicked = False
#     start_time = None

#     while game_state=="result":
#         mouse_pos = pygame.mouse.get_pos()
#         for event in pygame.event.get():
#             if event.type == QUIT: exit_game()
#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)

#                 if not mouse_clicked:
#                     mouse_clicked = True
#                     start_time = time.time()

#                 for b in buttons:
#                     b.check_click(mouse_pos)

#         screen.blit(pygame.transform.scale(bg_result, screen.get_size()), (0,0))
#         draw_text(f"{avg_ms:.1f}", (screen.get_width()*0.43, screen.get_height()*0.43), FONT, WHITE)

#         for b in buttons:
#             b.check_hover(mouse_pos)
#             b.draw(screen)

#         exit_button.draw(screen)
#         pygame.display.flip()
#         clock.tick(60)

# # ------------------ GRAPH SCREEN ------------------
# def show_graph():
#     """
#     Graph UI screen:
#       - fullscreen
#       - multiple lines: one per round (reaction vs trial)
#       - legend + best round in title
#       - CLOSE & RESTART button -> back to home & reset log
#     """
#     global game_state

#     # ---- load data from log file ----
#     round_to_times = {}
#     try:
#         with open(LOG_FILE, "r", encoding="utf-8") as f:
#             next(f)  # skip header
#             for line in f:
#                 line = line.strip()
#                 if not line or "," not in line:
#                     continue
#                 parts = line.split(",")
#                 if len(parts) != 3:
#                     continue
#                 r_str, t_str, react_str = parts
#                 try:
#                     r = int(r_str)
#                     t = int(t_str)
#                     react = float(react_str)
#                 except ValueError:
#                     continue
#                 round_to_times.setdefault(r, []).append(react)
#     except FileNotFoundError:
#         reset_log()
#         set_game_state("home")
#         return

#     if not round_to_times:
#         reset_log()
#         set_game_state("home")
#         return

#     # ---- compute averages & best round ----
#     avg_per_round = {r: sum(times)/len(times) for r, times in round_to_times.items()}
#     best_round = min(avg_per_round, key=avg_per_round.get)
#     best_avg   = avg_per_round[best_round]

#     all_times = [v for times in round_to_times.values() for v in times]
#     min_t = min(all_times)
#     max_t = max(all_times)
#     if max_t == min_t:
#         max_t += 10
#         min_t -= 10

#     # graph area
#     W, H = screen.get_size()
#     margin_left   = 120   # more space so y labels don't touch axis
#     margin_right  = 80
#     margin_top    = 160   # more space for title + legend
#     margin_bottom = 160
#     graph_w = W - margin_left - margin_right
#     graph_h = H - margin_top - margin_bottom

#     max_trials = max(len(times) for times in round_to_times.values())

#     # dynamic button size so text always fits
#     close_text = "CLOSE & RESTART"
#     label_surface = SMALL_FONT.render(close_text, True, WHITE)
#     button_w = label_surface.get_width() + 80
#     button_h = label_surface.get_height() + 30
#     close_rect = pygame.Rect(
#         W//2 - button_w//2,
#         H - margin_bottom//2 - button_h//2,
#         button_w,
#         button_h
#     )

#     running = True
#     while game_state == "graph" and running:
#         mouse_pos = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 exit_game()
#             if event.type == MOUSEBUTTONDOWN:
#                 exit_button.check_click(mouse_pos)
#                 if close_rect.collidepoint(mouse_pos):
#                     reset_log()
#                     set_game_state("home")
#                     running = False

#         # background
#         screen.fill(GREY)

#         # title
#         title_text = f"Reaction Time per Trial  |  Best Round: {best_round} (~{best_avg:.0f} ms)"
#         draw_text(title_text, (W//2, 80), SMALL_FONT, WHITE)

#         # axes box
#         pygame.draw.rect(screen, LIGHT_GREY,
#                          (margin_left, margin_top, graph_w, graph_h), 2)

#         # horizontal grid lines + y labels
#         grid_lines = 5
#         for i in range(grid_lines + 1):
#             frac = i / grid_lines
#             y = margin_top + graph_h * (1 - frac)
#             pygame.draw.line(screen, (80, 80, 80),
#                              (margin_left, y), (margin_left + graph_w, y), 1)
#             value = min_t + (max_t - min_t) * frac
#             label = f"{value:.0f} ms"
#             label_surf = TINY_FONT.render(label, True, WHITE)
#             label_rect = label_surf.get_rect()
#             label_rect.right = margin_left - 12
#             label_rect.centery = y
#             screen.blit(label_surf, label_rect)

#         # vertical grid lines (trial numbers) + x tick labels
#         for t in range(1, max_trials + 1):
#             if max_trials > 1:
#                 frac_x = (t - 1) / (max_trials - 1)
#             else:
#                 frac_x = 0.5
#             x = margin_left + graph_w * frac_x
#             pygame.draw.line(screen, (80, 80, 80),
#                              (x, margin_top), (x, margin_top + graph_h), 1)
#             label = str(t)
#             draw_text(label, (x, margin_top + graph_h + 20),
#                       TINY_FONT, WHITE, align="center")

#         # x-axis label
#         draw_text("Trial Number",
#                   (margin_left + graph_w/2, margin_top + graph_h + 55),
#                   TINY_FONT, WHITE, align="center")

#         # plot lines per round
#         for idx, r in enumerate(sorted(round_to_times.keys())):
#             times = round_to_times[r]
#             color = ROUND_COLORS[idx % len(ROUND_COLORS)]
#             points = []
#             for i, v in enumerate(times):
#                 t_idx = i + 1
#                 if max_trials > 1:
#                     frac_x = (t_idx - 1) / (max_trials - 1)
#                 else:
#                     frac_x = 0.5
#                 x = margin_left + graph_w * frac_x
#                 frac_y = (v - min_t) / (max_t - min_t)
#                 y = margin_top + graph_h * (1 - frac_y)
#                 points.append((x, y))
#             if len(points) >= 2:
#                 pygame.draw.lines(screen, color, False, points, 3)
#             elif len(points) == 1:
#                 pygame.draw.circle(screen, color,
#                                    (int(points[0][0]), int(points[0][1])), 4)

#         # legend (above the graph)
#         legend_x = margin_left + 10
#         legend_y = margin_top - 60
#         for idx, r in enumerate(sorted(avg_per_round.keys())):
#             color = ROUND_COLORS[idx % len(ROUND_COLORS)]
#             y_line = legend_y + idx*24 + 10
#             pygame.draw.line(screen, color,
#                              (legend_x, y_line),
#                              (legend_x + 40, y_line), 4)
#             text = f"Round {r}: ~{avg_per_round[r]:.0f} ms"
#             draw_text(text,
#                       (legend_x + 50, y_line),
#                       TINY_FONT, WHITE, align="topleft")

#         # close button
#         is_hover = close_rect.collidepoint(mouse_pos)
#         pygame.draw.rect(screen,
#                          (220, 70, 70) if is_hover else (180, 50, 50),
#                          close_rect, border_radius=15)
#         pygame.draw.rect(screen, WHITE, close_rect, 2, border_radius=15)
#         draw_text(close_text,
#                   close_rect.center, SMALL_FONT, WHITE, align="center")

#         exit_button.draw(screen)
#         pygame.display.flip()
#         clock.tick(60)

# def set_game_state(state):
#     global game_state, dragging_target
#     game_state = state
#     dragging_target = False

# # ------------------ Main loop ------------------
# while True:
#     if game_state=="home":
#         home_screen()
#     elif game_state=="choice":
#         choice_screen()
#     elif game_state=="play_ready":
#         set_game_state("play")
#         play_game()
#     elif game_state=="play":
#         play_game()
#     elif game_state=="hard_game":
#         play_hard_game()
#     elif game_state=="result":
#         result_screen(0)
#     elif game_state=="graph":
#         show_graph()

import pygame, random, sys, time, math
from pygame.locals import *

# ------------------ INITIALIZATION & FULLSCREEN ------------------
pygame.init()
# コード2のフルスクリーン設定を採用
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Very Very Serious Game")

# ------------------ COLORS ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
YELLOW = (255, 200, 50) # Hardモード用
GREY  = (40, 40, 40)
LIGHT_GREY = (180, 180, 180)

# Colors for graph lines (cycled per round)
ROUND_COLORS = [
    (255, 99, 132),
    (54, 162, 235),
    (255, 206, 86),
    (75, 192, 192),
    (153, 102, 255),
    (255, 159, 64),
]

# ------------------ IMAGES ------------------
# 画像読み込み
try:
    bg_home   = pygame.image.load("home.png")
    bg_choice = pygame.image.load("choice.png")
    bg_game   = pygame.image.load("game.png")
    bg_result = pygame.image.load("result.png")
    target_img = pygame.image.load("target.png")
    start_img  = pygame.image.load("start.png")
    easy_img   = pygame.image.load("easy.png")
    medium_img = pygame.image.load("medium.png") 
    hard_img   = pygame.image.load("hard.png")
    replay_img = pygame.image.load("replay.png")
    end_img    = pygame.image.load("end.png")
    close_img  = pygame.image.load("close.png") 
    
except FileNotFoundError as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# ------------------ SOUNDS ------------------
try:
    hitSound = pygame.mixer.Sound("hitsound.wav")
    missSound = pygame.mixer.Sound("misssound.wav")
    hitSound.set_volume(1)
    missSound.set_volume(1)
except:
    print("Sound files not found, running without sound.")
    class MockSound:
        def play(self): pass
        def set_volume(self, v): pass

hitSound.set_volume(1)
missSound.set_volume(1)

# ------------------ PARAMETERS ------------------
button_width  = int(screen.get_width() * 0.25)
button_height = int(button_width / 4)
TARGET_SIZE   = 175
target_img    = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))

# Hard Mode Specifics
DRAG_CIRCLE_RADIUS = 250
dragging_target = False
target_offset_x = 0
target_offset_y = 0

# Fonts
FONT       = pygame.font.SysFont(None, 128)
SMALL_FONT = pygame.font.SysFont(None, 82)
TINY_FONT  = pygame.font.SysFont(None, 32)

# ------------------ GAME STATE ------------------
game_state    = "home"   # home / choice / play_ready / play / hard_game / result / graph
game_mode     = None     # easy / medium / hard
total_targets = 0
current_round = 1        # 1st play, then 2, 3, ... for replays

clock = pygame.time.Clock()

# ------------------ LOGGING ------------------
LOG_FILE = "session_data.txt"

def reset_log():
    """Clear/create the log and reset round counter at the start of each session."""
    global current_round
    current_round = 1
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("round,trial,reaction_ms\n")

def log_trial(trial_num, reaction_ms):
    """Append one trial: current round + trial number + reaction time in ms."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{current_round},{trial_num},{reaction_ms:.2f}\n")
    print(f"[Round {current_round}] Logged trial {trial_num} with {reaction_ms:.2f} ms")

# ------------------ HELPER FUNCTIONS ------------------
def exit_game():
    pygame.quit()
    sys.exit()

def draw_text(text, pos, font=FONT, color=RED, align="center"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if align == "center":
        rect.center = pos
    elif align == "topleft":
        rect.topleft = pos
    screen.blit(surface, rect)

# ------------------ CLASSES ------------------
class Button:
    def __init__(self, image, x, y, width, height, action=None):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            temp_image = pygame.transform.scale(
                self.image,
                (int(self.rect.width*1.05), int(self.rect.height*1.05))
            )
            temp_rect = temp_image.get_rect(center=self.rect.center)
            surface.blit(temp_image, temp_rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

class ExitButton:
    def __init__(self):
        self.size = 60
        self.x = screen.get_width() - self.size - 25
        self.y = 50 # 画面上部に配置
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        # translucent background
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

class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.radius = random.randint(4, 8)
        self.color = random.choice([RED])
        self.speed = random.uniform(8, 16)
        self.angle = random.uniform(0, 360)
        self.life = random.randint(20, 40)

    def update(self):
        v = pygame.math.Vector2(1, 0).rotate(self.angle)
        self.x += self.speed * 0.8 * v.x
        self.y += self.speed * 0.8 * v.y
        self.speed *= 0.9
        self.life -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            alpha = max(50, int(255 * (self.life / 40)))
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

# Global UI Elements
exit_button = ExitButton()

# ------------------ SCREENS ------------------

def home_screen():
    global game_state
    reset_log()

    start_button = Button(
        start_img,
        screen.get_width()//2,
        int(screen.get_height()*0.8),
        button_width,
        button_height,
        lambda: set_game_state("choice")
    )

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
    global game_state
    
    # 3つのボタンを配置 (Easy, Medium, Hard)
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
                for button in buttons:
                    button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_choice, screen.get_size()), (0,0))
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def select_mode(mode):
    global game_mode, total_targets, game_state
    game_mode = mode
    total_targets = 20 # 全モード共通で20ターゲットとする（変更可能）
    
    if mode == "hard":
        set_game_state("hard_game")
    else:
        # Easy と Medium は通常のプレイ画面へ
        set_game_state("play_ready")

def new_target_for_mode(mode):
    # Hardモードは円の外側にターゲットを生成
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
        # Easy/Mediumは画面内にランダム
        x = random.randint(100, screen.get_width()-100-TARGET_SIZE)
        y = random.randint(100, screen.get_height()-100-TARGET_SIZE)
        return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)

# ------------------ PLAY GAME (EASY / MEDIUM) ------------------
def play_game():
    global game_state
    remaining_targets = total_targets
    start_time = None
    started = False
    
    target_rect = new_target_for_mode(game_mode)
    last_spawn_time = time.time()
    particles = []
    
    pygame.mouse.set_visible(False)

    while game_state == "play":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)

                # --- MEDIUM MODE Logic ---
                if game_mode == "medium":
                    # 最初のターゲットをクリックしてスタート
                    if not started and target_rect.collidepoint(mouse_pos):
                        started = True
                        start_time = time.time()
                    
                    if target_rect.collidepoint(mouse_pos):
                        pygame.mixer.Channel(1).play(hitSound)
                        # Log
                        reaction_ms = (time.time() - last_spawn_time) * 1000.0
                        trial_num = (total_targets - remaining_targets) + 1
                        log_trial(trial_num, reaction_ms)
                        
                        # Particles
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))
                            
                        remaining_targets -= 1
                        if remaining_targets == 0 and started:
                            avg_ms = (time.time() - start_time)/total_targets*1000
                            set_game_state("result")
                            result_screen(avg_ms)
                            return
                        
                        target_rect = new_target_for_mode(game_mode)
                        last_spawn_time = time.time()
                    else:
                        # Miss sound
                        if started: pygame.mixer.Channel(0).play(missSound)

        # --- EASY MODE Logic ---
        if game_mode == "easy":
            if target_rect.collidepoint(mouse_pos):
                if not started:
                    started = True
                    start_time = time.time()
                
                pygame.mixer.Channel(1).play(hitSound)
                
                reaction_ms = (time.time() - last_spawn_time) * 1000.0
                trial_num = (total_targets - remaining_targets) + 1
                log_trial(trial_num, reaction_ms)
                
                for _ in range(40):
                    particles.append(Particle(target_rect.center))
                
                remaining_targets -= 1
                if remaining_targets == 0 and started:
                    avg_ms = (time.time() - start_time)/total_targets*1000
                    set_game_state("result")
                    result_screen(avg_ms)
                    return
                
                target_rect = new_target_for_mode(game_mode)
                last_spawn_time = time.time()

        # Drawing
        screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        screen.blit(target_img, target_rect)
        draw_text(f"{remaining_targets}", (int(screen.get_width()*0.11), int(screen.get_height()*0.18)), SMALL_FONT, WHITE, align="center")

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0: particles.remove(p)

        # Custom Crosshair
        mx, my = mouse_pos
        pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not started:
             msg = "Click target to start" if game_mode=="medium" else "Move over target to start"
             draw_text(msg, (screen.get_width()//2, screen.get_height()//2), SMALL_FONT, WHITE)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

# ------------------ PLAY HARD GAME (DRAG) ------------------
def play_hard_game():
    global game_state, dragging_target, target_offset_x, target_offset_y
    remaining_targets = total_targets
    start_time = None
    started = False
    
    target_rect = new_target_for_mode("hard")
    drag_start_pos = target_rect.topleft
    last_spawn_time = time.time()
    particles = []
    
    pygame.mouse.set_visible(True) # Hardモードはマウスカーソル表示
    circle_center = (screen.get_width()//2, screen.get_height()//2)

    while game_state == "hard_game":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                
                if not started:
                    started = True
                    start_time = time.time()

                if target_rect.collidepoint(mouse_pos):
                    dragging_target = True
                    target_offset_x = mouse_pos[0] - target_rect.x
                    target_offset_y = mouse_pos[1] - target_rect.y
                    drag_start_pos = target_rect.topleft

            if event.type == MOUSEBUTTONUP:
                if dragging_target:
                    dragging_target = False
                    # Check drop zone
                    if math.dist(target_rect.center, circle_center) <= DRAG_CIRCLE_RADIUS:
                        pygame.mixer.Channel(1).play(hitSound)
                        for _ in range(40):
                            particles.append(Particle(target_rect.center))
                        
                        reaction_ms = (time.time() - last_spawn_time) * 1000.0
                        trial_num = (total_targets - remaining_targets) + 1
                        log_trial(trial_num, reaction_ms)
                        
                        remaining_targets -= 1
                        if remaining_targets == 0 and started:
                            avg_ms = (time.time() - start_time)/total_targets*1000
                            set_game_state("result")
                            result_screen(avg_ms)
                            return
                        
                        target_rect = new_target_for_mode("hard")
                        last_spawn_time = time.time()
                    else:
                        pygame.mixer.Channel(0).play(missSound)
                        target_rect.topleft = drag_start_pos # Reset position

        # Dragging logic
        if dragging_target:
            target_rect.x = mouse_pos[0] - target_offset_x
            target_rect.y = mouse_pos[1] - target_offset_y
            target_rect.x = max(0, min(target_rect.x, screen.get_width() - TARGET_SIZE))
            target_rect.y = max(0, min(target_rect.y, screen.get_height() - TARGET_SIZE))

        # Drawing
        screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        
        # Circle Zone
        DRAG_CIRCLE_RADIUS_DRAW = 150
        CIRCLE_DIAMETER = 2 * DRAG_CIRCLE_RADIUS_DRAW
        pygame.draw.circle(screen, WHITE, circle_center, DRAG_CIRCLE_RADIUS_DRAW, 5)
        s = pygame.Surface((CIRCLE_DIAMETER, CIRCLE_DIAMETER), pygame.SRCALPHA)
        pygame.draw.circle(s, (YELLOW[0], YELLOW[1], YELLOW[2], 50), (DRAG_CIRCLE_RADIUS_DRAW, DRAG_CIRCLE_RADIUS_DRAW), DRAG_CIRCLE_RADIUS_DRAW)
        screen.blit(s, (circle_center[0]-DRAG_CIRCLE_RADIUS_DRAW, circle_center[1]-DRAG_CIRCLE_RADIUS_DRAW))

        screen.blit(target_img, target_rect)
        draw_text(f"{remaining_targets}", (int(screen.get_width()*0.11), int(screen.get_height()*0.18)), SMALL_FONT, WHITE, align="center")

        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0: particles.remove(p)

        # Custom Crosshair
        mx, my = mouse_pos
        pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not started:
            draw_text("Drag targets into the circle", (screen.get_width()//2, screen.get_height()//2), SMALL_FONT, WHITE)

        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def start_replay():
    """Replay logic handling different modes."""
    global current_round, game_state
    current_round += 1
    if game_mode == "hard":
        set_game_state("hard_game")
    else:
        set_game_state("play_ready")

def on_end_button():
    set_game_state("graph")

def result_screen(avg_ms):
    global game_state
    pygame.mouse.set_visible(True)
    replay_button = Button(
        replay_img,
        screen.get_width()*0.35,
        screen.get_height()*0.8,
        button_width,
        button_height,
        start_replay
    )
    end_button = Button(
        end_img,
        screen.get_width()*0.65,
        screen.get_height()*0.8,
        button_width,
        button_height,
        on_end_button
    )
    buttons = [replay_button, end_button]

    while game_state=="result":
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                for button in buttons:
                    button.check_click(mouse_pos)

        screen.blit(pygame.transform.scale(bg_result, screen.get_size()), (0,0))
        draw_text(f"{avg_ms:.1f}",
                  (screen.get_width()*0.45, screen.get_height()*0.43),
                  FONT, WHITE)

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

# ------------------ GRAPH SCREEN (UPDATED) ------------------
def show_graph():
    global game_state

    # ---- load data from log file ----
    round_to_times = {}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            next(f)  # skip header
            for line in f:
                line = line.strip()
                if not line or "," not in line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                r_str, t_str, react_str = parts
                try:
                    r = int(r_str)
                    _t = int(t_str)
                    react = float(react_str)
                except ValueError:
                    continue
                round_to_times.setdefault(r, []).append(react)
    except FileNotFoundError:
        reset_log()
        set_game_state("home")
        return

    if not round_to_times:
        reset_log()
        set_game_state("home")
        return

    # ---- compute averages & best round ----
    avg_per_round = {r: sum(times) / len(times) for r, times in round_to_times.items()}
    best_round = min(avg_per_round, key=avg_per_round.get)
    best_avg = avg_per_round[best_round]

    # ---- pick visible rounds (Max 8) ----
    MAX_VISIBLE_ROUNDS = 8
    all_round_ids = sorted(round_to_times.keys())

    if len(all_round_ids) <= MAX_VISIBLE_ROUNDS:
        visible_round_ids = all_round_ids
    else:
        visible_set = set()
        visible_list = []
        visible_list.append(best_round)
        visible_set.add(best_round)
        for r in reversed(all_round_ids):
            if r not in visible_set:
                visible_list.append(r)
                visible_set.add(r)
            if len(visible_list) == MAX_VISIBLE_ROUNDS:
                break
        visible_round_ids = sorted(visible_list)

    visible_round_to_times = {r: round_to_times[r] for r in visible_round_ids}
    visible_avg_per_round = {r: avg_per_round[r] for r in visible_round_ids}

    # Scaling
    all_visible_times = [v for r in visible_round_ids for v in round_to_times[r]]
    min_t = min(all_visible_times)
    max_t = max(all_visible_times)
    if max_t == min_t:
        max_t += 10
        min_t -= 10

    # Layout
    W, H = screen.get_size()
    margin_left = 120
    margin_right = 80
    margin_bottom = 160
    banner_h = 100
    banner_rect = pygame.Rect(0, 0, W, banner_h)

    title_text = "Reaction Time per Trial"
    subtitle_text = f"Best Round: {best_round}  (~{best_avg:.0f} ms)   |   Showing: {len(visible_round_ids)} round(s)"

    def draw_shadow_text(text, pos, font, color, shadow=(0, 0, 0), offset=(2, 2), align="center"):
        s = font.render(text, True, shadow)
        r = s.get_rect()
        if align == "center":
            r.center = (pos[0] + offset[0], pos[1] + offset[1])
        elif align == "topleft":
            r.topleft = (pos[0] + offset[0], pos[1] + offset[1])
        screen.blit(s, r)
        draw_text(text, pos, font, color, align=align)

    # Legend Layout
    legend_area_left = margin_left
    legend_area_right = W - margin_right
    legend_inner_pad_x = 10
    legend_area_w = (legend_area_right - legend_area_left) - (legend_inner_pad_x * 2)
    legend_padding_y = 10
    legend_line_h = TINY_FONT.get_height() + 14
    COLS = 4
    rows = []
    for i in range(0, len(visible_round_ids), COLS):
        rows.append(visible_round_ids[i:i+COLS])
    legend_rows = max(1, len(rows))
    legend_height = legend_padding_y * 2 + legend_rows * legend_line_h
    margin_top = banner_h + legend_height + 20

    graph_w = W - margin_left - margin_right
    graph_h = H - margin_top - margin_bottom
    if graph_h < 50: graph_h = 50
    max_trials = max(len(times) for times in visible_round_to_times.values())

    # --- Close Button Logic (Updated to use Image Button) ---
    def on_close():
        reset_log()
        set_game_state("home")

    close_button = Button(
        close_img,
        W // 2,
        H - margin_bottom // 2,
        int(button_width * 1.15),   
        int(button_height * 1.15), 
        on_close
    )

    running = True
    while game_state == "graph" and running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT: exit_game()
            if event.type == MOUSEBUTTONDOWN:
                exit_button.check_click(mouse_pos)
                close_button.check_click(mouse_pos) # Buttonクラスのメソッドを使用

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                reset_log()
                set_game_state("home")
                running = False

        screen.fill(GREY)

        # Title Banner
        pygame.draw.rect(screen, (25, 25, 25), banner_rect)
        pygame.draw.line(screen, (80, 80, 80), (0, banner_h-1), (W, banner_h-1), 2)
        draw_shadow_text(title_text, (W // 2, 38), SMALL_FONT, WHITE)
        draw_shadow_text(subtitle_text, (W // 2, 78), TINY_FONT, WHITE, offset=(1, 1))

        # Legend
        legend_top = banner_h
        legend_bg = pygame.Rect(0, legend_top, W, legend_height)
        pygame.draw.rect(screen, (32, 32, 32), legend_bg)
        pygame.draw.line(screen, (80, 80, 80), (0, legend_top), (W, legend_top), 2)
        pygame.draw.line(screen, (80, 80, 80), (0, legend_top + legend_height), (W, legend_top + legend_height), 2)

        cell_w = legend_area_w / COLS
        y = legend_top + legend_padding_y
        for row in rows:
            mid_y = y + legend_line_h // 2
            for col_idx, r in enumerate(row):
                idx = visible_round_ids.index(r)
                color = ROUND_COLORS[idx % len(ROUND_COLORS)]
                txt = f"R{r}: {visible_avg_per_round[r]:.0f}ms"
                x0 = (legend_area_left + legend_inner_pad_x) + col_idx * cell_w
                pygame.draw.line(screen, color, (x0, mid_y), (x0 + 32, mid_y), 4)
                draw_text(txt, (x0 + 40, mid_y), TINY_FONT, WHITE, align="topleft")
            y += legend_line_h

        # Axes
        pygame.draw.rect(screen, LIGHT_GREY, (margin_left, margin_top, graph_w, graph_h), 2)

        # Y Axis
        grid_lines = 5
        for i in range(grid_lines + 1):
            frac = i / grid_lines
            y_line = margin_top + graph_h * (1 - frac)
            pygame.draw.line(screen, (80, 80, 80),
                             (margin_left, y_line), (margin_left + graph_w, y_line), 1)
            value = min_t + (max_t - min_t) * frac
            label = f"{value:.0f} ms"
            label_surf = TINY_FONT.render(label, True, WHITE)
            label_rect = label_surf.get_rect()
            label_rect.right = margin_left - 12
            label_rect.centery = y_line
            screen.blit(label_surf, label_rect)

        # X Axis
        for t in range(1, max_trials + 1):
            frac_x = (t - 1) / (max_trials - 1) if max_trials > 1 else 0.5
            x = margin_left + graph_w * frac_x
            pygame.draw.line(screen, (80, 80, 80),
                             (x, margin_top), (x, margin_top + graph_h), 1)
            draw_text(str(t), (x, margin_top + graph_h + 20), TINY_FONT, WHITE, align="center")

        draw_text("Trial Number",
                  (margin_left + graph_w / 2, margin_top + graph_h + 55),
                  TINY_FONT, WHITE, align="center")

        # Plot Lines
        for idx, r in enumerate(visible_round_ids):
            times = visible_round_to_times[r]
            color = ROUND_COLORS[idx % len(ROUND_COLORS)]
            points = []
            for i, v in enumerate(times):
                t_idx = i + 1
                frac_x = (t_idx - 1) / (max_trials - 1) if max_trials > 1 else 0.5
                x = margin_left + graph_w * frac_x
                frac_y = (v - min_t) / (max_t - min_t)
                y_plot = margin_top + graph_h * (1 - frac_y)
                points.append((x, y_plot))

            if len(points) >= 2:
                pygame.draw.lines(screen, color, False, points, 3)
            elif len(points) == 1:
                pygame.draw.circle(screen, color, (int(points[0][0]), int(points[0][1])), 4)

        # Draw Close Button (Updated)
        close_button.check_hover(mouse_pos)
        close_button.draw(screen)
        
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

# ------------------ STATE HELPER ------------------
def set_game_state(state):
    global game_state, dragging_target
    game_state = state
    dragging_target = False

# ------------------ MAIN LOOP ------------------
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
        pass 
    elif game_state=="graph":
        show_graph()