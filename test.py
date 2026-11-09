from src.orchestrator.task import Task

task1 =  Task(
    task_id = 'T1',
    description = 'Explain diff between GD and SGD',
    capabilities = 'reasoning'
)

task2 = Task(
    task_id="T2",
    description="Implement GD and SGD using NumPy",
    capabilities="coding",
    dependencies=["T1"]
)
print(task1)
print(task2)