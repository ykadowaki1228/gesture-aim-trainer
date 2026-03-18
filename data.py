# import pygame, random, sys, time
# from pygame.locals import *

# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Very Very Serious Game")

# # ------------------ COLORS ------------------
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED   = (255, 0, 0)
# GREY  = (40, 40, 40)
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

# # ------------------ IMAGES ------------------
# bg_home   = pygame.image.load("home.png")
# bg_choice = pygame.image.load("choice.png")
# bg_game   = pygame.image.load("game.png")
# bg_result = pygame.image.load("result.png")
# target_img = pygame.image.load("target.png")
# start_img  = pygame.image.load("start.png")
# easy_img   = pygame.image.load("easy.png")
# hard_img   = pygame.image.load("hard.png")
# replay_img = pygame.image.load("replay.png")
# end_img    = pygame.image.load("end.png")

# # ------------------ SOUNDS ------------------
# shootSound = pygame.mixer.Sound("snipersound.wav")
# hitSound   = pygame.mixer.Sound("metalHit.wav")
# shootSound.set_volume(0.25)
# hitSound.set_volume(1)

# ------------------ BUTTON / TARGET SIZE ------------------
# button_width  = int(screen.get_width() * 0.25)
# button_height = int(button_width / 4)
# TARGET_SIZE   = 175
# target_img    = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))

# # ------------------ FONTS ------------------
# FONT       = pygame.font.SysFont(None, 96)
# SMALL_FONT = pygame.font.SysFont(None, 64)
# TINY_FONT  = pygame.font.SysFont(None, 32)

# ------------------ GAME STATE ------------------
# game_state    = "home"   # home / choice / play_ready / play / result / graph
# game_mode     = None     # easy / hard
# total_targets = 0
# current_round = 1        # 1st play, then 2, 3, ... for replays

# clock = pygame.time.Clock()

# # ------------------ LOGGING ------------------
# LOG_FILE = "session_data.txt"

# def reset_log():
#     """Clear/create the log and reset round counter at the start of each session."""
#     global current_round
#     current_round = 1
#     with open(LOG_FILE, "w", encoding="utf-8") as f:
#         # round = replay number, trial = target index in that round
#         f.write("round,trial,reaction_ms\n")

# def log_trial(trial_num, reaction_ms):
#     """Append one trial: current round + trial number + reaction time in ms."""
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"{current_round},{trial_num},{reaction_ms:.2f}\n")
#     print(f"[Round {current_round}] Logged trial {trial_num} with {reaction_ms:.2f} ms")

# # ------------------ TEXT DRAWING ------------------
# def draw_text(text, pos, font=FONT, color=RED, align="center"):
#     surface = font.render(text, True, color)
#     rect = surface.get_rect()
#     if align == "center":
#         rect.center = pos
#     elif align == "topleft":
#         rect.topleft = pos
#     screen.blit(surface, rect)

# # ------------------ BUTTON CLASS ------------------
# class Button:
#     def __init__(self, image, x, y, width, height, action=None):
#         self.image = pygame.transform.scale(image, (width, height))
#         self.rect = self.image.get_rect(center=(x, y))
#         self.action = action
#         self.hovered = False

#     def draw(self, surface):
#         if self.hovered:
#             temp_image = pygame.transform.scale(
#                 self.image,
#                 (int(self.rect.width*1.05), int(self.rect.height*1.05))
#             )
#             temp_rect = temp_image.get_rect(center=self.rect.center)
#             surface.blit(temp_image, temp_rect.topleft)
#         else:
#             surface.blit(self.image, self.rect.topleft)

#     def check_hover(self, mouse_pos):
#         self.hovered = self.rect.collidepoint(mouse_pos)

#     def check_click(self, mouse_pos):
#         if self.rect.collidepoint(mouse_pos) and self.action:
#             self.action()

# # ------------------ SCREENS ------------------
# def home_screen():
#     """Home screen"""
#     global game_state

    # New overall session -> reset file + round counter
    # reset_log()

    # start_button = Button(
    #     start_img,
    #     screen.get_width()//2,
    #     int(screen.get_height()*0.8),
    #     button_width,
    #     button_height,
    #     lambda: set_game_state("choice")
    # )

    # while game_state == "home":
        # mouse_pos = pygame.mouse.get_pos()
        # for event in pygame.event.get():
            # if event.type == QUIT:
                # pygame.quit()
                # sys.exit()
            # if event.type == MOUSEBUTTONDOWN:
            #     start_button.check_click(mouse_pos)

        # screen.blit(pygame.transform.scale(bg_home, screen.get_size()), (0,0))
        # start_button.check_hover(mouse_pos)
        # start_button.draw(screen)

        # pygame.display.flip()
        # clock.tick(60)

# def choice_screen():
#     """Difficulty choice"""
#     global game_state, game_mode, total_targets
#     easy_button = Button(
#         easy_img,
#         screen.get_width()*0.35,
#         screen.get_height()*0.6,
#         button_width,
#         button_height,
#         lambda: select_mode("easy")
#     )
#     hard_button = Button(
#         hard_img,
#         screen.get_width()*0.65,
#         screen.get_height()*0.6,
#         button_width,
#         button_height,
#         lambda: select_mode("hard")
#     )
#     buttons = [easy_button, hard_button]

    # while game_state == "choice":
    #     mouse_pos = pygame.mouse.get_pos()
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == MOUSEBUTTONDOWN:
    #             for button in buttons:
    #                 button.check_click(mouse_pos)

        # screen.blit(pygame.transform.scale(bg_choice, screen.get_size()), (0,0))
        # for button in buttons:
        #     button.check_hover(mouse_pos)
        #     button.draw(screen)

        # pygame.display.flip()
        # clock.tick(60)

# def select_mode(mode):
#     global game_mode, total_targets, game_state
#     game_mode = mode
    # total_targets = 20 if mode=="easy" else 30
    # set_game_state("play_ready")

# def play_game():
#     """Main game loop (one round)"""
#     global game_state
#     remaining_targets = total_targets
#     targets_hit = 0
#     start_time = None
#     mouse_clicked = False
#     target_rect = new_target()
#     last_spawn_time = time.time()   # when THIS target appeared
#     pygame.mouse.set_visible(False)

    # while game_state=="play":
    #     mouse_pos = pygame.mouse.get_pos()
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == MOUSEBUTTONDOWN:
                # if not mouse_clicked:
                #     mouse_clicked = True
                #     start_time = time.time()
                # pygame.mixer.Channel(0).play(shootSound)

                # # HIT
                # if target_rect.collidepoint(mouse_pos):
                #     pygame.mixer.Channel(1).play(hitSound)

                    # per-target reaction time (ms)
                    reaction_ms = (time.time() - last_spawn_time) * 1000.0
                    trial_num = (total_targets - remaining_targets) + 1
                    log_trial(trial_num, reaction_ms)

                    targets_hit += 1
                    remaining_targets -= 1

                    # if remaining_targets==0:
                    #     avg_ms = (time.time()-start_time)/total_targets*1000
                    #     set_game_state("result")
                    #     result_screen(avg_ms)
                    #     return

                    # target_rect = new_target()
                    # last_spawn_time = time.time()

        # screen.blit(pygame.transform.scale(bg_game, screen.get_size()), (0,0))
        # screen.blit(target_img, target_rect)
        # draw_text(f"{remaining_targets}", (142,130), SMALL_FONT, WHITE, align="center")

        # # custom crosshair
        # mx,my = mouse_pos
        # pygame.draw.line(screen, WHITE, (mx-15,my),(mx+15,my),2)
        # pygame.draw.line(screen, WHITE, (mx,my-15),(mx,my+15),2)

        if not mouse_clicked:
            draw_text("Click target to start",
                      (screen.get_width()//2, screen.get_height()//2),
                      SMALL_FONT, WHITE)
        pygame.display.flip()
        clock.tick(60)

# def new_target():
#     x = random.randint(100, screen.get_width()-100-TARGET_SIZE)
#     y = random.randint(100, screen.get_height()-100-TARGET_SIZE)
#     return pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE)

# def start_replay():
#     """Action when Replay is pressed: go to next round and play again."""
#     global current_round, game_state
#     current_round += 1
#     game_state = "play_ready"

# def on_end_button():
#     """Action when END is pressed: go to graph screen."""
#     set_game_state("graph")

# def result_screen(avg_ms):
#     """Result screen (after one round)"""
#     global game_state
#     pygame.mouse.set_visible(True)
#     replay_button = Button(
#         replay_img,
#         screen.get_width()*0.35,
#         screen.get_height()*0.8,
#         button_width,
#         button_height,
#         start_replay         # new round, same log file
#     )
#     end_button = Button(
#         end_img,
#         screen.get_width()*0.65,
#         screen.get_height()*0.8,
#         button_width,
#         button_height,
#         on_end_button        # go to graph screen
#     )
#     buttons = [replay_button, end_button]

    # while game_state=="result":
    #     mouse_pos = pygame.mouse.get_pos()
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == MOUSEBUTTONDOWN:
    #             for button in buttons:
    #                 button.check_click(mouse_pos)

        # screen.blit(pygame.transform.scale(bg_result, screen.get_size()), (0,0))
        # draw_text(f"{avg_ms:.1f}",
        #           (screen.get_width()*0.45, screen.get_height()*0.43),
        #           FONT, WHITE)

        # for button 