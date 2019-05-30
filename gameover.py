def gameover_screen(screen,score,highscore):
    import pygame
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

    return_to_menu = False
    stop_game = False
    
    screen.fill(GRAY)

    mouse_click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    
    font = pygame.font.SysFont('Eurostile',72,True,False)
    font2 = pygame.font.SysFont('Eurostile',48,True,False)
    font3 = pygame.font.SysFont('Eurostile',36,True,False)
    
    title = font.render("GAME OVER",True,BLACK)
    return_menu = font2.render("Main Menu",True,BLACK)
    stop = font2.render("Quit",True,BLACK)
    
    highscore_text = font3.render(("Highscore: "+str(highscore)),True,BLACK)
    score_text = font3.render(("Score: "+str(score)),True,BLACK)

    light_return_menu = font2.render("Main Menu",True,DARK_GREEN)
    light_stop = font2.render("Quit",True,DARK_RED)

    pygame.draw.rect(screen, GREEN, [570,200,250,40])
    pygame.draw.rect(screen, RED, [570,400,250,40])

    screen.blit(title,[50,50])
    screen.blit(return_menu,[590,205])
    screen.blit(stop,[590,405])
    screen.blit(highscore_text,[200,300])
    screen.blit(score_text,[200,400])

    #Detects mouse button position for highlighting buttons
    if 570+250 > mouse[0] > 570 and 200+40 > mouse[1] > 200:
        pygame.draw.rect(screen, LIGHT_GREEN, [570,200,250,40])
        screen.blit(light_return_menu,[590,205])
        
    elif 570+250 > mouse[0] > 570 and 400+40 > mouse[1] > 400:
        pygame.draw.rect(screen, LIGHT_RED, [570,400,250,40])
        screen.blit(light_stop,[590,405])
    
    #Detects mouse clicks for buttons
    if 570+250 > mouse[0] > 570 and 200+40 > mouse[1] > 200 and mouse_click[0] == 1:
        print("'Return to Menu' Button Clicked")
        return_to_menu = True
        
    elif 570+250 > mouse[0] > 570 and 400+40 > mouse[1] > 400 and mouse_click[0] == 1:
        print("Quit Function intiated")
        stop_game = True

    gameover_list=(return_to_menu,stop_game)
    return gameover_list
