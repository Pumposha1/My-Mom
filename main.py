# В main.py
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Your Mom App")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont(None, FONT_SIZE)

    config = Config()
    pm     = PhraseManager()
    avatar = Avatar(position=(WIDTH//2, HEIGHT//2))
    avatar.show()         # сразу показываем «маму»
    ui     = UI(config, pm, avatar)

    last_phrase = ""

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 1) реакция на щелчок по маме
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if avatar.rect.collidepoint(event.pos):
                    last_phrase = pm.get_random(config.language)

            # передаём все события вашему UI
            ui.handle_event(event)

        # обновляем «маму»
        avatar.update(dt, config.show_interval, config.hide_interval)

        # если «мама» полностью исчезла — сбрасываем фразу
        if avatar.alpha == 0:
            last_phrase = ""

        # рисуем всё
        screen.fill(BG_COLOR)
        avatar.draw(screen)
        ui.draw(screen)

        # выводим фразу над головой
        if last_phrase and avatar.alpha > 0:
            txt = font.render(last_phrase, True, LABEL_TEXT_COLOR)
            txt.set_alpha(int(avatar.alpha))
            rect = txt.get_rect(midbottom=(avatar.rect.centerx, avatar.rect.top - 10))
            screen.blit(txt, rect)

        # fps (опционально)
        if SHOW_FPS:
            fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, LABEL_TEXT_COLOR)
            screen.blit(fps_text, (WIDTH-100, HEIGHT-FONT_SIZE-5))

        pygame.display.flip()

    config.save()
    pygame.quit()
    sys.exit()
