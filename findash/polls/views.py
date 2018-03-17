from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list':latest_question_list,
    }
    # render instead of HttpResponse for a more simple function
    return render(request, 'polls/index.html',context)

def detail(request, question_id):
    # try question or raise a 404, decoupling even more model from view.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html',{'question':question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
