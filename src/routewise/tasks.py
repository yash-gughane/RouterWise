from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    task_id: str
    description: str
    capability: str
    dependencies: list[str] = field(default_factory=list)
    status: str = "pending"
    result: Optional[str] = None
    attempts: int = 0
    max_retries: int = 1


class DependencyExecutor:
    \"\"\"Stores tasks and identifies pending tasks whose dependencies completed.\"\"\"

    def __init__(self, tasks: list[Task]):
        self.tasks = {task.task_id: task for task in tasks}
        if len(self.tasks) != len(tasks):
            raise ValueError("Task IDs must be unique.")

        for task in tasks:
            for dependency in task.dependencies:
                if dependency not in self.tasks:
                    raise ValueError(f"Unknown dependency: {dependency}")
                if dependency == task.task_id:
                    raise ValueError(f"Task {task.task_id} cannot depend on itself.")

    def get_ready_tasks(self) -> list[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status != "pending":
                continue
            if all(self.tasks[dep].status == "completed" for dep in task.dependencies):
                ready.append(task)
        return ready

    def has_pending_tasks(self) -> bool:
        return any(task.status == "pending" for task in self.tasks.values())
