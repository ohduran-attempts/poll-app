"""View suite."""
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice


class IndexView(generic.ListView):
    """View for Index."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last 5 published questions.
        No future.
        """
        return Question.objects.filter(
                        pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """View for Detail."""

    model = Question
    template_name = 'polls/detail.html'  # overwrite the default template
    # expects primary key to be called 'pk', thus the view.py reflects that.

    def get_queryset(self):
        """Exclude questions in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """View for Results."""

    model = Question
    template_name = 'polls/results.html'  # overwrite the default template


# Needs to fix race condition
def vote(request, question_id):
    """View for Vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redirect to the question voting form.
        return render(request, 'polls/detail.html',
                      {'question': question,
                       'error_message': "You didn't select a choice!"})
    else:
        selected_choice.votes += 1
        selected_choice.save()  # save the choice on the database

        # Now redirect to the results
        return HttpResponseRedirect(
                        reverse('polls:results', args=(question.id,)))
