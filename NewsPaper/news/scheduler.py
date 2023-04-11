from django.conf import settings

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from .tasks import check_new_posts


# Декоратор `close_old_connections` гарантирует, что соединения с базой данных, которые стали непригодны для
# использования или устарели, закрываются до и после выполнения вашего задания. Вы должны использовать это, чтобы
# обернуть любые запланированные вами задания, которые каким-либо образом обращаются к базе данных Django.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет из базы данных записи выполнения задания APScheduler старше `max_age`.
    Это помогает предотвратить заполнение базы данных устаревшими ненужными записями.
    :param max_age: Максимальный промежуток времени для сохранения записей о выполнении задания.
                    Значение по умолчанию равно 7 дням.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def create_scheduler():
    logger = logging.getLogger(__name__)

    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # добавляем работу нашему задачнику
    scheduler.add_job(
        check_new_posts,
        trigger=CronTrigger(day_of_week='tue', hour='17', minute='00'),
        id="check_new_posts_for_weekly_notification",  # "Идентификатор", присвоенный каждому заданию, должен быть уникальным
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'my_job'.")
    print("Added job 'my_job'.")

    # Каждый понедельник в 00:00 будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job: 'delete_old_job_executions'.")
    print("Added weekly job: 'delete_old_job_executions'.")

    return {'logger': logger, 'scheduler': scheduler}
