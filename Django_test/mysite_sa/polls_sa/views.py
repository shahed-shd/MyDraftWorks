from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, session


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

    # def get_queryset(self):
        # '''Excludes any questions that aren't published yet.'''
        # return session.query(Question).filter(Question.pub_date <= timezone.now())
        # return session.query(Question).filter(Question.id==pk)