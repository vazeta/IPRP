import turtle as t
import functools
import random
import math
import time
import csv
import os

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO_JOGADOR = 90
PIXEIS_MOVIMENTO_BOLA = 5
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO =  ALTURA_JANELA / 4
START_POS_BALIZAS = ALTURA_JANELA / 6
BOLA_START_POS = (5,5)
JOGADOR_START_POSX = 350
JOGADOR_START_POSY = 0

# Funções responsáveis pelo movimento dos jogadores no ambiente. 
# O número de unidades que o jogador se pode movimentar é definida pela constante 
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado 
# do jogo e o jogador que se está a movimentar. 

def jogador_cima(estado_jogo, jogador):
    jogador = estado_jogo[jogador]
    jogador.seth(90)
    jogador.up()
    jogador.fd(PIXEIS_MOVIMENTO_JOGADOR)
    pass

def jogador_baixo(estado_jogo, jogador):
    jogador = estado_jogo[jogador]    
    jogador.seth(-90)
    jogador.up()
    jogador.fd(PIXEIS_MOVIMENTO_JOGADOR)    
    pass
    
def jogador_direita(estado_jogo, jogador):
    jogador = estado_jogo[jogador]    
    jogador.seth(0)
    jogador.up()
    jogador.fd(PIXEIS_MOVIMENTO_JOGADOR)    
    pass

def jogador_esquerda(estado_jogo, jogador):
    jogador = estado_jogo[jogador]    
    jogador.seth(180)
    jogador.up()
    jogador.fd(PIXEIS_MOVIMENTO_JOGADOR)    
    pass

def desenha_linhas_campo():
    def desenha_balizas():
        a = 1
        for i in range(2):
            t.ht()
            t.pencolor("white")
            t.pensize(8)
            t.left(a*90)
            t.up()
            t.goto((-1*LARGURA_JANELA*a)/2,-1*START_POS_BALIZAS)
            t.down()
            t.right(a*90)
            t.fd(LADO_MENOR_AREA)
            t.left(a*90)
            t.fd(LADO_MAIOR_AREA)
            t.left(a*90)
            t.fd(LADO_MENOR_AREA)
            a = -1
    desenha_balizas()  
    def desenha_meioCampo():
        t.up()
        t.goto(0,-ALTURA_JANELA/2)
        t.seth(90)
        t.down()
        t.fd(ALTURA_JANELA/2)
        t.dot(40,"white")
        t.fd(ALTURA_JANELA/2)
        t.bk(ALTURA_JANELA/2 + ALTURA_JANELA/4)
        t.seth(0)
        t.circle(RAIO_MEIO_CAMPO)
    desenha_meioCampo()
    pass

def criar_bola():
    
    bola = t.Turtle()
    bola.shape("circle")
    bola.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE / 2, stretch_len=DEFAULT_TURTLE_SCALE / 2)
    bola.penup()
    bola.goto(BOLA_START_POS)    
    
    '''
    Função responsável pela criação da bola. 
    Deverá considerar que esta tem uma forma redonda, é de cor preta, 
    começa na posição BOLA_START_POS com uma direção aleatória. 
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores. 
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola, 
    a sua direção no eixo dos xx, a sua direção no eixo dos yy, 
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''
    estado_bola = {}
    estado_bola["bola"] = bola
    estado_bola["xx"] = bola.xcor()
    estado_bola["yy"] = bola.ycor()
    estado_bola["posAnt"] = None
    
    return estado_bola

def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE) 
    jogador.shape("circle")
    jogador.color(cor)
    jogador.up()    
    jogador.goto(x_pos_inicial,y_pos_inicial)    
    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    
    return jogador
def init_state():
    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola' : [],
        'jogador_vermelho' : [],
        'jogador_azul' : [],
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0
    return estado_jogo

def cria_janela():
    #create a window and declare a variable called window and call the screen()
    window=t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")  
    window.setup(width = LARGURA_JANELA,height = ALTURA_JANELA)
    window.tracer(0)
    return window

def cria_quadro_resultados():
    #Code for creating pen for scorecard update
    quadro=t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0,260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco',24,"normal"))
    return quadro


def terminar_jogo(estado_jogo):
    print("Adeus")
    guarda_resultados('historico_resultados.csv',estado_jogo)
    estado_jogo['janela'].bye() 
    
    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro 
     ''historico_resultados.csv'' com o número total de jogos até ao momento, 
     e o resultado final do jogo. Caso o ficheiro não exista, 
     ele deverá ser criado com o seguinte cabeçalho: 
     NJogo,JogadorVermelho,JogadorAzul.
    '''

def setup(estado_jogo, jogar):
    janela = cria_janela()
    # Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho'), 'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho'), 's')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho'), 'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho'), 'd')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul'), 'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul'), 'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul'), 'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul'), 'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), 'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    
    desenha_linhas_campo()
    
    estado_jogo['bola'] = criar_bola()
    
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']),align="center",font=('Monaco',24,"normal"))

def movimenta_bola(estado_jogo):
    bola = estado_jogo["bola"]["bola"] 
    bola.up()
    estado_jogo["bola"]["posAnt"] = bola.pos()
    estado_jogo["bola"]["xx"] = bola.xcor()
    estado_jogo["bola"]["yy"] = bola.ycor()
    bola.fd(PIXEIS_MOVIMENTO_BOLA)
    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''
    pass

def verifica_colisoes_ambiente(estado_jogo):
    bola = estado_jogo["bola"]["bola"]   
    if (bola.xcor() > (LARGURA_JANELA/2) - RAIO_BOLA or bola.xcor() < -((LARGURA_JANELA/2) - RAIO_BOLA)):
        bola.seth(180 - bola.heading())
    elif (bola.ycor() < (-(ALTURA_JANELA/2)+RAIO_BOLA)  or bola.ycor() > ((ALTURA_JANELA/2)-RAIO_BOLA)):
        bola.seth(-bola.heading())
                  
    jogador1 = estado_jogo["jogador_vermelho"]     
    jogador2 = estado_jogo["jogador_azul"]   
  
    if (jogador1.xcor() > 5):
        jogador_esquerda(estado_jogo,'jogador_vermelho')
    elif (jogador1.xcor() - RAIO_JOGADOR < -(LARGURA_JANELA/2)):
        jogador_direita(estado_jogo,'jogador_vermelho')
    elif (jogador1.ycor() + RAIO_JOGADOR < -(ALTURA_JANELA/2) + RAIO_BOLA):
        jogador_cima(estado_jogo,'jogador_vermelho')
    elif (jogador1.ycor() - RAIO_JOGADOR > (ALTURA_JANELA/2)-RAIO_BOLA):
        jogador_baixo(estado_jogo,'jogador_vermelho')
        
    if (jogador2.xcor() < -5):
        jogador_direita(estado_jogo,'jogador_azul')
    elif (jogador2.xcor() + RAIO_JOGADOR > (LARGURA_JANELA/2)):
        jogador_esquerda(estado_jogo,'jogador_azul')
    elif (jogador2.ycor() + RAIO_JOGADOR < -(ALTURA_JANELA/2) + RAIO_BOLA):
        jogador_cima(estado_jogo,'jogador_azul')
    elif (jogador2.ycor() - RAIO_JOGADOR > (ALTURA_JANELA/2) - RAIO_BOLA):
        jogador_baixo(estado_jogo,'jogador_azul')    
        '''
    Função responsável por verificar se há colisões com os limites do ambiente, 
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais, 
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''
    pass
def verifica_golo_jogador_vermelho(estado_jogo):
    bola = estado_jogo["bola"]["bola"]
    jogador1 = estado_jogo["jogador_vermelho"]
    jogador2 = estado_jogo["jogador_azul"]

    if (bola.xcor() > (LARGURA_JANELA/2) - RAIO_BOLA and (bola.ycor() <  (ALTURA_JANELA/2)-(ALTURA_JANELA/3) and bola.ycor() > -(ALTURA_JANELA/2) + (ALTURA_JANELA/3))):
        estado_jogo['bola']['bola'].setpos(0,0)  
        estado_jogo['jogador_vermelho'].setpos(-JOGADOR_START_POSX,JOGADOR_START_POSY)
        estado_jogo['jogador_azul'].setpos(JOGADOR_START_POSX,JOGADOR_START_POSY)               
        
        estado_jogo['pontuacao_jogador_vermelho'] += 1  
        replay_golo(estado_jogo, 'replay_golo_jv_{}_ja_{}.txt'.format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']))
        
        estado_jogo["var"]["bola"] = []
        estado_jogo["var"]["jogador_vermelho"] = []
        estado_jogo["var"]["jogador_azul"] = []  
        
        update_board(estado_jogo)
        estado_jogo["bola"]["bola"].seth(random.randint(0,360))      
                  
        
        for i in range(3, 0, -1):
            contador = t.Turtle()
            contador.speed(0)
            contador.color("Black")
            contador.penup()
            contador.hideturtle()
            contador.goto(0, -25)
            contador.write(i, align="center", font=('Monaco', 30, "normal"))
            contador.clear()
            time.sleep(1)

        
    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 
    
    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 
    
    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;
    
    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''
    pass

def verifica_golo_jogador_azul(estado_jogo):
    bola = estado_jogo["bola"]["bola"]
    jogador1 = estado_jogo["jogador_vermelho"]
    jogador2 = estado_jogo["jogador_azul"]

    if (bola.xcor() < (-LARGURA_JANELA/2) + RAIO_BOLA and (bola.ycor() < (ALTURA_JANELA/2) - (ALTURA_JANELA/3) and bola.ycor() > (-ALTURA_JANELA/2) + ALTURA_JANELA / 3)): 
        estado_jogo['bola']['bola'].setpos(0,0)
        estado_jogo['jogador_vermelho'].setpos(-JOGADOR_START_POSX,JOGADOR_START_POSY)
        estado_jogo['jogador_azul'].setpos(JOGADOR_START_POSX,JOGADOR_START_POSY)         

        
        estado_jogo['pontuacao_jogador_azul'] += 1        
        replay_golo(estado_jogo, 'replay_golo_jv_{}_ja_{}.txt'.format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']))
        
        estado_jogo["var"]["bola"] = []
        estado_jogo["var"]["jogador_vermelho"] = []
        estado_jogo["var"]["jogador_azul"] = []
        
        update_board(estado_jogo)  
        estado_jogo["bola"]["bola"].seth(random.randint(0,360))      
        
        for i in range(3, 0, -1):
            contador = t.Turtle()
            contador.speed(0)
            contador.color("Black")
            contador.penup()
            contador.hideturtle()
            contador.goto(0, -25)
            contador.write(i, align="center", font=('Monaco', 30, "normal"))
            contador.clear()
            time.sleep(1)
    
    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 
    
    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 
    
    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;
    
    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''
    pass


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    bola = estado_jogo["bola"]["bola"]   
    jogador2 = estado_jogo["jogador_azul"]   
    if((abs(bola.xcor() - jogador2.xcor())) < RAIO_BOLA*2 and (abs(bola.ycor() - jogador2.ycor())) < RAIO_BOLA*2): 
        diferenca_x = bola.xcor() - jogador2.xcor()
        diferenca_y = bola.ycor() - jogador2.ycor()
        nova_direcao = math.degrees(math.atan2(diferenca_y, diferenca_x))
        bola.seth(nova_direcao)             
        
    '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''
    pass


def verifica_toque_jogador_vermelho(estado_jogo):
    bola = estado_jogo["bola"]["bola"]   
    jogador1 = estado_jogo["jogador_vermelho"]   
    if((abs(bola.xcor() - jogador1.xcor())) < RAIO_BOLA*2 and (abs(bola.ycor() - jogador1.ycor())) < RAIO_BOLA*2): 
        diferenca_x = bola.xcor() - jogador1.xcor()
        diferenca_y = bola.ycor() - jogador1.ycor()
        nova_direcao = math.degrees(math.atan2(diferenca_y, diferenca_x))
        bola.seth(nova_direcao)          
        
        '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''
    pass

def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['bola'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())
        
def replay_golo(estado_jogo, nome_ficheiro):
    with open(nome_ficheiro, 'w') as f:
        for i in range(len(estado_jogo['var']['bola'])):
            f.write(f'{estado_jogo["var"]["bola"][i][0]},{estado_jogo["var"]["bola"][i][1]}\n')
            f.write(f'{estado_jogo["var"]["jogador_vermelho"][i][0]},{estado_jogo["var"]["jogador_vermelho"][i][1]}\n')
            f.write(f'{estado_jogo["var"]["jogador_azul"][i][0]},{estado_jogo["var"]["jogador_azul"][i][1]}\n')
          

def guarda_resultados(nome_ficheiro, estado_jogo):
    numero_jogo = 1

    # Check if the file exists
    if os.path.exists(nome_ficheiro):
        with open(nome_ficheiro, 'r') as file:
            numero_jogo = 0
            for line in file:
                numero_jogo += 1

    # Use 'a' mode to append if the file exists, and 'w' mode to create if it doesn't
    with open(nome_ficheiro, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['NJogo', 'JogadorVermelho', 'JogadorAzul'])    

        # If the file is empty or doesn't exist, write the headers
        if f.tell() == 0:
            writer.writeheader()

        linha = {
            'NJogo': numero_jogo, 
            'JogadorVermelho': estado_jogo['pontuacao_jogador_vermelho'],
            'JogadorAzul': estado_jogo['pontuacao_jogador_azul']
        }

        writer.writerow(linha)
    
def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    random.seed()
    estado_jogo['bola']['bola'].setheading(random.randint(-180,180))
    while True:            
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
            time.sleep(0.01)
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo['jogador_azul'] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)
        guarda_posicoes_para_var(estado_jogo)
if __name__ == '__main__':
    main()