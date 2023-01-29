import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def board_news():
    news = []
    week_number_last = datetime.now().isocalendar()[1] - 2

    for post in Post.objects.filter(date__week=week_number_last).values(
            'title',
            'date',
            'text',
            'category'):
        info = ({post.get("date")}, {post.get("title")}, {post.get("text")}, {post.get("category")})
        news.append(info)

    users = User.objects.all()
    for user in users:
        html_content = render_to_string(
            'subscription_letter_weekly.html', {'user': user,
                                                'text': news,
                                                'week_number_last': week_number_last})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {user.username}! На нашем форуме появились новые объявления',
            from_email='kuber01@yandex.ru',
            to=[user.email]
        )

        if news:
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            board_news,
            trigger=CronTrigger(second="*/30"),
            id="board_news",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
