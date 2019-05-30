#Converts positions on 10 by 10 grid to cordinats to be used by draw commands
def position(x_grid,y_grid):
    pos = {}
    x_pos = 40*(x_grid)+25
    y_pos = 40*(y_grid)+150
    
    pos[0] = x_pos
    pos[1] = y_pos
    
    return pos

def position2(x_grid,y_grid):
    pos = {}
    x_pos = 32*(x_grid)+25
    y_pos = 32*(y_grid)+150
    
    pos[0] = x_pos
    pos[1] = y_pos
    

    return pos

#Checks rows and columns, clears complete row or column, and returns score
def row_column_check(block_pos,colour_pos,score,airhorn,wow,line_clear,triple,no_one,damn_son,sanic,channel9):
    complete_rows = []
    complete_columns = []
    #Scans Y columns and adds full columns to list
    for a in range(0,10):
        blocksY = 0
        blocksY = block_pos[a].count(1)
        if blocksY == 10:
            complete_columns.append(a)
            print("Found a complete row y column! In column,",a)
            
    #Scans X rows and adds full rows to list
    for a in range(0,10):
        blocksX = 0
        for b in range(0,10):
            if block_pos[b][a] == 1:
                blocksX = blocksX + 1
        if blocksX == 10:
            complete_rows.append(a)
            print("Found a complete row x row! In row,",a)

    #Calculates score based on # of rows and columns
    if len(complete_rows) != 0 or len(complete_columns) != 0:
        total = len(complete_rows) + len(complete_columns)
        print("Total number of detected rows:",total)
        scorelist=(10,25,60,100,150,300)
        score = score+int(scorelist[total-1])
        print("SCORE:",score)
        if total == 1:
            channel9.play(airhorn)
        if total == 2:
            channel9.play(wow)
        if total == 3:
            channel9.play(triple)
        if total == 4:
            channel9.play(line_clear)
        if total == 5:
            channel9.play(damn_son)
        if total == 6:
            channel9.play(sanic)
        if total == 7:
            channel9.play(no_one)
        
    #CLEARS ROWS
        #Clears Y rows
        for a in range(10):
            if a in complete_columns:
                for b in range(10):
                    block_pos[a][b] = 0
        #Clears Y rows
        for a in range(10):
            if a in complete_rows:
                for b in range(10):
                    block_pos[b][a] = 0

    templist = {}
    templist[0] = block_pos
    templist[1] = colour_pos
    templist[2] = score
    
    return templist

#Given the block_pos and colour_pos matrix this function will draw blocks on screen
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
                pygame.draw.rect(screen,draw_colour,[pos[0],pos[1],30,30])

#Generates Random blocks to be put in inventory when it is fully empty
def block_get(inventory,BLOCKS):
    import random
    if inventory[0] == 0 and inventory[1] == 0 and inventory[2] == 0:
        for a in range(len(inventory)):
            inventory[a] = BLOCKS[random.randint(0,len(BLOCKS)-1)]
        print('INVENTORY:',inventory)
    return inventory

#Draws the inventory on screeen (To the right of the 10 by 10 board)
def inventory_draw(screen,inventory,BLOCKID,COLOURS,temp_select,select_pos2):
    import pygame
    for a in range(3):
        if inventory[a] != 0 and temp_select != a:
            temp_block = BLOCKID[inventory[a]]
            #print(temp_block)
            for y in range(len(temp_block)):
                try:
                    length = len(temp_block[0])
                except TypeError:
                    length = 1
                for x in range(length):
                    if temp_block[y][x] == 1:
                        pos = position2(16+x,y+(a*5.5))
                        if select_pos2 == a:
                            pygame.draw.rect(screen,(255,165,0),[pos[0]-5,pos[1]-5,35,35])
                        pygame.draw.rect(screen,COLOURS[inventory[a]],[pos[0],pos[1],25,25])

#Draws the arrows to show where you are selecting
def select_draw(screen,select_pos,block_pos,arrow,arrow2,block_hand):
    import pygame
    if block_hand == 0:
        box_colour = (255,165,0)
    else:
        box_colour = (255,0,0)
    if select_pos[1]<10:
        select_pos2 = -1
        #ORANGE HIGHLIGHTING BOX
        if block_hand == 0:
            pos = position(select_pos[1],select_pos[0])
            pygame.draw.rect(screen,box_colour,[pos[0]-5,pos[1]-5,40,40])
        #ARROW ON TOP
        pos = position(select_pos[1],-1)
        screen.blit(arrow,(pos[0],pos[1]+20))
        #ARROW ON LEFT
        pos = position(-1,select_pos[0])
        screen.blit(arrow2,(pos[0]+20,pos[1]))
    #Generates arrows to the left to select inventory slot
    elif select_pos[1]>=10:
        if select_pos[0]>=0 and select_pos[0]<3:
            select_pos2 = 0
        elif select_pos[0]>=3 and select_pos[0]<7:
            select_pos2 = 1
        elif select_pos[0]>=7 and select_pos[0]<=9:
            select_pos2 = 2
        pos = position(11,select_pos2*4)
        screen.blit(arrow2,(pos[0]+20,pos[1]))
    return select_pos2

#When the selector is selecting one of the inventory blocks and presses enter,
#script will 'pick up' the block and start drawing it relative to the selector
def block_grab(screen,select_pos,select_pos2,inventory,COLOURS,BLOCKID,enter_key,block_hand,temp_select):
    import pygame
    score_blocks = 0
    if select_pos[1] >= 10 and enter_key and block_hand == 0 and inventory[select_pos2] != 0:
        temp_select = select_pos2
        block_hand = inventory[select_pos2]
    elif select_pos[1] >= 10 and enter_key and block_hand != 0 and inventory[select_pos2] != 0 and temp_select == select_pos2:
        temp_select = None
        block_hand = 0
    elif block_hand != 0:
        #pos = position(select_pos[1],select_pos[0])
        #print(pos)
        #pygame.draw.rect(screen,COLOURS[inventory[temp_select]],[pos[0],pos[1],30,30])
        temp_block = BLOCKID[block_hand]
        #print(temp_block)
        for y in range(len(temp_block)):
            try:
                length = len(temp_block[0])
            except TypeError:
                length = 1
            for x in range(length):
                if temp_block[y][x] == 1:
                    pos = position(select_pos[1]+x,select_pos[0]+y)
                    pygame.draw.rect(screen,(255,0,0),[pos[0]-5,pos[1]-5,40,40])
                    pygame.draw.rect(screen,COLOURS[block_hand],[pos[0],pos[1],30,30])
                    score_blocks += 1
    #print(score_blocks)
    results = (block_hand,temp_select,score_blocks)
    return results
        

#Checks if the tiles are clear so the player can place the block
def block_place(screen,block_pos,colour_pos,score,highscore,inventory,BLOCKID,COLOURS,select_pos,block_hand,temp_select,enter_key,score_blocks):
    impossible = False
    #print("BLOCK HAND AT BEINNING OF FUNCTION:",block_hand)
    if block_hand != 0 and temp_select != None and  select_pos[0]>=0 and select_pos[0]<=9 and select_pos[1]>=0 and select_pos[1]<=9 and enter_key==True:
        temp_block = BLOCKID[block_hand]
        for y in range(len(temp_block)):
            try:
                length = len(temp_block[0])
            except TypeError:
                length = 1
            for x in range(length):
                if temp_block[y][x] == 1:
                    #print("select_pos:",select_pos)
                    #print("x:",x,"y:",y)
                    if select_pos[1]+x <= 9 and select_pos[0]+y <=9:
                        if block_pos[select_pos[1]+x][select_pos[0]+y] == 0:
                            random = 1
                            #print("Yes! at:",select_pos[1]+x,select_pos[0]+y)
                        else:
                            impossible = True
                            #print("Imposible")
                    else:
                        impossible = True
                        #print("Imposible2")

        if impossible == False:
            for y in range(len(temp_block)):
                try:
                    length = len(temp_block[0])
                except TypeError:
                    length = 1
                for x in range(length):
                    if temp_block[y][x] == 1:
                        if select_pos[1]+x <= 9 and select_pos[0]+y <=9:
                            if block_pos[select_pos[1]+x][select_pos[0]+y] == 0:
                                block_pos[select_pos[1]+x][select_pos[0]+y] = 1
                                colour_pos[select_pos[1]+x][select_pos[0]+y] = COLOURS[block_hand]
            inventory[temp_select] = 0
            block_hand = 0
            temp_select = None
            score += score_blocks

    templist=(block_pos,colour_pos,block_hand,temp_select,inventory,score)
    return templist

#Detect is you can't place any more blocks and initiates game over screen
def game_over(block_pos,inventory,BLOCKID):
##    possible_place = False
##    #Cyles through all 3 inventory items
##    for a in range(3):
##        impossible = False
##        #Skips loop if inventory slot is empty
##        if inventory[a] == 0:
##            continue
##        #Assigns Block Matrix to temporary variable
##        temp_block = BLOCKID[inventory[a]]
##        for i in range(len(block_pos)):
##            for j in range(len(block_pos)):
##                impossible = False
##                for y in range(len(temp_block)):
##                    try:
##                        length = len(temp_block[0])
##                    except TypeError:
##                        length_width = 1
##                    if j+len(temp_block)>9:
##                        continue
##                    for x in range(length_width):
##                        if i+length>9:
##                            continue
##                        if temp_block[y][x] == 1:
##                            print("j+x:",j+len(temp_block),"i+y:",i+length)
##                            if block_pos[j+x][i+y] == 1:
##                                impossible = True
##                                #print("No! at:",select_pos[1]+x,select_pos[0]+y)
##
##
##                if not impossible:
##                    possible_place = True
##    if possible_place == False:
##        gameover = True
##        print("No Possible Placements")
    gameover = False
    possible_place = False
    for a in range(3):
        if inventory[a] == 0:
            continue
        #pulls martix for current piece from BLOCKID registry
        temp_block = BLOCKID[inventory[a]]
        #turns len(temp_block[0]) into a number free from errors
        try:
            length_width = len(temp_block[0])
        except TypeError:
            length_width = 1

        length_height = len(temp_block)

        #print("Peice in inventory:",inventory[a],"Peice Width:",length_width,"Peice Height:",length_height)
        
        #These two for loops locate a possition on the 10*10 grid to later draw peice on
        for j in range(len(block_pos)-1):
            for i in range(len(block_pos)-1):
                #print("x",i,"y",j)
                #block_placeable = True unless disproved by code below
                block_placeable = True
                for y in range(len(temp_block)):     
                    if i+length_height>9:
                        block_placeable = False
                        continue
                    for x in range(length_width):
                        if j+length_width>9:
                            block_placeable = False
                            continue
                        if temp_block[y][x] == 1:
                            #print("j+x:",j+x,"i+y:",i+y)
                            #print(len(block_pos))
                            #print(len(block_pos[j]))
                            if block_pos[j+x][i+y] == 1:
                                block_placeable = False
                                #print("No! at:",select_pos[1]+x,select_pos[0]+y)
                if block_placeable == True:
                    possible_place = True
    if possible_place == False:
        gameover = True
        print("No Possible Placements")
    return gameover

def game(screen,block_pos,colour_pos,score,highscore,select_pos,BLOCKS,BLOCKID,COLOURS,inventory,arrow,arrow2,enter_key,block_hand,temp_select,score_blocks,airhorn,wow,line_clear,triple,no_one,damn_son,sanic,channel9):
    import pygame
    #Background and Other Colours
    GRAY = (220,220,220)
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    screen.fill(WHITE)

    block_get(inventory,BLOCKS)
    gameover = False
    gameover = game_over(block_pos,inventory,BLOCKID)

    templist = block_place(screen,block_pos,colour_pos,score,highscore,inventory,BLOCKID,COLOURS,select_pos,block_hand,temp_select,enter_key,score_blocks)
    #print(templist[2])
    block_pos = templist[0]
    colour_pos = templist[1]
    block_hand = templist[2]
    temp_select = templist[3]
    inventory = templist[4]
    score = templist[5]

    

    #Purely Drawing Functions
    select_pos2 = select_draw(screen,select_pos,block_pos,arrow,arrow2,block_hand)
    inventory_draw(screen,inventory,BLOCKID,COLOURS,temp_select,select_pos2)
    #Draws Grey 10 by 10 grid
    for y in range(10):
        for x in range(10):
            pygame.draw.rect(screen,GRAY,[40*x+25,40*y+150,30,30])
    block_draw(screen,block_pos,colour_pos)
    #Score and Highscore Draw
    font = pygame.font.SysFont('Airal',48,True,False)
    subtitle = font.render(("Score:"+str(score)),True,BLACK)
    subtitle2 = font.render(("Highscore:"+str(highscore)),True,BLACK)
    screen.blit(subtitle,[50,50])
    screen.blit(subtitle2,[450,50])
    

    results = block_grab(screen,select_pos,select_pos2,inventory,COLOURS,BLOCKID,enter_key,block_hand,temp_select)
    block_hand = results[0]
    temp_select = results[1]
    score_blocks = results[2]
    
    templist2= row_column_check(block_pos,colour_pos,score,airhorn,wow,line_clear,triple,no_one,damn_son,sanic,channel9)
    block_pos = templist2[0]
    colour_pos = templist2[1]
    score = templist2[2]
    
    game_list = (block_pos,colour_pos,score,block_hand,temp_select,score_blocks,select_pos2,gameover)
    return game_list
