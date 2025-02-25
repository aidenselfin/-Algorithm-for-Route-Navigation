# -Algorithm-for-Route-Navigation
정보융합탐구

## 탐구 주제:
현재 위치에서 장애물을 피해 목표물에 도달하는 최단 경로를 찾고 이를 시각화 하여 시뮬레이션할 수 있도록 할 예정이다. A*알고리즘에 대해 조사하고, 이를 대입하여 최단 경로를 찾을 것이다. 시뮬레이터에 x, y방향의 격자를 그리고, 격자를 클릭하면 장애물 생성 및 도착, 현재 위치를 지정할 수 있도록 할 것이다. 이후 길 찾기를 누르면 알고리즘에 따라 도착지까지 물체가 움직인다. 

## 알고리즘 소개
본 프로그램은 20*20 격자판에서 출발지에서 도착지까지 장애물을 피해 도달하는 것을 시뮬레이션하는 프로그램이다. 사용자는 시작 화면에서 Start, Goal버튼을 누른 후 격자를 클릭하여 출발지와 도착지를 지정할 수 있으며 Obstacle 버튼을 눌러 장애물을 지정하고 Run버튼으로 탐색을 시작할 수 있다. 

경로탐색 과정에서 자동차에게 보이는 장애물은 한정적이고 이를 통해 최선의 선택을 하기 위해서 다음과 같은 방법을 사용한다. 

자신에게 보이는 장애물을 고려하여 휴리스틱 함수를 계산한다. 이때 각위치의 휴리스틱 함수에서 출발지와 도착지 사이에 장애물이 있을 때 가중치를 준다.
휴리스틱 함수가 가장 작은 곳을 중간 지점으로 두고 인접한 네 곳의 휴리스틱 함수가 가장 작은 곳으로 이동한다. 
위 방법을 도착할 때까지 반복한다. 장애물을 만났을 때 가중치를 주는 방법은 다음과 같다. 
휴리스틱 함수를 계산하려는 지역에서 도착지점 또는 출발지점까지 선분을 그린뒤에 겹치는 부분을 장애물로 인식해서 가중치를 준다. 위와 같은 경우는 장애물이 2개가 감지된다. 감지된 장애물은 파란색으로 칠해져 있다. 


## Research Topic: 
The goal is to find the shortest path from the current position to the target while avoiding obstacles, visualize it, and simulate the movement. We will investigate the A* algorithm and apply it to find the shortest path. A simulator will be created with a grid of x and y directions, where users can click on the grid to create obstacles, set the start and goal positions. Afterward, by pressing the "Find Path" button, an object will move to the destination according to the algorithm.

## About Algorithm
This program simulates navigating from the start point to the goal point, avoiding obstacles on a 20x20 grid. The user can press the "Start" and "Goal" buttons on the initial screen to specify the start and goal points by clicking on the grid. The user can also press the "Obstacle" button to place obstacles and start the pathfinding by pressing the "Run" button.

During the pathfinding process, the car only detects visible obstacles, and in order to make the best choice, the following method is used:

The heuristic function is calculated by considering the visible obstacles. When there is an obstacle between the start and the goal at each position, a weight is added.
The point with the smallest heuristic function is selected as an intermediate point, and the next move is made toward the adjacent point with the smallest heuristic function.
This process is repeated until the destination is reached.
When an obstacle is detected, the following method is used to assign a weight: A line is drawn from the region where the heuristic function is being calculated to either the start or goal point, and the overlapping section is considered an obstacle and weighted. In the example shown, two obstacles are detected, and the detected obstacles are colored blue.
