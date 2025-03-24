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
pygame.display.set_caption("ImagePolylineMouseButton_Euclid_ErrorOnVertical")

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = []
count = 0
screen.fill(WHITE)

clock = pygame.time.Clock()

def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, color, pt, thick)

# ------------------------------------------------------------------------------
# 1) 수직선 예외처리를 제거하여, 분모 0 -> ZeroDivisionError 가 발생하게 함
#    그리고 에러가 발생하면 어떤 점 때문에 발생했는지 출력
# ------------------------------------------------------------------------------
def drawLineEuclid(pt0, pt1, color='GREEN', thick=1):
    x0, y0 = pt0
    x1, y1 = pt1
    
    try:
        slope = (y1 - y0) / (x1 - x0)  # 분모=0이면 ZeroDivisionError
    except ZeroDivisionError:
        print(f"[ZeroDivisionError] 수직선! pt0={pt0}, pt1={pt1}")
        raise  # 에러를 다시 던져서 상위에서도 처리하게 함

    # x를 1씩(또는 -1씩) 증가
    step = 1 if x1 > x0 else -1
    for x in range(x0, x1 + step, step):
        yy = slope*(x - x0) + y0
        pygame.draw.circle(screen, color, (x, int(round(yy))), thick)

def drawPolylinesEuclid(color='GREEN', thick=3):
    if count < 2:
        return
    for i in range(count - 1):
        drawLineEuclid(pts[i], pts[i + 1], color, thick)

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
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)
        print(f"len:{len(pts)} mouse x:{x} y:{y} button:{button1} pressed:{pressed} add pts ...")
    else:
        print(f"len:{len(pts)} mouse x:{x} y:{y} button:{button1} pressed:{pressed}")

    if len(pts) > 1:
        # ZeroDivisionError가 발생할 수 있으므로 try/except로 감싼다.
        try:
            drawPolylinesEuclid(GREEN, 1)
        except ZeroDivisionError:
            print("=> drawPolylinesEuclid 중 수직선 에러 발생!")
            # 원하는 동작(예: 프로그램 중단 등)을 여기서 처리할 수 있음

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
