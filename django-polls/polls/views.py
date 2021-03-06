from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render 
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset_rev(self):
        return Question.objects.order_by('-pub_date').reverse()[1:]

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def summary(request):

    summary = {}
    for choice in Choice.objects.all():
        q_text = choice.question.question_text
        c_text = choice.choice_text
        votes = choice.votes
        if not q_text in summary.keys():
            summary[q_text] = {c_text: votes}
        else:
            summary[q_text][c_text] = votes
    return render(request, 'polls/summary.html', {
        'summary': summary
    })


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message' :"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
