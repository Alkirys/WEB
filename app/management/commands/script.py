from django.core.management.base import BaseCommand
from app import models
from random import choice
from faker import Faker

faker = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)

    def add_people(self, cnt):
        for i in range(cnt):
            u = models.User(username=faker.name())
            u.save()
            author = models.Author(
                name=faker.name()
            )
            author.save()

    def add_tags(self, cnt):
        for i in range(cnt):
            tag = models.Tag(
                title=faker.sentence()[:15],
                count=faker.random_int(min=0, max=5)
            )
            tag.save()

    def add_questions(self, cnt):
        for i in range(cnt):
            question = models.Question(
                author=choice(models.Author.objects.all()),
                title=faker.sentence()[:20],
                content=faker.sentence()[:50])
            question.save()
            for j in range(cnt):
                answer = models.Answer(
                    content=faker.sentence()[:50],
                    author=choice(models.Author.objects.all()),
                )
                answer.question = question
                answer.save()
            question.save()
            question.tags.add(choice(models.Tag.objects.all()))
            question.save()

    def handle(self, *args, **options):
        self.add_people(options.get('authors', 25))
        self.add_tags(options.get('tags', 25))
        self.add_questions(options.get('questions', 25))

