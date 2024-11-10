#pygame para criar o jogo
#os para integrar condigo com arquivos do pc
#random para gerar numeros aleatorios

import pygame
import os
import random


#constantes
tela_largura = 500
tela_altura = 800
#conectando pastas e aumentando escala das imagens
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]
#definindos como vai aparecer a pontuação
pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = imagens_passaro
    #animaçoes de rotaçao
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    #definiçoes do passaro
    def __init__(self, x, y):
        #posiçao inicial eixo x (horizontal da esquerda para direita)
        self.x = x
        #posiçao inicial eixo y (vertical de cima para baixo)
        self.y = y
        #angulo inicial
        self.angulo = 0
        #velocidade inical
        self.velocidade = 0
        #altura inicial de acordo com eixo y
        self.altura = self.y
        #movimentaçao do passaro
        self.tempo = 0
        #imagem do passaro a a ser usada
        self.contagem_imagem = 0
        #imagem inicial
        self.imagem = self.IMGS[0]

    #definiçoes do pulo
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    #definiçoes de movimentaçao do passaro
    def mover(self):
        #calculo de deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        #restriçao de deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            #pulando um pouco mais alto
            deslocamento -= 2
        self.y += deslocamento
        #angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            #virando pra cima quando pula
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            #virando o passaro conforme desce
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    #definindo posiçoes e imagens do passaro
    def desenhar(self, tela):
        #qual imagem do passaro usar
        self.contagem_imagem += 1
        #asa para cima
        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.IMGS[0]
        #asa no meio
        elif self.contagem_imagem < self.tempo_animacao * 2:
            self.imagem = self.IMGS[1]
        #asa pra baixo
        elif self.contagem_imagem < self.tempo_animacao * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.tempo_animacao * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.tempo_animacao * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


        #se o passaro estiver caindo não bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            #quando voltar a bater asa a primeira batidavai ser para baixo depois
            self.contagem_imagem = self.tempo_animacao * 2

        #desenhando a imagem
        #rotacionando a imagem do passaro de acordo com o movimento
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        #centro da tela
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        #colocando a imagem rotacionada na tela
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        #aplicando tudo
        tela.blit(imagem_rotacionada, retangulo.topleft)

        #colisao de objetos
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    #distancia entre os canos verticais
    distancia = 200
    #velocidade dos canos
    velocidade = 5

    def __init__(self, x):
        #posiçoes do cano
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        #imagem de cima rotacionada do cano
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        #imagem de baixo do cano
        self.cano_base = imagem_cano
        #se passou pelo cano
        self.passou = False
        self.definir_altura()

    #alturas dos canos
    def definir_altura(self):
        #altura aleatoria
        self.altura = random.randrange(50, 450)
        #
        self.pos_topo = self.altura - self.cano_topo.get_height()
        #distancia entre canos
        self.pos_base = self.altura + self.distancia

    #movimentaçao do cano
    def mover(self):
        self.x -= self.velocidade

    #desenhando canos
    def desenhar(self, tela):
        #cano de cima
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        #cano de baixo
        tela.blit(self.cano_base, (self.x, self.pos_base))

     #colisao
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        #conferindo se houve colisao
        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):
        self.y = y
        #definindo os 2 chao
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        #velocidade do chao (negativo pois esta indo para o inico da tela)
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade
        #retornando o chao1 para o fim da tela
        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    #fundo da tela
    tela.blit(imagem_background, (0, 0))
    #passaros caso tenha a possibilidade de varios passaros de uma vez
    for passaro in passaros:
        passaro.desenhar(tela)
    #canos
    for cano in canos:
        cano.desenhar(tela)
    #pontuaçao com texto, formato e cor
    texto = fonte_pontos.render(f'Pontuação: {pontos}', 1, (255, 255, 255))
    #colocando na posiçao da tela
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    #criando tela
    pygame.display.update()

#funçao que roda o jogo
def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(760)]
    #criando tela final
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    #tempo de atulizaçao de tela
    relogio = pygame.time.Clock()

    #rodando o jogo
    rodando = True
    while rodando:
        #quantos fps de atualizacao de tela
        relogio.tick(30)
        #interaçao com o usuario
        for evento in pygame.event.get():
            #fechando jogo
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            #realizando pulo com barra de espaço
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        #movimentando tudo
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            #verificando se cano bateu com passaros
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                #se o passaro passou pelo cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)
        #se passou pelo cano ganha um ponto e um novo cano é adicionando no final
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        #remover cano que ja passou
        for cano in remover_canos:
            canos.remove(cano)

        #colisao com chao e teto
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        #mostrando tudo
        desenhar_tela(tela, passaros, canos, chao, pontos)

#executando o jogo se for o arquivo e não importaçao
if __name__ == '__main__':
    main()