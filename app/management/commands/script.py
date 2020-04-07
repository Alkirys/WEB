from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app import models
from random import choice
from faker import Faker
import random

faker = Faker()


def add_vote(cnt, obj):
    authors_ids = list(models.Author.objects.values_list('id', flat=True))
    vote_list = list()
    if obj == "Question":
        q_set = models.Question.objects
        obj_type = models.ContentType.objects.get_for_model(models.Question)
        koef = 1
    else:
        q_set = models.Answer.objects
        obj_type = models.ContentType.objects.get_for_model(models.Answer)
        koef = cnt

    for i in range(cnt*koef):
        for j in range(cnt-10):
            vote = models.Vote(vote=random.choice([-1, 1]),
                               author_id=choice(authors_ids),
                               content_type=obj_type,
                               object_id=q_set.all()[i].id,
                               )
            # vote.save()
            vote_list.append(vote)
            # questions[i].rate.add(vote)
    models.Vote.objects.bulk_create(objs=vote_list)

    for i in range(cnt*koef):
        quest = q_set.filter(pk=i + 1)
        votes_set = models.Vote.objects.filter(object_id=i + 1, content_type=obj_type)
        for j in range(cnt-10):
            quest[0].vote.add(votes_set[j])


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)

    def add_people(self, cnt):
        user_list = list()
        author_list = list()
        for i in range(cnt):
            u = User(username=faker.name())
            user_list.append(u)
        User.objects.bulk_create(objs=user_list)

        users_set = User.objects.all()
        for i in range(cnt):
            author = models.Author(
                user=users_set[i],
                rating=faker.random_int(min=0, max=7),
            )
            author_list.append(author)
        models.Author.objects.bulk_create(objs=author_list)

    def add_tags(self, cnt):
        tag_list = list()
        for i in range(cnt):
            tag = models.Tag(
                title=faker.sentence()[:10],
            )
            tag_list.append(tag)
        models.Tag.objects.bulk_create(objs=tag_list)

    def add_questions(self, cnt):
        authors_set = models.Author.objects.all()
        tags_set = models.Tag.objects.all()
        answer_list = list()
        quest_list = list()
        for i in range(cnt):
            question = models.Question(
                author=choice(authors_set),
                title=faker.sentence()[:20],
                content=faker.sentence()[:50]
            )
            # question.save()
            quest_list.append(question)
        models.Question.objects.bulk_create(objs=quest_list)
        questions = models.Question.objects.all()

        add_vote(cnt, "Question")

        for i in range(cnt):
            questions[i].tags.add(choice(tags_set))
            questions[i].tags.add(choice(tags_set))
            for j in range(cnt):
                answer = models.Answer(
                    content=faker.sentence()[:50],
                    author=choice(authors_set),
                )
                answer.question = questions[i]
                answer_list.append(answer)
        models.Question.objects.update()
        models.Answer.objects.bulk_create(objs=answer_list)

        add_vote(cnt, "Answer")

    def handle(self, *args, **options):
        self.add_people(options.get('authors', 15))
        self.add_tags(options.get('tags', 15))
        self.add_questions(options.get('questions', 15))
