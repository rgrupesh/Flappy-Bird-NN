import pygame
import neat
import time
import os
import random

WIDTH=600
HEIGHT=800

bird_img= [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
bg_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
base_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
pipe_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

class Bird:
    IMGS=bird_img
    ROT_VEL=20
    MAX_ROT=25
    ANI_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.val=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[0]

    def jump(self):
        self.val=-15
        self.tick_count=0
        self.height=self.y

    def move(self):
        self.tick_count+=1

        d=self.val*self.tick_count + 1.5*self.tick_count**2

        if d>=16:
            d=16
        if d<0:
            d-=2

        self.y=self.y + d

        if d<0 or self.y<self.height +50:
            if self.tilt < self.MAX_ROT:
                self.tilt= self.MAX_ROT
        else:
            if self.tilt> -90:
                self.tilt-= self.ROT_VEL
    def draw(self,win):
        self.img_count+=1

        if self.img_count <= self.ANI_TIME:
            self.img= self.IMGS[0]
        elif self.img_count <= self.ANI_TIME*2:
            self.img= self.IMGS[1]
        elif self.img_count <= self.ANI_TIME*3:
            self.img= self.IMGS[2]
        elif self.img_count <= self.ANI_TIME*4:
            self.img= self.IMGS[1]
        elif self.img_count == self.ANI_TIME*4 + 1:
            self.img= self.IMGS[0]
            self.img_count=0

        if self.tilt <= -80:
            self.img=self.IMGS[1]
            self.img_count= self.ANI_TIME*2

        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win,bird):
    win.blit(bg_img,(0,0))

    bird.draw(win)
    pygame.display.update()


def main():
    bird=Bird(200,200)
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
        draw_window(win,bird)

    pygame.quit()
    quit()
