import logging

from django.utils import timezone
from django_q.models import Task, Schedule
from django_q.tasks import schedule


def on_start_workers_event(task: Task):
    """

    :param task:
    :return:
    """
    logger = logging.getLogger("django")
    logger.info(f"Hook trigger for `{task.func}` | {task.id}-{task.name} -> success: {task.success}")
    if task.success:
        try:
            _schedule = schedule(
                func="service.tasks.after_work_completed",
                hook="service.hooks.on_after_work_completed_event",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now().replace(minute=5)
            )
            logger.info(f"Scheduled new task `{_schedule.func}`")
        except Exception as e:
            logger.info(f"Failed to schedule relations tasks", exc_info=e)


def on_after_work_completed_event(task: Task):
    """

    :param task:
    :return:
    """
    logger = logging.getLogger("django")
    logger.info(f"Hook trigger for `{task.func}` | {task.id}-{task.name} -> success: {task.success}")
