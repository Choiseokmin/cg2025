import pygame
from sys import exit
import numpy as np

# 화면 크기 설정
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# 색 정의
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

pts = []      # 클릭된 점들

clock = pygame.time.Clock()
margin = 6

def drawPolylines(color=GREEN, thick=1):
    """직선 폴리라인"""
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)

def drawLagrangePolylines(color=BLUE, samples=200, thick=2):
    """Lagrange 보간 곡선"""
    n = len(pts)
    if n < 2: return

    ts = np.linspace(0, n-1, samples)
    curve = []
    for t in ts:
        x_t, y_t = 0.0, 0.0
        for i in range(n):
            Li = 1.0
            for j in range(n):
                if j != i:
                    Li *= (t - j) / float(i - j)
            x_t += pts[i][0] * Li
            y_t += pts[i][1] * Li
        curve.append((int(x_t), int(y_t)))
    pygame.draw.lines(screen, color, False, curve, thick)

# 마우스 클릭 상태
pressed = old_pressed = 0
old_button1 = 0

done = False
while not done:
    clock.tick(30)

    # 화면 초기화 (배경을 쓸 경우에는 blit background)
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, _, _ = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    # 클릭이 완전히 눌렸다가 떨어지면 점 추가
    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        # 클릭 위치 강조 사각형 (원하면 주석 처리 가능)
        pygame.draw.rect(screen, BLUE,
                         (x - margin, y - margin, 2*margin, 2*margin), 2)

    # 기존 점들은 매 프레임 재렌더링
    for p in pts:
        pygame.draw.circle(screen, RED, p, 4)

    # 폴리라인 & Lagrange 곡선
    if len(pts) > 1:
        drawPolylines(GREEN, thick=2)
        drawLagrangePolylines(BLUE, samples=300, thick=2)

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
