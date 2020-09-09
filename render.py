import pygame
import math,os


class Defs:
    colorMax = 255
    colorMin = 0


class RenderDesc:
    winWidth = 800
    winHeight = 600


class Camera:
    x = 0
    y = 0


class Render:

    renderTarget = 0
    rtWidthHalf = 0
    rtHeightHalf = 0
    camera = 0
    affection = 1

    matId = 0
    materials = []

    color = (Defs.colorMax, Defs.colorMax, Defs.colorMax)

    def __init__(self, Width,Height,FullSc):
        pygame.display.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
       
        if(FullSc==False):
            self.rtWidthHalf = Width / 2
            self.rtHeightHalf = Height / 2
            self.renderTarget = pygame.display.set_mode((Width, Height))
            self.camera = Camera
        else:
            #screen_width,screen_height = info.current_w,info.current_h
            self.rtWidthHalf = Width / 2
            self.rtHeightHalf = Height / 2
            self.renderTarget = pygame.display.set_mode((Width, Height),pygame.FULLSCREEN)
            self.camera = Camera


    def loadMaterial(self, filename):
        img = pygame.image.load(filename)
        img = img.convert()
        self.materials.append(img)
        return len(self.materials) - 1

    def drawRectangle(self, x, y, hw, hh, useMat = False, ang = 0):
        if useMat:
            self.__renderMat(x, y, hw, hh, ang)
        else:
            self.__renderRect(x, y, hw, hh)
    def drawRect(self,vert):
        xc = (vert[0][0]+vert[1][0]+vert[2][0]+vert[3][0])/4
        yc = (vert[0][1]+vert[1][1]+vert[2][1]+vert[3][1])/4
        width = xc - vert[0][0]
        height = yc - vert[0][1]
        self.__renderRect(xc,-yc,width,height)




    def drawTriangle(self, x1, y1, x2, y2, x3, y3):
        pygame.draw.polygon(self.renderTarget, self.color,
                            [(x1 + self.rtWidthHalf - self.camera.x*self.affection,
                              y1 + self.rtHeightHalf - self.camera.y*self.affection),
                             (x2 + self.rtWidthHalf - self.camera.x*self.affection,
                              y2 + self.rtHeightHalf - self.camera.y*self.affection),
                             (x3 + self.rtWidthHalf - self.camera.x*self.affection,
                              y3 + self.rtHeightHalf - self.camera.y*self.affection)])

    def drawLine(self, x1, y1, x2, y2):
        pygame.draw.line(self.renderTarget, self.color, (int(x1 + self.rtWidthHalf - self.camera.x*self.affection),
                                                         int(y1 + self.rtHeightHalf - self.camera.y*self.affection)),
                                                        (int(x2 + self.rtWidthHalf - self.camera.x*self.affection),
                                                         int(y2 + self.rtHeightHalf - self.camera.y*self.affection)))
    def drawPolygon(self, x1, y1, x2, y2, x3, y3, x4, y4):
        pygame.draw.polygon(self.renderTarget, self.color,
                            [(x1 + self.rtWidthHalf - self.camera.x*self.affection,
                              -y1 + self.rtHeightHalf - self.camera.y*self.affection),
                             (x2 + self.rtWidthHalf - self.camera.x*self.affection,
                              -y2 + self.rtHeightHalf - self.camera.y*self.affection),
                             (x3 + self.rtWidthHalf - self.camera.x*self.affection,
                              -y3 + self.rtHeightHalf - self.camera.y*self.affection),
                             (x4 + self.rtWidthHalf - self.camera.x*self.affection,
                              -y4 + self.rtHeightHalf - self.camera.y*self.affection)])
    def get_render_target(self):
        return self.renderTarget

    def drawCircle(self, x, y, r):
        pygame.draw.circle(self.renderTarget, self.color,
                           (int(x + self.rtWidthHalf - self.camera.x*self.affection),
                            int(y + self.rtHeightHalf - self.camera.y*self.affection)), r)

    def setCameraAffection(self, affect):
        assert (affect >= 0 and affect <= 1), "Camera affection must be in range [0 ... 1]"
        self.affection = affect

    def setCameraPos(self, x, y):
        self.camera.x = int(x)
        self.camera.y = int(y)

    def setMaterial(self, mat):
        self.matId = mat

    def setColor(self, r, g, b):
        assert (r >= 0 and g >= 0 and b >= 0), "Color component must be >= 0"
        r = min(Defs.colorMax, r)
        g = min(Defs.colorMax, g)
        b = min(Defs.colorMax, b)

        self.color = (r, g, b)

    def draw(self,running):
        pygame.display.flip()
        if(running==True):
            self.renderTarget.fill((255,255,255))
        else:
            self.renderTarget.fill((223,73,60))
        #pygame.event.get()

    def __renderMat(self, x, y, hw, hh, ang):
        self.renderTarget.blit(pygame.transform.rotate(self.materials[self.matId], ang),
                               (x - hw + self.rtWidthHalf - self.camera.x*self.affection,
                                y - hh + self.rtHeightHalf - self.camera.y*self.affection, hw*2, hh*2))

    def __renderRect(self, x, y, hw, hh):
        pygame.draw.rect(self.renderTarget, self.color,
                         pygame.Rect(x - hw + self.rtWidthHalf - self.camera.x*self.affection, y - hh
                                     + self.rtHeightHalf - self.camera.y*self.affection, hw*2, hh*2))
    def getDimHalf(self):
        return (self.rtWidthHalf,self.rtHeightHalf)