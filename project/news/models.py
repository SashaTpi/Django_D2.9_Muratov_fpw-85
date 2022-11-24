from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    ratingAuthor = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(CommentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscriber', blank=True) #'category', blank=True)

    def __str__(self):
        return self.name

    class Meta: #!!!!!
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name='Тип публикации')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
    #category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Категория')


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])
        # return reverse('post_detail', args=[str(self.id)])

    def message_subscriber(self):
        return f'Новая статья - "{self.title}" в разделе "{self.postCategory.first()}" '

    def __str__(self):
        return '{}'.format(self.title)


    # def date(self):
    #     return f'{self.dateCreation.strftime("%d. %m. %Y")}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-dateCreation']


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Публикация')
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return '{}'.format(self.categoryThrough.name)

    class Meta:
        verbose_name = 'Тип публикации'
        verbose_name_plural = 'Типы публикаций'

class Comment(models.Model): #..Comment
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.commentUser)

    def post_com(self):
        return f'Комментарий к статье:\n Дата: {self.dateCreation}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Коментарий: {self.text}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



