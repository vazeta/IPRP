import time
import random
import functools
import turtle

MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
# Controla a velocidade da cobra. Quanto menor o valor, mais rápido é o movimento da cobra.
SPEED = 0.14
def load_high_score(state):
    high_scores = open(HIGH_SCORES_FILE_PATH,'r')
    state['high_score'] = high_scores.readlines()[-1]
    high_scores.close()
    # se já existir um high score devem guardar o valor em state['high_score']
    pass

def write_high_score_to_file(state):
    high_scores = open(HIGH_SCORES_FILE_PATH,'r+')
    high_scores.read()
    high_scores.write('\n')
    high_scores.write(str(state['new_high_score']))
    high_scores.close()
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    pass

def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(60, MAX_Y / 2.25)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

def gasolina(state):
    state['gasolina'] = turtle.Screen()
    state['gasolina'].addshape('gasoleo2.gif')
    state['gasolina'] = turtle.Turtle()
    state['gasolina'].hideturtle()
    state['gasolina'].speed(0)
    state['gasolina'].shape('gasoleo2.gif')
    state['gasolina'].showturtle()
    state['gasolina'].up()
    state['gasolina'].goto(-250, MAX_Y / 2.15)
    state['gasolina'].down()

def record(state):
    state['record'] = turtle.Screen()
    state['record'].addshape('record1.gif')
    state['record'] = turtle.Turtle()
    state['record'].hideturtle()
    state['record'].speed(0)
    state['record'].shape('record1.gif')
    state['record'].showturtle()
    state['record'].up()
    state['record'].goto(-120, MAX_Y / 2.15)
    state['record'].down()            

def update_score_board(state):
    state['score_board'].clear()
    state['score_board'].goto(-180, MAX_Y / 2.28)
    state['score_board'].write("{}".format(state['score']), align="right", font=("Helvetica", 24, "italic"))
    state['score_board'].goto(-50, MAX_Y / 2.28)
    state['score_board'].write("{}".format(state['high_score']), align="right", font=("Helvetica", 24, "italic"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    high_scores = open(HIGH_SCORES_FILE_PATH,'r')
    state['high_score'] = high_scores.read()
    high_scores.close()
    state['win'] = None
    state['pont'] = None
    state['borda'] = None
    state['fundo'] = None
    state['gasolina'] = None
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = None
    state['window'] = None
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'current_direction': None,                             # Indicação da direcção atual do movimento da cobra
        'body': []
    }
    state['snake'] = snake
    return state
def setup(state):
    window = turtle.Screen()
    window.bgcolor("gray")
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Screen()
    snake['head'].addshape('tr1.gif')           
    snake['head'].addshape('truck-down1.gif') 
    snake['head'].addshape('truck-left1.gif')
    snake['head'].addshape('truck-right1.gif')         
    snake['head'] = turtle.Turtle()
    snake["head"].hideturtle()
    snake['head'].shape('tr1.gif')
    snake['head'].showturtle()
    snake['head'].pu()
    create_score_board(state)
    create_food(state)
##def verify_if_high_score_updates(state):
  ##  if state['new_high_score'] > state['high_score']:
    ##    state['high_score'] = state['new_high_score']                
def fundo(state):
    state['fundo'] = turtle.Screen()
    state['fundo'].addshape('road.gif')           
    state['fundo'] = turtle.Turtle()
    state['fundo'].speed(0)
    state['fundo'].up()
    state['fundo'].goto(0,49)
    state['fundo'].down()
    state['fundo'].hideturtle()
    state['fundo'].shape('road.gif') 
    state['fundo'].showturtle()
    state['fundo'].up()    

def borda(state):       
    state['borda'] = turtle.Turtle()
    state['borda'].hideturtle()
    state['borda'].color('red')
    state['borda'].speed(0)
    state['borda'].up()
    state['borda'].goto(-300,-250)
    state['borda'].seth(0)
    state['borda'].down()
    state['borda'].pensize(5)
    for i in range(2):
        state['borda'].fd(600)
        state['borda'].left(90)
        state['borda'].fd(600)
        state['borda'].left(90)
def move(state):
    snake = state['snake']
    if state['snake']['current_direction'] == "up":
        snake['head'].shape('tr1.gif')       
        snake['head'].seth(90)
        snake['head'].fd(20)  
    elif state['snake']['current_direction'] == "down":
        snake['head'].shape('truck-down1.gif')
        snake['head'].seth(-90)
        snake['head'].fd(20)                   
    elif state['snake']['current_direction'] == "left":
        snake['head'].shape('truck-left1.gif') 
        snake['head'].seth(180)
        snake['head'].fd(20)                         
    elif state['snake']['current_direction'] == "right":
        snake['head'].shape('truck-right1.gif')
        snake['head'].seth(0)
        snake['head'].fd(20)              
def snake_body(state):    
    snake = state['snake']
    tale = turtle.Screen()
    tale.addshape('t1.gif')           
    tale = turtle.Turtle()
    tale.hideturtle()
    tale.shape('t1.gif') 
    tale.showturtle()
    tale.pu()
    snake['body'].append(tale)
def move_snake_tail(state):
    snake = state['snake']
    for i in range(len(snake['body'])-1, 0, -1):
        x = snake['body'][i-1].xcor()
        y = snake['body'][i-1].ycor()
        snake['body'][i].goto(x,y)  
    if state['score'] > 0:
        x = snake['head'].xcor()
        y = snake['head'].ycor()
        snake['body'][0].goto(x,y)    
def pontuacao(state):
    pont = turtle.Turtle()
    pont.clear()
    pont.goto(0,0)
    a = 0
    while a < 10:
        time.sleep(0.2)
        pont.color("red")
        pont.write("Ficaste com {} litros no depósito ".format(state['score']), align ="center", font=("hendershot", 24, "bold"))      
        pont.clear()
        a = a + 0.5
def win(state):
    win = turtle.Turtle()
    win.clear()
    win.up()
    win.goto(0,40)
    win.down()
    a = 0
    while a < 10:
        time.sleep(0.2)
        win.color("red")
        win.write("Novo recorde de {} litros".format(state['score']), align ="center", font=("hendershot", 24, "bold"))      
        win.clear()
        a = a + 0.5
def create_food(state):  
        state['food'] = turtle.Screen()
        state['food'].addshape('gasoleo4.gif')
        state['food'] = turtle.Turtle()
        state['food'].shape('gasoleo4.gif')        
        Pos_X = random.uniform(-280,280)
        Pos_Y = random.uniform(-230,330)
        state['food'].pensize(7)
        state['food'].up()
        state['food'].goto(Pos_X,Pos_Y)
        state['food'].down() 
        ''' 
            Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias, mas dentro dos limites do ambiente.
        '''
    # a informação sobre a comida deve ser guardada em state['food']

def check_if_food_to_eat(state,SPEED):
    snake = state['snake'] 
    food = state['food']
    if (state['food'].distance(snake['head']) < 15):
        state['food'].hideturtle()
        state['score'] = state['score'] + 10
        update_score_board(state)
        if int(state['score']) > int(state['high_score']):
            state['new_high_score'] = state['score']
        SPEED -= 0.05
        snake_body(state)
        create_food(state)    
    ''' 
        Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida estiver a uma distância inferior a 15 pixels a cobra pode comer a peça de comida. 
    '''
    food = state['food']
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do state: state['high_score'], state['score'] e state['new_high_score']

def boundaries_collision(state):
    snake = state['snake']
    if ((-300> snake['head'].xcor()) or (-250 > snake['head'].ycor()) or (299< snake['head'].xcor()) or (350 < snake['head'].ycor())):
        return True 
    
''' 
        Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a função deverá returnar o valor booleano True, caso contrário retorna False.
    '''
def check_collisions(state):
    '''
        Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com os limites do ambiente. No entanto deverá escrever o código para verificar quando é que a tartaruga choca com uma parede ou com o seu corpo.
    '''
    snake = state['snake']    
    for snake_segments in snake['body']:
        if snake_segments.distance(snake['head']) < 15:                      
            return True
    return boundaries_collision(state)
def main():
    state = init_state()
    gasolina(state)
    record(state)    
    borda(state)
    fundo(state)    
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state,SPEED)
        move_snake_tail(state)
        move(state)
        time.sleep(SPEED)  
    print("YOU LOSE")
    if int(state['score']) < int(state['high_score']):
        pontuacao(state)
    if int(state['score']) > int(state['high_score']):
        win(state)
    if state['new_high_score']:
        write_high_score_to_file(state)
    turtle.clearscreen()
    main()
main()

