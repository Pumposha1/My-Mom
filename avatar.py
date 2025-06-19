import pygame, random, math
from settings import AVATAR_IMG, FADE_DURATION, WIDTH, HEIGHT

class Avatar:
    def __init__(self, position=None):
        # загрузка и базовая настройка
        self.image_orig = pygame.image.load(AVATAR_IMG).convert_alpha()
        self.image      = self.image_orig.copy()
        px, py = position or (WIDTH//2, HEIGHT//2)
        self.rect       = self.image.get_rect(center=(px, py))

        # полуспрайтовые размеры для границ
        self.half_w = self.rect.width  // 2
        self.half_h = self.rect.height // 2

        # fade-in/out
        self.visible = False
        self.alpha   = 0
        self.timer   = 0.0

        # движение
        self.speed         = 120
        self.move_interval = 4.0
        self.move_timer    = 0.0
        self.target        = self.rect.center

    def show(self):
        self.visible = True
        self.timer   = 0.0

    def hide(self):
        self.visible = False
        self.timer   = 0.0

    def pick_new_target(self):
        # центр аватара выбираем так, чтобы весь он помещался
        tx = random.randint(self.half_w, WIDTH  - self.half_w)
        ty = random.randint(self.half_h, HEIGHT - self.half_h)
        self.target = (tx, ty)

    def update(self, dt, show_interval, hide_interval):
        # ===== fade-in/out (без изменений) =====
        self.timer += dt
        if self.visible:
            if self.alpha < 255:
                self.alpha = min(255, self.alpha + 255 * dt / FADE_DURATION)
            elif self.timer >= show_interval:
                self.hide()
        else:
            if self.alpha > 0:
                self.alpha = max(0, self.alpha - 255 * dt / FADE_DURATION)
            elif self.timer >= hide_interval:
                self.show()
        self.image = self.image_orig.copy()
        self.image.set_alpha(int(self.alpha))

        # ===== движение =====
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.pick_new_target()
            self.move_timer = 0.0

        cx, cy = self.rect.center
        tx, ty = self.target
        dx, dy = tx - cx, ty - cy
        dist = math.hypot(dx, dy)
        if dist > 5:
            vx, vy = dx / dist * self.speed, dy / dist * self.speed
            self.rect.centerx += vx * dt
            self.rect.centery += vy * dt

            # зажимаем внутри окна
            screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            self.rect.clamp_ip(screen_rect)

    def draw(self, surface):
        if self.alpha > 0:
            surface.blit(self.image, self.rect)
