import pygame
import numpy as np

# 초기화
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Autonomous Car Path Simulator")

# 색상 정의
WHITE = (255, 255, 255)  # 기본: 흰색
GOAL = (0, 255, 0)  # 초록색
START = (0, 0, 255)  # 파란색
OBSTACLE = (128, 128, 128)  # 회색
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PASSED = (200, 200, 200)
SEARCHING = (255, 165, 0)
FOUND = (255, 255, 0) #중간지점, 노란색

# 초기 격자 배열 생성
cell_size = size[0] // 20
arr = np.zeros((20, 20))

goalx, goaly = 3, 3
arr[goalx][goaly] = 2
startx, starty = 10, 10
arr[startx][starty] = 5

font = pygame.font.Font(None, 20)

# 격자 그리기 함수 기본: 0, 목표지점: 2 출발지점: 5 장애물:1 지나온 길:6 탐색: 7 선택 완료: 8
def draw_grid():
    for x in range(20):
        for y in range(20):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if arr[x, y] == 2:
                pygame.draw.rect(screen, GOAL, rect)
            elif arr[x, y] == 5:
                pygame.draw.rect(screen, START, rect)
            elif arr[x, y] == 1:
                pygame.draw.rect(screen, OBSTACLE, rect)
            elif arr[x, y] == 6:
                pygame.draw.rect(screen, PASSED, rect)
            elif arr[x, y] == 7:
                pygame.draw.rect(screen, SEARCHING, rect)
            elif arr[x, y] == 8:
                pygame.draw.rect(screen, FOUND, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))

def button_clicked(x, y, w, h, mouse_pos):
    return x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h

def draw_number(x, y, number):
    if number!=10000:
        text_surf = font.render(f"{number:.2f}", True, BLACK)
        text_rect = text_surf.get_rect(center=((x * cell_size) + cell_size // 2, (y * cell_size) + cell_size // 2))
        screen.blit(text_surf, text_rect)

def heuristic(x, y, goalx, goaly, startx, starty):
    if x>=20 or x<0 or y>=20 or y<0:
                return
    f = np.sqrt((goalx - x)**2 + (goaly - y)**2)
    g = np.sqrt((x - startx)**2 + (y - starty)**2)
    # 장애물 가중치, 우선 goal<x<start
    i = 0; j=0
    if goalx<x and goaly<y: j=1; i=1
    elif goalx<x and goaly>y: j=1; i=-1
    elif goalx>x and goaly<y: j=-1; i=1
    else: j=-1; i=-1
    
    if abs(goalx - x) > 1 and abs(goaly - y) > 1:
        for movex in range(1, abs(goaly - y) + 1):
            y_index = y - i * int((goaly - y) / (goalx - x) * j * movex)
            if 0 <= x - j * movex < 20 and 0 <= y_index < 20:
                if (arr[x - j * movex][y_index] == 1 or
                    arr[x - j * movex][y_index + 1] == 1 or
                    arr[x - j * movex][y_index - 1] == 1):
                    f *= 2
    
    k = 0; r=0
    if goalx<x and goaly<y: k=1; r=1
    elif goalx<x and goaly>y: k=1; r=-1
    elif goalx>x and goaly<y: k=-1; r=1
    else: k=-1; r=-1
    
    if abs(startx - x) > 1 and abs(starty - y) > 1:
        for movex in range(1, abs(starty - y) + 1):
            y_index = y + r * int((starty - y) / (startx - x) * movex)
            if 0 <= x + k * movex < 20 and 0 <= y_index < 20:
                if (arr[x + k * movex][y_index] == 1 or
                    arr[x + k * movex][y_index + 1] == 1 or
                    arr[x + k * movex][y_index - 1] == 1):
                    g *= 2
    h = g + f
    return h

def move(x,y):
    pygame.time.delay(100)
    #단계 2
    heu1 = np.full((20,20), 10000, dtype=float)
    mx = x; my =y
    for i in range(-3, 4):
        for j in range(-3, 4):
            if abs(i)+abs(j)>4:
                continue
            if x+i>=20 or x+i<0 or y+j>=20 or y+j<0:
                continue
            if i==0 and j==0: continue
            if arr[x+i][y+j]==0 or arr[x+i][y+j]==2:
                arr[x+i][y+j] = 7
                heu1[x+i][y+j] = heuristic(x+i, y+j, goalx, goaly, x, y)
            if heu1[mx][my]>heu1[x+i][y+j]:
                mx = x+i; my = y+j
    draw_grid()
    for i in range(-3, 4):
        for j in range(-3, 4):
            if abs(i)+abs(j)>4:
                continue
            if x+i>=20 or x+i<0 or y+j>=20 or y+j<0:
                continue
            draw_number(x+i, y+j, heu1[x+i][y+j])
            
    pygame.display.flip()
    pygame.event.pump()  # Pygame 이벤트 처리
    pygame.time.delay(500)
    
    arr[mx][my] = 8 #중간 지점 표시
    draw_grid()
    for i in range(-3, 4):
        for j in range(-3, 4):
            if abs(i)+abs(j)>4:
                continue
            if x+i>=20 or x+i<0 or y+j>=20 or y+j<0:
                continue
            draw_number(x+i, y+j, heu1[x+i][y+j])
    pygame.display.flip()
    pygame.event.pump()  # Pygame 이벤트 처리 
    pygame.time.delay(2000)
       
    arr[mx][my] = 0 #중간 지점 초기화   
    for i in range(-3, 4):
        for j in range(-3, 4):
            if abs(i)+abs(j)>4:
                continue
            if x+i>=20 or x+i<0 or y+j>=20 or y+j<0:
                continue
            if arr[x+i][y+j]==7:    
                arr[x+i][y+j]=0
    #중간지점 선택 완료(mx, my)
    #단계 3
    heu2 = np.full((20,20), 10000, dtype=float)
    direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    newx = x; newy = y
    
    for i, j in direction:
        if x+i>=20 or x+i<0 or y+j>=20 or y+j<0:
                continue
        if arr[x+i][y+j]==0 or arr[x+i][y+j]==2:
            heu2[x+i][y+j] = heuristic(x+i, y+j, mx, my, x, y)
        if heu2[newx, newy]>heu2[x+i][y+j]:
            newx = x+i; newy = y+j
    #이동 위치 선택 완료
    
    if newx == goalx and newy == goaly:
        arr[x][y] = 2 #다녀간 경로
        draw_grid()
        pygame.display.flip()
        return
    elif x==startx and y==starty:
        draw_grid()
        pygame.display.flip()
        pygame.event.pump()  # Pygame 이벤트 처리
        move(newx, newy)
    else:
        arr[x][y] = 6 #다녀간 경로
        draw_grid()
        move(newx, newy)

running = True
mode = None  # 모드: 'start', 'goal', 'obstacle'

while running:
    screen.fill(WHITE)
    draw_grid()
    draw_button("Start", 650, 100, 100, 50, START)
    draw_button("Goal", 650, 200, 100, 50, GOAL)
    draw_button("Obstacle", 650, 300, 100, 50, OBSTACLE)
    draw_button("Run", 650, 400, 100, 50, RED)

    for event in pygame.event.get(): #버튼 클릭시 모드 바꾸기
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button_clicked(650, 100, 100, 50, pos):
                mode = 'start'
            elif button_clicked(650, 200, 100, 50, pos):
                mode = 'goal'
            elif button_clicked(650, 300, 100, 50, pos):
                mode = 'obstacle'
            elif button_clicked(650, 400, 100, 50, pos):
                if startx != -1 and starty != -1 and goalx != -1 and goaly != -1:
                    move(startx, starty) #탐색시작 
            else: #START, GOAL 지점 하나만 선택하게끔 하기
                x, y = pos[0] // cell_size, pos[1] // cell_size
                if x < 20 and y < 20:
                    if mode == 'start':
                        if startx != -1 and starty != -1:
                            arr[startx, starty] = 0  # 이전 시작점 초기화
                        startx, starty = x, y
                        arr[startx, starty] = 5
                    elif mode == 'goal':
                        if goalx != -1 and goaly != -1:
                            arr[goalx, goaly] = 0  # 이전 목표점 초기화
                        goalx, goaly = x, y
                        arr[goalx, goaly] = 2
                    elif mode == 'obstacle':
                        arr[x, y] = 1

    pygame.display.flip()

pygame.quit()
