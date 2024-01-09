import pygame
import sys
import socket
import threading
import random

# Inicialização do Pygame
pygame.init()

# Cores disponíveis para os tanques
CORES = {
    'amarelo': (255, 255, 0),
    'azul': (0, 0, 255),
    'vermelho': (255, 0, 0),
    'verde': (0, 255, 0)
}

# Configurações do jogo
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Tanque - Multiplayer")

# Configurações do servidor
HOST = '127.0.0.1'
PORTA = 5555
BUFFER_SIZE = 1024

# Classe do Tanque
class Tanque(pygame.sprite.Sprite):
    def __init__(self, cor, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = 5
        self.tiros_disponiveis = 5

    def mover(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.x < largura - self.rect.width:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN] and self.rect.y < altura - self.rect.height:
            self.rect.y += self.velocidade

    def atirar(self):
        if self.tiros_disponiveis > 0:
            self.tiros_disponiveis -= 1
            return Tiro(self.rect.centerx, self.rect.centery)

# Classe do Tiro
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = 8

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.x > largura:
            self.kill()

# Classe do Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Tela de Pré-jogo
def tela_pre_jogo():
    escolhendo = True
    num_jogadores = 1
    cor_tanque = 'amarelo'

    while escolhendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    num_jogadores = min(4, num_jogadores + 1)
                elif event.key == pygame.K_DOWN:
                    num_jogadores = max(1, num_jogadores - 1)
                elif event.key == pygame.K_RETURN:
                    escolhendo = False

        tela.fill((255, 255, 255))
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Escolha o número de jogadores: {num_jogadores}", True, (0, 0, 0))
        tela.blit(texto, (largura // 4, altura // 4))
        texto = fonte.render("Pressione ENTER para iniciar", True, (0, 0, 0))
        tela.blit(texto, (largura // 4, altura // 4 + 50))
        pygame.display.flip()

    cor_escolhida = escolher_cor_tanque()
    return num_jogadores, cor_escolhida

# Função para escolher a cor do tanque
def escolher_cor_tanque():
    escolhendo_cor = True
    cor_tanque = 'amarelo'

    while escolhendo_cor:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cor_tanque = proxima_cor(cor_tanque)
                elif event.key == pygame.K_LEFT:
                    cor_tanque = cor_anterior(cor_tanque)
                elif event.key == pygame.K_RETURN:
                    escolhendo_cor = False

        tela.fill((255, 255, 255))
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render("Escolha a cor do tanque:", True, (0, 0, 0))
        tela.blit(texto, (largura // 4, altura // 4))
        texto = fonte.render(cor_tanque.capitalize(), True, CORES[cor_tanque])
        tela.blit(texto, (largura // 4, altura // 4 + 50))
        texto = fonte.render("Pressione ENTER para confirmar", True, (0, 0, 0))
        tela.blit(texto, (largura // 4, altura // 4 + 100))
        pygame.display.flip()

    return cor_tanque

# Função para obter a próxima cor
def proxima_cor(cor_atual):
    cores = list(CORES.keys())
    indice_atual = cores.index(cor_atual)
    return cores[(indice_atual + 1) % len(cores)]

# Função para obter a cor anterior
def cor_anterior(cor_atual):
    cores = list(CORES.keys())
    indice_atual = cores.index(cor_atual)
    return cores[(indice_atual - 1) % len(cores)]

# Função para receber dados do servidor
def receber_dados(socket_cliente, tanque_grupo, tiro_grupo):
    while True:
        dados = socket_cliente.recv(BUFFER_SIZE).decode('utf-8').split(',')
        tanque.rect.x = int(dados[0])
        tanque.rect.y = int(dados[1])
        tiros_inimigos = int(dados[2])
        if tiros_inimigos > tanque.tiros_disponiveis:
            tanque.tiros_disponiveis = tiros_inimigos

# Criar obstáculos aleatórios
def criar_obstaculos():
    obstaculos = pygame.sprite.Group()
    for _ in range(5):
        x = random.randint(0, largura - 50)
        y = random.randint(0, altura - 50)
        obstaculo = Obstaculo(x, y, 50, 50)
        obstaculos.add(obstaculo)
    return obstaculos

# Função principal
def main():
    num_jogadores, cor_tanque = tela_pre_jogo()

    clock = pygame.time.Clock()
    FPS = 60

    tanque = Tanque(CORES[cor_tanque], largura // 2, altura // 2)
    tiros = pygame.sprite.Group()
    tiros_inimigos = 5  # Inicialmente, inimigos têm 5 tiros

    tanque_grupo = pygame.sprite.Group()
    tanque_grupo.add(tanque)

    # Configuração do socket
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((HOST, PORTA))

    # Iniciar thread para receber dados do servidor
    thread_receber = threading.Thread(target=receber_dados, args=(socket_cliente, tanque_grupo, tiros))
    thread_receber.daemon = True
    thread_receber.start()

    # Criar obstáculos
    obstaculos = criar_obstaculos()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        tanque.mover(keys)

        # Atirar
        if keys[pygame.K_SPACE]:
            tiro = tanque.atirar()
            if tiro:
                tiros.add(tiro)

        # Enviar dados para o servidor
        dados = f"{tanque.rect.x},{tanque.rect.y},{tanque.tiros_disponiveis}".encode('utf-8')
        socket_cliente.sendall(dados)

        # Atualizar tiros
        tiros.update()
        for tiro in tiros:
            # Colisão com obstáculos
            if pygame.sprite.spritecollide(tiro, obstaculos, True):
                tiro.kill()

        # Colisão do tiro inimigo com o tanque
        if pygame.sprite.spritecollide(tanque, tiros, True):
            print("Você foi atingido!")
            tanque.tiros_disponiveis = 5  # Reseta tiros após ser atingido

        tela.fill((255, 255, 255))

        # Desenhar obstáculos
        obstaculos.draw(tela)

        tanque_grupo.draw(tela)

        # Desenhar tiros
        tiros.draw(tela)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
