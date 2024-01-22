class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [['_' for _ in range(10)] for _ in range(10)]
        
    def exibir_tabuleiro(self):
        print("  A B C D E F G H I J")
        i = 1
        for linha in self.tabuleiro:
            print(f"{i} {' '.join(linha)}")
            i += 1
        
    def posicionarNavio(self, orientacao, tamanhoNavio, linha, coluna):
        linha = int(linha)
        if (
            (orientacao == "h" and coluna + tamanhoNavio > len(self.tabuleiro[0])) or
            (orientacao == "v" and linha + tamanhoNavio > len(self.tabuleiro))
        ):
            print("O navio não cabe no tabuleiro")
            return
        
        if orientacao == "h":
            for i in range(coluna, coluna + tamanhoNavio):
                if self.tabuleiro[linha - 1][i] != '_':
                    print("Já há uma peça aqui")
                    return
            for i in range(coluna, coluna + tamanhoNavio):
                    self.tabuleiro[linha - 1][i] = 'O'
                    
        elif orientacao == "v":
            for i in range(linha, linha + tamanhoNavio):
                if self.tabuleiro[i - 1][coluna] != '_':
                    print("Já há uma peça aqui")
                    return 
            for i in range(linha, linha + tamanhoNavio):
                    self.tabuleiro[i - 1][coluna] = 'O'
            

    
    def acertou_ou_errou(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == 'O':
            print("Parabéns! Você acertou um navio.")
            self.tabuleiro[linha][coluna] = 'X'
            return True
        elif self.tabuleiro[linha][coluna] == '_':
            print("Você acertou a água.")
            self.tabuleiro[linha][coluna] = 'X'
            return True
        elif self.tabuleiro[linha][coluna] == 'X' or self.tabuleiro[linha][coluna] == '*':
            print("Você já tentou essa posição. Tente novamente.")
        else:
            print("Você errou. Tente novamente.")
            self.tabuleiro[linha][coluna] = '*'
        return False

def verificar_se_afundou(tabuleiro, linha, coluna):
    print("Você afundou um navio")
    
    
   ################################################ 
    
def play_battleship():
    print("Bem-vindo ao jogo Batalha Naval!")
    
    #PREPARAÇÃO
    tabuleiro = Tabuleiro()
    tabuleiro.exibir_tabuleiro()
    
    for i in range (1):
        tamanhoNavio = int(input("Escolha o tamanho do navio: "))
        orientacao = input("Digite a posição para colocar o navio (h/v): ")
        posicao = input("Digite a posição para atacar (letra/número): ").lower()
        linha = int(posicao[1:])
        coluna = ord(posicao[0].upper()) - ord('A')
        tabuleiro.posicionarNavio(orientacao, tamanhoNavio, linha, coluna)
        tabuleiro.exibir_tabuleiro()
    
    #JOGO
    while True:
        tabuleiro.exibir_tabuleiro()
        jogada = input("Digite a posição para atacar (letra/número): ").lower()
        linha = int(jogada[1:]) - 1
        coluna = ord(jogada[0].upper()) - ord('A')
        tabuleiro.acertou_ou_errou(linha, coluna)

    
#####################

play_battleship()