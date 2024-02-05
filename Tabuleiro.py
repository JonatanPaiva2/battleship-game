import random

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [['_' for _ in range(10)] for _ in range(10)]
        self.tabuleiro_oculto = [['_' for _ in range(10)] for _ in range(10)]
        self.navios = []  # Lista para armazenar informações sobre os navios
        self.memoria = []  # Memória para armazenar partes atingidas pelo computador
        self.posicoes_acertadas_agua = [] # Memória para armazenar se o computador deve mudar de direção
        self.exibir_erros_jogador = True  # Flag para exibir mensagens de erro para o jogador

    def exibir_tabuleiro(self):
        print("  A B C D E F G H I J")
        i = 1
        for linha in self.tabuleiro:
            print(f"{i} {' '.join(linha)}")
            i += 1
        print("")

    def exibir_tabuleiro_oculto(self):
        print("  A B C D E F G H I J")
        i = 1
        for linha in self.tabuleiro_oculto:
            print(f"{i} {' '.join(linha)}")
            i += 1
        print("")

    def posicionar_navio(self, orientacao, tamanho_navio, linha, coluna):
        partes_navio = []

        if orientacao == "h":
            for i in range(coluna, coluna + tamanho_navio):
                partes_navio.append((linha - 1, i))
                self.tabuleiro[linha - 1][i] = 'O'

        elif orientacao == "v":
            for i in range(linha, linha + tamanho_navio):
                partes_navio.append((i - 1, coluna))
                self.tabuleiro[i - 1][coluna] = 'O'

        # Armazenar informações sobre o navio
        self.navios.append({'tamanho': tamanho_navio, 'partes': partes_navio})

    def posicionar_navio_aleatorio(self, tamanho_navio):
        orientacao = random.choice(["h", "v"])

        while True:
            try:
                if orientacao == "h":
                    linha = random.randint(1, len(self.tabuleiro))
                    coluna = random.randint(1, len(self.tabuleiro[0]) - tamanho_navio + 1)
                else:
                    linha = random.randint(1, len(self.tabuleiro) - tamanho_navio + 1)
                    coluna = random.randint(1, len(self.tabuleiro[0]))

                if self.verificar_posicao_disponivel(orientacao, tamanho_navio, linha, coluna):
                    # Se a posição estiver disponível, posicione o navio e saia do loop
                    self.posicionar_navio(orientacao, tamanho_navio, linha, coluna)
                    break
            except (ValueError, IndexError):
                # Se ocorrer um erro, tente novamente com uma nova orientação
                orientacao = random.choice(["h", "v"])

    def verificar_posicao_disponivel(self, orientacao, tamanho_navio, linha, coluna):
        linha = int(linha)
        if (
            (orientacao == "h" and coluna + tamanho_navio > len(self.tabuleiro[0])) or
            (orientacao == "v" and linha + tamanho_navio - 1 > len(self.tabuleiro))
        ):
            if self.exibir_erros_jogador:
                print("O navio não cabe no tabuleiro")
                print("")
            return False
        if orientacao == "h":
            for i in range(coluna, coluna + tamanho_navio):
                if self.tabuleiro[linha - 1][i - 1] != '_':
                    if self.exibir_erros_jogador:
                        print("Já há uma peça aqui")
                    return False
        elif orientacao == "v":
            for i in range(linha, linha + tamanho_navio):
                if self.tabuleiro[i - 1][coluna] != '_':
                    if self.exibir_erros_jogador:
                        print("Já há uma peça aqui")
                    return False
        else:
            if self.exibir_erros_jogador:
                print("A orientação não é válida")
            return False
        return True

    def acertou_ou_errou(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == 'O':
            print("Parabéns! Você acertou um navio.")
            print("")
            self.tabuleiro_oculto[linha][coluna] = '*'
            self.tabuleiro[linha][coluna] = '*'
            self.verificar_se_afundou(linha, coluna)
            return True
        elif self.tabuleiro[linha][coluna] == '_':
            print("Você acertou a água.")
            print("")
            self.tabuleiro_oculto[linha][coluna] = 'X'
            self.tabuleiro[linha][coluna] = 'X'
            return True
        elif self.tabuleiro[linha][coluna] == 'X' or self.tabuleiro[linha][coluna] == '*':
            print("Você já tentou essa posição. Tente novamente.")
            print("")
        else:
            print("Você errou. Tente novamente.")
            print("")
            self.tabuleiro[linha][coluna] = '*'
        return False

    def verificar_se_afundou(self, linha, coluna):
        for navio in self.navios:
            if (linha, coluna) in navio['partes']:
                navio['partes'].remove((linha, coluna))
                if not navio['partes']:
                    print(f"Você afundou um navio de tamanho {navio['tamanho']}!")
                    print("")
                    self.navios.remove(navio)
                    self.memoria = []
                    self.posicoes_acertadas_agua = []
                    break

    def verificar_fim_de_jogo(self):
        return not bool(self.navios)