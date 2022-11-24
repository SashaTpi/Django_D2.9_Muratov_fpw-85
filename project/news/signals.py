# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.db.models. signals import m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
#
# from news.models import PostCategory
#
#
# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'subscribe_created',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pl}',
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content)
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers - [s.mail for s in subscribers]
#
#         send_notifications(instance.preiew(), instance.pk, instance.title, subscribers)

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category
from .views import sending_emails_to_subscribers


@receiver(post_save, sender=Post)
# описываем функцию сигнала и передаем экземпляр модели
def send_emails_on_signal(sender, created, instance, **kwargs):
    # запускаем функцию представление
    sending_emails_to_subscribers(instance)

# Функция обработчик для сигнала "post_save"
# создаём функцию обработчик с параметрами под регистрацию сигнала
# запускает выполнение кода при каком-либо действии пользователя, в нашем случае -
# сохранение в БД модели Post записи
# @receiver(post_save, sender=Post)
# def send_sub_mail(sender, instance, created, **kwargs):
#     global subscriber
#     sub_title = instance.title
#     sub_text = instance.text
#     category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).post_category.pk)
#     subscribers = category.subscribers.all()
#     post = instance
#
#     for subscriber in subscribers:
#         html_content = render_to_string(
#             'news/mail.html', {'user': subscriber, 'title': sub_title, 'text': sub_text[:50], 'post': post})
#
#         msg = EmailMultiAlternatives(
#             subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
#             from_email='kalosha21541@yandex.ru',
#             to=[subscriber.email]
#         )
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()
#     return redirect('/posts/')
