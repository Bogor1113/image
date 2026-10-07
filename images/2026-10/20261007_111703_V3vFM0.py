import random
import sys

import pygame

WIDTH, HEIGHT = 900, 600
FONT_SIZE = 18
FALL_SPEED = 1.6
FPS = 30

BG = (0, 0, 0)
HEAD = (220, 255, 220)
BODY = (0, 255, 70)
DIM = (0, 160, 50)

CHARS = (
    "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "ｦｧｨｩｪｫｬｭｮｯｰ:･=+*<>$#@%&"
)


class Stream:
    def __init__(self, col, rows):
        self.col = col
        self.speed = random.uniform(FALL_SPEED * 0.6, FALL_SPEED * 1.5)
        self.length = random.randint(5, rows // 3)
        self.head = float(random.randint(-rows, 0))
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.reset_chance = 0.02

    def update(self, rows):
        self.head += self.speed
        if self.head - self.length > rows:
            self.head = float(random.randint(-rows // 2, -1))
            self.length = random.randint(5, rows // 3)
            self.chars = [random.choice(CHARS) for _ in range(self.length)]
        elif random.random() < self.reset_chance:
            idx = random.randrange(len(self.chars))
            self.chars[idx] = random.choice(CHARS)

    def draw(self, screen, font, rows, row_h):
        for i in range(self.length):
            r = int(self.head) - i
            if r < 0 or r >= rows:
                continue
            ch = self.chars[i]
            y = r * row_h
            x = self.col * FONT_SIZE
            if i == 0:
                color = HEAD
                surf = font.render(ch, True, color)
            elif i < 3:
                color = tuple(min(255, c + 60) for c in BODY)
                surf = font.render(ch, True, color)
            else:
                t = i / max(1, self.length - 1)
                color = (
                    int(BODY[0] * (1 - t) + DIM[0] * t),
                    int(BODY[1] * (1 - t) + DIM[1] * t),
                    int(BODY[2] * (1 - t) + DIM[2] * t),
                )
                surf = font.render(ch, True, color)
            screen.blit(surf, (x, y))


def main():
    pygame.init()
    pygame.display.set_caption("Matrix Rain")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)

    def build_streams(w, h):
        cols = max(1, w // FONT_SIZE)
        rows = max(1, h // FONT_SIZE)
        return [Stream(c, rows) for c in range(cols)], rows

    streams, rows = build_streams(WIDTH, HEIGHT)
    row_h = FONT_SIZE
    fade = pygame.Surface((WIDTH, HEIGHT)).convert()
    fade.fill(BG)

    running = True
    while running:
        w, h = screen.get_size()
        cols = max(1, w // FONT_SIZE)
        new_rows = max(1, h // row_h)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                w, h = screen.get_size()
                fade = pygame.Surface((w, h)).convert()
                fade.fill(BG)

        if cols != len(streams):
            if cols > len(streams):
                streams.extend(Stream(c, new_rows) for c in range(len(streams), cols))
            else:
                streams = streams[:cols]
        rows = new_rows

        # 半透明黑色矩形覆盖，形成拖尾
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 28))
        screen.blit(overlay, (0, 0))

        for s in streams:
            s.update(rows)
            s.draw(screen, font, rows, row_h)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
