from django_q.models import Task

from app.dependencies import AppContainer


def on_task_completed(task: Task):
    logging_utility = AppContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info(f"Hook trigger for `{task.func}` | {task.id}-{task.name} -> success: {task.success}")
