from datetime import datetime

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@shared_task
def mailing():
    print('It went on!')
    news = []
    week_number_last = datetime.now().isocalendar()[1] - 2
#date__week=week_number_last
    for post in Post.objects.filter().values(
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
