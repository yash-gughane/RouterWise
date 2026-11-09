from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    task_id: str
    description: str
    capabilities: str

    dependencies: list[str] = field(default_factory=list)

    status: str = "pending"

    result: Optional[str] = None
