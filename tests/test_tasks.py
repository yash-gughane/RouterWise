import pytest
from src.routewise.tasks import Task, DependencyExecutor


def test_task_without_dependencies_is_ready():
    task = Task("T1", "first task", "fast")
    executor = DependencyExecutor([task])
    assert executor.get_ready_tasks() == [task]


def test_dependent_task_waits_until_dependency_completes():
    first = Task("T1", "first", "fast")
    second = Task("T2", "second", "fast", dependencies=["T1"])
    executor = DependencyExecutor([first, second])

    assert executor.get_ready_tasks() == [first]
    first.status = "completed"
    assert executor.get_ready_tasks() == [second]


def test_unknown_dependency_rejected():
    with pytest.raises(ValueError):
        DependencyExecutor([Task("T1", "first", "fast", dependencies=["missing"])])


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError):
        DependencyExecutor([
            Task("T1", "one", "fast"),
            Task("T1", "two", "fast"),
        ])
