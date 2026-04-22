from pathlib import Path
from typing import Self

from pydantic import (
    BaseModel,
)


class SubTask(BaseModel):
    description: str
    priority: int
    duration: float

    def modify(
        self,
        description: str | None = None,
        priority: int | None = None,
        duration: float | None = None,
    ):
        if description:
            self.description = description
        if priority:
            self.priority = priority
        if duration:
            self.duration = duration


class Task(BaseModel):
    name: str
    subtasks: dict[str, SubTask] = {}

    # Self properties

    def rename(self, name: str):
        self.name = name

    @property
    def duration(self) -> float:
        return sum(subtask.duration for subtask in self.subtasks.values())

    # SubTask Management

    def rename_subtask(self, old_description: str, new_description: str):
        subtask = self.subtasks.pop(old_description)
        subtask.modify(new_description)
        self.subtasks[new_description] = subtask

    def get_subtask(self, subtask_description: str) -> SubTask:
        return self.subtasks.get(subtask_description)

    def add_subtask(self, description: str, priority: int, duration: float = 0):
        self.subtasks[description] = SubTask(
            description=description,
            priority=priority,
            duration=duration,
        )

    def clear_subtask(self, description: str):
        self.subtasks.pop(description)


class Project(BaseModel):
    name: str
    tasks: dict[str, Task] = {}

    # Self properties

    @property
    def duration(self) -> float:
        return sum(task.duration for task in self.tasks.values())

    def rename(self, name: str):
        self.name = name

    # Task Management

    def get_task(self, task_name: str) -> Task:
        return self.tasks.get(task_name)

    def add_task(self, name: str):
        self.tasks[name] = Task(name=name)

    def clear_task(self, name: str):
        self.tasks.pop(name)

    # Retrieval

    def subtasks(self, priority: int | None = None) -> list[tuple[Task, SubTask]]:
        return_list: list[tuple[Task, SubTask]] = []

        for task in self.tasks.values():
            list_subtasks = [(task, subtask) for subtask in task.subtasks.values()]
            return_list += list_subtasks

        if priority:
            return_list = [
                (task, subtask)
                for task, subtask in return_list
                if subtask.priority == priority
            ]

        return return_list


class Repo(BaseModel):
    projects: dict[str, Project] = {}

    # Self properties

    @property
    def duration(self):
        return sum(project.duration for project in self.projects.values())

    # Project Management

    def get_project(self, project_name: str) -> Project:
        return self.projects.get(project_name)

    def add_project(self, name: str):
        self.projects[name] = Project(name=name)

    def clear_project(self, name: str):
        self.projects.pop(name)

    # Retrieval

    def subtasks(
        self, priority: int | None = None
    ) -> list[tuple[Project, Task, SubTask]]:
        return_list: list[tuple[Project, Task, SubTask]] = []

        for project in self.projects.values():
            return_list += [
                (project, task, subtask)
                for task, subtask in project.subtasks(priority=priority)
            ]
        return return_list

    # JSON association

    def save(self, path: Path):
        with open(path, "w") as f:
            f.write(self.model_dump_json())

    @classmethod
    def load(cls, path: Path) -> Self:
        with open(path) as f:
            data = f.read()
        repo = Repo.model_validate_json(data)
        return repo
