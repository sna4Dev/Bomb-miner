
import sys
import pygame as pg
from random import randint
pg.font.init()

FPS = 60
W = 1000  # ширина экрана
H = 1000  # высота экрана
WHITE = (255, 255, 255)
BLUE = (255, 255, 0)

x = W//2
y = H//2
qual = 50

delayTime = 150
sc = pg.display.set_mode((W, H))
clock = pg.time.Clock()
isRunning = True
r = 50

player = ('sprites\player.png')
bg = pg.image.load('sprites\Bg.png')
blockImg = ('sprites\Block.png')
bombImg = ('sprites\Bomb.png')
emptyBlock = ('sprites\Bg_block.png')
winImg = ('sprites\WinZone.png')
XrayBlock = ('sprites\XrayBlock.png')
bg1 = pg.transform.scale(bg,(W,H))

class Scoreboard:
    def __init__(self, font_size=32, font_color=(0, 0, 0), x_pos=100, y_pos=10):
        self.score = 0
        self.font = pg.font.Font(None, font_size)
        self.font_color = font_color
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self, text, screen):
        score_text = self.font.render(f"{text}: {self.score}", True, self.font_color)
        screen.blit(score_text, (self.x_pos, self.y_pos))

    def update(self, seconds):
        self.score = seconds
scoreboard = Scoreboard(x_pos = 100)
xrayTime = Scoreboard(x_pos = 300)
winCount = Scoreboard(x_pos = 500)
class Player(pg.sprite.Sprite):
    def __init__(self, X, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(player).convert_alpha()
        self.rect = self.image.get_rect(center=(X, 25))
playerObj = Player(475,player)

class Block(pg.sprite.Sprite):
    def __init__(self, X, Y, blockImg):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(blockImg).convert_alpha()
        self.rect = self.image.get_rect(center=(X, Y))

class EmptyBlock(pg.sprite.Sprite):
    def __init__(self, X, Y, emptyBlock):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(emptyBlock).convert_alpha()
        self.rect = self.image.get_rect(center=(X, Y))

class Bomb(pg.sprite.Sprite):
    def __init__(self, X, Y, bombImg):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(bombImg).convert_alpha()
        self.rect = self.image.get_rect(center=(X, Y))

class Xray(pg.sprite.Sprite):
    def __init__(self, X, Y, XrayBlock):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(XrayBlock).convert_alpha()
        self.rect = self.image.get_rect(center=(X, Y))

class WinZone(pg.sprite.Sprite):
    def __init__(self, winImg):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(winImg).convert_alpha()
        self.rect = self.image.get_rect(center=(500,1000))

WinSurface = WinZone(winImg)

def CreateSurface(bombCount, blocksCount): #Создание поля с BombCount( кол-во бомб )
    global xrayPos
    for _ in range(bombCount-1):
        a = randint(1,359)
        if a not in bombSur:
            bombSur.append(a)
    countX = 0
    countY = 0
    CreateBombCount = bombCount
    a = randint(1,359)
    if a not in bombSur:
        xrayPos = a
    else:
        xrayPos = randint(1,359)
    for _ in range(blocksCount):
        if _ in bombSur and CreateBombCount != 0:
            if countX == 20:
                countX = 0
                countY += 1
            bombSur.remove(_)
            bombs.append(Bomb(countX * 50+25, countY * 50 + 75, bombImg))
            CreateBombCount -= 1
        elif _ == xrayPos:
            blocks.append(Xray(countX * 50+25, countY * 50 + 75, blockImg))
        else:
            if countX == 20:
                countX = 0
                countY += 1
            blocks.append(Block(countX * 50+25, countY * 50 + 75, blockImg))
        countX+=1

#
heldKeys = [] #Список для пошаговых действий
def getEvents(): #Пошаговое движение
    global heldKeys
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if playerObj.rect.x > W + qual:
            playerObj.rect.x = 0
        if playerObj.rect.x < -qual:
            playerObj.rect.x = W - qual
        if i.type == pg.KEYDOWN:

            if i.key == pg.K_s:
                heldKeys.append('Down')
            elif i.key == pg.K_w:
                heldKeys.append('Up')
            elif i.key == pg.K_a:
                heldKeys.append('Left')
            elif i.key == pg.K_d:
                heldKeys.append('Right')

        elif i.type == pg.KEYUP:

            if i.key == pg.K_s:
                heldKeys.remove('Down')
            elif i.key == pg.K_w:
                heldKeys.remove('Up')
            elif i.key == pg.K_a:
                heldKeys.remove('Left')
            elif i.key == pg.K_d:
                heldKeys.remove('Right')

def checkHeldKeys():
    for i in heldKeys:
        if len(heldKeys) == 1:
            if 'Down' in heldKeys:
                playerObj.rect.y += qual

            if 'Up' in heldKeys:
                playerObj.rect.y -= qual

            if 'Left' in heldKeys:
                playerObj.rect.x -= qual

            if 'Right' in heldKeys:
                playerObj.rect.x += qual
        pg.time.delay(delayTime)
        print(heldKeys,'-',playerObj.rect.x, playerObj.rect.y)

def Collisions():
    global xrayRemain
    global GameOn
    for _ in range(len(blocks)):  #blocksCount - bombCount + 1
        if playerObj.rect.colliderect(blocks[_].rect) and _ != xrayPos:
            blocks.remove(blocks[_])
            blocks.append(EmptyBlock(0, 0, emptyBlock))

        if _ == xrayPos or (xrayRemain <= 3 and xrayRemain > 0):
            xrayRemain = 3 - (pg.time.get_ticks() - start_ticks) // 1000
        sc.blit(blocks[_].image,blocks[_].rect)
    for _ in range(len(bombs)):
        if xrayRemain > 0:
            sc.blit(bombs[_].image, bombs[_].rect)
        else:
            sc.blit(blocks[_].image,bombs[_].rect)
        if playerObj.rect.colliderect(bombs[_].rect) or seconds == 0:
            GameOn = 1
            playerObj.rect.x = 50
            playerObj.rect.y = 950

    WinLevel()


def WinLevel():

    global WinCount
    global levelDiff
    global start_ticks
    global seconds
    global checkCreate
    global bombs
    global bombSur
    global blocks

    sc.blit(WinSurface.image, WinSurface.rect)

    if playerObj.rect.colliderect(WinSurface.rect): #new level
        blocks.clear()
        bombs.clear()
        bombSur.clear()
        checkCreate = True
        playerObj.rect.x = 450
        playerObj.rect.y = 0
        pg.time.delay(500)
        Collisions()
        start_ticks = pg.time.get_ticks()
        levelDiff += 1
        WinCount += 1

blocks = []  # 20*18 блоков 10% бомб(36)
bombSur = []
bombs = []
checkCreate = True
start_ticks = pg.time.get_ticks()  # starter tick
seconds = 0
levelDiff = 0
xrayRemain = 0
xrayPos = 0
WinCount = 0

GameOn = 1
while isRunning: #цикл игры

    if GameOn:
        levelDiff = 0
        WinCount = 0
        sc.fill((0,0,0))
        sc.blit((pg.font.SysFont('Corbel',35)).render('Press any key to start' , True , BLUE) , (W / 2 - 160, H / 2))
        for i in pg.event.get():
            if i.type == pg.KEYDOWN:
                if i.key ==pg.K_ESCAPE:
                    sys.exit()
                else:
                    GameOn = 0
    else:
        seconds = 60 - (pg.time.get_ticks() - start_ticks) // 1000  # calculate how many seconds

        # xrayRemain = 10 - (pg.time.get_ticks() - start_ticks) // 1000
        checkHeldKeys()
        getEvents()
        bombCount = 30 + levelDiff*10
        blocksCount = 360

        sc.blit(bg1, (0,0))
        xrayTime.update(xrayRemain)

        if xrayRemain > 0:
            xrayTime.draw("Xray time", sc)


        scoreboard.draw("Score",sc)
        scoreboard.update(seconds)

        winCount.draw("Win count", sc)
        winCount.update(WinCount)
        if checkCreate:
            CreateSurface(bombCount, blocksCount)#Кол-во бомб и созднаие поля игры
            checkCreate = False
            # print("yes",bombCount, blocksCount)

        Collisions()
        sc.blit(playerObj.image, playerObj.rect)

    clock.tick(FPS)
    pg.display.update()

