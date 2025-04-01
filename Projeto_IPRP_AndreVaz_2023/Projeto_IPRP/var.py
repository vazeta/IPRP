import turtle as t
import time
import fossball_alunos

def le_replay(nome_ficheiro):
    replay = {'bola': [], 'jogador_vermelho': [], 'jogador_azul': []}
    a = 1
    with open(nome_ficheiro, 'r') as f:
        for linha in f:
            posicoes = linha.split(',')
            if a == 1:
                replay['bola'].append(tuple(map(float, posicoes)))
            elif a == 2:
                replay['jogador_vermelho'].append(tuple(map(float, posicoes)))
            elif a == 3:
                replay['jogador_azul'].append(tuple(map(float, posicoes)))

            a = (a % 3) + 1  
    return replay

def main(nome_ficheiro):  
    estado_jogo = fossball_alunos.init_state()
    fossball_alunos.setup(estado_jogo, False)
    replay = le_replay(nome_ficheiro)
    estado_jogo['jogador_vermelho'].up()
    estado_jogo['jogador_azul'].up()
    estado_jogo['bola']['bola'].up()
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho'].goto(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].goto(replay['jogador_azul'][i])
        estado_jogo['bola']['bola'].goto(replay['bola'][i])
        time.sleep(0.0001)
    estado_jogo['jogador_vermelho'].reset()
    estado_jogo['jogador_azul'].reset()
    estado_jogo['bola']['bola'].reset()
    
if __name__ == '__main__':
    main("replay_golo_jv_0_ja_1.txt")  # Substitua pelo nome correto do arquivo
    t.done()
    t.bye()    