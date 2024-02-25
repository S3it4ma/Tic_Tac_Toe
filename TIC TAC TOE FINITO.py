import pygame
import random
from pygame.locals import *
import os
import sys
from funzioni_i import init_matrix, calc_grid

WIDTH = 900
HEIGHT = 700
box_lenght = 170                                   # grandezza di ogni box quadrato che conterrà 'X' o 'O'
grid_dim = 170*3                                   # grandezza della griglia

# prima mossa
turn = random.choice(['computer', 'player'])

# variabile utile per passare dalla schermata iniziale a quella di scelta della difficoltà e del segno, prima di giocare effettivamente
game_state = 'start'     

# scelta della difficoltà         
difficulty = ''

# scelta del segno
symbol =''

# first e num_turn sono necessari per gestire i casi più difficili nell'algoritmo delle difficoltà, in particolare first è vero quando il computer esegue la prima mossa
# mentre num_turn calcola il numero di turni
first = False                                          
num_turn = 0

if turn == 'computer':
    first = True


pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')

box_dict = calc_grid(WIDTH, HEIGHT, box_lenght, 3)

clock = pygame.time.Clock()


start = pygame.sprite.Sprite
start.image = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "button_play.png"))
start.rect = (start.image).get_rect()
start.rect.center = (450,337)

choose = pygame.sprite.Sprite()
choose.image = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "choose_diff.png"))
choose.rect = choose.image.get_rect()
choose.rect.center = (WIDTH/2, HEIGHT/2)

choose_sym = pygame.sprite.Sprite()
choose_sym.image = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "symbol.png"))
choose_sym.rect = pygame.Rect(0, 0, 400, 200)                                 
choose_sym.rect.center = (WIDTH/2, HEIGHT/2)

restart = pygame.sprite.Sprite()
restart.image = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "restart.png"))
restart.rect = restart.image.get_rect()
restart.rect.center = (100, 50)

draw_surf = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "draw.png"))
won_surf = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "you_won.png"))
lost_surf = pygame.image.load(os.path.join("sounds_and_images\\tic_tac_toe", "you_lost.png"))                                              


def set_restart():
    '''Riporta il gioco alle condizioni iniziali'''
    
    global turn, game_state, difficulty, symbol, first, num_turn, matrix, box_dict, buttons_group
    
    turn = random.choice(['computer', 'player'])
    game_state = 'start'
    difficulty = ''
    symbol = ''
    first = False
    num_turn = 0

    if turn == 'computer':
        first = True

    matrix = init_matrix(3, 3) 

    buttons_group = pygame.sprite.Group(choose, restart)


def victory_check(matrix):
    '''Verifica se qualcuno tra i due giocatori ha vinto'''

    for i in range(3):

        if (matrix[i][0] != 0) and (matrix[i][0] == matrix[i][1] == matrix[i][2]):
            return True

        if (matrix[0][i] != 0) and (matrix[0][i] == matrix[1][i] == matrix[2][i]):
            return True

    if matrix[1][1] != 0 and (matrix[0][0] == matrix[1][1] == matrix[2][2] or matrix[2][0] == matrix[1][1] == matrix[0][2]):
        return True
    
    return False


def full_grid(matrix):
    '''Verifica se la griglia è piena (utile nel caso di un pareggio)'''

    for i in range(3):
        for j in range(3):

            if matrix[i][j] == 0:
                return False
    return True


def computer_move(difficulty, matrix, first, num_turn):
    '''mossa del computer basata sulla scelta della difficoltà:
    easy --> scelta casuale;
    medium --> l'algoritmo riconosce righe e colonne, ma non diagonali;
    impossible --> oltre a riconoscere i casi principali (righe, colonne, diagonali) riconosce anche i casi particolari come i "doppi tris" '''

    # l'algoritmo si basa sulla somma delle righe/colonne/diagonali (alla posizione (i, j) della matrice corrisponde 1 se è una scelta del computer, -1 se dell'avversario)

    # la variabile switch_value entra in gioco nelle modalità medio/difficile, dove per riconoscere due elementi sulla stessa riga/colonna/diagonale
    # (e quindi un potenziale tris), l'algoritmo verifica che la loro somma sia esattamente 2 al primo ciclo del for, e -2 nel secondo e in tal caso siamo anche
    # sicuri che il terzo elemento sia vuoto, poichè altrimenti andrebbe sottratto o aggiunto un 1 alla somma

    switch_value = 2                              
    
    if difficulty == 'easy':
        
        move = False
        while not move:
            
            choice = (random.randint(0,2), random.randint(0,2))
            
            if matrix[choice[0]][choice[1]] == 0 or full_grid(matrix):
                move = True

    if difficulty == 'medium':
        
        if matrix[1][1] == 0:
            return (1, 1)

        for check in range(2):                              
            col = 2                                       

            for i in range(3):

                sum_ = 0

                ### verifica le righe
                if sum(matrix[i]) == switch_value:
                        
                    for j in range(3):

                        if matrix[i][j] == 0:
                            return (i, j)

                #### verifica le colonne
                for j in range(3):

                    if matrix[j][i] == 0:
                        box = (j, i)
                    
                    sum_ += matrix[j][i]

                if sum_ == switch_value:
                    return box
            
            switch_value = -2


        else:
            move = False
            while not move:
                    
                choice = (random.randint(0,2), random.randint(0,2))
                    
                if matrix[choice[0]][choice[1]] == 0 or full_grid(matrix):
                    move = True
        

    if difficulty == 'impossible':

        if matrix[1][1] == 0:
            return (1, 1)

        # empty_m_diag e empty_s_diag si riferiscono rispettivamente alla diagonale principale e secondaria e serviranno
        # per gestire i casi più difficili. Diverranno True se almeno un elemento della diagonale è vuoto
        empty_m_diag = False
        empty_s_diag = False

        for check in range(2):
            col = 2
            sum_m_diag = 0
            sum_s_diag = 0

            for i in range(3):

                sum_ = 0

                ### verifica le righe
                if sum(matrix[i]) == switch_value:
                        
                    for j in range(3):

                        if matrix[i][j] == 0:
                            return (i, j)

                #### verifica le colonne
                for j in range(3):

                    if matrix[j][i] == 0:
                        box = (j, i)
                    
                    sum_ += matrix[j][i]

                if sum_ == switch_value:
                    return box

                ###  verifica la diagonale secondaria
                sum_s_diag += matrix[i][col]
                
                if matrix[i][col] == 0:                   
                    box_s = (i, col)
                    empty_s_diag = True                               
                
                col -= 1

                ### verifica la diagonale principale
                if matrix[i][i] == 0:                    
                    box_m = (i, i)
                    empty_m_diag= True                                          

                sum_m_diag += matrix[i][i]


            if sum_m_diag == switch_value:
                return box_m

            if sum_s_diag == switch_value:
                return box_s
            
            switch_value = -2

##################################################################### casi più difficili, che occorrono esclusivamente al terzo turno

        if  num_turn == 3:

            if not first:

                if matrix[1][1] == -1:

                    if not empty_m_diag:                        
                        choice = random.choice([(2, 0), (0, 2)])                                       
                    if not empty_s_diag:
                        choice = random.choice([(0, 0), (2, 2)])

                else:
                    if (not empty_m_diag) or (not empty_s_diag):
                        return random.choice([(1, 0), (1, 2), (0, 1), (2, 1)])

                    if empty_m_diag or empty_s_diag:
                            
                        if sum(matrix[1]) == 1:
                            return random.choice([(1, 0), (1, 2)])

                        elif (matrix[0][1] + matrix[2][1]) == 0:
                            return random.choice([(0, 1), (2, 1)])
                            
                        else:
                            for i in range(3):
                                    
                                if sum(matrix[i]) == -1:

                                    for j in range(3):
                                            
                                        if matrix[i][j] == 0:
                                            return (i, j)

###############################################################################

        else: 
            move = False
            while not move:
                    
                choice = (random.randint(0,2), random.randint(0,2))
                    
                if matrix[choice[0]][choice[1]] == 0 or full_grid(matrix):
                    move = True
                    
    return choice

        

def draw_win():
    '''draw_win è necessaria solamente nella fase iniziale del gioco, prima e durante la scelta della difficoltà e del simbolo. Questo perchè l'interfaccia
    rimane statica dopo tali fasi: solo i segni vengono aggiunti dentro le caselle.'''

    win.fill((100,100,100))

    # grazie a start_setup il gruppo di sprite buttons_group viene opportunamente modificato per disegnare correttamente i bottoni
    buttons_group.draw(win)

    # l'if serve ad evitare che la griglia venga disegnata prima dell'inizio effettivo del gioco, attraverso i booleani choose.alive() e choose_sym.alive(), che
    # verificano che i due sprite siano all'interno del gruppo start_group.

    if (not choose.alive() and not choose_sym.alive()):
        pygame.draw.line(win, (0,0,0), ((WIDTH/2)-(box_lenght/2), (HEIGHT/2)-(grid_dim/2)), ((WIDTH/2)-(box_lenght/2), (HEIGHT/2)+(grid_dim/2)), 2)
        pygame.draw.line(win, (0,0,0), ((WIDTH/2)+(box_lenght/2), (HEIGHT/2)-(grid_dim/2)), ((WIDTH/2)+(box_lenght/2), (HEIGHT/2)+(grid_dim/2)), 2)

        pygame.draw.line(win, (0,0,0), ((WIDTH/2)-(grid_dim/2), (HEIGHT/2)-(box_lenght/2)), ((WIDTH/2)+(grid_dim/2), (HEIGHT/2)-(box_lenght/2)), 2)
        pygame.draw.line(win, (0,0,0), ((WIDTH/2)-(grid_dim/2), (HEIGHT/2)+(box_lenght/2)), ((WIDTH/2)+(grid_dim/2), (HEIGHT/2)+(box_lenght/2)), 2)
    
    pygame.display.flip()



def start_setup():

    win.fill((100,100,100))
    win.blit(start.image, start.rect)                     # schermata e bottone di inizio
    pygame.display.flip()

    game_start = False 

    global game_state, difficulty, symbol

    while not game_start:
        
        for ev in pygame.event.get():

            if ev.type == QUIT:
                game_start = True
                pygame.quit()

            # il continue in ciascuno degli if è essenziale per evitare che la macchina consideri un click come una scelta di più fasi (ad esempio lo stesso click
            # determina la modalità facile e il segno cerchio)

            if ev.type == MOUSEBUTTONUP and start.rect.collidepoint(ev.pos) and game_state == 'start':
                draw_win()    
                # ||               
                # \/ 
                # in draw_win(), il comando buttons_group.draw() disegna, alla prima chiamata, il bottone di scelta della difficoltà e il 'restart'

                game_state = 'choose'
                continue
                        
            if ev.type == MOUSEBUTTONUP and choose.rect.collidepoint(ev.pos) and game_state == 'choose':

                click = ev.pos

                if 368 <= click[0] <= 532 and 285 <= click[1] <= 340:
                    difficulty = 'easy'
                if 368 <= click[0] <= 532 and 355 <= click[1] <= 410:
                    difficulty = 'medium'
                if 368 <= click[0] <= 532 and 425 <= click[1] <= 480:
                    difficulty = 'impossible'               

                if difficulty != '':

                    choose.remove(buttons_group)
                    buttons_group.add(choose_sym)
                    draw_win()

                    game_state = 'choose_sym'               
                continue


            if ev.type == MOUSEBUTTONUP and choose_sym.rect.collidepoint(ev.pos) and game_state == 'choose_sym':

                click = ev.pos

                if 275 <= click[0] <= 425 and 345 <= click[1] <= 420:
                        symbol = 'X'
                if 475 <= click[0] <= 625 and 345 <= click[1] <= 420:
                        symbol = 'O'
                        
                if symbol != '':

                    choose_sym.remove(buttons_group)
                    draw_win()

                    game_start = True



def draw_sign(symbol, player, ev): 
    '''funzione utile a disegnare i simboli (croce o cerchio) dove symbol è il simbolo scelto dall'utente, player è il giocatore: 1 = computer; -1 = utente,
    ev è l'evento pygame.
    La funzione inoltre cambia il turno: da computer a player e viceversa.'''

    global turn

    if symbol == 'X':

        if player == 1:                                                   

            (i, j) = computer_move(difficulty, matrix, first, num_turn)

            matrix[i][j] = 1

            rect = box_dict[(i, j)]

            pygame.draw.circle(win, (255,0,0), rect.center, 50, 3)

            turn = 'player'

        
        elif player == -1:

            click = ev.pos                
                
            for box, values in box_dict.items():

                rect = values
                (i, j) = box              
                    
                if rect.collidepoint(click) and matrix[i][j] == 0:

                    matrix[i][j] = -1
                    (x, y) = rect.center

                    pygame.draw.line(win, (0, 0, 255), (x-50, y-50), (x+50, y+50), 5)
                    pygame.draw.line(win, (0, 0, 255), (x-50, y+50), (x+50, y-50), 5)

                    turn = 'computer'


    if symbol == 'O':
        
        if player == 1:

            (i, j) = computer_move(difficulty, matrix, first, num_turn)

            matrix[i][j] = 1

            rect = box_dict[(i, j)]

            (x, y) = rect.center

            pygame.draw.line(win, (0, 0, 255), (x-50, y-50), (x+50, y+50), 5)
            pygame.draw.line(win, (0, 0, 255), (x-50, y+50), (x+50, y-50), 5)
            
            turn = 'player'

        
        elif player == -1:

            click = ev.pos                
                
            for box, values in box_dict.items():

                rect = values
                (i, j) = box
                    
                if rect.collidepoint(click) and matrix[i][j] == 0:

                    matrix[i][j] = -1

                    pygame.draw.circle(win, (255,0,0), rect.center, 50, 3)

                    turn = 'computer'




def main():

    global turn, game_state, difficulty, symbol, first, num_turn

    set_restart()

    clock.tick(20)

    start_setup()

    done = False 

    while not done:
        for ev in pygame.event.get():
            
            if ev.type == QUIT:
                done = True
            
            if ev.type == MOUSEBUTTONUP and restart.rect.collidepoint(ev.pos):
                done = True
                main()

            if victory_check(matrix):

                # il turno viene cambiato dopo ogni mossa perciò se il turno è dell'utente vuol dire che l'ultima mossa, quella vincente, è del computer e viceversa.
                
                if turn == 'player':                   
                    win.blit(lost_surf, (200, 200))

                elif turn == 'computer':
                    win.blit(won_surf, (200, 200))

                # i numeri magici qui sotto sono le posizioni in cui si trova il bottone 'play again' (è solo disegnato su una surface, non ha un rect, poichè ho creato
                # le immagini con gimp al fine di avere un miglior aspetto grafico)
                if ev.type == MOUSEBUTTONUP and 330 < ev.pos[0] < 570 and 350 < ev.pos[1] < 450:
                    done = True
                    main()

            if not victory_check(matrix) and full_grid(matrix):

                win.blit(draw_surf, (200, 200))

                if ev.type == MOUSEBUTTONUP and 330 < ev.pos[0] < 570 and 350 < ev.pos[1] < 450:
                    done = True
                    main()


            if not victory_check(matrix) and not full_grid(matrix):

                if turn == 'computer' and not victory_check(matrix):
                    draw_sign(symbol, 1, ev)
                    num_turn +=1

                elif ev.type == MOUSEBUTTONUP and turn == 'player': 
                    draw_sign(symbol, -1, ev)
                    num_turn += 1
        
        pygame.display.flip()


if __name__ == '__main__':
    main()

pygame.quit()
sys.exit()