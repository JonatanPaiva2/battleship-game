import random

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [['_' for _ in range(10)] for _ in range(10)]
        self.tabuleiro_oculto = [['_' for _ in range(10)] for _ in range(10)]
        self.navios = []  # Lista para armazenar informações sobre os navios
        self.memoria = []  # Memória para armazenar partes atingidas pelo computador
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
                    break

    def verificar_fim_de_jogo(self):
        return not bool(self.navios)


def jogada_computador(tabuleiro_jogador):
    if len(tabuleiro_jogador.memoria) == 1:
        # Se a memória não estiver vazia, o computador tem partes atingidas para tentar encontrar o navio
        linha = tabuleiro_jogador.memoria[0]['linha']
        coluna = tabuleiro_jogador.memoria[0]['coluna']
        tentar_encontrar_navio(tabuleiro_jogador, linha, coluna)
    elif len(tabuleiro_jogador.memoria) > 1:
        orientacao = verificar_orientacao_memoria(tabuleiro_jogador)
        print(orientacao)
    else:
        # Caso contrário, atirar aleatoriamente
        jogada_aleatoria(tabuleiro_jogador)
        
def jogada_aleatoria(tabuleiro_jogador):
    while True:
            try:
                linha = random.randint(0, 9)
                coluna = random.randint(0, 9)
                
                if tabuleiro_jogador.tabuleiro[linha][coluna] == 'O':
                    tabuleiro_jogador.memoria.append({'linha': linha, 'coluna': coluna})
                    print (tabuleiro_jogador.memoria)
                
                if tabuleiro_jogador.acertou_ou_errou(linha, coluna):
                    break
            except (ValueError, IndexError):
                continue

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
        
def encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha, coluna, direcao='horizontal'):
    # Encontrar a próxima posição vazia ao longo da linha ou coluna
    linha = int(linha)
    coluna = int(coluna)

    if direcao == 'horizontal':
        # Busca para frente
        for i in range(coluna + 1, len(tabuleiro_jogador.tabuleiro[0])):
            if tabuleiro_jogador.tabuleiro[linha][i] not in ['X', '*']:
                return i

        # Busca para trás
        for i in range(coluna - 1, -1, -1):
            if tabuleiro_jogador.tabuleiro[linha][i] not in ['X', '*']:
                return i

    elif direcao == 'vertical':
        # Busca para frente
        for i in range(linha + 1, len(tabuleiro_jogador.tabuleiro)):
            if tabuleiro_jogador.tabuleiro[i][coluna] not in ['X', '*']:
                return i

        # Busca para trás
        for i in range(linha - 1, -1, -1):
            if tabuleiro_jogador.tabuleiro[i][coluna] not in ['X', '*']:
                return i

    # Se não encontrar, retornar a posição original
    return coluna if direcao == 'horizontal' else linha

def verificar_orientacao_memoria(tabuleiro_jogador):
    # Pega as coordenadas das duas partes atingidas
    linha1, coluna1 = tabuleiro_jogador.memoria[0]['linha'], tabuleiro_jogador.memoria[0]['coluna']
    linha2, coluna2 = tabuleiro_jogador.memoria[1]['linha'], tabuleiro_jogador.memoria[1]['coluna']

    # Verifica se as partes atingidas estão na mesma linha
    if linha1 == linha2:
        coluna_vazia = encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha1, coluna1, direcao='horizontal')
        tabuleiro_jogador.acertou_ou_errou(linha1, coluna_vazia)
    
    # Verifica se as partes atingidas estão na mesma coluna
    elif coluna1 == coluna2:
        linha_vazia = encontrar_proxima_posicao_vazia(tabuleiro_jogador, linha1, coluna1, direcao='vertical')
        tabuleiro_jogador.acertou_ou_errou(linha_vazia, coluna1)

##################################################

def criacao_tabuleiro_jogador(tabuleiro_jogador, navios_predefinidos):
    # Jogador
    print("Jogador, posicione seus navios:")
    for tamanho_navio, quantidade in navios_predefinidos:
        for i in range(quantidade):
            while True:
                try:
                    orientacao = input(f"Digite a orientação para colocar o navio de tamanho {tamanho_navio} (h/v): ").lower()
                    posicao = input("Digite a posição da primeira parte do navio (letra/número): ").lower()
                    print("")
                    linha = int(posicao[1:])
                    coluna = ord(posicao[0].upper()) - ord('A')

                    if tabuleiro_jogador.verificar_posicao_disponivel(orientacao, tamanho_navio, linha, coluna):
                        tabuleiro_jogador.posicionar_navio(orientacao, tamanho_navio, linha, coluna)
                        tabuleiro_jogador.exibir_tabuleiro()
                        break
                    else:
                        print("Posição indisponível. Tente novamente.")
                except (ValueError, IndexError):
                    print("Entrada inválida. Certifique-se de seguir o formato correto.")

    tabuleiro_jogador.exibir_tabuleiro()

def criacao_tabuleiro_computador(tabuleiro_computador, navios_predefinidos):
    # Computador
    print("O computador está posicionando os navios...")
    tabuleiro_computador.exibir_erros_jogador = False
    for tamanho_navio, quantidade in navios_predefinidos:
        for i in range(quantidade):
            tabuleiro_computador.posicionar_navio_aleatorio(tamanho_navio)
    print("O computador já posicionou os navios.")
    print("")


def jogada_jogador(tabuleiro_jogador):
    tabuleiro_jogador.exibir_tabuleiro_oculto()
    while True:
        try:
            jogada = input("Digite a posição para atacar (letra/número): ").lower()
            linha = int(jogada[1:]) - 1
            coluna = ord(jogada[0].upper()) - ord('A')

            if tabuleiro_jogador.acertou_ou_errou(linha, coluna):
                break
            else:
                print("Posição inválida. Tente novamente.")
        except (ValueError, IndexError):
            print("Entrada inválida. Certifique-se de seguir o formato correto.")

def jogada_jogador_2(tabuleiro_jogador):
    while True:
        try:
            tabuleiro_jogador.exibir_tabuleiro_oculto()
            jogada = input("Jogador 2, digite a posição para atacar (letra/número): ").lower()
            linha = int(jogada[1:]) - 1
            coluna = ord(jogada[0].upper()) - ord('A')

            if tabuleiro_jogador.acertou_ou_errou(linha, coluna):
                break
        except (ValueError, IndexError):
            print("Por favor, digite uma posição válida.")
            print("")
            
def rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_adversario):
    while not (tabuleiro_jogador.verificar_fim_de_jogo() or tabuleiro_adversario.verificar_fim_de_jogo()):
        # Jogada do jogador 1
        jogada_jogador(tabuleiro_adversario)
        
        # Verificar se o jogador 1 venceu após sua jogada
        if tabuleiro_adversario.verificar_fim_de_jogo():
            print("Parabéns! Jogador 1 derrubou todos os navios do adversário!")
            break

        # Jogada do jogador 2
        if tipo_de_jogo == '1':
            # Se o adversário for o computador (modo 1 jogador)
            jogada_computador(tabuleiro_jogador)
        if tipo_de_jogo == '2':
            # Se o adversário for um Tabuleiro (modo 2 jogadores)
            jogada_jogador_2(tabuleiro_jogador)
            

        # Verificar se o jogador 2 venceu após sua jogada
        if tabuleiro_jogador.verificar_fim_de_jogo():
            if isinstance(tabuleiro_adversario, Tabuleiro):
                print("Parabéns! Jogador 2 derrubou todos os navios do adversário!")
            else:
                print("Você perdeu! O computador afundou todos os seus navios.")
            break

    print("Fim da partida.")

    
   
##################################################

def play_battleship():
    print("Bem-vindo ao jogo Batalha Naval!")
    print("")
    
    print("Como deseja jogar?")
    tipo_de_jogo = input("Um Jogador (1) | Dois Jogadores (2): ")

    # PREPARAÇÃO
    navios_predefinidos = [(3, 1), (4, 1), (5, 1)]
    tabuleiro_jogador = Tabuleiro()
    tabuleiro_jogador_2 = Tabuleiro()
    tabuleiro_computador = Tabuleiro()
    
    if tipo_de_jogo == '1':
        criacao_tabuleiro_jogador(tabuleiro_jogador, navios_predefinidos)
        criacao_tabuleiro_computador(tabuleiro_computador, navios_predefinidos)
        # Iniciar a rodada de jogo para 1 jogador
        rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_computador)
    elif tipo_de_jogo == '2':
        criacao_tabuleiro_jogador(tabuleiro_jogador, navios_predefinidos)
        criacao_tabuleiro_jogador(tabuleiro_jogador_2, navios_predefinidos)
         # Iniciar a rodada de jogo para 2 jogadores
        rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_jogador_2)

'''
    # JOGO
    while not (tabuleiro_jogador.verificar_fim_de_jogo() or tabuleiro_computador.verificar_fim_de_jogo()):
        # Jogada do jogador
        tabuleiro_computador.exibir_erros_jogador = True
        try:
            tabuleiro_computador.exibir_tabuleiro_oculto()  # Exibir o tabuleiro oculto
            jogada_jogador = input("Digite a posição para atacar (letra/número): ").lower()
            linha_jogador = int(jogada_jogador[1:]) - 1
            coluna_jogador = ord(jogada_jogador[0].upper()) - ord('A')
            tabuleiro_computador.acertou_ou_errou(linha_jogador, coluna_jogador)
        except (ValueError, IndexError):
            print("Por favor, digite uma posição válida.")
            print("")

        # Verificar se o jogador venceu após sua jogada
        if tabuleiro_computador.verificar_fim_de_jogo():
            print("Parabéns! Você derrubou todos os navios do computador!")
            break

        # Jogada do computador
        tabuleiro_computador.exibir_erros_jogador = False
        jogada_computador(tabuleiro_jogador)
        tabuleiro_jogador.exibir_tabuleiro()
        
        # Verificar se o jogador venceu após sua jogada
        if tabuleiro_jogador.verificar_fim_de_jogo():
            print("Você perdeu! O computador afundou todos os seus navios.")
            break
'''

##################################################

# Executar o jogo
play_battleship()