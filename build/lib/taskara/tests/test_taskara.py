import pytest
import json
from taskara import Taskara

# Initialize a Taskara instance for tests
@pytest.fixture
def taskara():
    return Taskara()

def test_initialization(taskara):
    assert taskara.title == "Taskara"
    assert taskara.project_root == "."
    assert taskara.tasks == set()

def test_set_mode_valid(taskara):
    taskara.set_mode(Taskara.mode.INFO)
    assert taskara.mode == Taskara.mode.INFO

def test_set_mode_invalid(taskara):
    taskara.set_mode("INVALID_MODE")
    assert taskara.mode == Taskara.mode.TODO  # Default mode

def test_add_task_string(taskara):
    taskara.add_task("My first task", Taskara.mode.DEBUG)
    assert len(taskara.tasks) == 1

def test_add_task_object(taskara):
    taskara.add_task({"task": "Check this"}, Taskara.mode.TODO)
    assert len(taskara.tasks) == 1

    task_text = list(taskara.tasks)[0][1]
    assert task_text == json.dumps({"task": "Check this"}, indent=4)

def test_print_filtered_tasks(taskara, capsys):
    taskara.add_task("Task 1", Taskara.mode.DEBUG)
    taskara.add_task("Task 2", Taskara.mode.INFO)
    
    taskara.print(filter_mode=Taskara.mode.DEBUG)  # Print only DEBUG tasks

    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" not in captured.out  # Ensure other tasks are not printed

def test_format_task_from_object_dict(taskara):
    formatted = taskara._format_task_from_object({"key": "value"})
    assert formatted == json.dumps({"key": "value"}, indent=4)

def test_format_task_from_object_list(taskara):
    formatted = taskara._format_task_from_object(["item1", "item2"])
    assert formatted == "item1, item2"

def test_format_task_from_object_set(taskara):
    formatted = taskara._format_task_from_object({"item1", "item2"})
    assert formatted == "{item1, item2}" or formatted == "{item2, item1}"  # Sets are unordered

def test_format_task_from_object_other(taskara):
    formatted = taskara._format_task_from_object(12345)
    assert formatted == "12345"

if __name__ == "__main__":
    pytest.main()