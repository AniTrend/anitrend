from django_q.models import Task
from di import MainContainer


def on_poll_from_xem_event(task: Task):
    """

    :param task:
    :return:
    """
    logging_utility = MainContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info(f"Task `get_all_data_from_xem` ({task.name}:{task.id}) status changed to {task.result}")


def on_poll_from_relations_event(task: Task):
    """

    :param task:
    :return:
    """
    logging_utility = MainContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info(f"Task `get_all_data_from_relations` ({task.name}:{task.id}) status changed to {task.result}")
