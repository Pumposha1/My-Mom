import pygame, sys
from settings import *
from config import Config
from phrase_manager import PhraseManager
from avatar import Avatar
from ui import UI

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Your Mom App")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont(None, FONT_SIZE)

    # Инициализация конфигурации, фраз и аватара
    config = Config()
    pm     = PhraseManager()
    avatar = Avatar(position=(WIDTH//2, HEIGHT//2))
    avatar.show()         # сразу показываем «маму»
    ui     = UI(config, pm, avatar)

    last_phrase = ""
    last_audio = None  # Храним последний аудиофайл, чтобы не проигрывать его несколько раз

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Передаём событие перетаскивания в avatar
            avatar.handle_event(event)

            # Реакция на щелчок по маме
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if avatar.rect.collidepoint(event.pos):
                    # Получаем фразу для текущего языка
                    last_phrase = pm.get_random(config.language)

                    # Проигрываем звуковую фразу
                    if last_phrase != "" and last_audio != last_phrase:
                        # Прогоняем аудиофайл для фразы
                        last_audio = last_phrase
                        pm.play_audio(config.language, last_phrase)

            # Передаём все события вашему UI
            ui.handle_event(event)

        # Обновляем «маму»
        avatar.update(dt, config.show_interval, config.hide_interval)

        # Если «мама» полностью исчезла — сбрасываем фразу
        if avatar.alpha == 0:
            last_phrase = ""

        # Рисуем всё
        screen.fill(BG_COLOR)
        avatar.draw(screen)
        ui.draw(screen)

        # Выводим фразу над головой
        if last_phrase and avatar.alpha > 0:
            txt = font.render(last_phrase, True, LABEL_TEXT_COLOR)
            txt.set_alpha(int(avatar.alpha))
            rect = txt.get_rect(midbottom=(avatar.rect.centerx, avatar.rect.top - 10))
            screen.blit(txt, rect)

        # FPS (опционально)
        if SHOW_FPS:
            fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, LABEL_TEXT_COLOR)
            screen.blit(fps_text, (WIDTH-100, HEIGHT-FONT_SIZE-5))

        pygame.display.flip()

    config.save()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
