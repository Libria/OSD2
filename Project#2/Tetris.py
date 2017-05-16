from random import *
import pygame
from pygame.locals import *
import time

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
tetrominoes[0]=[[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],[[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]]
#colors[0]=0x00FFFF
# T : ㅗ, purple 컬러
tetrominoes[1]=[[[0,0,0,0],[1,1,1,0],[0,1,0,0],[0,0,0,0]],[[0,1,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]],[[0,1,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],[[0,1,0,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]]
#colors[1]=0x767676
# L : ㄱ회전, orange 컬러
tetrominoes[2]=[[[0,0,0,0],[1,1,1,0],[1,0,0,0],[0,0,0,0]],[[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]],[[0,0,1,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],[[0,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,0,0]]]
#colors[2]=0xFFA500
# J : ㄴ, blue 컬러
tetrominoes[3]=[[[1,0,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],[[0,1,1,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]],[[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]],[[0,1,0,0],[0,1,0,0],[1,1,0,0],[0,0,0,0]]]
#colors[3]=0x0000FF
# Z : z, red 컬러
tetrominoes[4]=[[[0,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,0]],[[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]]
#colors[4]=0xFF0000
# S : 벼락, green 컬러
tetrominoes[5]=[[[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]],[[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]]]
#colors[5]=0x00FF00
# O : 네모, yellow 컬러
tetrominoes[6]=[[[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]]]
#colors[6]=0xFFFF00


def DrawBlock() :
    screen.lock()
    for col in range(cols) :
        for row in range(rows) :
            if area[row][col] == 1 :
                pygame.draw.rect(screen, (255,220,143), Rect((col*30,row*30), (27, 27)))
    pygame.display.update()
    screen.unlock()

def CleanUp() :
    screen.lock()
    screen.fill((10,10,10))
    pygame.display.update()
    screen.unlock()

def InsertAreaBlock(num) :
    chooseTet = tetrominoes[num]

    for tetcol in range(4) :
        for tetrow in range(4) :
            area[0 + tetrow][3 + tetcol] = chooseTet[0][tetrow][tetcol]

def DownBlock(blocklocation, blocknum, blockstate) :
    def Check_1(list) :
        for n in list :
            if n == 1 :
                return True

    block = tetrominoes[blocknum][blockstate]
    srow = blocklocation[0]
    scol = blocklocation[1]

    alpha = 3
    check1 = False
    while not check1 :
        check1 = Check_1(block[alpha])
        alpha -= 1

    if (srow + alpha + 2 >= rows) :
        return False

    checkarea = False
    targetarea = area[srow + alpha + 2]

    for col in range(scol, scol + 4) :
        if area[srow + alpha + 1][col] == 1 and targetarea[col] == 1 :
            checkarea = True
            break

    if checkarea == True :
        return False
    elif checkarea == False :
        for row in range(srow, srow + 4) :
            for col in range(scol, scol + 4) :
                if area[row][col] == 1 :
                    area[row][col] -= block[row - srow][col - scol]

        for row in range(srow, srow + 3) :
            for col in range(scol, scol + 4) :
                area[row+1][col] += block[row - srow][col - scol]

        return True



def CheckHorizon(blocknum, blocklocation) :
    def Check_1(list) :
        for n in list :
            if n == 1 :
                return True

    srow = blocklocation[0]
    scol = blocklocation[1]
    block = tetrominoes[blocknum][0]

    for col in range(3,6) :
        if area[4][col] == 1 :
            return False

    return True


gameover = False

while not gameover :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameover = True

    speed_up = 1
    blocknum = randint(0, 6)
    noncollision = True
    InsertAreaBlock(blocknum)
    blocklocation = [0, 3]
    blockstate = 0

    if not CheckHorizon(blocknum, blocklocation) :
        CleanUp()
        DrawBlock()
        noncollision = False
        gameover = True

    while noncollision :
        CleanUp()
        DrawBlock()
        if DownBlock(blocklocation, blocknum, blockstate) :
            blocklocation[0] += 1
            noncollision = True
        else :
            noncollision = False
        #time.sleep(float(0.1)/speed/speed_up)
        time.sleep(0.1)

        for row in range(rows) :
            print(area[row])
        print("Cut")

pygame.quit()
