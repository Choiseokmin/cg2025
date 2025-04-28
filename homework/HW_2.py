import pygame
from sys import exit
import numpy as np

# 화면 크기 설정
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton_MergedMode")

# Define colors in RGB
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (0,   0, 255)
GREEN = (0, 255,   0)
RED   = (255, 0,   0)

# 모드별 점 리스트
pts_free   = []
pts_euclid = []

mode = 'free'   # 'free' = coord-free, 'euclid' = Euclid 방식
screen.fill(WHITE)

clock = pygame.time.Clock()
margin = 6

# 한 번만 에러 메시지 출력용 플래그
euclid_error_printed = False

def drawLineCoordFree(pt0, pt1, color=GREEN, thick=1):
    x0, y0 = pt0; x1, y1 = pt1
    steps = max(abs(x1-x0), abs(y1-y0)) or 1
    for i in range(steps+1):
        t = i/steps
        px = round((1-t)*x0 + t*x1)
        py = round((1-t)*y0 + t*y1)
        pygame.draw.circle(screen, color, (px, py), thick)

def drawPolylinesFree(color=GREEN, thick=3):
    if len(pts_free) < 2: return
    for i in range(len(pts_free)-1):
        drawLineCoordFree(pts_free[i], pts_free[i+1], color, thick)

def drawLineEuclid(pt0, pt1, color=GREEN, thick=1):
    global euclid_error_printed
    x0, y0 = pt0; x1, y1 = pt1
    try:
        slope = (y1 - y0) / (x1 - x0)
    except ZeroDivisionError:
        if not euclid_error_printed:
            print("=> drawPolylinesEuclid 중 수직선 에러 발생!")
            euclid_error_printed = True
        return
    if (y1 - y0) == 0:
        if not euclid_error_printed:
            print("=> drawPolylinesEuclid 중 수평선 에러 발생!")
            euclid_error_printed = True
        return
    step = 1 if x1 > x0 else -1
    for x in range(x0, x1+step, step):
        yy = slope*(x - x0) + y0
        pygame.draw.circle(screen, color, (x, int(round(yy))), thick)

def drawPolylinesEuclid(color=GREEN, thick=3):
    if len(pts_euclid) < 2: return
    for i in range(len(pts_euclid)-1):
        drawLineEuclid(pts_euclid[i], pts_euclid[i+1], color, thick)

done = False
pressed = old_pressed = old_button1 = 0

while not done:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # 모드 토글
            mode = 'euclid' if mode=='free' else 'free'
            euclid_error_printed = False  # 플래그 리셋
            print(f"=== Mode switched to: {mode} ===")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        else:
            pressed = 0

    button1, _, _ = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    # 빨간 점으로 마우스 위치 표시
    pygame.draw.circle(screen, RED, pt, 0)

    # 좌클릭 → 점 추가 (현재 모드 리스트에만)
    if old_pressed==-1 and pressed==1 and old_button1==1 and button1==0:
        if mode == 'free':
            pts_free.append(pt)
        else:
            pts_euclid.append(pt)
        euclid_error_printed = False  # 새 점 추가 시 에러 메시지 재허용
        pygame.draw.rect(screen, BLUE, (x-margin, y-margin, 2*margin, 2*margin), 5)
        print(f"[{mode}] point added: {pt}")

    # 모드별 그리기
    if mode == 'free':
        drawPolylinesFree(GREEN, 1)
    else:
        drawPolylinesEuclid(GREEN, 1)

    pygame.display.update()
    old_button1, old_pressed = button1, pressed

pygame.quit()
