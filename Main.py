import pygame
import sys
import os
import random
import GolP
import arabic_reshaper
from bidi.algorithm import get_display

pygame.init()

# تنظیمات نمایش
HALF_WIDTH, HALF_HEIGHT = 1152, 648
FULL_WIDTH, FULL_HEIGHT = 1280, 720
is_fullscreen_bg = False

# مسیرها
BASE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(BASE_DIR, "font")
PHOTO_DIR = os.path.join(BASE_DIR, "Photos")

# بارگذاری فونت‌ها
FONT_PATH_YEKAN = os.path.join(FONT_DIR, "Yekan.ttf")
FONT_PATH_YEKAN_BOLD = os.path.join(FONT_DIR, "Yekan-Bold.ttf")
FONT_SMALL = pygame.font.Font(FONT_PATH_YEKAN, 24)
FONT_MEDIUM = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 36)
FONT_LARGE = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 48)
FONT_HUGE = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 70)
FONT_SCORE = pygame.font.Font(FONT_PATH_YEKAN_BOLD, 100)

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
HOVER_COLOR = (0, 255, 180)
BUTTON_COLOR = (60, 60, 60)
ORANGE = (255, 165, 0)
BACKGROUND_COLOR = (25, 25, 25)
NEON_ORANGE = (255, 165, 0)
NEON_BLUE = (0, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# صفحه نمایش اولیه
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("بازی گل یا پوچ")

# بارگذاری تصاویر
def load_background(path):
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    return None

background_full = load_background(os.path.join(PHOTO_DIR, "background_full.jpg"))
background_half = load_background(os.path.join(PHOTO_DIR, "background_half.jpg"))
clock = pygame.time.Clock()
FPS = 60


# متن فارسی
def render_text(text, font, color):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    return font.render(bidi_text, True, color)

# تغییر حالت پنجره
def set_window_mode(fullscreen):
    global screen, WIDTH, HEIGHT
    if fullscreen:
        screen = pygame.display.set_mode((FULL_WIDTH, FULL_HEIGHT), pygame.FULLSCREEN)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    else:
        screen = pygame.display.set_mode((HALF_WIDTH, HALF_HEIGHT))
        WIDTH, HEIGHT = HALF_WIDTH, HALF_HEIGHT

def draw_text(text, font, color, surface, x, y):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    rendered = font.render(bidi_text, True, color)
    surface.blit(rendered, rendered.get_rect(center=(x, y)))


# حالت تمام‌صفحه
def toggle_fullscreen():
    global is_fullscreen_bg
    is_fullscreen_bg = not is_fullscreen_bg
    #set_window_mode(is_fullscreen_bg)

# رسم پس‌زمینه با کیفیت بالا
def draw_background():
    if is_fullscreen_bg and background_full:
        bg_scaled = pygame.transform.smoothscale(background_full, (WIDTH, HEIGHT))
        screen.blit(bg_scaled, (0, 0))
    elif background_half:
        bg_scaled = pygame.transform.smoothscale(background_half, (WIDTH, HEIGHT))
        screen.blit(bg_scaled, (0, 0))
    else:
        screen.fill(BACKGROUND_COLOR)

# دکمه با افکت hover نرم
class Button:
    def __init__(self, text, y, callback):
        self.text = text
        self.y = y
        self.callback = callback
        self.rect = pygame.Rect(0, 0, 300, 60)
        self.color = BUTTON_COLOR
        self.hover_alpha = 0



    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        self.hover_alpha = min(self.hover_alpha + 15, 255) if is_hover else max(self.hover_alpha - 15, 0)

        color = [
            BUTTON_COLOR[i] + (HOVER_COLOR[i] - BUTTON_COLOR[i]) * self.hover_alpha // 255
            for i in range(3)
        ]
        pygame.draw.rect(surface, color, self.rect, border_radius=16)
        txt_surf = render_text(self.text, FONT_MEDIUM, BLACK if is_hover else WHITE)
        surface.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def update_pos(self, center_x):
        self.rect.center = (center_x, self.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


def show_rules():
    selected = None
    back = False
    scroll_offset = 0

    # این تابع وقتی در صفحه آموزش یا قوانین هستیم و می‌خوایم برگردیم به صفحه اصلی راهنماها
    def go_back_to_main_menu():
        nonlocal back
        back = True
        # اینجا می‌تونید کدی بزارید که منوی اصلی نمایش داده بشه

    # صفحه نمایش متن (آموزش یا قوانین)
    def show_text_screen(title, lines):
        scroll_offset = 0
        back = False  # فقط مخصوص این صفحه متن است

        def go_back_from_text_screen():
            nonlocal back
            back = True

        max_scroll = max(0, len(lines) * 40 + 120 - HEIGHT + 100)

        back_button = Button("بازگشت", HEIGHT - 60, go_back_from_text_screen)
        back_button.update_pos(WIDTH // 2)

        while not back:
            draw_background()
            draw_text(title, FONT_LARGE, BLACK, screen, WIDTH // 2, 40)
            draw_text("اسکرول کنید", FONT_SMALL, BLACK, screen, WIDTH // 20, 90)

            y_start = 120 - scroll_offset
            for line in lines:
                draw_text(line, FONT_SMALL, GRAY, screen, WIDTH // 2, y_start)
                y_start += 40

            back_button.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                back_button.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        go_back_from_text_screen()
                    elif event.key == pygame.K_UP:
                        scroll_offset = max(0, scroll_offset - 20)
                    elif event.key == pygame.K_DOWN:
                        scroll_offset = min(max_scroll, scroll_offset + 20)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        scroll_offset = max(0, scroll_offset - 20)
                    elif event.button == 5:  # Scroll down
                        scroll_offset = min(max_scroll, scroll_offset + 20)

    # دکمه‌ها برای انتخاب "آموزش" یا "قوانین"
    tutorial = [
        "**آموزش کامل بازی گل یا پوچ (نسخه دیجیتال)**",
        "",
        "1. بازی بین دو تیم 3 نفره انجام می‌شود که هر تیم یک سرگروه (اوستا) دارد.",
        "2. هدف اصلی حدس زدن محل قرارگیری \"گل\" (یک شیء کوچک) در دستان تیم مقابل است.",
        "3. تیم مخفی‌کننده گل را در دست یکی از اعضا پنهان می‌کند.",
        "4. تیم حدس‌زننده می‌تواند 3 بار از \"خالی بازی\" استفاده کند تا دست‌های خالی را حذف کند.",
        "5. اگر حدس درست باشد، تیم حدس‌زننده 1 امتیاز می‌گیرد و نوبت بعدی آنها گل را مخفی می‌کنند.",
        "6. اگر حدس اشتباه باشد، تیم مخفی‌کننده 1 امتیاز می‌گیرد.",
        "7. اگر تیم مقابل بدون استفاده از \"خالی بازی\" گل را حدس بزند، 2 امتیاز می‌گیرد.",
        "8. هر تیم می‌تواند از کارت‌های ویژه مانند \"گوی بزرگ\"، \"آنتن\" یا \"دوئل\" استفاده کند.",
        "9. وقتی یک تیم به 20 امتیاز برسد، باید \"شاه‌گل\" را تشخیص دهد.",
        "10. اگر شاه‌گل درست حدس زده شود، تیم برنده می‌شود، در غیر این صورت امتیازات صفر می‌شود.",
        "11. بازی تا رسیدن یک تیم به امتیاز از پیش تعیین شده (معمولاً 21) ادامه دارد.",
        "12. در نسخه دیجیتال شما می‌توانید با کلیدهای W/S و O/L امتیازات را تغییر دهید.",
        "13. با کلیک روی کارت‌های ویژه می‌توانید از آنها استفاده کنید.",
        "14. هر کارت اثر خاصی دارد، مثلاً \"گوی صدادار\" باعث می‌شود گل راحت‌تر پیدا شود.",
        "15. رابط بازی شامل صفحه امتیازات، لیست بازیکنان و کارت‌های قابل استفاده است.",
        "16. تیم برنده باید به امتیاز نهایی تعیین شده برسد.",
        "17. بازی دارای انیمیشن‌های جذاب برای کارت‌ها و نمایش برنده است.",
        "18. می‌توانید تعداد بازیکنان هر تیم را از 2 تا 5 نفر انتخاب کنید.",
        "19. نام تیم‌ها و بازیکنان قابل تنظیم است.",
        "20. در پایان بازی، صفحه برنده با جزئیات تیم و امتیاز نمایش داده می‌شود.",
    ]

    rules = [
        "**قوانین رسمی بازی گل یا پوچ (نسخه دیجیتال)**",
        "",
        "1. **تعداد بازیکنان**:",
        "   - دو تیم 3 نفره با یک سرگروه (اوستا) در هر تیم",
        "   - امکان تغییر تعداد بازیکنان از 2 تا 5 نفر وجود دارد",
        "",
        "2. **هدف بازی**:",
        "   - رسیدن به امتیاز تعیین شده (پیش فرض: 21 امتیاز)",
        "   - کسب امتیاز از طریق حدس صحیح محل گل",
        "",
        "3. **گردش بازی**:",
        "   - تیم شروع کننده به تصادف انتخاب می‌شود",
        "   - تیم اول گل را در دست یکی از اعضا مخفی می‌کند",
        "   - تیم مقابل باید محل گل را تشخیص دهد",
        "",
        "4. **مکانیک حدس زدن**:",
        "   - 3 فرصت \"خالی بازی\" برای حذف دست‌های خالی",
        "   - پس از 3 خالی بازی، باید حدس نهایی زده شود",
        "",
        "5. **سیستم امتیازدهی**:",
        "   - حدس معمولی صحیح: 1 امتیاز",
        "   - حدس یک‌ضرب (بدون خالی بازی): 2 امتیاز",
        "   - حدس اشتباه: 1 امتیاز برای تیم مخفی‌کننده",
        "",
        "6. **کارت‌های ویژه** (15 نوع مختلف):",
        "   - هر تیم 5 کارت تصادفی دریافت می‌کند",
        "   - هر بار فقط می‌توان یک کارت استفاده کرد",
        "   - نمونه کارت‌ها:",
        "     * گوی بزرگ: سخت‌تر کردن مخفی‌سازی",
        "     * آنتن: پرسش از حریف",
        "     * دوئل: رقابت تک به تک",
        "",
        "7. **مرحله حساس (شاه‌گل)**:",
        "   - هنگام رسیدن به 20 امتیاز فعال می‌شود",
        "   - باید گل را بدون خالی بازی حدس زد",
        "   - موفقیت: برد بازی",
        "   - شکست: بازگشت امتیاز به صفر",
        "",
        "8. **قوانین ویژه**:",
        "   - استفاده از هر کارت نیاز به تایید دارد",
        "   - بعد از هر امتیازگیری، کارت‌ها ریست می‌شوند",
        "   - در صورت تساوی، بازی تا 2 امتیاز دیگر ادامه می‌یابد",
        "",
        "9. **قوانین فنی**:",
        "   - تغییر امتیاز با کلیدهای W/S (تیم چپ) و O/L (تیم راست)",
        "   - کلیک روی کارت‌ها برای فعال‌سازی اثر آنها",
        "   - امکان تنظیم امتیاز نهایی قبل از شروع بازی",
        "",
        "10. **پایان بازی**:",
        "    - نمایش صفحه برنده با مشخصات تیم",
        "    - نمایش کارت‌های استفاده شده",
        "    - امکان شروع مجدد بازی وجود دارد",
        "",
        "**نکته**: تمام قوانین در حین بازی قابل مشاهده و پیگیری هستند.",
    ]

    tutorial_button = Button("آموزش", HEIGHT // 2 - 60, lambda: show_text_screen("آموزش بازی", tutorial))
    rules_button = Button("قوانین", HEIGHT // 2 + 10, lambda: show_text_screen("قوانین بازی", rules))
    back_button = Button("بازگشت", HEIGHT - 60, go_back_to_main_menu)

    tutorial_button.update_pos(WIDTH // 2)
    rules_button.update_pos(WIDTH // 2)
    back_button.update_pos(WIDTH // 2)

    while not back:
        draw_background()
        draw_text("راهنمای بازی", FONT_LARGE, BLACK, screen, WIDTH // 2, 50)

        tutorial_button.draw(screen)
        rules_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            tutorial_button.handle_event(event)
            rules_button.handle_event(event)
            back_button.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                go_back_to_main_menu()







def show_cards():
    back = False
    selected_card = None
    animation_progress = 0

    def go_back():
        nonlocal back
        back = True

    back_button = Button("بازگشت", HEIGHT - 50, go_back)
    back_button.update_pos(WIDTH // 2)

    cards_info = [
        ("کارت دو گله", [
            "کارت زمانی استفاده میشود که 6 (تمام دست های بازی) دست باقی مانده باشد و قبل از شروع دور بازی باشد",
            "این کارت تیم مخفی کننده را موجاب میکند با دو گل بازی کنند"
        ]),
        ("چپ راست", [
            "این کارت زمانی استفاده میشود که حداقل 4 دست باقی مانده باشد یعنی دو نفر با دو دست",
            "اوستا تیم حدس زننده باید از یک نفر بپرسد گل چپ است یا راست",
            "اگر شخص گل داشته باشد موظف است دست گل را بگوید و در غیر این صورت می‌تواند الکی بگوید"
        ]),
        ("گفتگو مرگبار", [
            "زمانی این کارت استفاده میشود که 6 (تمام دست های بازی) دست باقی مانده باشد",
            "این کارت را اوستا تیم حدس زننده میتواند بگذارد و یک نفر از تیم مخفی کننده را انتخاب کند",
            "آن فرد باید دوتا حقیقت راجع به گل بگوید؛ یکی راست و یکی دروغ",
            "تیم حدس زننده باید تشخیص دهد کدام راست و کدام دروغ است",
            "نمی‌تواند دوتا را راست یا دوتا را دروغ بگوید"
        ]),
        ("کارت 2 به 4", [
            "زمانی این کارت استفاده میشود که حداقل 6 دست باقی مانده باشد",
            "این کارت یک نفر از تیم مخفی کننده را مجاب میکند دوتا دست خود را در دست اوستا بریزد",
            "حتی زمانی که اوستا دو دست پر داشته باشد"
        ]),
        ("خیانت", [
            "زمانی که تمام دست های بازی باقی مانده باشد",
            "این کارت برای این است که وقتی به یک نفر شک دارید می‌توانید او را مجاب به خیانت کنید",
            "این کارت روی دست اوستا کار نمیکند",
            "اگر دست چپ با راست گل داشته باشد باید بدهد و تک ضرب هم اضافه می‌شود",
            "اگر نداشته باشد جفت پوچ می‌شود و بازی ادامه پیدا می‌کند",
            "اگر در ادامه دست بعدی را پوچ نزنید و گل بزنید، مستقیم تک ضرب زده می‌شود"
        ]),
        ("دست شکسته", [
            "زمانی این کارت استفاده میشود که بازی یا دور جدید هنوز شروع نشده و باید در دور قبلی گذاشته شود",
            "همه باید فقط با یک دست بازی کنند حتی اوستا",
            "در صورت یک ضرب زدن گل بین همان 3 دست، تک ضرب حساب می‌شود",
            "اگر پوچ بدهید چه گل را بگیرید یک امتیاز به تیم مخفی کننده میرسد",
            "اگر پوچ بدهید و نگیرید هیچ امتیازی رد و بدل نمی‌شود"
        ]),
        ("گل نامرئی", [
            "هنگامی که این کارت گذاشته میشود در دور قبل باید باشد",
            "این کارت تیم مخفی کننده را مجاب می‌کند بدون گل بازی کنند",
            "یا گل فقط دست اوستا باشد",
            "اگر تیم حدس زننده متوجه شود تیم مقابل گل ندارد باید تمام دست‌ها را پوچ اعلام کند یا شش پوچ بدهد",
            "در این صورت فقط گل می‌رود و امتیازی رد و بدل نمی‌شود",
            "اگر شک کنند یا متوجه دست اوستا شوند میتوانند یک ضرب بزنند و گل یک ضرب با ۲ امتیاز به این سمت می‌آید"
        ]),
        ("شکارچی", [
            "زمانی که شش دست باقی مانده باشد",
            "این کارت را زمانی که تیم حدس زننده بگذارد فقط اوستا آنها باید 3 دست را پوچ اعلام کند",
            "اگر گل در بیاید بدون رد و بدل امتیاز گل می‌رود",
            "اگر گل در نیاید بازی ادامه پیدا می‌کند"
        ]),
        ("قفل بد", [
            "باید قبل از دور استفاده شود",
            "اگر با این کارت بتوانید گل را بگیرید 4 امتیاز برای شما حساب می‌شود حتی با پوچ",
            "اگر موفق به گرفتن گل نشوید 2 امتیاز به تیم حریف می‌دهید",
            "و 2 دست نمی‌توانید کارت بگذارید"
        ]),
        ("سنگ طلایی شاه", [
            "این کارت فقط و فقط در شاه گل استفاده میشود و مخصوص شاه گل است",
            "زمانی که این کارت بگذارید در شاه گل می‌توانید دو دست را گل اعلام کنید",
            "پنج بار گل می‌گیرید و دوبار آخر آن دو دستی است که می‌خواهید گل باشد",
            "اگر گل بود که می‌آید این طرف و از آن تیم بجای 3 امتیاز 1 امتیاز کم می‌شود",
            "اگر گل نبود شاه گل مجدد انجام می‌شود"
        ]),
        ("آنتن", [
            "زمانی که حداقل 3 دست باقی مانده باشد",
            "حقیقت را با بله و خیر از یک نفر بپرسید"
        ]),
        ("دوئل", [
            "ماندن 6 دست (تمام دست های بازی)",
            "دو نفر مقابل هم که گل دارند مقابل هم دوئل میروند"
        ]),
        ("یک تیر و دو نشان", [
            "زمانی که حداقل شش (تمام دست های بازی) دست مانده باشد",
            "گل را یک ضرب بزنید و در صورت گل نبودن بازی ادامه دارد"
        ]),
        ("حذف یک دست", [
            "زمانی که 3 دست باقی مانده باشد",
            "با گذاشتن این کارت اوستا تیم مخفی کننده باید یک دست از تیم خود را پوچ اعلام کند"
        ])
    ]

    card_width, card_height = 200, 80
    margin_x, margin_y = 20, 40
    cols = 5
    rows = 3

    start_x = (WIDTH - (cols * card_width + (cols - 1) * margin_x)) // 2
    start_y = (HEIGHT - (rows * card_height + (rows - 1) * margin_y + 100)) // 2

    cards = []
    for i, (title, desc_lines) in enumerate(cards_info):
        row = i // cols
        col = i % cols

        x = start_x + col * (card_width + margin_x)
        y = start_y + row * (card_height + margin_y)
        rect = pygame.Rect(x, y, card_width, card_height)
        cards.append((rect, title, desc_lines))

    def close_modal():
        nonlocal selected_card, animation_progress
        selected_card = None
        animation_progress = 0

    modal_back_button = Button("بازگشت", HEIGHT - 60, close_modal)
    modal_back_button.update_pos(WIDTH // 2)

    PURPLE_LIGHT = (130, 60, 130)

    clock = pygame.time.Clock()

    def split_text(text, max_chars=40):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    while not back:
        dt = clock.tick(60) / 1000

        draw_background()

        if selected_card is None:
            draw_text("کارت‌ها", FONT_LARGE, ORANGE, screen, WIDTH // 2, 50)

            for rect, title, desc_lines in cards:
                pygame.draw.rect(screen, WHITE, rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

                title_surf = render_text(title, FONT_SMALL, BLACK)
                screen.blit(title_surf, title_surf.get_rect(center=rect.center))

            back_button.draw(screen)

        else:
            animation_speed = 4
            if animation_progress < 1:
                animation_progress += animation_speed * dt
                if animation_progress > 1:
                    animation_progress = 1

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(180 * animation_progress)))
            screen.blit(overlay, (0, 0))

            modal_max_width, modal_max_height = WIDTH * 0.7, HEIGHT * 0.7
            w = int(modal_max_width * animation_progress)
            h = int(modal_max_height * animation_progress)
            modal_rect = pygame.Rect(
                (WIDTH - w) // 2,
                (HEIGHT - h) // 2,
                w,
                h
            )
            pygame.draw.rect(screen, WHITE, modal_rect, border_radius=20)
            pygame.draw.rect(screen, BLACK, modal_rect, 3, border_radius=20)

            if animation_progress == 1:
                title_surf = render_text(selected_card[1], FONT_SMALL, PURPLE_LIGHT)
                screen.blit(title_surf, title_surf.get_rect(center=(modal_rect.centerx, modal_rect.top + 30)))

                lines = []
                for paragraph in selected_card[2]:
                    lines.extend(split_text(paragraph, max_chars=40))

                lines = lines[:9]

                line_height = FONT_SMALL.get_height() + 6
                start_text_y = modal_rect.top + 60

                for i, line in enumerate(lines):
                    text_surf = render_text(line, FONT_SMALL, PURPLE_LIGHT)
                    screen.blit(text_surf, text_surf.get_rect(topleft=(modal_rect.left + 20, start_text_y + i * line_height)))

                modal_back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if selected_card is None:
                back_button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for rect, title, desc_lines in cards:
                        if rect.collidepoint(mouse_pos):
                            selected_card = (rect, title, desc_lines)
                            animation_progress = 0
                            break

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    back = True
            else:
                modal_back_button.handle_event(event)










def show_about():
    back = False
    animation_progress = 0

    def go_back():
        nonlocal back
        back = True

    header_lines = [
        "بازی گل یا پوچ",
        "نام سازنده: علیرضا امجدی",
        "سال ساخت: 1404 / 2025",
    ]

    about_lines = [
        "بازی «گل یا پوچ» یک بازی کاملاً ایرانی است که تصمیم گرفتم",
        "نسخه دیجیتال آن را بسازم تا تجربه بازی فیزیکی را دیجیتال کنم.",
        "سیستم کارت‌ها و امتیازدهی دقیق ثبت شده و از تاریخچه ارزشمند",
        "آن در فرهنگ ایرانی حمایت می‌کنم. امیدوارم از بازی لذت ببرید.",
        "نسخه موبایل را زمانی خواهم ساخت که با برنامه‌نویسی اندروید آشنا شوم."
    ]

    back_button = Button("بازگشت", HEIGHT - 80, go_back)
    back_button.update_pos(WIDTH // 2)

    clock = pygame.time.Clock()

    while not back:
        dt = clock.tick(60) / 1000
        if animation_progress < 1:
            animation_progress += dt * 1.5
            if animation_progress > 1:
                animation_progress = 1

        draw_background()

        padding = 30
        total_lines = len(header_lines) + len(about_lines)
        line_height = FONT_SMALL.get_height() + 20
        total_height = total_lines * line_height
        rect_width = WIDTH * 0.8
        rect_height = total_height + padding * 2
        rect_x = (WIDTH - rect_width) // 2

        start_y = HEIGHT + rect_height
        end_y = (HEIGHT - rect_height) // 2
        rect_y = start_y - (start_y - end_y) * animation_progress

        overlay_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        overlay_surf.fill((255, 255, 255, 180))  # سفید کم‌رنگ شفاف
        screen.blit(overlay_surf, (rect_x, rect_y))

        draw_text("درباره بازی", FONT_LARGE, (0, 0, 139), screen, WIDTH // 2, 30)

        y = rect_y + padding
        for line in header_lines:
            draw_text(line, FONT_MEDIUM, BLACK, screen, WIDTH // 2, y)
            y += line_height

        for line in about_lines:
            draw_text(line, FONT_SMALL, GRAY, screen, WIDTH // 2, y)
            y += line_height

        back_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            back_button.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                back = True










# Callbackهای منو
def start_game():
    GolP.main()


sys.stdout.reconfigure(encoding='utf-8')







def show_settings():
    print("تنظیمات")

def exit_game():
    pygame.quit()
    sys.exit()



# تعریف دکمه‌ها
buttons = [
    Button("شروع بازی", 150, start_game),
    Button("قوانین", 220, show_rules),
    Button("کارت ها", 290, show_cards),
    Button("درباره بازی", 360, show_about),
    Button("عوض کردن زمینه", 430, toggle_fullscreen),
    Button("تنظیمات(بزودی)", 500, show_settings),
    Button("خروج", 570, exit_game)
]

# منوی اصلی
def main_menu():
    global WIDTH, HEIGHT
    while True:
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (3,4,5,6,7):
                continue
            for btn in buttons:
                btn.handle_event(event)

        # عنوان
        title = render_text("بازی گل یا پوچ", FONT_LARGE, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        for btn in buttons:
            btn.update_pos(WIDTH // 2)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)



if __name__ == "__main__":
    main_menu()
