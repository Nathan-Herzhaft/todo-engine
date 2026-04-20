import pickle
from pathlib import Path
from typing import Self


class Todo:
    priority: int
    description: str
    overall_task: str | None

    def __init__(
        self, priority: int, description: str, overall_task: str | None = None
    ):
        self.id = id
        self.priority = priority
        self.description = description
        self.overall_task = overall_task

    def change_description(self, description: str):
        self.description = description

    def change_overall_task(self, overall_task: str):
        self.overall_task = overall_task


class Project:
    todo_list: dict[int:Todo]
    name: str

    def __init__(self, name: str):
        self.todo_list = {}

    def add_todo(
        self, priority: int, description: str, overall_task: str | None = None
    ):
        id = 0
        while any(self.todo_list.keys() == id):
            id += 1
        todo = Todo(
            id=id,
            priority=priority,
            description=description,
            overall_task=overall_task,
        )
        self.todo_list[id] = todo

    def close_todo(self, id: int):
        self.todo_list.pop(id)


class GlobalEngine:
    projects: list[Project]

    def __init__(self):
        self.projects = {}

    def new_project(self, name: str):
        self.projects[name] = Project(name)

    def close_project(self, name: str):
        self.projects.pop(name)

    def save_to_pkl(self, path: str | Path):
        with open(path, "wb") as f:
            pickle.dump(path, f)

    @classmethod
    def init_from_saved_file(cls, path: str | Path) -> Self:
        with open(path, "rb") as f:
            loaded = pickle.load(f)
        return loaded
