from django.core.management.base import BaseCommand
from app import models
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = models.User(username=f.name())
            u.save()
            author = models.Author(
                name=f.name()
            )
            author.save()

    def fill_tags(self, cnt):
        for i in range(cnt):
            tag = models.Tag(
                title=f.sentence()[:128],
                count=f.random_int(min=0, max=10)
            )
            tag.save()

    def fill_questions(self, cnt):
        for i in range(cnt):
            q = models.Question(
                author=choice(models.Author.objects.all()),
                title=f.sentence()[:28],
                content=f.sentence()[:46],
            )
            q.save()
            for k in range(cnt):
                answ = models.Answer(
                    content=f.sentence()[:46],
                    author=choice(models.Author.objects.all()),
                )
                answ.question = q
                answ.save()
            q.save()
            q.tags.add(choice(models.Tag.objects.all()))
            q.save()

    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 15))
        self.fill_tags(options.get('tags', 15))
        self.fill_questions(options.get('questions', 15))