
import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class AuthenticationTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user("Phumrapee", email="phumrapee.c@ku.th", password="123456")
        user.first_name = "Sahanon"
        user.last_name = "Chaowanapricha"
        user.save()

    def test_login(self):
        self.client.login(username="Phumrapee", password="123456")
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 200)
        self.assertContains(respone, "Phumrapee")

    def test_logout(self):
        self.client.login(username="Phumrapee", password="123456")
        self.client.logout()
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertNotContains(respone, "Phumrapee")

    def test_authenticate_vote(self):
        self.client.login(username="Phumrapee", password="123456")
        question = create_question(question_text='This is a question', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)