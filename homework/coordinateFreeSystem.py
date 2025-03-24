"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import pygame
from sys import exit
import numpy as np
    
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'image/curve_pattern.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = [] 
knots = []
count = 0
screen.fill(WHITE)

clock= pygame.time.Clock()

def drawPoint(pt, color='GREEN', thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

# 기존 drawLine 함수는 그대로 두되, 사용은 안 함
def drawLine(pt0, pt1, color='GREEN', thick=3):
    drawPoint((100,100), color, thick)
    drawPoint(pt0, color, thick)
    drawPoint(pt1, color, thick)

# ------------------------------------------------------------------------------
# coordinate free system:
#   p(t) = a0*p0 + a1*p1,   (a0=1-t, a1=t),   t in [0,1]
#   --> 아래에서 steps만큼 t를 나눠 픽셀 단위로 그린다.
# ------------------------------------------------------------------------------
def drawLineCoordFree(pt0, pt1, color='GREEN', thick=1):
    x0, y0 = pt0
    x1, y1 = pt1
    
    # 두 점이 같은 경우 -> 그냥 한 점만 찍고 종료
    if x0 == x1 and y0 == y1:
        pygame.draw.circle(screen, color, pt0, thick)
        return
    
    # steps를 대충 두 점 사이의 거리(가장 긴 축) 정도로 설정
    steps = max(abs(x1 - x0), abs(y1 - y0))
    if steps == 0:
        steps = 1
    
    for i in range(steps + 1):
        t = i / steps
        # p(t) = (1-t)*p0 + t*p1
        px = (1 - t)*x0 + t*x1
        py = (1 - t)*y0 + t*y1
        # 소수점 보정
        pygame.draw.circle(screen, color, (int(round(px)), int(round(py))), thick)

def drawPolylines(color='GREEN', thick=3):
    if (count < 2):
        return
    for i in range(count - 1):
        # 여기서 a0*p0 + a1*p1 방식으로 선을 그림
        drawLineCoordFree(pts[i], pts[i+1], color, thick)

# ------------------------------------------------------------------------------
# 메인 루프
# ------------------------------------------------------------------------------
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    # 마우스 좌표에 빨간 점 표시
    pygame.draw.circle(screen, RED, pt, 0)

    # 마우스 왼 버튼을 눌렀다가 뗀 시점에 점을 추가
    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt) 
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+
              " button:"+repr(button1)+" pressed:"+repr(pressed)+" add pts ...")

    # 점이 2개 이상일 때 폴리라인 그리기
    if len(pts) > 1:
        drawPolylines(GREEN, 1)

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
