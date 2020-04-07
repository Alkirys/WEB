from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from datetime import datetime
from django.db.models import Sum


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Тэг", unique=True, primary_key=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/")
    rating = models.IntegerField()

    def __str__(self):
        return self.user.name


class VoteManager(models.Manager):
    use_for_related_fields = True

    def get_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)


class Vote(models.Model):
    votes = ((1, 'like'), (-1, 'dislike'))
    vote = models.IntegerField(choices=votes, verbose_name=u"Голосование")
    name = models.CharField(max_length=255, verbose_name=u"Пользователь")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_obj = GenericForeignKey()

    objects = VoteManager()


class QuestionManager(models.Manager):
    def by_tag(self, tag):
        return self.filter(tags__title=tag)

    def most_popular(self):
        return self.order_by('-author__rating')


class Question(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=u"Заголовок вопроса")
    content = models.TextField(verbose_name=u"Текст вопроса")
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Опубликован ли вопрос")
    tags = models.ManyToManyField(Tag, blank=True)
    rate = GenericRelation(Vote, related_query_name=u'Question')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"


class Answer(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"Текст ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время ответа")
    rate = GenericRelation(Vote, related_query_name=u'Answer')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"
