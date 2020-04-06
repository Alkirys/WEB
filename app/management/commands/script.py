from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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
            u = User(username=faker.name())
            u.save()
            author = models.Author(
                user=u,
                name=faker.name(),
                password=faker.sentence()[:128],
            )
            author.save()

    def add_tags(self, cnt):
        for i in range(cnt):
            tag = models.Tag(
                title=faker.sentence()[:10],
                count=faker.random_int(min=0, max=7)
            )
            tag.save()

    def add_questions(self, cnt):
        authors_set = models.Author.objects.all()
        tags_set = models.Tag.objects.all()
        for i in range(cnt):
            question = models.Question(
                author=choice(authors_set),
                title=faker.sentence()[:20],
                content=faker.sentence()[:50])
            question.save()
            for j in range(cnt):
                answer = models.Answer(
                    content=faker.sentence()[:50],
                    author=choice(authors_set),
                )
                answer.question = question
                answer.save()
            question.save()
            question.tags.add(choice(tags_set))
            question.tags.add(choice(tags_set))
            question.save()

    def handle(self, *args, **options):
        self.add_people(options.get('authors', 25))
        self.add_tags(options.get('tags', 25))
        self.add_questions(options.get('questions', 25))
