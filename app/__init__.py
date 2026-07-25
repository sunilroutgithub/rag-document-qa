import pytest

def test_task1() -> None:
    """Test task1 function.

    Returns:
        None
    """
    task1()
    assert True

def test_task2() -> None:
    """Test task2 function.

    Returns:
        None
    """
    task2("Task 2", "This is task 2")
    assert True

def test_task_class() -> None:
    """Test Task class.

    Returns:
        None
    """
    task = Task("Task 3", "This is task 3")
    task.execute()
    assert task.get_status() == "Completed"
