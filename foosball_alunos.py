import turtle as t
import functools
import random
import time
import math


LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 45
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 4
BOLA_START_POS = (5, 5)


# Funções responsáveis pelo movimento dos jogadores no ambiente. 
# O número de unidades que o jogador se pode movimentar é definida pela constante 
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado 
# do jogo e o jogador que se está a movimentar. 


def jogador_cima(estado_jogo, jogador):
    j = estado_jogo[jogador]
    if j.ycor() < ALTURA_JANELA/2 - PIXEIS_MOVIMENTO:
        j.pu()
        j.setheading(90)
        j.fd(PIXEIS_MOVIMENTO)

def jogador_baixo(estado_jogo, jogador):
    j = estado_jogo[jogador]
    if j.ycor() > -ALTURA_JANELA/2 + PIXEIS_MOVIMENTO:
        j.pu()
        j.setheading(-90)
        j.fd(PIXEIS_MOVIMENTO)


def jogador_direita(estado_jogo, jogador):
    j = estado_jogo[jogador]
    if j.xcor() < LARGURA_JANELA/2 - PIXEIS_MOVIMENTO:
        j.pu()
        j.setheading(0)
        j.fd(PIXEIS_MOVIMENTO)


def jogador_esquerda(estado_jogo, jogador):
    j = estado_jogo[jogador]
    if j.xcor() > -LARGURA_JANELA/2 + PIXEIS_MOVIMENTO:
        j.pu()
        j.setheading(180)
        j.fd(PIXEIS_MOVIMENTO)


def desenha_linhas_campo():
    t.color('white')
    t.pensize(15)
    t.goto(0, ALTURA_JANELA / 2)
    t.goto(0, -ALTURA_JANELA / 2)
    t.goto(0, -RAIO_MEIO_CAMPO*2)
    t.circle(RAIO_MEIO_CAMPO*2)

    t.pu()
    # baliza
    t.fd(-LARGURA_JANELA / 2)
    t.pd()

    for i in range(2):
        t.fd(LADO_MENOR_AREA)
        t.left(90)
        t.fd(LADO_MAIOR_AREA)
        t.left(90)
        t.fd(LADO_MENOR_AREA)

        t.pu()
        t.backward(LARGURA_JANELA)
        t.pd()
    ''' Função responsável por desenhar as linhas do campo, 
    nomeadamente a linha de meio campo, o círculo central, e as balizas. '''
    


def criar_bola():

    bola_t = t.Turtle()
    bola_t.speed(0)
    bola_t.shape("circle")
    bola_t.color("black")
    bola_t.shapesize(stretch_len=1.5, stretch_wid=1.5)
    bola_t.pu()
    bola_t.goto(BOLA_START_POS)
    
    dir_x = random.uniform(-1, 1)
    norma = 1
    dir_y = (norma**2 - dir_x**2)**0.5  #garante q a norma do vetor é ao valor da norma definido na variavel norma em funcao do random dir_x
    
    #print(dir_x)
    #print(dir_y)
    
    bola = {
        'objeto': bola_t,
        'dir_x': dir_x,
        'dir_y': dir_y,
        'last_pos': None
    }
    return bola

    '''
    Função responsável pela criação da bola. 
    Deverá considerar que esta tem uma forma redonda, é de cor preta, 
    começa na posição BOLA_START_POS com uma direção aleatória. 
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores. 
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola, 
    a sua direção no eixo dos xx, a sua direção no eixo dos yy, 
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''



def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.speed(0)
    jogador.shape("circle")
    jogador.color(cor)
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    jogador.pu()
    jogador.goto(x_pos_inicial, y_pos_inicial)
    return jogador

    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''


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
    window = t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width = LARGURA_JANELA,height = ALTURA_JANELA)
    window.tracer(0)
    return window

def cria_quadro_resultados():
    #Code for creating pen for scorecard update
    quadro = t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0,260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco',24,"normal"))
    return quadro


def terminar_jogo(estado_jogo):
    '''
    Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro 
    ''historico_resultados.csv'' com o número total de jogos até ao momento, 
    e o resultado final do jogo. Caso o ficheiro não exista, 
    ele deverá ser criado com o seguinte cabeçalho: 
    NJogo,JogadorVermelho,JogadorAzul.
    '''
    pontos_red = estado_jogo['pontuacao_jogador_vermelho']
    pontos_azul = estado_jogo['pontuacao_jogador_azul']
    open('historico_resultados.csv', 'a').close()
    ficheiro = open('historico_resultados.csv', 'r')
    lines = ficheiro.readlines()
    n_lines = len(lines)
    ficheiro.close()
    ficheiro = open('historico_resultados.csv', 'a')
    if (n_lines == 0):
        ficheiro.write("NJogo,JogadorVermelho,JogadorAzul\n")
        n_lines += 1
    if n_lines > 0: 
        ficheiro.write('{}, {}, {}\n'.format(n_lines, pontos_red, pontos_azul))
        ficheiro.close()

    print("Adeus")
    estado_jogo['janela'].bye()

def setup(estado_jogo, jogar):
    janela = cria_janela()
    #Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho') ,'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho') ,'s')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho') ,'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho') ,'d')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul') ,'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul') ,'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul') ,'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul') ,'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo) ,'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul

def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']),align="center",font=('Monaco',24,"normal"))

def movimenta_bola(estado_jogo):
    dir_x = estado_jogo['bola']['dir_x']
    dir_y = estado_jogo['bola']['dir_y']
    bola_t = estado_jogo['bola']['objeto']
    estado_jogo['bola']['last_pos'] = bola_t.position()

    x, y = bola_t.position()

    bola_t.setpos(x + dir_x, y + dir_y)
    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''
    

def verifica_colisoes_ambiente(estado_jogo):
    var_bola = estado_jogo['var']['bola']
    var_azul = estado_jogo['var']['jogador_azul']
    var_vermelho = estado_jogo['var']['jogador_vermelho']
    
    bola_t = estado_jogo['bola']['objeto']
    jogador_azul = estado_jogo['jogador_azul']
    jogador_vermelho = estado_jogo['jogador_vermelho']
    dir_x = estado_jogo['bola']['dir_x']
    dir_y = estado_jogo['bola']['dir_y']

    x, y = bola_t.position()

    if x <= (-LARGURA_JANELA / 2) + 15 or x >= (LARGURA_JANELA / 2) - 25:  # 15 para a da esquerda, 25 para da direita
        dir_x = -dir_x
        estado_jogo['bola']['dir_x'] = round(dir_x, 2)

        var_bola.append(bola_t.pos())
        var_azul.append(jogador_azul.pos())
        var_vermelho.append(jogador_vermelho.pos())

    if y <= (-ALTURA_JANELA / 2) + 25 or y >= (ALTURA_JANELA / 2) - 20:  # 25 para a de baixo, 20 para a de cima
        dir_y = -dir_y
        estado_jogo['bola']['dir_y'] = round(dir_y, 2)

        var_bola.append(bola_t.pos())
        var_azul.append(jogador_azul.pos())
        var_vermelho.append(jogador_vermelho.pos())

    '''
    Função responsável por verificar se há colisões com os limites do ambiente, 
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais, 
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''


def verifica_golo_jogador_vermelho(estado_jogo):
    var_bola = estado_jogo['var']['bola']
    var_azul = estado_jogo['var']['jogador_azul']
    var_red = estado_jogo['var']['jogador_vermelho']
    ja = estado_jogo['jogador_azul']
    jv = estado_jogo['jogador_vermelho']
    bola_t = estado_jogo['bola']['objeto']

    pontos_vermelho = estado_jogo['pontuacao_jogador_vermelho']
    pontos_azul = estado_jogo['pontuacao_jogador_azul']

    x, y = bola_t.position()

    if x >= LARGURA_JANELA / 2 - 25 and y >= -LADO_MAIOR_AREA / 2 and y <= LADO_MAIOR_AREA / 2:  # -30 para nao contar como colisao, assim, nao salva os dados no var duas vezes atoa :)

        pontos_vermelho += 1
        estado_jogo['pontuacao_jogador_vermelho'] = pontos_vermelho

        linha1 = ''
        linha2 = ''
        linha3 = ''

        for pos1 in var_bola:
            linha1 = linha1 + ','.join(map("{:.3f}".format, pos1))
            linha1 += ';'
        linha1 = linha1[:-1]

        for pos2 in var_red:
            linha2 = linha2 + ','.join(map("{:.3f}".format, pos2))
            linha2 += ';'
        linha2 = linha2[:-1]

        for pos3 in var_azul:
            linha3 = linha3 + ','.join(map("{:.3f}".format, pos3))
            linha3 += ';'
        linha3 = linha3[:-1]

        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha1 + '\n'))
        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha2 + '\n'))
        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha3))

        var_bola.clear()
        var_azul.clear()
        var_red.clear()

        time.sleep(1)

        bola_t.goto(BOLA_START_POS)

        ja.goto(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)
        jv.goto(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)

        dir_x = random.uniform(-1, 1)
        norma = 1
        dir_y = (norma**2 - dir_x**2)**0.5
    
        
        estado_jogo['bola']['dir_x'] = dir_x
        estado_jogo['bola']['dir_y'] = dir_y

        update_board(estado_jogo)
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

def verifica_golo_jogador_azul(estado_jogo):
    var_bola = estado_jogo['var']['bola']
    var_azul = estado_jogo['var']['jogador_azul']
    var_red = estado_jogo['var']['jogador_vermelho']
    ja = estado_jogo['jogador_azul']
    jv = estado_jogo['jogador_vermelho']
    bola_t = estado_jogo['bola']['objeto']

    pontos_vermelho = estado_jogo['pontuacao_jogador_vermelho']
    pontos_azul = estado_jogo['pontuacao_jogador_azul']

    x, y = bola_t.position()

    if x <= -LARGURA_JANELA / 2 + 20 and y >= -LADO_MAIOR_AREA / 2 and y <= LADO_MAIOR_AREA / 2:  # -30 para nao contar como colisao, assim, nao salva os dados no var duas vezes atoa :)

        pontos_azul += 1
        estado_jogo['pontuacao_jogador_azul'] = pontos_azul

        linha1 = ''
        linha2 = ''
        linha3 = ''

        for pos1 in var_bola:
            linha1 = linha1 + ','.join(map("{:.3f}".format, pos1))
            linha1 += ';'
        linha1 = linha1[:-1]

        for pos2 in var_red:
            linha2 = linha2 + ','.join(map("{:.3f}".format, pos2))
            linha2 += ';'
        linha2 = linha2[:-1]

        for pos3 in var_azul:
            linha3 = linha3 + ','.join(map("{:.3f}".format, pos3))
            linha3 += ';'
        linha3 = linha3[:-1]

        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha1 + '\n'))
        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha2 + '\n'))
        open('replay_golo_jv_{}_ja_{}.txt'.format(pontos_vermelho, pontos_azul), 'a').write(str(linha3))

        var_bola.clear()
        var_azul.clear()
        var_red.clear()

        time.sleep(1)

        bola_t.goto(BOLA_START_POS)
        ja.goto(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)
        jv.goto(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)

        dir_x = random.uniform(-1, 1)
        norma = 1
        dir_y = (norma**2 - dir_x**2)**0.5
    
        estado_jogo['bola']['dir_x'] = dir_x
        estado_jogo['bola']['dir_y'] = dir_y

        update_board(estado_jogo)
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


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    
    bola_t = estado_jogo['bola']['objeto']

    bola_x, bola_y = bola_t.pos()
    ja_x, ja_y = estado_jogo['jogador_azul'].pos()
    jogador_azul = estado_jogo['jogador_azul']

    if (ja_x - bola_x)**2 + (ja_y - bola_y)**2 <= (RAIO_BOLA + RAIO_JOGADOR + 10)**2:
        angulo = jogador_azul.towards(bola_x, bola_y)
        dir_y = math.sin(90 - angulo)
        dir_x = math.cos(90 - angulo)
        estado_jogo['bola']['dir_x'] = dir_x
        estado_jogo['bola']['dir_y'] = dir_y



'''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''


def verifica_toque_jogador_vermelho(estado_jogo):

    bola_t = estado_jogo['bola']['objeto']

    bola_x, bola_y = bola_t.pos()
    ja_x, ja_y = estado_jogo['jogador_vermelho'].pos()
    jogador_vermelho = estado_jogo['jogador_vermelho']

    if (ja_x - bola_x) ** 2 + (ja_y - bola_y) ** 2 <= (RAIO_BOLA + RAIO_JOGADOR + 10) ** 2:
        angulo = jogador_vermelho.towards(bola_x, bola_y)
        dir_y = math.sin(90 - angulo)
        dir_x = math.cos(90 - angulo)
        estado_jogo['bola']['dir_x'] = dir_x
        estado_jogo['bola']['dir_y'] = dir_y
    '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''

def guarda_posicoes_para_var(estado_jogo):
    
    estado_jogo['var']['bola'].append(estado_jogo['bola']['objeto'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    while True:
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
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

