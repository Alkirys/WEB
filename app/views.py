from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app import models


def paginate(objects_list, request):
    try:
        paginator = Paginator(list(objects_list), 5)
    except ValueError:
        paginator = list()

    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)

    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def all_questions(request):
    quest = models.Question.objects.all()
    pag_data = paginate(quest, request)
    return render(request, 'all_questions.html', {
        'questions': pag_data,
    })


def hot_questions(request):
    quest = models.Question.objects.most_popular()
    pag_data = paginate(quest, request)
    return render(request, 'hot_questions.html', {
        'nickname': 'Alex',
        'questions': pag_data,
    })


def question(request, qid):
    #quest = models.Question.objects.get(pk=qid)
    quest = get_object_or_404(models.Question, pk=qid)
    ans = quest.answer_set.all()
    pag_data = paginate(ans, request)
    return render(request, 'question.html', {
        'nickname': 'Alex',
        'questions': quest,
        'answers': pag_data,
    })


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {
        'nickname': 'Alex',
    })


def ask(request):
    return render(request, 'ask.html', {
        'nickname': 'Alex',
    })


def tag(request, tag_name):
    #quest = models.Question.objects.by_tag(tag_name)
    quest = get_list_or_404(models.Question, tags=tag_name)
    pag_data = paginate(quest, request)

    return render(request, 'tag.html', {
        'temp_tag': tag_name,
        'questions': pag_data,
    })
