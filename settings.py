import os

# Размеры окна приложения
WIDTH = 1200
HEIGHT = 900

# Частота обновления экрана (FPS)
FPS = 60

# Фоновый цвет (RGB)
BG_COLOR = (240, 240, 240)

# Корневая папка проекта
BASE_DIR = os.path.dirname(__file__)

# Папка с ассетами (изображения, шрифты, звук)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Файл с фразами
PHRASES_FILE = os.path.join(BASE_DIR, "phrases.json")

# Файл с конфигурацией пользователя
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Изображение аватара (мама)
AVATAR_IMG = os.path.join(ASSETS_DIR, "avatar.png")

# Сколько секунд аватар остаётся полностью видимым
SHOW_INTERVAL = 99999

# Сколько секунд аватар остаётся полностью скрытым
HIDE_INTERVAL = 99999

# Длительность fade-in и fade-out (в секундах)
FADE_DURATION = 0.5

# Размеры кнопок
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 35

# Отступы между элементами UI
BUTTON_MARGIN = 10
UI_PADDING = 15

# Цвета кнопок и текста
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (180, 180, 180)
BUTTON_TEXT_COLOR = (0, 0, 0)
LABEL_TEXT_COLOR = (20, 20, 20)

# Шрифты (будет инициализирован в main.py)
FONT_NAME = None     # None — системный шрифт
FONT_SIZE = 24

# Коды пользовательских событий Pygame
USEREVENT_SHOW  = pygame_event_show = 24    # не конфликтует с Pygame
USEREVENT_HIDE  = pygame_event_hide = 25
USEREVENT_BLINK = pygame_event_hide = 26

# Индикация FPS в уголке экрана
SHOW_FPS = True

# Максимальное число языков (ограничение UI)
MAX_LANGUAGES = 10

# Версия приложения
APP_VERSION = "1.0.0"


