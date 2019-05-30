print ('Loading: \nImporting Libraries and Functions')

import pygame,json,pygame.mixer,random,time

from menu import menu
from game import game
from blocks import *
from gameover import gameover_screen


display_menu = True
display_game = False
display_gameover = False

print ('Initiating Pygame and Mixer')

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.set_num_channels(16)

print('Loading Files From Disk')

#IMAGES
arrow = pygame.image.load('arrow.gif')
arrow2 = pygame.image.load('arrow2.gif')
sound_true = pygame.image.load('sound.gif')
sound_false = pygame.image.load('nosound.gif')
music_true = pygame.image.load('music.gif')
music_false =  pygame.image.load('nomusic.gif')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#LOADS ALL FROG IMAGES
frog = []
for a in range(8):
    frog.append(pygame.image.load(str(a)+'.gif'))

#DEFINES SOUNDS AND CHANNELS
#Music
menu_theme = pygame.mixer.Sound('menu_theme.ogg')
menu_theme2 = pygame.mixer.Sound('epic_sax.ogg')
menu_theme3 = pygame.mixer.Sound('Hugh_Mungus_REMIX.ogg')
game_theme = pygame.mixer.Sound('game_theme.ogg')
game_theme2 = pygame.mixer.Sound('HEYYEA.ogg')
game_theme3 = pygame.mixer.Sound('ProleteR-April_Showers.ogg')
game_theme4 = pygame.mixer.Sound('MY HOPE WILL NEVER DIE.ogg')
gameover_theme = pygame.mixer.Sound('game_over.ogg')

mlg = pygame.mixer.Sound('WOMBOCOMBO.ogg')

#Sound Effects
hitmarker = pygame.mixer.Sound('HITMARKER.ogg')
chan = pygame.mixer.Sound('chan.ogg')
line_clear = pygame.mixer.Sound('MOM_GET_THE_CAMERA.ogg')
triple = pygame.mixer.Sound('Oh_Baby_A_Triple.ogg')
airhorn = pygame.mixer.Sound('AIRHORN.ogg')
wow = pygame.mixer.Sound('wow.ogg')
no_one = pygame.mixer.Sound('NEVER_DONE_THAT.ogg')
damn_son = pygame.mixer.Sound('DAMN_SON_WOW.ogg')
sanic = pygame.mixer.Sound('SANIC.ogg')

channel1 = pygame.mixer.Channel(0) # menu_theme
channel2 = pygame.mixer.Channel(1) # game_theme
channel3 = pygame.mixer.Channel(2) # WOMBO COMBO
channel4 = pygame.mixer.Channel(3) # Hitmarker 1
channel5 = pygame.mixer.Channel(4) # Hitmarker 2
channel6 = pygame.mixer.Channel(5) # Hitmarker 3
channel7 = pygame.mixer.Channel(6) # Hitmarker 4
channel8 = pygame.mixer.Channel(7) # Chan
channel9 = pygame.mixer.Channel(8) # line_clear
channel10 = pygame.mixer.Channel(9) # gameover_theme


#LOADS SAVE FILES
with open("blocks.txt",'r') as block_pos:
    loaded_block_pos = json.load(block_pos)
with open("colours.txt",'r') as colour_pos:
    loaded_colour_pos = json.load(colour_pos)
with open("inventory.txt",'r') as inventory:
    loaded_inventory = json.load(inventory)
with open("score.txt",'r') as score:
    loaded_score = json.load(score)
with open("highscore.txt",'r') as highscore:
    highscore = json.load(highscore)

def save(block_pos,colour_pos,inventory,score,highscore):
    if score>highscore:
        highscore = score
    with open("blocks.txt",'w') as outfile:
        json.dump(block_pos,outfile)
    with open("colours.txt",'w') as outfile:
        json.dump(colour_pos,outfile)
    with open("inventory.txt",'w') as outfile:
        json.dump(inventory,outfile)
    with open("score.txt",'w') as outfile:
        json.dump(score,outfile)
    with open("highscore.txt",'w') as outfile:
        json.dump(highscore,outfile)


    
print('Defining Variables')

#Window define
size = (900,700)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Calibri',25,True,False)
pygame.display.set_caption("1010!")

#Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
GRAY = (100,100,100)

#Default values for game logic
score = 0
inventory = [0,0,0]
game_list = []
select_pos = [0,10]
enter_key = False
block_hand = 0
temp_select = None
score_blocks = 0
quit_now = False
SOUND = True
MUSIC = True
gameover_theme_played = False
autosave_interval = 0

#menu_list = {}
##image_number
#menu_list[0] = 1
##menu_choice
#menu_list[1] = 0
##Done? Must remain 'False' unless you want game to quit
#menu_list[3] = False
##Remains false unless you want to load game before intiaiating main game
#menu_list[4] = False
##Copy of SOUND
#menu_list[5] = SOUND
##Copy of MUSIC
#menu_list[6] = MUSIC
#menu_list = [image_number, menu_choice, Done? Must remain 'False' unless you want game to quit, Copy of SOUND, Copy of MUSIC]
menu_list = [1,0,None,False,False,SOUND,MUSIC]


#MATRIXES FOR HOLDING BLOCK MAPS AND COLOUR MAPS
#Rows in the matrix represent columns in the game, or the 'Y' values
#Columns in the matrix represent rows in the game, or the 'X' values
block_pos =[
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]

colour_pos =[
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]

height=375

defaults = {'block_pos':block_pos,'colour_pos':colour_pos,'inventory':inventory,'score':score,'menu_list':menu_list,}

# Loop until user clicks the close button
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

print ('Starting Main Loop\nDrawing Menu')


#------------Main Program Loop------------
while not done:
    enter_key = False
    #-- Main event loop
    pressed = None
    for event in pygame.event.get(): # User did something/
        if event.type == pygame.QUIT or quit_now == True: #If user clicked close
            done = True # Flag that that we are done so we exit
            if display_game == True:
                save(block_pos,colour_pos,inventory,score,highscore)
                
        #Key Presses
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and select_pos[0]>0:
            select_pos[0]-=1
            if SOUND:
                channel4.play(hitmarker)
            if display_game:
                if select_pos2 == 1 and select_pos[1] == 10:
                    select_pos[0] = 1
                elif select_pos2 == 2 and select_pos[1] == 10:
                    select_pos[0] = 4
            #print("Moved Up One Space")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and select_pos[0]<9:
            select_pos[0]+=1
            if display_game:
                if select_pos2 == 0 and select_pos[1] == 10:
                    select_pos[0] = 4
                elif select_pos2 == 1 and select_pos[1] == 10:
                    select_pos[0] = 8
            if SOUND:
                channel5.play(hitmarker)
            #print("Moved Down One Space")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and select_pos[1]>0:
            select_pos[1]-=1
            if SOUND:
                channel6.play(hitmarker)
            #print("Moved Left One Space")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and select_pos[1]<10:
            select_pos[1]+=1
            if SOUND:
                channel7.play(hitmarker)
            #print("Moved Right One Space")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            enter_key = True
            if SOUND:
                channel8.play(chan)
            #print("Enter Key Pressed")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            select_pos[1] = 10

    # ---Game Logic
    if not MUSIC:
        channel1.stop()
        channel2.stop()
        channel10.stop()
        
    
    #ALL CODE INVOLVING MENU SCREEN
    if display_menu == True:
        if channel2.get_busy() or channel10.get_busy() and MUSIC:
            channel2.stop()
            channel10.stop()
        if not channel1.get_busy() and MUSIC:
            song_number = random.randint(1,3)
            print("MENU SONG ID:",song_number)
            if MUSIC and song_number == 1:
                channel1.play(menu_theme)
            elif MUSIC and song_number == 2:
                channel1.play(menu_theme2)
            elif MUSIC and song_number == 3:
                channel1.play(menu_theme3)
        menu_list = menu(menu_list,frog,done,loaded_block_pos,loaded_colour_pos,loaded_inventory,loaded_score,highscore,BLOCKID,COLOURS,channel3,mlg,SOUND,MUSIC,sound_true,sound_false,music_true,music_false)
        done = menu_list[3]
        if menu_list[1] == 1:
            display_menu = False
            display_game = True
            score = defaults['score']
            inventory = defaults['inventory']
            block_pos = defaults['block_pos']
            colour_pos = defaults['colour_pos']
        if menu_list[4] == True:
            display_menu = False
            display_game = True
            #This code loads the game data from file
            with open("blocks.txt",'r') as block_pos:
                block_pos = json.load(block_pos)
            with open("colours.txt",'r') as colour_pos:
                colour_pos = json.load(colour_pos)
            with open("inventory.txt",'r') as inventory:
                inventory = json.load(inventory)
            with open("score.txt",'r') as score:
                score = json.load(score)
        SOUND = menu_list[5]
        MUSIC = menu_list[6]
    #ALL CODE INVOLVING THE GAME SCREEN       
    if display_game == True:
        if channel1.get_busy() or channel10.get_busy() and MUSIC:
            channel1.stop()
            channel10.stop()
        if not channel2.get_busy() and MUSIC:
            song_number2 = random.randint(1,4)
            print("GAME SONG ID:",song_number2)
            if MUSIC and song_number2 == 1:
                channel2.play(game_theme)
            elif MUSIC and song_number2 == 2:
                channel2.play(game_theme2)
            elif MUSIC and song_number2 == 3:
                channel2.play(game_theme3)
            elif MUSIC and song_number2 == 4:
                channel2.play(game_theme4)
        game_list = game(screen,block_pos,colour_pos,score,highscore,select_pos,BLOCKS,BLOCKID,COLOURS,inventory,arrow,arrow2,enter_key,block_hand,temp_select,score_blocks,airhorn,wow,line_clear,triple,no_one,damn_son,sanic,channel9)
        block_pos = game_list[0]
        colour_pos = game_list[1]
        score = game_list[2]
        block_hand = game_list[3]
        #print("BLOCKHAND IN MAIN LOOP",block_hand)
        temp_select = game_list[4]
        score_blocks = game_list[5]
        select_pos2 = game_list[6]
        gameover = game_list[7]
        if gameover == True:
            display_game = False
            display_menu = False
            display_gameover = True
            
            
    #ALL CODE INVOLVING GAME OVER SCREEN
    if display_gameover == True:
        score = defaults['score']
        inventory = defaults['inventory']
        block_pos = defaults['block_pos']
        colour_pos = defaults['colour_pos']
        save(block_pos,colour_pos,inventory,score,highscore)
        gameover_list = gameover_screen(screen,score,highscore)
        quit_now = gameover_list[1]
        if gameover_theme_played == False and MUSIC:
            pygame.mixer.stop()
            channel10.play(gameover_theme)
            gameover_theme_played = True
        if gameover_list[0] == True:
            display_game = False
            display_gameover = False
            display_menu = True
            menu_list = [1,0,None,False,False,SOUND,MUSIC]
    
    #AUTOSAVE
    if display_game == True:
        autosave_interval += 1
        if autosave_interval == 1000:
            save(block_pos,colour_pos,inventory,score,highscore)
            autosave_interval = 0
            print("Autosave Completed")

    # ---Drawing code should go here
    
    
    # First clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased
    clock.tick(20)
    # ---Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # ---Limit to 60 frames per second
pygame.quit()
