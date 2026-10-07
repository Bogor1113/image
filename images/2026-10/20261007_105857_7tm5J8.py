import pygame
import random
import sys

WIDTH, HEIGHT = 600, 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL
FPS = 10

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (40, 180, 80)
DARK_GREEN = (30, 140, 60)
RED = (220, 60, 60)
BLUE = (90, 150, 230)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("贪吃蛇")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("simsun", 30)
    over_font = pygame.font.SysFont("simsun", 48)

    def reset():
        return [(COLS // 2, ROWS // 2)], (random.randint(0, COLS - 1), random.randint(0, ROWS - 1)), (1, 0), 0

    snake, food, direction, score = reset()

    def place_food():
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in snake:
                return pos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_r:
                    snake, food, direction, score = reset()

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if (new_head in snake
                or new_head[0] < 0 or new_head[0] >= COLS
                or new_head[1] < 0 or new_head[1] >= ROWS):
            dst = over_font.render("游戏结束！得分：%d" % score, True, RED)
            tip = font.render("按 R 重新开始，按 Q 退出", True, WHITE)
            screen.fill(BLACK)
            screen.blit(dst, (WIDTH // 2 - dst.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT // 2 + 10))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        snake, food, direction, score = reset()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            continue

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = place_food()
        else:
            snake.pop()

        screen.fill(BLACK)

        for i, (x, y) in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

        pygame.draw.rect(screen, RED, (food[0] * CELL, food[1] * CELL, CELL, CELL))
        text = font.render("得分：%d" % score, True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()