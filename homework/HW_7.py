import pygame
from sys import exit
import numpy as np

# 화면 크기 설정
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Cubic B-spline Interpolation")

# 색 정의
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

pts = []      # 클릭된 점들

clock = pygame.time.Clock()
margin = 6

def drawPolylines(color=GREEN, thick=1):
    """직선 폴리라인 (제어점 연결)"""
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)

def drawBSpline(color=RED, samples=300, thick=2):
    """Cubic B-spline 보간 곡선 (끝점 연결)"""
    n = len(pts)
    if n < 4:
        return

    # t ∈ [0, n-3], endpoint=True로 마지막 t=n-3 포함
    ts = np.linspace(0, n-3, samples, endpoint=True)
    spline = []
    for t in ts:
        k = min(int(t), n-4)  # k 최대 n-4로 클램핑
        u = t - k

        p0 = np.array(pts[k])
        p1 = np.array(pts[k+1])
        p2 = np.array(pts[k+2])
        p3 = np.array(pts[k+3])

        # Cubic B-spline 기저 함수
        B0 = ((1 - u)**3) / 6.0
        B1 = (3*u**3 - 6*u**2 + 4) / 6.0
        B2 = (-3*u**3 + 3*u**2 + 3*u + 1) / 6.0
        B3 = (u**3) / 6.0

        pt = p0*B0 + p1*B1 + p2*B2 + p3*B3
        spline.append((int(pt[0]), int(pt[1])))

    # 시작점과 끝점을 제어점과 정확히 맞춤
    spline[0] = tuple(pts[0])
    spline[-1] = tuple(pts[-1])

    pygame.draw.lines(screen, color, False, spline, thick)

# 마우스 클릭 상태 변수
pressed = old_pressed = 0
old_button1 = 0

done = False
while not done:
    clock.tick(30)
    screen.fill(WHITE)  # 화면 초기화

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

    # 제어점 그리기
    for p in pts:
        pygame.draw.circle(screen, GREEN, p, 4)

    # 제어점 폴리라인 (원하면 제거)
    if len(pts) > 1:
        drawPolylines()

    # Cubic B-spline 곡선 그리기
    if len(pts) >= 4:
        drawBSpline()

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
