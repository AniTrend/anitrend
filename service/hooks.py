from django_q.models import Task
from di import MainContainer


def on_task_status_changed(task: Task):
    logging_utility = MainContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info(f"Task {task.name}:{task.id} status changed to {task.result}")
