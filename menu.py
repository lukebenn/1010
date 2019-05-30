def position(x_grid,y_grid):
    pos = {}
    x_pos = 20*(x_grid)+650
    y_pos = 20*(y_grid)+350
    
    pos[0] = x_pos
    pos[1] = y_pos
    
    return pos

def block_draw(screen,block_pos,colour_pos):
    import pygame
    for y in range(0,10):
        for x in range(0,10):
            if block_pos[x][y] == 1:
                if colour_pos[x][y] != 0:
                    #print("BLOCK at ",x,y,"is",block_pos[x][y])
                    draw_colour = colour_pos[x][y]
                elif colour_pos[x][y] == 0:
                    draw_colour = (255,0,0)
                pos = position(x,y)
                pygame.draw.rect(screen,draw_colour,[pos[0],pos[1],15,15])

def inventory_draw(screen,inventory,BLOCKID,COLOURS):
    import pygame
    for a in range(3):
        if inventory[a] != 0:
            temp_block = BLOCKID[inventory[a]]
            #print(temp_block)
            for y in range(len(temp_block)):
                try:
                    length = len(temp_block[0])
                except TypeError:
                    length = 1
                for x in range(length):
                    if temp_block[y][x] == 1:
                        pos = position(x+(a*5.5)-3,y+11.5)
                        pygame.draw.rect(screen,COLOURS[inventory[a]],[pos[0],pos[1],15,15])


def menu(menu_list,frog,done,block_pos,colour_pos,inventory,score,highscore,BLOCKID,COLOURS,channel3,mlg,SOUND,MUSIC,sound_true,sound_false,music_true,music_false):
    import pygame
    import pygame.mixer
    GRAY = (100,100,100)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    LIGHT_GREEN = (0,255,0)
    GREEN = (0,200,0)
    DARK_GREEN = (0,160,0)
    RED = (200,0,0)
    LIGHT_RED = (255,0,0)
    DARK_RED = (160,0,0)
    DEEP_BLUE = (12,50,87)
    LIGHT_YELLOW = (255,255,0)
    YELLOW = (200,200,0)
    
    image_number = menu_list[0]
    if image_number>7:
        image_number = 0
        
    mouse_click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    
    event = pygame.event.get()
    size = (900,700)
    screen = pygame.display.set_mode(size)

    #Defines fonts
    font = pygame.font.SysFont('Eurostile',72,True,False)
    font2 = pygame.font.SysFont('Eurostile',24,True,False)
    font3 = pygame.font.SysFont('Eurostile',48,True,False)
    font4 = pygame.font.SysFont('Eurostile',36,True,False)

    #Defines text
    title = font.render("1010!:",True,BLACK)
    subtitle = font2.render("The Untold, Underwelming Story",True,BLACK)
    subtitle2 = font2.render("About Blocks.",True,BLACK)
    score_text = font2.render(("Score: "+str(score)),True,BLACK)
    
    new = font3.render("New Game",True,BLACK)
    load = font3.render("Load Game",True,BLACK)
    stop = font3.render("Quit",True,BLACK)
    
    current = font2.render("Last Saved Game",True,BLACK)
    highscore_text = font4.render(("Highscore: "+str(highscore)),True,BLACK)
    
    light_new = font3.render("New Game",True,DARK_GREEN)
    light_load = font3.render("Load Game",True,DARK_GREEN)
    light_stop = font3.render("Quit",True,DARK_RED)
    
    howto = []
    howto.append(font4.render("HOW TO PLAY:",True,BLACK))
    howto.append(font2.render("-Use Arrow Keys to Select Block",True,BLACK))
    howto.append(font2.render("-Press Enter Key to Pick Up Block",True,BLACK))
    howto.append(font2.render("-Place Block in Complete Rows to Raise Score",True,BLACK))
    howto.append(font2.render("-Press Space Bar to Quickly Snap to Right Side",True,BLACK))
    howto.append(font2.render("-Frog = WOMBO COMBO",True,BLACK))

    #Code to draw everything on screen
    screen.fill(WHITE)
    screen.blit(title,[50,50])
    screen.blit(subtitle,[50,100])
    screen.blit(subtitle2,[50,120])
    pygame.draw.rect(screen, GREEN, [80,200,250,40])
    pygame.draw.rect(screen, GREEN, [80,300,250,40])
    pygame.draw.rect(screen, RED, [80,400,250,40])
    screen.blit(new,[100,205])
    screen.blit(load,[100,305])
    screen.blit(stop,[100,405])
    screen.blit(frog[image_number],[100,505])
    for a in range(6):
        screen.blit(howto[a],[450,10+a*25])

    #Code to draw sound and music icons
    if SOUND:
        screen.blit(sound_true,[520,640])
    if not SOUND:
        screen.blit(sound_false,[520,640])
    if MUSIC:
        screen.blit(music_true,[450,640])
    if not MUSIC:
        screen.blit(music_false,[450,640])
    
    #THIS CODE WILL DRAW PREVIOUS SAVE ON MENU SCREEN
    pygame.draw.rect(screen, WHITE, [575,250,325,475])
    screen.blit(score_text,[610,310])
    for y in range(10):
        for x in range(10):
            pygame.draw.rect(screen,GRAY,[20*x+650,20*y+350,15,15])
            
    block_draw(screen,block_pos,colour_pos)
    inventory_draw(screen,inventory,BLOCKID,COLOURS)
    screen.blit(current,[610,280])
    screen.blit(highscore_text,[620,670])
    
    #Detects mouse button position for highlighting buttons
    #New Game Button
    if 80+250 > mouse[0] > 80 and 200+40 > mouse[1] > 200:
        pygame.draw.rect(screen, LIGHT_GREEN, [80,200,250,40])
        screen.blit(light_new,[100,205])
    #Load Game Button
    elif 80+250 > mouse[0] > 80 and 300+40 > mouse[1] > 300:
        pygame.draw.rect(screen, LIGHT_GREEN, [80,300,250,40])
        screen.blit(light_load,[100,305])
    #Quit Button    
    elif 80+250 > mouse[0] > 80 and 400+40 > mouse[1] > 400:
        pygame.draw.rect(screen, LIGHT_RED, [80,400,250,40])
        screen.blit(light_stop,[100,405])

    #Music Button
    elif 450+50 > mouse[0] > 450 and 640+50 > mouse[1] > 640:
        #pygame.draw.rect(screen, LIGHT_RED, [450,640,50,50])
        if mouse_click[0] == 1:
            if MUSIC:
                MUSIC = False
            elif not MUSIC:
                MUSIC = True
    #Sound Button
    elif 520+50 > mouse[0] > 520 and 640+50 > mouse[1] > 640:
        #pygame.draw.rect(screen, LIGHT_RED, [520,640,50,50])
        if mouse_click[0] == 1:
            if SOUND:
                SOUND = False
            elif not SOUND:
                SOUND = True
    
    #Detects mouse clicks for buttons
    if 80+250 > mouse[0] > 80 and 200+40 > mouse[1] > 200 and mouse_click[0] == 1:
        print("Play Button Clicked")
        menu_list[1] = 1
        
    elif 80+250 > mouse[0] > 80 and 300+40 > mouse[1] > 300 and mouse_click[0] == 1:
        print("Load Function intiated")
        menu_list[4] = True
        
    elif 80+250 > mouse[0] > 80 and 400+40 > mouse[1] > 400 and mouse_click[0] == 1:
        print("Quit Function intiated")
        menu_list[3] = True
    elif 100+200 > mouse[0] > 80 and 505+200 > mouse[1] > 400 and mouse_click[0] == 1:
        if not channel3.get_busy() and SOUND:
            channel3.play(mlg)
            print("WOMBO COMBO")
        elif channel3.get_busy():
            channel3.stop()
            print("EDDIE FALCON")
    image_number += 1
    menu_list[0] = image_number

    menu_list[5] = SOUND
    menu_list[6] = MUSIC
    
    return menu_list
