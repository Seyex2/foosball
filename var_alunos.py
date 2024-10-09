import foosball_alunos

def le_replay(nome_ficheiro):
    bola = []
    ja = []
    jv = []
    listas_str = []
    a = open(nome_ficheiro, 'r').read().split('\n')
    for i in range(3):
        valores_str = a[i].split(';')
        listas_str.append(valores_str)
        valores_str = ''
    
    for str_cord in listas_str[0]:
        str_cord_list = str_cord.split(',')
        a = tuple([float(str_cord_list[0]),float(str_cord_list[1])])
        bola.append(a)
    #print(bola)
    for str_cord in listas_str[1]:
        str_cord_list = str_cord.split(',')
        a = tuple([float(str_cord_list[0]),float(str_cord_list[1])])
        jv.append(a)
    #print(ja)
    for str_cord in listas_str[2]:
        str_cord_list = str_cord.split(',')
        a = tuple([float(str_cord_list[0]),float(str_cord_list[1])])
        ja.append(a)
    #print(jv)
    
    dados = {
            'bola' : bola,
            'jogador_vermelho' : jv,
            'jogador_azul' : ja
    }
    
    return dados
    
    '''
    Função que recebe o nome de um ficheiro contendo um replay, e que deverá 
    retornar um dicionário com as seguintes chaves:
    bola - lista contendo tuplos com as coordenadas xx e yy da bola
    jogador_vermelho - lista contendo tuplos com as coordenadas xx e yy da do jogador\_vermelho
    jogador_azul - lista contendo tuplos com as coordenadas xx e yy da do jogador\_azul
    '''
    
        


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay('replay_golo_jv_1_ja_1.txt')
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['objeto'].setpos(replay['bola'][i])
    estado_jogo['janela'].exitonclick()


if __name__ == '__main__':
    main()