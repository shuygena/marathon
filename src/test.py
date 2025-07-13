import pytest
import requests

BASE_URL = "http://localhost:8080"


@pytest.mark.parametrize('input_json, expexted_status_code, expected_response',
                    [
                        ({"view": [[2,1,0],[0,3,1]]}, 200, {"action": "Something"}),
                        ({"view": [['a','b'],['c','d']]}, 400, {"action": "None"}),
                        ({"view": [2,1,0,0,3,1]}, 400, {"action": "None"}),
                        ({"view": "lol"}, 400, {"action": "None"}),
                        ({"something": 1}, 400, {"action": "None"}),
                        (123, 400, {"action": "None"}),
                        ({}, 400, {"action": "None"}),
                     ])
def test_create_input(input_json, expexted_status_code, expected_response):
    response = requests.post(f"{BASE_URL}/inputs", json=input_json)
    assert response.status_code == expexted_status_code
    assert response.json() == expected_response

@pytest.mark.parametrize('task_json, expexted_status_code, expected_response',
                    [
                        ({"type": "Question", "task": "Ты готов?"}, 200, {"answer": "Да"}),
                        ({"view": [2,1,0,0,3,1]}, 400, None),
                        ({"type": "Question"}, 400, None),
                        ({"task": "Ты готов?", "type": 1}, 400, None),
                        ({"task": 5, "type": "Ты готов?"}, 400, None),
                        ({"task": "Ты готов?"}, 400, None),
                        (123, 400, None),
                        ({}, 400, None),
                     ])
def test_create_task(task_json, expexted_status_code, expected_response):
    response = requests.post(f"{BASE_URL}/tasks", json=task_json)
    assert response.status_code == expexted_status_code
    if response.status_code == 200:
        assert response.json() == expected_response

@pytest.mark.parametrize('result_json, expexted_status_code',
                    [
                        ({"result": "Ok"}, 200),
                        ({"result": "Fail"}, 404),
                        ({"result": "TryAgain"}, 400),
                        ({"result": 5}, 400),
                        ({"task": "Ты готов?"}, 400),
                        (123, 400),
                        ({}, 400),
                     ])
def test_update_last_task(result_json, expexted_status_code):
    # Сначала создаем задачу
    # requests.post(f"{BASE_URL}/tasks", json={"type": "example", "task": "Solve the problem"})
    
    response = requests.patch(f"{BASE_URL}/tasks/last", json=result_json)
    assert response.status_code == expexted_status_code


@pytest.mark.parametrize('notifications_json, expexted_status_code',
                    [
                        ({"type": "PreparationDone",
                          "desc": "Ждем тебя в финале!"}, 200),
                        ({"type": "PreparationDone"}, 400),
                        ({"desc": "Ждем тебя в финале!"}, 400),
                        ({"type": 5, "desc": "Ждем тебя в финале!"}, 400),
                        ({"type": "PreparationDone", "desc": 6}, 400),
                        (123, 400),
                        ({}, 400),
                     ])
def test_send_notifications(notifications_json, expexted_status_code):
    response = requests.post(f"{BASE_URL}/notifications", json=notifications_json)
    assert response.status_code == expexted_status_code
