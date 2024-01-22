import random

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [['_' for _ in range(10)] for _ in range(10)]
        self.tabuleiro_oculto = [['_' for _ in range(10)] for _ in range(10)]
        self.navios = []  # Lista para armazenar informações sobre os navios
        
    def exibir_tabuleiro(self):
        print("  A B C D E F G H I J")
        i = 1
        for linha in self.tabuleiro:
            print(f"{i} {' '.join(linha)}")
            i += 1
            
    def exibir_tabuleiro_oculto(self):
        print("  A B C D E F G H I J")
        i = 1
        for linha in self.tabuleiro_oculto:
            print(f"{i} {' '.join(linha)}")
            i += 1
        
    def posicionar_navio(self, orientacao, tamanho_navio, linha, coluna):
        linha = int(linha)
        if (
            (orientacao == "h" and coluna + tamanho_navio > len(self.tabuleiro[0])) or
            (orientacao == "v" and linha + tamanho_navio > len(self.tabuleiro))
        ):
            print("O navio não cabe no tabuleiro")
            return
        
        partes_navio = []
        if orientacao == "h":
            for i in range(coluna, coluna + tamanho_navio):
                if self.tabuleiro[linha - 1][i] != '_':
                    print("Já há uma peça aqui")
                    return
            
            for i in range(coluna, coluna + tamanho_navio):
                partes_navio.append((linha - 1, i))
                self.tabuleiro[linha - 1][i] = 'O'
                    
        elif orientacao == "v":
            for i in range(linha, linha + tamanho_navio):
                if self.tabuleiro[i - 1][coluna] != '_':
                    print("Já há uma peça aqui")
                    return 
            
            for i in range(linha, linha + tamanho_navio):
                partes_navio.append((i - 1, coluna))
                self.tabuleiro[i - 1][coluna] = 'O'
            
        # Armazenar informações sobre o navio
        self.navios.append({'tamanho': tamanho_navio, 'partes': partes_navio})
        
    def posicionar_navio_aleatorio(self, tamanho_navio):
        orientacao = random.choice(["h", "v"])
        if orientacao == "h":
            linha = random.randint(1, len(self.tabuleiro))
            coluna = random.randint(1, len(self.tabuleiro[0]) - tamanho_navio + 1)
        else:
            linha = random.randint(1, len(self.tabuleiro) - tamanho_navio + 1)
            coluna = random.randint(1, len(self.tabuleiro[0]))

        if not self.verificar_posicao_disponivel(orientacao, tamanho_navio, linha, coluna):
            return self.posicionar_navio_aleatorio(tamanho_navio)
        else:
            self.posicionar_navio(orientacao, tamanho_navio, linha, coluna)

    def verificar_posicao_disponivel(self, orientacao, tamanho_navio, linha, coluna):
        if orientacao == "h":
            for i in range(coluna, coluna + tamanho_navio):
                if self.tabuleiro[linha - 1][i - 1] != '_':
                    return False
        elif orientacao == "v":
            for i in range(linha, linha + tamanho_navio):
                if self.tabuleiro[i - 1][coluna - 1] != '_':
                    return False
        return True

    
    def acertou_ou_errou(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == 'O':
            print("Parabéns! Você acertou um navio.")
            self.tabuleiro_oculto[linha][coluna] = '*'
            self.tabuleiro[linha][coluna] = '*'
            self.verificar_se_afundou(linha, coluna)
            return True
        elif self.tabuleiro[linha][coluna] == '_':
            print("Você acertou a água.")
            self.tabuleiro_oculto[linha][coluna] = 'X'
            self.tabuleiro[linha][coluna] = 'X'
            return True
        elif self.tabuleiro[linha][coluna] == 'X' or self.tabuleiro[linha][coluna] == '*':
            print("Você já tentou essa posição. Tente novamente.")
        else:
            print("Você errou. Tente novamente.")
            self.tabuleiro[linha][coluna] = '*'
        return False

    def verificar_se_afundou(self, linha, coluna):
            for navio in self.navios:
                if (linha, coluna) in navio['partes']:
                    navio['partes'].remove((linha, coluna))
                    if not navio['partes']:
                        print(f"Você afundou um navio de tamanho {navio['tamanho']}!")
                        self.navios.remove(navio)
                        break
                    
    def verificar_fim_de_jogo(self):
        return not bool(self.navios)


   ################################################ 
    
def play_battleship():
    print("Bem-vindo ao jogo Batalha Naval!")
    
    #PREPARAÇÃO
    tabuleiro = Tabuleiro()
    tabuleiro.exibir_tabuleiro()
    
    navios_predefinidos = [(3, 2), (4, 1), (5, 1)]
    
    '''
    for tamanho_navio, quantidade in navios_predefinidos:
        for i in range (quantidade):
            #tamanho_navio = int(input("Escolha o tamanho do navio: "))
            orientacao = input(f"Digite a orientação para colocar o navio de tamanho {tamanho_navio} (h/v): ")
            posicao = input("Digite a posição da primeira parte do navio (letra/número): ").lower()
            linha = int(posicao[1:])
            coluna = ord(posicao[0].upper()) - ord('A')
            tabuleiro.posicionar_navio(orientacao, tamanho_navio, linha, coluna)
            tabuleiro.exibir_tabuleiro()
    '''
    for tamanho_navio, quantidade in navios_predefinidos:
        for i in range(quantidade):
            tabuleiro.posicionar_navio_aleatorio(tamanho_navio)
    
    #JOGO
    while not tabuleiro.verificar_fim_de_jogo():
        tabuleiro.exibir_tabuleiro_oculto()  # Exibir o tabuleiro oculto
        jogada = input("Digite a posição para atacar (letra/número): ").lower()
        linha = int(jogada[1:]) - 1
        coluna = ord(jogada[0].upper()) - ord('A')
        tabuleiro.acertou_ou_errou(linha, coluna)

    tabuleiro.exibir_tabuleiro_oculto()
    print("Parabéns! Você derrubou todos os navios!")
    
#####################

play_battleship()