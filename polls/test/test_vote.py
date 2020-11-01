from unittest import TestCase
from polls.models import Question
from django.utils import timezone
import datetime

class TestVoteAndPublished(TestCase):
    def test_is_published(self):
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertTrue(question.is_published())

    def test_is_published_with_not_published_question(self):
        end_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=end_time)
        self.assertFalse(question.is_published())

    def test_can_vote(self):
        pub_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertTrue(question.can_vote())

    def test_can_vote_after_question(self):
        pub_time = timezone.now() - datetime.timedelta(days=2)
        end_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.can_vote())

    def test_can_vote_before_question(self):
        pub_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertFalse(question.can_vote())