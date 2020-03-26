from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


questions = {
   i: {'id': i, 'title': f'Question # {i}', 'tags': ['first_tag', 'second_tag']}
   for i in range(1, 5)
}
questions[5] = {'id': 5, 'title': f'Question # {5}', 'tags': ['Python', 'MySQL']}

answers = {
   i: {'id': i, 'title': f'Answer # {i}'}
   for i in range(1, 4)
}


def all_questions(request):
   return render(request, 'all_questions.html', {
      'nickname': 'Alex',
      'questions': questions.values(),
   })

def hot_questions(request):
   return render(request, 'hot_questions.html', {
      'nickname': 'Alex',
      'questions': questions.values(),
   })

def question(request, qid):
   question = questions.get(qid)
   return render(request, 'question.html', {
   'nickname': 'Alex',
   'questions': question,
   'answers': answers.values(),
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

   return render(request, 'tag.html', {
   'temp_tag': tag_name,
   'questions': render_questions.values(),
})

