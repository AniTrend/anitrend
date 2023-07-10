import logging

from django_q.models import Task


def on_task_completed(task: Task):
    logger = logging.getLogger("django")
    logger.info(f"Hook trigger for `{task.func}` | {task.id}-{task.name} -> success: {task.success}")
