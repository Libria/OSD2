from random import *
import pygame
from pygame.locals import *
import time
import sys

pygame.init()

pygame.display.set_caption('OSD2 Tetrix')

rows, cols = 20, 10
area = [[0 for col in range(cols)] for row in range(rows)]
screen = pygame.display.set_mode((cols*30 + 250 ,rows*30 + 10),0,32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((10, 10, 10))
speed = 1

# 블럭들
tetrominoes = [0, 0, 0, 0, 0, 0, 0]
# I : 막대, cyan 컬러
tetrominoes[0]=[[
                [1,1,1,1]],

                [
                [1],
                [1],
                [1],
                [1]]]
#colors[0]=0x00FFFF
# T : ㅗ, purple 컬러
tetrominoes[1]=[[
                [1,1,1],
                [0,1,0]],

                [
                [0,1],
                [1,1],
                [0,1]],

                [
                [0,1,0],
                [1,1,1]],

                [
                [1,0],
                [1,1],
                [1,0]]]
#colors[1]=0x767676
# L : ㄱ회전, orange 컬러
tetrominoes[2]=[[
                [1,1,1],
                [1,0,0]],

                [
                [1,1],
                [0,1],
                [0,1]],

                [
                [0,0,1],
                [1,1,1]],

                [
                [1,0],
                [1,0],
                [1,1]]]
#colors[2]=0xFFA500
# J : ㄴ, blue 컬러
tetrominoes[3]=[[
                [1,0,0],
                [1,1,1]],

                [
                [1,1],
                [1,0],
                [1,0]],

                [
                [1,1,1],
                [0,0,1]],

                [
                [0,1],
                [0,1],
                [1,1]]]
#colors[3]=0x0000FF
# Z : z, red 컬러
tetrominoes[4]=[[
                [1,1,0],
                [0,1,1]],

                [
                [0,1],
                [1,1],
                [1,0]]]
#colors[4]=0xFF0000
# S : 벼락, green 컬러
tetrominoes[5]=[[
                [0,1,1],
                [1,1,0]],

                [
                [1,0],
                [1,1],
                [0,1]]]
#colors[5]=0x00FF00
# O : 네모, yellow 컬러
tetrominoes[6]=[[
                [1,1],
                [1,1]]]
#colors[6]=0xFFFF00


def ColEnd(blocknum, blockstate) : 
    end = 0
    for row in range(len(tetrominoes[blocknum][blockstate])) :
        for col in range(4) : 
            if tetrominoes[blocknum][blockstate] == 1 :
                if end < col : 
                    end = col
    return end

def DrawBlock() :
    screen.lock()
    for col in range(cols) :
        for row in range(rows) :
            if area[row][col] >= 1 :
                pygame.draw.rect(screen, (255,220,143), Rect((col*30,row*30), (27, 27)))
    pygame.display.update()
    screen.unlock()

def CleanUp() :
    screen.lock()
    screen.fill((10,10,10))
    pygame.display.update()
    screen.unlock()

def InsertAreaBlock(num) :
    tet = tetrominoes[num][0]
    tetrow = len(tetrominoes[num][0])
    tetcol = len(tetrominoes[num][0][0])
    row = 0

    while (tetrow > 0) :
        for col in range(tetcol) : 
                area[0 + row][3 + col] = area[0 + row][3 + col] + tet[row][col]
        tetrow = tetrow - 1
        row = row + 1

def DownBlock(blocklocation, blocknum, blockstate) :
    tet = tetrominoes[blocknum][blockstate]
    tetcol = len(tetrominoes[blocknum][blockstate][0])
    tetlen = len(tet)
    row = 0
    x = blocklocation[0]
    y = blocklocation[1]

    if (x + tetlen == 20) :
        return False

    for col in range(tetcol) : 
        if (x + tetlen < 20 and tet[tetlen - 1][col] > 0) :
            if (area[x + tetlen][y + col] > 0) :
                return False

    while (tetlen > 0) :
        for col in range(tetcol) : 
                area[x + row][y + col] = area[x + row][y + col] - tet[row][col]
        tetlen = tetlen - 1
        row = row + 1

    tetlen = len(tet)
    row = 0
    while (tetlen > 0) :
        for col in range(tetcol) : 
                area[x + 1 + row][y + col] = area[x + 1 + row][y + col] + tet[row][col]
        tetlen = tetlen - 1
        row = row + 1

    return True

def CheckHorizon(blocknum, blocklocation) :
    for col in range(10) :
        for row in range(4) :
            if (area[row][col] > 1) :
                return False

    return True

def Rotation(blocklocation, blocknum, blockstate) :
    rotatelen = len(tetrominoes[blocknum])
    tetcol = len(tetrominoes[blocknum][blockstate][0])
    x = blocklocation[0]
    y = blocklocation[1]

    blockstate2 = blockstate
    if (blockstate2 + 1 == rotatelen) :
        blockstate2 = 0
    else :
        blockstate2 += 1

    tet = tetrominoes[blocknum][blockstate]
    tetlen = len(tet)

    for row in range(tetlen) :
        for col in range(tetcol) : 
            area[x + row][y + col] = area[x + row][y + col] - tet[row][col]

    tet = tetrominoes[blocknum][blockstate2]
    tetcol = len(tetrominoes[blocknum][blockstate2][0])
    tetlen = len(tet)

    for row in range(tetlen) :
        for col in range(tetcol) : 
                area[x + row][y + col] = area[x + row][y + col] + tet[row][col]

    return blockstate2

def Move(blocklocation, blocknum, blockstate, way) :
    rotatelen = len(tetrominoes[blocknum])
    tetcol = len(tetrominoes[blocknum][blockstate][0])
    x = blocklocation[0]
    y = blocklocation[1]

    tet = tetrominoes[blocknum][blockstate]
    tetlen = len(tet)
    row = 0

    while (tetlen > 0) :
        for col in range(tetcol) : 
                area[x + row][y + col] = area[x + row][y + col] - tet[row][col]
        tetlen = tetlen - 1
        row = row + 1

    tet = tetrominoes[blocknum][blockstate]
    tetlen = len(tet)
    row = 0

    while (tetlen > 0) :
        for col in range(tetcol) : 
                area[x + row][y + col + way] = area[x + row][y + col + way] + tet[row][col]
        tetlen = tetlen - 1
        row = row + 1

def Lineall() :
    check = 0
    row2 = 0

    for row in range(20) :
        for col in range(10) :
            row2 = 19 - row
            if (area[row2][col] == 1) :
                check += 1
            else :
                break
        if check == 10 :
            return row2
        else :
            check = 0

    return 0

def DownAll(lineall) :
    area2 = area
    row2 = 0

    for row in range(rows) :
        print(area[row])
    #print("area")

    for row in range(rows) :
        print(area2[row])
    #print("area2")

    for col in range(10) : 
        area[lineall][col] = 0

    for row in range(lineall + 1) : 
        for col in range(10) : 
            row2 = 19 - row
            if row2 == 0 :
                break
            area[row2][col] = area2[row2 - 1][col]

    for row in range(rows) :
        print(area[row])
    #print("downall")


def Run() : 
    gameover = False
    noncollision = False
    while not gameover :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

            speed_up = 1

            if (noncollision == False) :
                while Lineall() != 0 : 
                    lineall = Lineall()
                    DownAll(lineall)

                blocknum = randint(0, 6)
                noncollision = True
                InsertAreaBlock(blocknum)
                blocklocation = [0, 3]
                blockstate = 0

            if not CheckHorizon(blocknum, blocklocation) :
                noncollision = False
                gameover = True
                break

            CleanUp()
            DrawBlock()

            if event.type == pygame.KEYDOWN :
                if event.key == K_UP :
                    blockstate = Rotation(blocklocation, blocknum, blockstate)
                    CleanUp()
                    DrawBlock()

                elif event.key == K_RIGHT :
                    colend = ColEnd(blocknum, blockstate)
                    if (colend + blocklocation[1] < 7 and blocknum != 0) or (colend + blocklocation[1] < 6 and blocknum == 0) : 
                        temp = blockstate
                        blockstate = Move(blocklocation, blocknum, blockstate, 1)
                        blocklocation[1] += 1
                        blockstate = temp
                        CleanUp()
                        DrawBlock()

                elif event.key == K_LEFT :
                    if blocklocation[1] > 0 :
                        temp = blockstate
                        blockstate = Move(blocklocation, blocknum, blockstate, -1)
                        blocklocation[1] -= 1
                        blockstate = temp
                        CleanUp()
                        DrawBlock()

            downboolean = DownBlock(blocklocation, blocknum, blockstate)
            if downboolean :
                blocklocation[0] += 1
            elif not downboolean :
                noncollision = False

            time.sleep(float(0.1)/speed/speed_up * 3)

            '''for row in range(rows) :
                print(area[row])
            print("Cut")'''

            #if not hasattr(event, 'key') : 
            #    continue

Run()

pygame.quit()