from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, User
import datetime as DT

from datetime import datetime, timedelta
from backports.zoneinfo import ZoneInfo
from django.core.mail import send_mail


MSC = datetime(2022, 1,  1,  tzinfo=ZoneInfo("Europe/Moscow"))

@shared_task
def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week_ago = today - DT.timedelta(days=7)
    week = timedelta(days=7)
    # print(today)
    # print(week_ago)
    # print(week)

    for category in categories:
        # subscribers_emails = category.subscribers.all().values('email')
        # print(subscribers_emails)

        category_subscribers = category.subscribers.all()

        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(postCategory=f'{category.id}')

        for post in posts_in_category:
            # print(post.pubDate)
            time_delta = DT.datetime.now().replace(MSC) - post.pubDate
            # days_delta = today - post.pubDate
            if time_delta < week:
                weekly_posts_in_category.append(post)
                print(f'Дата публикации: {post.pubDate}')
                print(f'Дельта: {time_delta}')
                print('----------------   ---------------')

        print(f'ID: {category.id}')
        print(category)
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email='testpostnoname@yandex.ru',
                to=category_subscribers_emails,
            )

            html_content = render_to_string(
                'weekly_digest.html',
                {
                    'digest': weekly_posts_in_category,
                    'category': category,
                }
            )

            msg.attach_alternative(html_content, "text/html")

            msg.send()
        else:
            continue

@shared_task
def post_now():
    for cat_id in Post.objects.get(pk=id).postCategory.all():
        users = Category.objects.filter(name=cat_id).values("subscribers")
        for user_id in users:
            send_mail(
                subject=f"{Post.objects.get(pk=id).title}",
                message=f"Привет, {User.objects.get(pk=user_id['subscribers']).username}. \n Новая статья в твоём любимом разделе! \n Заголовок : {Post.objects.get(pk=id).title} \n Текст : {Post.objects.get(pk=id).text[:50]} \n Ссылка на статью: http://127.0.0.1:8000/posts/{id}",
                from_email='testpostnoname@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )

