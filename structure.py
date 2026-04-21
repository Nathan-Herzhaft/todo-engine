from pydantic import (
    BaseModel,
)


class SubTask(BaseModel):
    # properties
    description: str
    priority: int
    duration: float

    # arborescence
    parent_task: str
    parent_project: str


class Task(BaseModel):
    name: str
    subtasks: list[SubTask] = []
    parent_project: str

    @property
    def priority(self):
        return sum(subtask.priority for subtask in self.subtasks)

    @property
    def duration(self):
        return sum(subtask.duration for subtask in self.subtasks)


class Project(BaseModel):
    name: str
    tasks: dict[str, Task] = {}

    @property
    def priority(self):
        return sum(task.priority for task in self.tasks.values())

    @property
    def duration(self):
        return sum(task.duration for task in self.tasks.values())

    def get_subtasks(self, priority: int | None) -> list[SubTask]:
        return_list: list[SubTask] = []

        for task in self.tasks.values():
            return_list += task.subtasks

        if priority:
            return_list = [
                subtask for subtask in return_list if subtask.priority == priority
            ]

        return return_list


class Repo(BaseModel):
    projects: dict[str, Project] = {}

    @property
    def priority(self):
        return sum(project.priority for project in self.projects.values())

    @property
    def duration(self):
        return sum(project.duration for project in self.projects.values())

    def get_tasks(self) -> list[Task]:

        return_list: list[Task] = []

        for project in self.projects.values():
            return_list += project.tasks.values()

        return return_list

    def get_subtasks(self, priority: int | None = None) -> list[SubTask]:
        return_list: list[SubTask] = []

        for project in self.projects.values():
            return_list += project.get_subtasks(priority=priority)
        return return_list
