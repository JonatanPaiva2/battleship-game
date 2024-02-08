from Battleship import *
import random

class Computador:
    @staticmethod
    def jogada_computador(tabuleiro_jogador):
        if len(tabuleiro_jogador.memoria) == 1:
            # Se a memória não estiver vazia, o computador tem partes atingidas para tentar encontrar o navio
            linha = tabuleiro_jogador.memoria[0]['linha']
            coluna = tabuleiro_jogador.memoria[0]['coluna']
            Computador.tentar_encontrar_navio(tabuleiro_jogador, linha, coluna)
        elif len(tabuleiro_jogador.memoria) > 1:
            orientacao = Computador.verificar_orientacao_memoria(tabuleiro_jogador)
            print(orientacao)
        else:
            # Caso contrário, atirar aleatoriamente
            Computador.jogada_aleatoria(tabuleiro_jogador)

    @staticmethod
    def jogada_aleatoria(tabuleiro_jogador):
        while True:
            try:
                linha = random.randint(0, 9)
                coluna = random.randint(0, 9)

                if tabuleiro_jogador.tabuleiro[linha][coluna] == 'O':
                    tabuleiro_jogador.memoria.append({'linha': linha, 'coluna': coluna})
                    print(tabuleiro_jogador.memoria)

                if tabuleiro_jogador.acertou_ou_errou(linha, coluna):
                    break
            except (ValueError, IndexError):
                continue

    @staticmethod
    def tentar_encontrar_navio(tabuleiro_jogador, linha, coluna):
        direcoes_possiveis = ["acima", "abaixo", "esquerda", "direita"]
        random.shuffle(direcoes_possiveis)

        for direcao in direcoes_possiveis:
            if direcao == "acima" and linha > 0:
                linha -= 1
            elif direcao == "abaixo" and linha < 9:
                linha += 1
            elif direcao == "esquerda" and coluna > 0:
                coluna -= 1
            elif direcao == "direita" and coluna < 9:
                coluna += 1

            if not tabuleiro_jogador.tabuleiro[linha][coluna] in ['X', '*']:
                # Se a posição não foi atacada anteriormente, realizar a jogada
                tabuleiro_jogador.acertou_ou_errou(linha, coluna)
                if tabuleiro_jogador.tabuleiro[linha][coluna] == '*':
                    tabuleiro_jogador.memoria.append({'linha': linha, 'coluna': coluna})
                break

    @staticmethod
    def encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha, coluna, direcao='horizontal'):
        # Encontrar a próxima posição vazia ao longo da linha ou coluna
        linha = int(linha)
        coluna = int(coluna)

        if direcao == 'horizontal':
            # Verifica se há posições acertadas que são água
            if tabuleiro_jogador.posicoes_acertadas_agua:
                # Se houver, fazer a busca para trás
                for i in range(coluna - 1, -1, -1):
                    if tabuleiro_jogador.tabuleiro[linha][i] not in ['X', '*']:
                        return i
            else:
                # Se não houver, fazer a busca para frente
                for i in range(coluna + 1, len(tabuleiro_jogador.tabuleiro[0])):
                    if tabuleiro_jogador.tabuleiro[linha][i] not in ['X', '*']:
                        return i

        elif direcao == 'vertical':
            # Verifica se há posições acertadas que são água
            if tabuleiro_jogador.posicoes_acertadas_agua:
                # Se houver, fazer a busca para trás
                for i in range(linha - 1, -1, -1):
                    if tabuleiro_jogador.tabuleiro[i][coluna] not in ['X', '*']:
                        return i
            else:
                # Se não houver, fazer a busca para frente
                for i in range(linha + 1, len(tabuleiro_jogador.tabuleiro)):
                    if tabuleiro_jogador.tabuleiro[i][coluna] not in ['X', '*']:
                        return i

        # Se não encontrar, retornar a posição original
        return coluna if direcao == 'horizontal' else linha

    @staticmethod
    def verificar_orientacao_memoria(tabuleiro_jogador):
        # Pega as coordenadas das duas partes atingidas
        linha1, coluna1 = tabuleiro_jogador.memoria[0]['linha'], tabuleiro_jogador.memoria[0]['coluna']
        linha2, coluna2 = tabuleiro_jogador.memoria[1]['linha'], tabuleiro_jogador.memoria[1]['coluna']

        # Verifica se as partes atingidas estão na mesma linha
        if linha1 == linha2:
            coluna_vazia = Computador.encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha1, coluna1, direcao='horizontal')
            tabuleiro_jogador.acertou_ou_errou(linha1, coluna_vazia)
            
            # Verifica se a posição acertada é água
            if tabuleiro_jogador.tabuleiro[linha1][coluna_vazia] == 'X':
                if tabuleiro_jogador.posicoes_acertadas_agua == True:
                    tabuleiro_jogador.memoria = []
                else:
                    tabuleiro_jogador.posicoes_acertadas_agua = True

        # Verifica se as partes atingidas estão na mesma coluna
        elif coluna1 == coluna2:
            linha_vazia = Computador.encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha1, coluna1, direcao='vertical')
            tabuleiro_jogador.acertou_ou_errou(linha_vazia, coluna1)
            
            # Verifica se a posição acertada é água
            if tabuleiro_jogador.tabuleiro[linha_vazia][coluna1] == 'X':
                if tabuleiro_jogador.posicoes_acertadas_agua == True:
                    tabuleiro_jogador.memoria = []
                else:
                    tabuleiro_jogador.posicoes_acertadas_agua = True
