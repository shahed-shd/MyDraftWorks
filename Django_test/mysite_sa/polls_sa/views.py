import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, session


class IndexView(generic.ListView):
    template_name = 'polls_sa/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        '''Returns the last five published questions.'''
        return session.query(Question).filter(Question.pub_date <= timezone.now()).all()[:5]


class DetailView(generic.DetailView):
    template_name = 'polls_sa/detail.html'
    context_object_name = 'object'

    def get_object(self, *args, **kwargs):
        x = self.kwargs.get('question_id')
        instance = session.query(Question).filter_by(id=x).one()
        return instance


class ResultsView(generic.DetailView):
    context_object_name = 'object'
    template_name = 'polls_sa/results.html'

    def get_queryset(self):
        return session.query(Question).all()

    def get_object(self, *args, **kwargs):
        x = self.kwargs.get('question_id')
        instance = session.query(Question).filter_by(id=x).one()
        return instance


def add_question_view(request):
    template_name = 'polls_sa/add_question.html'
    return render(request, template_name)


def add_question(request):
    question_text = request.POST['question_text']
    pub_date = request.POST['pub_date']
    pub_time = request.POST['pub_time']

    choice_texts = request.POST['choice_texts']
    choice_text_list = choice_texts.split('\n')
    choice_text_list = [x.strip() for x in choice_text_list]

    question = Question()
    question.question_text = question_text
    try:
        question.pub_date = datetime.datetime.strptime("{} {}".format(pub_date, pub_time), "%Y-%m-%d %H:%M")
    except:
        question.pub_date = timezone.now()

    for x in choice_text_list:
        choice = Choice()
        choice.choice_text = x
        choice.votes = 0
        question.choices.append(choice)

    session.add(question)
    session.commit()

    print("HERE Q:", question)

    return HttpResponseRedirect(reverse('polls_sa:index'))


def vote(request, question_id):
    question = session.query(Question).filter_by(id=question_id)

    try:
        choice_id = int(request.POST['choice'])
        selected_choice = session.query(Choice).filter_by(question_id=question_id).filter_by(id=choice_id).one()
    except:
        # Redisplay the question voting form.
        return render(request, 'polls_sa/detail.html', {
            'object': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        session.commit()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls_sa:results', args=(question_id,)))
