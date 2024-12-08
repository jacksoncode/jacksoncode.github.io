import pygame
import random
import tkinter as tk
from tkinter import messagebox

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# 定义方块大小和间距
BLOCK_SIZE = 80
MARGIN = 10

# 初始化屏幕
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048 Game")

# 初始化字体
font = pygame.font.Font(None, 36)

# 初始化游戏板
board = [[0] * 4 for _ in range(4)]

# 在游戏板上随机生成一个2或4
def add_tile():
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

# 绘制游戏板
def draw_board():
    screen.fill(BLACK)
    for i in range(4):
        for j in range(4):
            color = WHITE
            if board[i][j]!= 0:
                color = GRAY
            pygame.draw.rect(screen, color, [(MARGIN + BLOCK_SIZE) * j + MARGIN, (MARGIN + BLOCK_SIZE) * i + MARGIN, BLOCK_SIZE, BLOCK_SIZE])
            if board[i][j]!= 0:
                text = font.render(str(board[i][j]), True, BLACK)
                text_rect = text.get_rect(center=((MARGIN + BLOCK_SIZE) * j + MARGIN + BLOCK_SIZE // 2, (MARGIN + BLOCK_SIZE) * i + MARGIN + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)
    pygame.display.flip()

# 游戏主循环
def game_loop():
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 向上移动
                    pass
                elif event.key == pygame.K_DOWN:
                    # 向下移动
                    pass
                elif event.key == pygame.K_LEFT:
                    # 向左移动
                    pass
                elif event.key == pygame.K_RIGHT:
                    # 向右移动
                    pass
        
        # 检查游戏是否结束
        if not any(0 in row for row in board):
            # 游戏结束，弹出消息框
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Game Over", "游戏结束！")
            game_over = True
        
        draw_board()
    
    pygame.quit()

# 初始化游戏板并开始游戏
add_tile()
add_tile()
game_loop()
