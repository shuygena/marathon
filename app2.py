from flask import Flask, request, jsonify, Response
from collections import deque

app = Flask(__name__)

last_task = None
last_result = None
last_step = None
step_list = list()
phase = 1
# 1 - first_labirint, 2 - tonel, 3 - sphinx, 4 - exit

def find_shortest_path(matrix, target):
    # Определим размеры матрицы
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Направления движения (вверх, вниз, влево, вправо)
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    steps = ["Right", "Left", "Up", "Down"]
    
    def is_valid(x, y):
        return x >= 0 and x < rows and y >= 0 and y < cols and matrix[x][y] in [1, target]
    
    # Поиск позиции игрока (символ '3')
    start_x, start_y = None, None
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 3:
                start_x, start_y = i, j
                
    # Очередь для алгоритма BFS
    queue = deque([(start_x, start_y)])
    visited = [[False]*cols for _ in range(rows)]  # Матрица посещенных клеток
    parent = {}  # Родительские узлы для восстановления пути
    found_door = False
    
    while queue:
        current_x, current_y = queue.popleft()
        
        if matrix[current_x][current_y] == target:
            found_door = True
            break
            
        visited[current_x][current_y] = True
        
        for idx, (dx, dy) in enumerate(directions):
            new_x, new_y = current_x + dx, current_y + dy
            
            if not is_valid(new_x, new_y) or visited[new_x][new_y]:
                continue
                
            parent[(new_x, new_y)] = ((current_x, current_y), steps[idx])  # Запоминаем предыдущее положение и направление шага
            queue.append((new_x, new_y))
    
    if not found_door:
        return []
    
    path = []
    current_pos = (current_x, current_y)
    
    while current_pos != (start_x, start_y):
        prev_pos, step = parent[current_pos]
        path.insert(0, step)
        current_pos = prev_pos
    
    return path

def tunnel_counter(matrix, last_step):
    # Размер матрицы
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Определяем возможные направления шагов
    directions = {
        'Up': (-1, 0),   # Вверх
        'Down': (1, 0),    # Вниз
        'Left': (0, -1),  # Влево
        'Right': (0, 1)     # Вправо
    }
    
    # Находим позицию персонажа
    position = None
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 3:
                position = (i, j)
                break
        if position:
            break
    
    # Получаем направление последнего шага
    dx, dy = directions[last_step]
    
    # Начинаем считать шаги
    count = 0
    curr_x, curr_y = position
    
    # Идём в нужном направлении, пока не наткнёмся на препятствие
    while True:
        nx, ny = curr_x + dx, curr_y + dy
        if nx < 0 or nx >= rows or ny < 0 or ny >= cols or matrix[nx][ny] == 0:
            break
        count += 1
        curr_x, curr_y = nx, ny
    
    return count

def get_json_response(json_dict, status):
    response = jsonify(json_dict)
    response.status_code = status
    return response


def check_view_format(view):
    if not isinstance(view, list):
        return False
    
    for row in view:
        if not isinstance(row, list):
            return False
        
        for item in row:
            if not isinstance(item, int):
                return False
            
    return True



@app.route('/inputs', methods=['POST'])
def create_input():
    try:
        global last_step
        global step_list
        global phase
        data = request.get_json()

        # for arr in data['view']:
            # print(arr)
        if not isinstance(data, dict) or 'view' not in data or check_view_format(data['view']) is False:
            return get_json_response({"action": "None"}, status=400)
        if last_step == None or phase == 1:
            step_list = find_shortest_path(data['view'], 4)
        elif phase == 2 and not step_list:
            step_list = [last_step] * (tunnel_counter(data['view'], last_step) + 1)
        elif phase == 3 and not step_list:
            step_list = find_shortest_path(data['view'], 5)
        elif phase == 4 and not step_list:
            step_list = find_shortest_path(data['view'], 2)


        
        if step_list:
            action = step_list.pop(0)
            # print(f'phase: {phase} current_action{action}, step_list{step_list}')
            last_step = action
        else:
            action = "None"
        if not step_list:
            if phase <= 4:
                phase += 1
            # if phase < 4:
            #     phase += 1
            # else:
            #     phase = 1
        # print(f'response: "action": {action}')
        return get_json_response({"action": action}, status=200)
    except Exception as e:
        print(f'response: "action": "None"; {e}')
        return get_json_response({"action": "None"}, status=400)


@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        # print(f'data: {data}')
        if not isinstance(data, dict) or 'type' not in data or 'task' not in data or not isinstance(data['type'], str) or not isinstance(data['task'], str):
            return Response(status=400)
        
        global last_task
        last_task = data
        
        # Здесь можно добавить логику решения задачи
        
        # print(f'response: "answer": "Да"')
        return get_json_response({"answer": "Да"}, status=200)
    except Exception as e:
        return Response(status=400)


@app.route('/tasks/last', methods=['PATCH'])
def update_last_task():
    try:
        data = request.get_json()
        # print(f'data: {data}')
        if not isinstance(data, dict) or 'result' not in data or not isinstance(data['result'], str) or data['result'] not in ['Ok','Fail']: # TryAgain должен быть 400?
            return Response(status=400)

        if last_task is None or data['result'] == 'Fail':
            return Response(status=404)

        global last_result
        last_result = data['result']

        return Response(status=200)
    except Exception as e:
        return Response(status=400)
    

@app.route('/notifications', methods=['POST'])
def send_notification():
    try:
        data = request.get_json()
        # print(f'data: {data}')
        if not isinstance(data, dict) or ('type' not in data or 'desc' not in data 
            or not isinstance(data['type'], str)
            or not isinstance(data['desc'], str)):
            return Response(status=400)
        # if data: ['type'] == 'NewLevel' and data['desc':] == '1':
            
        return Response(status=200)
    except Exception as e:
        return Response(status=400)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
