import pygame
import numpy as np
from math import comb

# 화면 크기 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# 색 정의
WHITE = (255, 255, 255)
BLUE  = (0,   0, 255)  # 클릭 강조용
GREEN = (0, 255,   0)  # 폴리라인
RED   = (255, 0,   0)  # 점
BLACK = (0,   0,   0)  # Bézier

pts = []      # 클릭된 점들
clock = pygame.time.Clock()
margin = 6

def drawPolylines(color=GREEN, thick=2):
    """직선 폴리라인"""
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)

def drawBezierAll(color=BLACK, samples=200, thick=2):
    """모든 클릭된 점을 제어점으로 하는 Bézier 곡선 그리기"""
    n = len(pts)
    if n < 2:
        return

    P = [np.array(p, dtype=float) for p in pts]
    m = n - 1
    # 이항 계수 미리 계산
    coeffs = [comb(m, i) for i in range(n)]
    ts = np.linspace(0.0, 1.0, samples)

    curve = []
    for t in ts:
        point = np.zeros(2, dtype=float)
        for i in range(n):
            bern = coeffs[i] * ((1 - t) ** (m - i)) * (t ** i)
            point += bern * P[i]
        curve.append((int(point[0]), int(point[1])))

    pygame.draw.lines(screen, color, False, curve, thick)

# 마우스 클릭 상태 변수
pressed = old_pressed = 0
old_button1 = 0

done = False
while not done:
    clock.tick(30)
    screen.fill(WHITE)  # 매 프레임 화면 초기화

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
        # 클릭 위치 강조 사각형
        pygame.draw.rect(screen, BLUE,
                         (x - margin, y - margin, 2*margin, 2*margin), 2)

    # 점들 다시 그리기
    for p in pts:
        pygame.draw.circle(screen, RED, p, 4)

    # 폴리라인과 Bézier 곡선 그리기
    if len(pts) > 1:
        drawPolylines()
        drawBezierAll()

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
