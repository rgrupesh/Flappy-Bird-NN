import pygame
import neat
import time
import os
import random

width=600
height=800

bird_img=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
bg_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
base_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
pipe_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

class Bird:
    img=bird_img
    rot_vel=20
    max_rot=25
    ani_time=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.val=0
        self.height=self.y
        self.img_count=0
        self.img=self.img[0]

    def jump(self):
        self.val=-15
        self.tick_count=0
        self.height=self.y

    def move(self):

while True:
    bird.move()
