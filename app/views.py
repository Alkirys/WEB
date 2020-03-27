from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


questions = {
   i: {'id': i, 'title': f'Question # {i}', 'tags': ['first_tag', 'second_tag']}
   for i in range(1, 26)
}
questions[5] = {'id': 5, 'title': f'Question # {5}', 'tags': ['Python', 'MySQL']}

answers = {
   i: {'id': i, 'title': f'Answer # {i}'}
   for i in range(1, 4)
}


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
   pagData = paginate(questions.values(), request)
   return render(request, 'all_questions.html', {
      'questions': pagData,
   })

def hot_questions(request):
   pagData = paginate(questions.values(), request)
   return render(request, 'hot_questions.html', {
      'nickname': 'Alex',
      'questions': pagData,
   })

def question(request, qid):
   pagData = paginate(answers.values(), request)
   question = questions.get(qid)
   return render(request, 'question.html', {
   'nickname': 'Alex',
   'questions': question,
   'answers': pagData,
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
   render_questions = {}
   for question in questions.values():
      for tag in question.get('tags'):
         if tag_name == tag:
            render_questions[question.get('id')] = question
            continue

   pagData = paginate(render_questions.values(), request)

   return render(request, 'tag.html', {
   'temp_tag': tag_name,
   'questions': pagData,
})

