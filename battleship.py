import os
from Tabuleiro import Tabuleiro
from Computador import Computador

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

##################################################

def jogada_jogador(tabuleiro_adversario, nome_jogador):
    print("Vez do", nome_jogador)
    tabuleiro_adversario.exibir_tabuleiro_oculto()
    while True:
        try:
            jogada = input("Digite a posição para atacar (letra/número): ").lower()
            linha = int(jogada[1:]) - 1
            coluna = ord(jogada[0].upper()) - ord('A')

            if tabuleiro_adversario.acertou_ou_errou(linha, coluna):
                break
            else:
                print("Posição inválida. Tente novamente.")
                print("")
        except (ValueError, IndexError):
            print("Entrada inválida. Certifique-se de seguir o formato correto.")
            print("")
            
            
def rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_adversario):
    while not (tabuleiro_jogador.verificar_fim_de_jogo() or tabuleiro_adversario.verificar_fim_de_jogo()):
        # Jogada do jogador 1
        nome_jogador = "jogador 1"
        jogada_jogador(tabuleiro_adversario, nome_jogador)
        
        # Verificar se o jogador 1 venceu após sua jogada
        if tabuleiro_adversario.verificar_fim_de_jogo():
            print("Parabéns! Jogador 1 derrubou todos os navios do adversário!")
            break

        # Jogada do jogador 2
        if tipo_de_jogo == '1':
            # Se o adversário for o computador (modo 1 jogador)
            print("Vez do Computador")
            Computador.jogada_computador(tabuleiro_jogador)
            tabuleiro_jogador.exibir_tabuleiro()
        if tipo_de_jogo == '2':
            # Se o adversário for um Tabuleiro (modo 2 jogadores)
            nome_jogador = "jogador 2"
            jogada_jogador(tabuleiro_jogador, nome_jogador)
            
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
    print("")

    # PREPARAÇÃO
    navios_predefinidos = [(3, 1), (4, 1), (5, 1)]
    tabuleiro_jogador = Tabuleiro()
    tabuleiro_jogador_2 = Tabuleiro()
    tabuleiro_computador = Tabuleiro()
    
    if tipo_de_jogo == '1':
        tabuleiro_jogador.exibir_tabuleiro_oculto()
        criacao_tabuleiro_jogador(tabuleiro_jogador, navios_predefinidos)
        criacao_tabuleiro_computador(tabuleiro_computador, navios_predefinidos)
        # Iniciar a rodada de jogo para 1 jogador
        rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_computador)
    elif tipo_de_jogo == '2':
        tabuleiro_jogador.exibir_tabuleiro_oculto()
        criacao_tabuleiro_jogador(tabuleiro_jogador, navios_predefinidos)
        os.system('cls')
        criacao_tabuleiro_jogador(tabuleiro_jogador_2, navios_predefinidos)
        os.system('cls')
         # Iniciar a rodada de jogo para 2 jogadores
        rodada_jogo(tipo_de_jogo, tabuleiro_jogador, tabuleiro_jogador_2)
