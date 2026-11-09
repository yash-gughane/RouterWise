
from src.orchestrator.task import Task
from src.orchestrator.executor import DependencyExecutor


class TaskRunner:

    def __init__(self, executor: DependencyExecutor):
        self.executor = executor

    def execute_task(self, task: Task) -> str:
        """
        Simulate execution by a model.
        Real LLM calls will be integrated later.
        """

        print(f"Executing {task.task_id}: {task.description}")

        return (
            f"[SIMULATED {task.capability.upper()} OUTPUT] "
            f"Completed: {task.description}"
        )

    def run(self):

        while True:

            ready_tasks = self.executor.get_ready_tasks()

            if not ready_tasks:

                pending_tasks = [
                    task
                    for task in self.executor.tasks.values()
                    if task.status == "pending"
                ]

                if pending_tasks:
                    raise RuntimeError(
                        "Execution blocked: unresolved dependencies."
                    )

                break

            for task in ready_tasks:

                task.status = "running"

                try:
                    task.result = self.execute_task(task)
                    task.status = "completed"

                except Exception:
                    task.status = "failed"
                    raise

        print("\nAll tasks completed.")
