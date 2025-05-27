import pygame
import sys
import os
import random
import arabic_reshaper
from bidi.algorithm import get_display



pygame.init()

WIDTH, HEIGHT = 1152, 648
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("بازی گل یا پوچ")
background_path = os.path.join("Photos", "Background_gol.jpg")
background_image = pygame.image.load(background_path).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

BASE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(BASE_DIR, "font")

FONT_PATH_YEKAN = os.path.join(FONT_DIR, "Yekan.ttf")
FONT_PATH_YEKAN_BOLD = os.path.join(FONT_DIR, "Yekan-Bold.ttf")
FONT_PATH_VAZIR = os.path.join(FONT_DIR, "Vazir.ttf")

def load_font(paths, size):
    for path in paths:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except:
                continue
    return pygame.font.SysFont("Arial", size)

FONT_SMALL = load_font([FONT_PATH_YEKAN, FONT_PATH_VAZIR], 20)
FONT_MEDIUM = load_font([FONT_PATH_YEKAN_BOLD, FONT_PATH_VAZIR], 30)
FONT_LARGE = load_font([FONT_PATH_YEKAN_BOLD, FONT_PATH_VAZIR], 48)
FONT_HUGE = load_font([FONT_PATH_YEKAN_BOLD, FONT_PATH_VAZIR], 70)
FONT_SCORE = load_font([FONT_PATH_YEKAN_BOLD, FONT_PATH_VAZIR], 100)  # سایز بزرگ‌تر، مثلاً 70



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
NEON_ORANGE = (255, 165, 0)
NEON_BLUE = (0, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

def render_text(text, font, color):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    return font.render(bidi_text, True, color)

def get_text_input(prompt, only_chars=False):
    input_text = ""
    active = True
    while active:
        screen.blit(background_image, (0, 0))
        prompt_surf = render_text(prompt + input_text, FONT_MEDIUM, WHITE)
        screen.blit(prompt_surf, (50, HEIGHT//2 - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    char = event.unicode
                    if only_chars:
                        if char.isalpha() or char == ' ':
                            input_text += char
                    else:
                        input_text += char

        pygame.display.flip()
        clock.tick(FPS)
    return input_text.strip()

def choose_num_players():
    options = ["2", "3", "4", "5"]
    selected = 0
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        title = render_text("انتخاب تعداد بازیکنان هر تیم", FONT_HUGE, NEON_ORANGE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(options):
            color = CYAN if i == selected else GRAY
            opt_surf = render_text(option + "v" + option, FONT_LARGE, color)
            screen.blit(opt_surf, (WIDTH//2 - opt_surf.get_width()//2, 250 + i * 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return int(options[selected])

        pygame.display.flip()
        clock.tick(FPS)

def get_teams_and_players(num_players):
    team1_name = get_text_input("نام تیم اول را وارد کنید (فقط حروف): ", only_chars=True)
    team2_name = get_text_input("نام تیم دوم را وارد کنید (فقط حروف): ", only_chars=True)

    team1_players = []
    team2_players = []

    for i in range(num_players):
        p1 = get_text_input(f"نام بازیکن {i+1} تیم {team1_name}: ", only_chars=True)
        team1_players.append(p1)

    for i in range(num_players):
        p2 = get_text_input(f"نام بازیکن {i+1} تیم {team2_name}: ", only_chars=True)
        team2_players.append(p2)

    def get_osta(team_name, players):
        while True:
            osta_name = get_text_input(f"نام اوستا تیم {team_name} : ", only_chars=True)
            if osta_name in players:
                return osta_name
            else:
                for _ in range(3):
                    screen.blit(background_image, (0, 0))
                    err = render_text(f"اوستا باید یکی از بازیکنان تیم {team_name} باشد!", FONT_MEDIUM, WHITE)
                    screen.blit(err, err.get_rect(center=(WIDTH//2, HEIGHT//2)))
                    pygame.display.flip()
                    pygame.time.delay(500)
                    screen.blit(background_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(500)

    team1_osta = get_osta(team1_name, team1_players)
    team2_osta = get_osta(team2_name, team2_players)

    return team1_name, team1_players, team1_osta, team2_name, team2_players, team2_osta

def draw_scoreboard(team1_name, score1, team2_name, score2):
    rect_width = 400
    rect_height = 150
    rect_x = WIDTH//2 - rect_width//2
    rect_y = 30
    pygame.draw.rect(screen, GRAY, (rect_x, rect_y, rect_width, rect_height), border_radius=20)

    score1_color = WHITE if score1 < 5 else YELLOW
    score2_color = WHITE if score2 < 5 else YELLOW

    score1_surf = render_text(str(score1), FONT_SCORE, score1_color)
    score2_surf = render_text(str(score2), FONT_SCORE, score2_color)


    screen.blit(score1_surf, (rect_x + 40, rect_y + -6))
    screen.blit(score2_surf, (rect_x + rect_width - 120, rect_y + -6))


    team1_surf = render_text(team1_name, FONT_SMALL, NEON_ORANGE)
    team2_surf = render_text(team2_name, FONT_SMALL, NEON_ORANGE)

    screen.blit(team1_surf, (rect_x + 40 + (score1_surf.get_width()//2) - (team1_surf.get_width()//2), rect_y + 110))
    screen.blit(team2_surf, (rect_x + rect_width - 120 + (score2_surf.get_width()//2) - (team2_surf.get_width()//2), rect_y + 110))

def animate_card_removal(card_text):
    # انیمیشن طولانی‌تر (1 ثانیه)
    card_font_start = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 40)
    card_font_end = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 140)
    duration = FPS  # 60 فریم برای 1 ثانیه
    for i in range(duration):
        screen.blit(background_image, (0, 0))
        font_size = int(40 + (140 - 40) * (i / duration))
        font = pygame.font.Font(FONT_PATH_YEKAN_BOLD, font_size)
        text_surf = render_text(card_text, font, NEON_ORANGE)
        rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surf, rect)
        pygame.display.flip()
        clock.tick(FPS)

def show_winner_screen(team_name, osta_name, players, used_cards):
    # بارگذاری تصاویر جام و ستاره
    trophy_img = pygame.image.load("Photos/trophy.png").convert_alpha()
    trophy_img = pygame.transform.smoothscale(trophy_img, (180, 180))
    star_img = pygame.image.load("Photos/star.png").convert_alpha()
    star_img = pygame.transform.smoothscale(star_img, (30, 30))
    
    running = True
    while running:
        screen.blit(background_image, (0, 0))

        # جام بالا وسط صفحه (واقعاً بالا)
        trophy_rect = trophy_img.get_rect(center=(WIDTH // 2, 100))  # قبلاً 180 بود
        screen.blit(trophy_img, trophy_rect)

        # عنوان برنده (بدون ایموجی، یا با ایموجی کم)
        title_text = f"تیم {team_name} با رهبری {osta_name} برنده شد!"
        title_surf = render_text(title_text, FONT_HUGE, YELLOW)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, trophy_rect.bottom + 40))
        screen.blit(title_surf, title_rect)

        # اوستا + ستاره
        osta_text = f"رهبر تیم (اوستا): {osta_name}  "
        osta_surf = render_text(osta_text, FONT_MEDIUM, CYAN)
        osta_rect = osta_surf.get_rect(topleft=(50, title_rect.bottom + 30))
        screen.blit(osta_surf, osta_rect)

        star_pos = (osta_rect.right + 5, osta_rect.top + (osta_rect.height - star_img.get_height()) // 2)
        screen.blit(star_img, star_pos)

        # بازیکنان
        players_text = " بازیکنان: " + "، ".join(players)
        players_surf = render_text(players_text, FONT_MEDIUM, WHITE)
        screen.blit(players_surf, (50, osta_rect.bottom + 20))

        # پیام پایانی پایین صفحه
        msg = " تبریک! قدرت، استراتژی و اتحاد تیم شما را به پیروزی رساند. به راهتان ادامه دهید! "
        msg_surf = render_text(msg, FONT_SMALL, NEON_ORANGE)
        screen.blit(msg_surf, (50, HEIGHT - 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def show_players(team1_name, team1_players, team1_osta, team2_name, team2_players, team2_osta, win_score):
    CARDS = [
        "سنگ مفت گنجشک مفت",
        "کارت دو گله",
        "چپ راست",
        "گفتگو مرگبار",
        "کارت 2 به 4",
        "خیانت",
        "دست شکسته",
        "گل نامرعی",
        "شکارچی",
        "قفل بد",
        "سنگ طلایی شاه",
        "آنتن",
        "دوئل",
        "یک تیر و دو نشان",
        "حذف یک دست"
    ]

    team1_cards = random.sample(CARDS, 5)
    team2_cards = random.sample(CARDS, 5)

    score1, score2 = 0, 0
    can_use_card_team1 = True
    can_use_card_team2 = True
    used_cards_team1 = []
    used_cards_team2 = []

    card_font = pygame.font.Font(FONT_PATH_YEKAN, 20)
    card_spacing = 24
    card_box_w, card_box_h = 220, 40

    while True:
        screen.blit(background_image, (0, 0))
        middle_x = WIDTH // 2

        # اسم تیم ها و بازیکنان بالای صفحه وسط
        t1_title = render_text(f"تیم {team1_name}", FONT_MEDIUM, NEON_ORANGE)
        screen.blit(t1_title, (middle_x - 500, 80))

        for i, p in enumerate(team1_players):
            p_surf = render_text(p, FONT_SMALL, WHITE)
            screen.blit(p_surf, (middle_x - 500, 120 + i * 30))

        osta_surf = render_text(team1_osta + "  :  اوستا ", FONT_SMALL, YELLOW)
        screen.blit(osta_surf, (middle_x - 500, 120 + len(team1_players) * 30))

        t2_title = render_text(f"تیم {team2_name}", FONT_MEDIUM, NEON_ORANGE)
        screen.blit(t2_title, (middle_x + 350, 80))

        for i, p in enumerate(team2_players):
            p_surf = render_text(p, FONT_SMALL, WHITE)
            screen.blit(p_surf, (middle_x + 350, 120 + i * 30))

        osta2_surf = render_text(team2_osta + "  :  اوستا ", FONT_SMALL, YELLOW)
        screen.blit(osta2_surf, (middle_x + 350, 120 + len(team2_players) * 30))

        # نمره ها وسط بالا
        draw_scoreboard(team1_name, score1, team2_name, score2)
        # راهنمای کلید ها
        help1 = render_text("اضافه کردن امتیاز  W   |   کم کردن امتیاز  S", FONT_SMALL, WHITE)
        help2 = render_text("اضافه کردن امتیاز  O   |   کم کردن امتیاز  L", FONT_SMALL, WHITE)
        screen.blit(help1, (50, 10))
        screen.blit(help2, (WIDTH - help2.get_width() - 50, 10))


        # کارت های تیم ها - بالاتر از قبل
        team1_card_rects = []
        base_y_team1 = HEIGHT - 265  # بالاتر کارت ها
        base_x_team1 = 50 
        for i, card in enumerate(team1_cards):
            rect = pygame.Rect(base_x_team1, base_y_team1 + i * (card_box_h + 10), card_box_w, card_box_h)
            pygame.draw.rect(screen, CYAN, rect, border_radius=5)
            text_surf = render_text(card, card_font, BLACK)
            screen.blit(text_surf, (rect.x + 5, rect.y + 3))
            team1_card_rects.append((rect, card))

        team2_card_rects = []
        base_y_team2 = HEIGHT - 265  # بالاتر کارت ها
        base_x_team2 = WIDTH - card_box_w - 50
        for i, card in enumerate(team2_cards):
            rect = pygame.Rect(base_x_team2, base_y_team2 + i * (card_box_h + 10), card_box_w, card_box_h)
            pygame.draw.rect(screen, NEON_ORANGE, rect, border_radius=5)
            text_surf = render_text(card, card_font, BLACK)
            screen.blit(text_surf, (rect.x + 5, rect.y + 3))
            team2_card_rects.append((rect, card))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # کارت فقط وقتی مجازه که تیم مربوطه بتونه استفاده کنه
                # تیم 1
                if can_use_card_team1:
                    for i, (rect, card) in enumerate(team1_card_rects):
                        if rect.collidepoint(mouse_pos):
                            # حذف کارت از لیست و ثبت استفاده شده
                            used_cards_team1.append(card)
                            team1_cards.pop(i)
                            animate_card_removal(card)
                            can_use_card_team1 = False  # غیر فعال کردن کارت بعدی تا نمره تغییر کنه
                            break

                # تیم 2
                if can_use_card_team2:
                    for i, (rect, card) in enumerate(team2_card_rects):
                        if rect.collidepoint(mouse_pos):
                            used_cards_team2.append(card)
                            team2_cards.pop(i)
                            animate_card_removal(card)
                            can_use_card_team2 = False
                            break

            if event.type == pygame.KEYDOWN:
            
                
                old_score1, old_score2 = score1, score2

                if event.key == pygame.K_w:
                    score1 += 1
                elif event.key == pygame.K_s:
                    score1 = max(0, score1 - 1)
                elif event.key == pygame.K_o:
                    score2 += 1
                elif event.key == pygame.K_l:
                    score2 = max(0, score2 - 1)

                # اگر نمره تغییر کرد اجازه کارت بعدی رو بده
                if (score1 != old_score1) or (score2 != old_score2):
                    can_use_card_team1 = True
                    can_use_card_team2 = True

        # چک برد تیم
        if score1 >= win_score:
            show_winner_screen(team1_name, team1_osta, team1_players, used_cards_team1 + used_cards_team2)
            break
        elif score2 >= win_score:
            show_winner_screen(team2_name, team2_osta, team2_players, used_cards_team1 + used_cards_team2)
            break

        pygame.display.flip()
        clock.tick(FPS)

def get_win_score():
    while True:
        try:
            score = int(get_text_input("امتیاز نهایی برای برد را وارد کنید (عدد): "))
            if score > 0:
                return score
        except:
            pass

def main():
    num_players = choose_num_players()
    team1_name, team1_players, team1_osta, team2_name, team2_players, team2_osta = get_teams_and_players(num_players)
    global win_score
    win_score = get_win_score()
    show_players(team1_name, team1_players, team1_osta, team2_name, team2_players, team2_osta, win_score)

if __name__ == "__main__":
    main()
