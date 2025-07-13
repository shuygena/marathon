from flask import Flask, request, jsonify, Response

app = Flask(__name__)

last_task = None
last_result = None

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
        data = request.get_json()
        
        if not isinstance(data, dict) or 'view' not in data or check_view_format(data['view']) is False:
            return get_json_response({"action": "None"}, status=400)

            # Здесь можно добавить логику обработки матрицы (data['view'])
        return get_json_response({"action": "Something"}, status=200)
    except Exception as e:
        return get_json_response({"action": "None"}, status=400)


@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()

        if not isinstance(data, dict) or 'type' not in data or 'task' not in data or not isinstance(data['type'], str) or not isinstance(data['task'], str):
            return Response(status=400)
        
        global last_task
        last_task = data
        
        # Здесь можно добавить логику решения задачи
        return get_json_response({"answer": "Да"}, status=200)
    except Exception as e:
        return Response(status=400)


@app.route('/tasks/last', methods=['PATCH'])
def update_last_task():
    try:
        data = request.get_json()
        
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

        if not isinstance(data, dict) or ('type' not in data or 'desc' not in data 
            or not isinstance(data['type'], str)
            or not isinstance(data['desc'], str)):
            return Response(status=400)

        return Response(status=200)
    except Exception as e:
        return Response(status=400)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
