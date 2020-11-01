from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote():
                return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "Already closed. Can't vote!"))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "This poll does not exist."))
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=self.get_object()))

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return HttpResponseRedirect(reverse('polls:index'), messages.error("Poll closed already."))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "Didn't select choices.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

log = logging.getLogger("polls")
logging.basicConfig(level=logging.INFO)


def get_client_ip(request):
    """Get the client ip."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def update_choice_login(request, **kwargs):
    """Update the previous vote when login."""
    for question in Question.objects.all():
        question.previous_vote = str(request.user.vote_set.get(question=question).selected_choice)
        question.save()


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log info when user login."""
    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Login user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log info when user logout."""
    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Logout user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log info when the login failed."""
    ip = get_client_ip(request)
    date = datetime.now()
    log.warning('Login user(failed): %s , IP: %s , Date: %s', credentials['username'], ip, str(date))

@login_required()
def vote(request, question_id):
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {'question': question, 'error_message': "You didn't select a choice.", })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'selected_choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(selected_choice=choice).count()
            choice.save()
        for question in Question.objects.all():
            question.previous_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()
        date = datetime.now()
        log = logging.getLogger("polls")
        log.info("User: %s, Poll's ID: %d, Date: %s.", user, question_id, str(date))
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

