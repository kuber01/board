from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response


@receiver(post_save, sender=Response)
def response_notifications(sender, instance, created, **kwargs):
    if created:
        print('Письмо ушло получателю отклика')
        send_mail(
            subject='У вас новый отклик',
            message=f'На ваше объявление {instance.post.title} пришёл отклик от пользователя'
                    f'{instance.author.username}: {instance.text}',
            from_email='kuber01@yandex.ru',
            recipient_list=[f'{instance.post.author.email}']
        )
    else:
        print('Письмо ушло автору отклика')
        send_mail(
            subject='Отклик принят!',
            message=f'Ваш отклик на объявление {instance.post.title} был принят пользователем'
                    f'{instance.post.author}. Поздравляем!',
            from_email='kuber01@yandex.ru',
            recipient_list=[f'{instance.author.email}']
        )
