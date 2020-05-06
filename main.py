import pygame
import neat
import time
import os
import random
pygame.font.init()

WIDTH=500
HEIGHT=800

bird_img= [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
bg_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
base_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
pipe_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
Font= pygame.font.SysFont("comisans", 50)


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
        new_rect=(rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center))
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP=200
    VEL=5


    def __init__(self,x):
        self.x= x
        self.height= 0
        self.gap= 100

        self.top =0
        self.bottom=0
        self.PIPE_TOP=pygame.transform.flip(pipe_img,False,True)
        self.PIPE_BOTTOM = pipe_img

        self.passed=False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top= self.height - self.PIPE_TOP.get_height()
        self.bottom= self.height + self.gap

    def move(self):
        self.x -= self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask= bird.get_mask()
        top_mask= pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask= pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset= (self.x - bird.x,self.top - round(bird.y))
        bottom_offset= (self.x - bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

class Base:
    VEL=5
    WIDTH= base_img.get_width()
    IMG= base_img


    def __init__(self,y):
        self.y= y
        self.x1=0
        self.x2 = self.WIDTH
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1=self.x2+ self.WIDTH
        if self.x2 + self.WIDTH <0:
            self.x2=self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))























def draw_window(win,bird,pipes,base,score):
    win.blit(bg_img,(0,0))

    for pipe in pipes:
        pipe.draw(win)

    text= Font.render("Score:" + str(score),1,(255,255,255))
    win.blit(text,(WIDTH - 10 - text.get_width(),10))

    base.draw(win)


    bird.draw(win)
    pygame.display.update()


def main():
    bird=Bird(230,350)
    base= Base(730)
    pipes = [Pipe(700)]
    win=pygame.display.set_mode((WIDTH,HEIGHT))

    clock=pygame.time.Clock()
    run=True
    score =0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
        #bird.move()
        base.move()

        add_pipe= False
        remove=[]
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed =True
                add_pipe= True


            pipe.move()

        if add_pipe:
            score +=1
            pipes.append(Pipe(550))

        for r in remove:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >=700:
            pass


        draw_window(win,bird,pipes,base,score)

    pygame.quit()
    quit()

main()
