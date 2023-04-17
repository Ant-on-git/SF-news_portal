from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Post, User
from django.conf.global_settings import DEFAULT_FROM_EMAIL


def send_new_post_email(username, email, title, text, id):
    html_email_message = render_to_string('email/new_post_email_notification.html',
                                          {'username': username, 'title': title, 'text': text, 'href': f'http://127.0.0.1:8000/{id}'})
    msg = EmailMultiAlternatives(
        subject=title,
        body=text,
        from_email=DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print('ошибка при отправке письма. возможно, ЯНДЕКС\РАМБЛЕР ПОСЧИТАЛ ПИСЬМО ЗА СПАМ и заблокировал почту на 24 часа')
        print(e)


@receiver(m2m_changed, sender=Post.category.through)  # на сайте объясняется через post_save - срабатывает при сохранении поста. НО, ОКАЗЫВАЕТСЯ ЭТО НЕ РАБОТАЕТ ПРИ СВЯЗЯХ manyToMany. ПОТОМУ ОБЪЯСНЕНИЕ САЙТА ИДЕТ НАХРЕН. ДЛЯ отслеживания m2m нужно использовать m2m_changed
def notify_subscribers_new_post(sender, instance, action, **kwargs):  #  instance - только что измененный объект
    if action == 'post_add':
        id = instance.id
        title = instance.title
        text = instance.text[:50]
        subscribers_data = dict()
        for category in instance.category.all():
            subscribers = category.subscribers.all()
            for user in subscribers:
                if user.username not in subscribers_data:
                    subscribers_data[user.username] = user.email
        for username, email in subscribers_data.items():
            send_new_post_email(username, email, title, text, id)


@receiver(post_save, sender=User)
def notify_subscribers_new_post(sender, instance, created, **kwargs):
    html_email_message = render_to_string('email/hi_new_user.html',
                                          {'username': instance.username, 'href': 'http://127.0.0.1:8000'})
    msg = EmailMultiAlternatives(
        subject=f'newspaper.com приветствует тебя, {instance.username}',
        from_email=DEFAULT_FROM_EMAIL,
        to=[instance.email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print('ошибка при отправке письма. возможно, ЯНДЕКС\РАМБЛЕР ПОСЧИТАЛ ПИСЬМО ЗА СПАМ и заблокировал почту на 24 часа')
        print(e)