"""
Модуль пользовательского интерфейса:
- Кнопки Button
- Слайдер Slider для регулировки громкости
- Метки Label
- Меню языков LanguageMenu
- Обработка событий и отрисовка всех компонентов
"""

import pygame
import logging
from settings import (
    WIDTH, HEIGHT,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, UI_PADDING,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
    LABEL_TEXT_COLOR, FONT_NAME, FONT_SIZE,
    APP_VERSION
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class UIComponent:
    """Базовый класс для всех UI-элементов."""
    def draw(self, surface):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError

class Button(UIComponent):
    """Кнопка с текстом и callback-функцией."""
    def __init__(self, x, y, w, h, text, callback):
        self.rect     = pygame.Rect(x, y, w, h)
        self.text     = text
        self.callback = callback
        self.font     = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.hovered  = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        txt_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                logger.debug("Button '%s' clicked", self.text)
                self.callback()

class Label(UIComponent):
    """Простая текстовая метка без фонового прямоугольника."""
    def __init__(self, x, y, text):
        self.pos  = (x, y)
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def draw(self, surface):
        txt_surf = self.font.render(self.text, True, LABEL_TEXT_COLOR)
        surface.blit(txt_surf, self.pos)

    def handle_event(self, event):
        pass  # Label не реагирует на события

class Slider(UIComponent):
    """
    Горизонтальный слайдер:
    - min_val, max_val — диапазон
    - length — длина полосы (px)
    - callback(value) вызывается при отпускании мыши
    """
    def __init__(self, x, y, length, height, min_val, max_val, start, callback):
        self.rect = pygame.Rect(x, y, length, height)
        self.handle_radius = height // 2
        self.min_val = min_val
        self.max_val = max_val
        self.value   = start
        self.callback = callback
        self.dragging = False

    def draw(self, surface):
        # рисуем полосу
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        # позиция ручки
        pos_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
        pos_y = self.rect.y + self.rect.h // 2
        pygame.draw.circle(surface, BUTTON_HOVER_COLOR if self.dragging else BUTTON_TEXT_COLOR,
                           (pos_x, pos_y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # проверить попадание внутрь ручки
            mx, my = event.pos
            pos_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
            pos_y = self.rect.y + self.rect.h // 2
            if (mx - pos_x)**2 + (my - pos_y)**2 <= self.handle_radius**2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            logger.debug("Slider released, value=%.2f", self.value)
            self.callback(self.value)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # передвинуть ручку по X
            rel_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w))
            proportion = (rel_x - self.rect.x) / self.rect.w
            self.value = self.min_val + proportion * (self.max_val - self.min_val)

class LanguageMenu(UIComponent):
    """Горизонтальное меню для выбора языка."""
    def __init__(self, x, y, languages, current_lang, callback):
        self.x = x
        self.y = y
        self.languages = languages
        self.current   = current_lang
        self.callback  = callback
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def draw(self, surface):
        # рисуем все языки в ряд
        offset = 0
        for lang in self.languages:
            txt_surf = self.font.render(lang, True,
                                        (0, 100, 0) if lang == self.current else LABEL_TEXT_COLOR)
            txt_rect = txt_surf.get_rect(topleft=(self.x + offset, self.y))
            surface.blit(txt_surf, txt_rect)
            offset += txt_rect.width + BUTTON_MARGIN

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            offset = 0
            for lang in self.languages:
                txt_surf = self.font.render(lang, True, LABEL_TEXT_COLOR)
                txt_rect = txt_surf.get_rect(topleft=(self.x + offset, self.y))
                if txt_rect.collidepoint(mx, my):
                    logger.debug("LanguageMenu: выбрали язык %s", lang)
                    self.current = lang
                    self.callback(lang)
                offset += txt_rect.width + BUTTON_MARGIN

class UI:
    """Главный контейнер всех UI-элементов."""
    def __init__(self, config, phrase_manager, avatar):
        self.config = config
        self.pm     = phrase_manager
        self.avatar = avatar
        self.components = []

        # Языковое меню
        langs = self.pm.list_languages()
        self.language_menu = LanguageMenu(
            UI_PADDING, UI_PADDING, langs, self.config.language, self._on_language_change
        )
        self.components.append(self.language_menu)

        # Кнопка переключения мамы
        btn_x = WIDTH - BUTTON_WIDTH - UI_PADDING
        btn_y = UI_PADDING
        self.toggle_btn = Button(
            btn_x, btn_y, BUTTON_WIDTH, BUTTON_HEIGHT,
            "Toggle Mom", self._on_toggle_mom
        )
        self.components.append(self.toggle_btn)

        # Слайдер громкости (куплепродажа TTS в будущем)
        slider_y = btn_y + BUTTON_HEIGHT + BUTTON_MARGIN
        self.volume_slider = Slider(
            btn_x, slider_y, BUTTON_WIDTH, BUTTON_HEIGHT//2,
            0.0, 1.0, self.config.volume, self._on_volume_change
        )
        self.components.append(self.volume_slider)

        # Метка версии
        version_label = Label(
            UI_PADDING, HEIGHT - FONT_SIZE - UI_PADDING,
            f"v{APP_VERSION}"
        )
        self.components.append(version_label)

    def _on_language_change(self, lang):
        """Callback при выборе языка."""
        try:
            self.config.update_language(lang)
            logger.info("Язык изменён на %s", lang)
        except Exception as e:
            logger.error("Не удалось изменить язык: %s", e)

    def _on_toggle_mom(self):
        """Callback кнопки Toggle Mom."""
        if self.avatar.visible:
            self.avatar.hide()
        else:
            self.avatar.show()

    def _on_volume_change(self, val):
        """Callback слайдера громкости."""
        self.config.volume = val
        logger.info("Громкость установлена на %.2f", val)

    def draw(self, surface):
        """Отрисовать все компоненты."""
        for comp in self.components:
            comp.draw(surface)

    def handle_event(self, event):
        """Передать событие всем компонентам."""
        for comp in self.components:
            comp.handle_event(event)
