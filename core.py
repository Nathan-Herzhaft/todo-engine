from pathlib import Path

from structure import Project, Repo, SubTask, Task

# JSON save and load


def save_repo(repo: Repo, path: Path):
    with open(path, "w") as f:
        f.write(repo.model_dump_json())


def load_repo(path: Path):
    with open(path) as f:
        data = f.read()
    repo = Repo.model_validate_json(data)
    return repo


# Add methods


def add_subtask(task: Task, description: str, priority: int, duration: float = 0):
    task.subtasks.append(
        SubTask(
            description=description,
            priority=priority,
            duration=duration,
            parent_task=task.name,
            parent_project=task.parent_project,
        )
    )


def add_task(project: Project, name: str):
    project.tasks[name] = Task(name=name, parent_project=project.name)


def add_project(repo: Repo, name: str):
    repo.projects[name] = Project(name=name)


# Clear methods


def clear_subtask(task: Task, index: int):
    task.subtasks.pop(index)


def clear_task(project: Project, name: str):
    project.tasks.pop(name)


def clear_project(repo: Repo, name: str):
    repo.projects.pop(name)


# In-place modification methods


def modify_subtask(
    subtask: SubTask,
    description: str | None = None,
    priority: int | None = None,
    duration: float | None = None,
):
    if description:
        subtask.description = description
    if priority:
        subtask.priority = priority
    if duration:
        subtask.duration = duration
