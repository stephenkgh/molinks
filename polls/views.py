from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions that have been published """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    try:
        choice = q.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # go back to the form
        #return detail(request, question_id, error_message="You didn't select anything, dude.")
        return render(request, 'polls/detail.html', {
            'question': q,
            'error_message': "You didn't select a choice.",
        })
    else:
        choice.votes += 1
        choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


""" old version
def index(request):
    return render(request, 'polls/index.html', {
        'latest_question_list': Question.objects.order_by('-pub_date')[:5],
    })


def detail(request, question_id, error_message=None):
    q = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {
        'question': q,
        'choices': q.choice_set.all(),
        'error_message': error_message,
    })


def results(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/results.html', {
        'question': q,
        'choices': q.choice_set.all(),
    })
"""
