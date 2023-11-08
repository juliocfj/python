import pygame
import random

# Configurações
pygame.init()
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

# Cores
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Peças do Tetris
tetrominos = [
    [[1, 1, 1, 1], [0, 0, 0, 0], CYAN],
    [[1, 1, 1, 0], [1, 0, 0, 0], YELLOW],
    [[1, 1, 0, 0], [0, 1, 1, 0], GREEN],
    [[1, 1, 1, 0], [0, 0, 1, 0], MAGENTA],
    [[1, 1, 1, 0], [1, 0, 0, 0], RED],
    [[1, 1, 1, 0], [0, 1, 0, 0], WHITE]
]

# Função para criar uma nova peça
def new_piece():
    piece = random.choice(tetrominos)
    color = piece[2]
    return piece[:2], color

current_piece, current_color = new_piece()
x, y = width // 2, 0

# Função para desenhar uma peça na tela
def draw_piece(piece, color, x, y):
    for row in range(2):
        for col in range(4):
            if piece[row][col]:
                pygame.draw.rect(screen, color, pygame.Rect((x + col * 30, y + row * 30, 30, 30)))

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica do jogo aqui

    # Limpe a tela
    screen.fill(BLACK)

    # Desenhe a peça atual
    draw_piece(current_piece, current_color, x, y)

    # Atualize a tela
    pygame.display.flip()

    # Controle a velocidade do jogo
    clock.tick(30)

pygame.quit()
