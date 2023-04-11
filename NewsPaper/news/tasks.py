# задачи для scheduler.py (apscheduler)
from .models import Post
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



def send_week_posts_mail(user, post_list):
    html_email_message = render_to_string('email/week_posts_updates.html',
                                          {'username': user.username, 'post_list': post_list})
    msg = EmailMultiAlternatives(
        subject='Новые посты за неделю на newspaper.com',
        from_email='17smile17@rambler.ru',
        to=[user.email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print('ошибка при отправке письма. возможно, ЯНДЕКС\РАМБЛЕР ПОСЧИТАЛ ПИСЬМО ЗА СПАМ и заблокировал почту на 24 часа')
        print(e)


def check_new_posts():
    week_posts = Post.objects.filter(datetime_create__gte=timezone.now()-timedelta(days=7))
    week_posts_recipients = {}
    for post in week_posts:
        for category in post.category.all():
            for user in category.subscribers.all():
                if user in week_posts_recipients.keys() and post not in week_posts_recipients[user]:
                    week_posts_recipients[user].append(post)
                else:
                    week_posts_recipients[user] = [post]
    for user, post_list in week_posts_recipients.items():
        send_week_posts_mail(user, post_list)
    print('end of check_new_posts')


