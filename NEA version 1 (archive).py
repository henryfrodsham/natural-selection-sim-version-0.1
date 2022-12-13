import pygame
import sys
import random
import math
import json
try:
    JsonFile = open('config.json')
    Config = json.load(JsonFile)
    JsonFile.close()
except:
    print("resolving Json File exception!, loading default.json")
    file = open('default.json')
    RecoveryLibrary = json.load(file)
    file.close()
    file = open("config.json", "w")
    json.dump(RecoveryLibrary, file)
    file.close()
    print("success! note: you will have lost all your saved changes")
    JsonFile = open('config.json')
    Config = json.load(JsonFile)
    JsonFile.close()
#for data in Config["cursor"]["color"]:
    #print(data)
pygame.init()
surface = pygame.display.set_mode((800, 600))
font = pygame.font.Font('freesansbold.ttf', 12)

GREY = (128,128,128)
BLACK = (20,20,20)
WHITE = (255,255,255)
DarkGrey = (170,170,170)
RED = (100,0,0)
BLUE = (0,0,200)
FoodRegister = []
SpeciesRegister = []

def VectorCalculation(ObjectPositionX,ObjectPositionY,Range): #object x is the host
    global Config
    ChangeInX = abs(ObjectPositionY[0] - ObjectPositionX[0])
    ChangeInY = abs(ObjectPositionY[1] - ObjectPositionX[1])
    distance = math.sqrt(Sqr(ChangeInX) + Sqr(ChangeInY))
    if distance < Range:
        if Config["misc"]["DrawVector"]:
            pygame.draw.line(surface,RED,(ObjectPositionX[0],ObjectPositionX[1]),(ObjectPositionY[0],ObjectPositionY[1]))
        return distance
def Sqr(arg):
    return (arg * arg)
def IsPrime(arg): # this checks for prime numbers
    for i in range(2,int(arg**0.5)+1):
        if arg%i==0:
            return False
    return True

def InHitboxRect(X,Y,posX,posY,sizeX,sizeY):
    if posX > X and posX < (X + sizeX): #checks for allignment on the X axis
        if posY > Y and posY < (Y + sizeY): #checks for allignment on the Y axis
            #print("object allignment, details below")
            #print(X,Y,posX,posY,sizeX,sizeY)
            return True
def GetPosInArray(find,array):
    pointer = 0
    for thing in array:
        if thing == find:
            return pointer
        else:
            pointer += 1
def DrawCustomCursor(x,y,state):
    global CursorColor
    global PressedCursorColor
    global Config
    if state == 1:
        pygame.draw.rect(surface, Config["cursor"]["pressed"], pygame.Rect((x+5),(y+5),(3),(3)))
    else:
        pygame.draw.rect(surface, Config["cursor"]["color"], pygame.Rect((x+5),(y+5),(3),(3)))
       
def GetPositionOnClick(mousepos,mousestate,posX,posY,sizeX,sizeY):
    if mousepos[0] > posX and mousepos[0] < (posX + sizeX):
        if mousepos[1] > posY and mousepos[1] < (posY + sizeY):
            if mousestate[0]:
                return mousepos
def DrawColorPicker(x,y,mousepos,mousestate,offsetX,offsetY):
    pygame.draw.rect(surface, BLACK, pygame.Rect(x,y,261,261))
    pygame.draw.rect(surface, WHITE, pygame.Rect((x+3),(y+3),255,255))
    for color in range(256):
        pygame.draw.line(surface,(offsetX,offsetY,color),((x + color + 3),(y + 3)),((x + color + 3),(y + 258)))
    if (GetPositionOnClick(mousepos,mousestate,x+3,y+3,255,255)) != None:
        Color = list(GetPositionOnClick(mousepos,mousestate,x+3,y+3,255,255))
        SelectedColor = (offsetX,offsetY,(Color[0] - x+3))
        return SelectedColor
class button:
   
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,text,textcolor):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.text = text
        self.textcolor = textcolor
       
    def DrawButton(self,mousestate,mousepos):
        pygame.draw.rect(surface, DarkGrey, pygame.Rect(self.position[0] - 3,self.position[1] - 3,self.size[0] + 6,self.size[1] + 6))
        #print(mousestate,mousepos,self.position,self.size)
        if mousestate == 0 and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]): #hovered but not clicked
            #print("hovered")
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the hovered state of the button
           
        elif mousestate == 1 and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]): #pressed
            #print("pressed")
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #pressed state
            return True
       
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the static state of the button
           
        text = font.render(self.text, True, self.textcolor, GREY)
        surface.blit(text,(self.position[0] + self.size[0] + 3,self.position[1] + (self.size[1] // 2)))
       
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.text,self.textcolor)
class slider:
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,slidersize,level,text):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.sliderpos = [position[0],(position[1] + level)]
        self.slidersize = slidersize
        self.text = text
    def DrawSlider(self,mousepos,mousestate):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        text = font.render(self.text + ":" + str(self.sliderpos[1] - self.position[1]), True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0],self.position[1]))
        if InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0] + 10),(self.slidersize[1] + 10)) and mousestate == 1:
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
            if self.sliderpos[1] >= self.position[1]:
                if self.sliderpos[1] <= (self.position[1] + self.size[1]):
                    self.sliderpos[1] = (mousepos[1] - 5)
                else:
                    self.sliderpos[1] = (self.position[1] + (self.size[1] - self.slidersize[1]))
            else:
                self.sliderpos[1] = self.position[1]
        elif InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0]),(self.slidersize[1])):
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
        else:
            pygame.draw.rect(surface, WHITE, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))

        if (self.sliderpos[1] - self.position[1]) < (self.size[1] - self.slidersize[1]):
            if (self.sliderpos[1] - self.position[1]) > 0:
                return (self.sliderpos[1] - self.position[1])
            else:
                return 0
        else:
            return (self.size[1] - self.slidersize[1])
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.sliderpos,self.slidersize)
class SideSlider:
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,slidersize,text):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.sliderpos = [position[0],position[1]]
        self.slidersize = slidersize
        self.text = text
    def DrawSlider(self,mousepos,mousestate):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        text = font.render(self.text + ":" + str(self.sliderpos[0] - self.position[0]), True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0] + self.slidersize[0],self.position[1]))
        if InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0] + 10),(self.slidersize[1] + 10)) and mousestate == 1:
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
            if self.sliderpos[0] >= self.position[0]:
                if self.sliderpos[0] <= (self.position[0] + self.size[0]):
                    self.sliderpos[0] = (mousepos[0] - 10)
                else:
                    self.sliderpos[0] = (self.position[0] + (self.size[0] - self.slidersize[0]))
            else:
                self.sliderpos[0] = self.position[0]
        elif InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0]),(self.slidersize[1])):
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
        else:
            pygame.draw.rect(surface, WHITE, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
           
        if (self.sliderpos[0] - self.position[0]) < (self.size[0] - self.slidersize[0]):
            if (self.sliderpos[0] - self.position[0]) > 0:
                return (self.sliderpos[0] - self.position[0])
            else:
                return 0
        else:
            return (self.size[0] - self.slidersize[0])
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.sliderpos,self.slidersize)
class CheckBox():
    def __init__(self,size,position,color,HoverColor,CheckColor,state,text):
        self.size = size
        self.position = position
        self.color = color
        self.HoverColor = HoverColor
        self.CheckColor = CheckColor
        self.state = state
        self.text = text
    def Draw(self,mousepos,mousestate):
        global LastPress
        if InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]):
            pygame.draw.rect(surface, self.HoverColor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
            if mousestate[0] and mousestate[0] != LastPress:
                self.state = not self.state
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        if self.state:
            pygame.draw.line(surface,self.CheckColor,(self.position[0],self.position[1]),(self.position[0] + self.size[0],self.position[1] + self.size[1]))
            pygame.draw.line(surface,self.CheckColor,(self.position[0] + self.size[0],self.position[1]),(self.position[0],self.position[1] + self.size[1]))
        text = font.render(self.text, True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0],self.position[1]))
        LastPress = mousestate[0]
        return self.state
class Species:
   
    def  __init__(self, name, color, charcolor, size, charsize, position, genes):
        self.name = name
        self.color = color
        self.charcolor = charcolor
        self.size = size
        self.charsize = charsize
        self.position = position
        self.genes = genes
       
    def DrawSprite(self):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        text = font.render(self.name, True, BLACK, GREY)
        surface.blit(text,((self.position[0] + self.size[0]),(self.position[1])))
        factor = 0
        for Pointer in range((len(self.genes) // 2) - 2):
            Horizontal = (self.position[0] + self.size[0])
            Down = (self.position[1] + self.size[1])
            X = (Horizontal - self.genes[factor])
            Y = (Down - self.genes[factor + 1])
            A = (Horizontal - self.genes[factor+2])
            B = (Down - self.genes[factor+3])
           
            if self.genes[factor] % 2 == 0: #even check
                pygame.draw.circle(surface, self.charcolor[Pointer],(X,Y),self.charsize[Pointer])
            elif IsPrime(self.genes[factor]):
                pygame.draw.line(surface,self.charcolor[Pointer],(X,Y),(A,B))
            else:
                 pygame.draw.rect(surface, self.charcolor[Pointer], pygame.Rect(X,Y,self.charsize[Pointer],self.charsize[Pointer]))
                 
            factor += 2
        return self.position
    def TargetMove(self,TargetPos):
        global Config
        #print(TargetPos,self.position)
        if self.position[0] != 0 and self.position[0] < 800:
            if TargetPos[0] < math.floor(self.position[0]):
                self.position[0] -= 1
            elif TargetPos[0] != math.floor(self.position[0]):
                self.position[0] += 1
        if self.position[1] != 0 and self.position[1] < 600:
            if TargetPos[1] < math.floor(self.position[1]):
                self.position[1] -= 1
            elif TargetPos[1] != math.floor(self.position[1]):
                self.position[1] += 1
        if TargetPos[0] == math.floor(self.position[0]) and TargetPos[1] == math.floor(self.position[1]):
            return True
        if Config["misc"]["DrawVector"]:
            pygame.draw.line(surface,BLUE,(self.position[0],self.position[1]),(TargetPos[0],TargetPos[1]))
    def GetPos(self):
        return self.position
    def Wander(self,amount,direction):
        for steps in range(amount):
            if self.position[0] > 0 and (self.position[0] + self.size[0]) < 800 and self.position[1] > 0 and (self.position[1] + self.size[1]) < 600:
                if direction == 1:
                    self.position[0] -= 0.1
                    self.position[1] -= 0.1
                if direction == 2:
                    self.position[0] -= 0.1
                    self.position[1] += 0.1
                if direction == 3:
                    self.position[0] += 0.1
                    self.position[1] -= 0.1
                if direction == 4:
                    self.position[0] += 0.1
                    self.position[1] += 0.1
                
    def Output(self):
        self.name,self.color,self.charcolor,self.size,self.charsize,self.position,self.genes
       
class Food:
    def __init__(self,position,color,size,dotsize):
        self.position = position
        self.color = color
        self.size = size
        self.dotsize = dotsize
       
    def DrawFoodObject(self,multiplier):
        pygame.draw.circle(surface, self.color,(self.position[0],self.position[1]),(self.size * multiplier))
        pygame.draw.circle(surface, BLACK,(self.position[0],self.position[1]),(self.dotsize * multiplier))
        return self.position
    def GetPos(self):
        return self.position
    def Output(self):
        print(self.position,self.color,self.size,self.dotsize)
   
def InitiateSpeciesObject():
    global Config
    name = ""
    genes = []
    charcolor = []
    charsize = []
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = (random.randint(35,65),random.randint(35,65))
    position = [random.randint(100,700),random.randint(100,500)]
   
    for i in range(random.randint(1,6)):
        for o in range(random.randint(1,6)): #this generates alien like names
            name += chr(random.randint(65,122))
        name += "-"
       
    for i in range(random.randint(Config["genes"]["lower"],Config["genes"]["upper"])): #genetic code generator, codes for the appearance
        X = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        genes.append(random.randint(1,size[0]))
        genes.append(random.randint(1,size[1]))
        charcolor.append(X)
        charsize.append(random.randint(1,4))
       
    SpeciesRegister.append(Species(name,color,charcolor,size,charsize,position,genes))

def CreateFoodObject():
    global Config
    position = [random.randint(50,750),random.randint(50,550)]
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = random.randint(1,6)
    dotsize = random.randint(0,(size // 2))
    FoodRegister.append(Food(position,color,size,dotsize))
   
def DrawObjects(zoom):
    global StickyTarget
    global Target
    Targets = []
    Distances = []
    for i in range(len(FoodRegister)):
        Ping = VectorCalculation(SpeciesRegister[0].DrawSprite(),FoodRegister[i].DrawFoodObject(zoom),100)
        if Ping != None:
            Targets.append(i)
            Distances.append(Ping)
    if len(FoodRegister) == 0:
        SpeciesRegister[0].DrawSprite()
    if len(Targets) != 0 and not StickyTarget:
        Pointer = GetPosInArray(min(Distances),Distances)
        Target = Targets[Pointer]
        if Config["misc"]["DrawVector"]:
            print("DEBUG: TARGET POINTER:", Pointer, "TARGET POSITION", FoodRegister[Target].GetPos(), "CHARACTER POS:", SpeciesRegister[0].GetPos())
        StickyTarget = True
    if len(Targets) != 0:
        if (SpeciesRegister[0].TargetMove(FoodRegister[Target].GetPos())):
            del FoodRegister[Target]
            StickyTarget = False
    else:
        SpeciesRegister[0].Wander(random.randint(1,50),random.randint(1,4))
        #SpeciesRegister[i].CreateMove()
#def CheckObjectClipping(objectX,objectY):
    #if InHitboxRect(objectX.position[0],objectX.position[1],objectY.position[0],objectY.position[1],(objectY.size * 2),(objectY.size * 2)):
        #print("object clipping")

    #print(objectX.position,objectY.position,objectY.size)
InitiateSpeciesObject()
CreateFoodObject()
#buttons are size,position,color,pressedcolor,hoveredcolor,text,textcolor
#sliders are size,position,color,pressedcolor,hoveredcolor,slidersize,text
SpawnFood = button((50,30),(0,0),(40,40,40),(200,0,0),(100,0,0),"FOOD",(0,0,200))
play = button((50,30),(360,450),(40,40,40),(200,0,0),(100,0,0),"start simulation",(0,0,200))
back = button((50,30),(300,450),(40,40,40),(200,0,0),(100,0,0),"BACK",(0,0,200))
options = button((50,30),(300,500),(40,40,40),(200,0,0),(100,0,0),"OPTIONS",(0,0,200))
information = button((50,30),(410,500),(40,40,40),(200,0,0),(100,0,0),"INFO",(0,0,200))
CustomCursor = button((50,30),(400,200),(40,40,40),(200,0,0),(100,0,0),"change cursor color",(0,0,200))
CustomCursorClicked = button((50,30),(400,150),(40,40,40),(200,0,0),(100,0,0),"change pressed cursor color",(0,0,200))
NewSlider = slider((20,80),(0,500),BLACK,(200,0,0),(100,0,0),(20,20),0,("ZOOM"))
GeneRangeLower = slider((20,80),(40,300),BLACK,(200,0,0),(100,0,0),(20,20),Config["genes"]["lower"],("CHANGE GENE LOWER BOUND"))
GeneRangeUpper = slider((20,80),(40,200),BLACK,(200,0,0),(100,0,0),(20,20),Config["genes"]["upper"],("CHANGE GENE UPPER BOUND"))
colorR1 = SideSlider((255,20),(400,450),BLACK,(200,0,0),(100,0,0),(20,20),("RED"))
colorG1 = SideSlider((255,20),(400,490),BLACK,(200,0,0),(100,0,0),(20,20),("GREEN"))
colorR2 = SideSlider((255,20),(400,500),BLACK,(200,0,0),(100,0,0),(20,20),("RED"))
colorG2 = SideSlider((255,20),(400,540),BLACK,(200,0,0),(100,0,0),(20,20),("GREEN"))
DrawVector = CheckBox((20,20),(40,40),BLACK,(200,0,0),(0,200,0),Config["misc"]["DrawVector"],"vectors")
#ScreenSizeX = slider((20,80),(0,500),BLACK,(200,0,0),(100,0,0),(20,20),("SCREEN X")) would require a rewrite not going to touch until version 3
#ScreenSizeY = slider((20,80),(0,500),BLACK,(200,0,0),(100,0,0),(20,20),("SCREEN Y"))
pygame.mouse.set_visible(False)
zoom = 0
ButtonToggle1 = False
ButtonToggle2 = False
LastPress = 0
Target = 0
StickyTarget = False
def main():
    global Config
    OptionPage = False
    InfoPage = False
    MainMenu = True
    game = False
    while MainMenu:
        mousepos = pygame.mouse.get_pos()
        mousestate = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys. exit()
        surface.fill(GREY)
        DrawCustomCursor(mousepos[0],mousepos[1],mousestate[0])
        if (play.DrawButton(mousestate[0],mousepos)):
            MainMenu = False
            game = True
        if (options.DrawButton(mousestate[0],mousepos)):
            OptionPage = True
            MainMenu = False
        if (information.DrawButton(mousestate[0],mousepos)):
            InfoPage = True
            MainMenu = False
        pygame.display.flip()
       
    while OptionPage:
        global ButtonToggle1
        global ButtonToggle2
        mousepos = pygame.mouse.get_pos()
        mousestate = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys. exit()
        surface.fill(GREY)
        if DrawVector.Draw(mousepos,mousestate) != Config["misc"]["DrawVector"]:
            Config["misc"]["DrawVector"] = DrawVector.Draw(mousepos,mousestate)
        if (GeneRangeUpper.DrawSlider(mousepos,mousestate[0])) != 0:
            Config["genes"]["upper"] = (GeneRangeUpper.DrawSlider(mousepos,mousestate[0]))
            file = open("config.json","w")
            json.dump(Config,file)
            file.close()
        if (GeneRangeLower.DrawSlider(mousepos,mousestate[0])) != 0:
            if (GeneRangeLower.DrawSlider(mousepos,mousestate[0])) < Config["genes"]["upper"]:
                Config["genes"]["lower"] = (GeneRangeLower.DrawSlider(mousepos,mousestate[0]))
                file = open("config.json","w")
                json.dump(Config,file)
                file.close()
        if ButtonToggle2 != True:
            if (CustomCursorClicked.DrawButton(mousestate[0],mousepos)) or ButtonToggle1:
                offsetX = colorR1.DrawSlider(mousepos,mousestate[0])
                offsetY = colorG1.DrawSlider(mousepos,mousestate[0])
                if DrawColorPicker(400,185,mousepos,mousestate,offsetX,offsetY) != None:
                    file = open("config.json","w")
                    Config["cursor"]["pressed"] = list(DrawColorPicker(400,185,mousepos,mousestate,offsetX,offsetY))
                    json.dump(Config,file)
                    file.close()
                    ButtonToggle1 = False
                else:
                    ButtonToggle1 = True
        if ButtonToggle1 != True:
            if (CustomCursor.DrawButton(mousestate[0],mousepos)) or ButtonToggle2:
                offsetX = colorR2.DrawSlider(mousepos,mousestate[0])
                offsetY = colorG2.DrawSlider(mousepos,mousestate[0])
                if DrawColorPicker(400,235,mousepos,mousestate,offsetX,offsetY) != None:
                    file = open("config.json","w")
                    Config["cursor"]["color"] = list(DrawColorPicker(400,235,mousepos,mousestate,offsetX,offsetY))
                    json.dump(Config,file)
                    file.close()
                    ButtonToggle2 = False
                else:
                    ButtonToggle2 = True
        if (back.DrawButton(mousestate[0],mousepos)):
            main()
        DrawCustomCursor(mousepos[0],mousepos[1],mousestate[0])
        pygame.display.flip()
    while InfoPage:
        mousepos = pygame.mouse.get_pos()
        mousestate = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys. exit()
        surface.fill(GREY)
        text = font.render("this is a project produced by henry frodsham in 12C, its a simulation of natural selection", True, BLACK, GREY)
        surface.blit(text,(10,400))
        if (back.DrawButton(mousestate[0],mousepos)):
            main()
        DrawCustomCursor(mousepos[0],mousepos[1],mousestate[0])
        pygame.display.flip()
    while game:
        mousepos = pygame.mouse.get_pos()
        mousestate = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys. exit()
        surface.fill(GREY)
        zoom = (NewSlider.DrawSlider(mousepos,mousestate[0]) + 1)
        DrawObjects(zoom)
        if (SpawnFood.DrawButton(mousestate[0],mousepos)):
            CreateFoodObject()
        DrawCustomCursor(mousepos[0],mousepos[1],mousestate[0])
        pygame.display.flip()
while True:
    main()
#plans for version 3
#have functions in seperate files
#json data handling # done in this version
#more options
#notes
#start doing work document
#threading for performance maybe?
#ui rework, definitely not looking forward to that
#probably make zoom button do something but that might be for version 4
