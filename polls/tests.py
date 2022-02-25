import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    Create a question 'days' days in the future (negative for past)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        Appropriate message shown
        """
        r = self.client.get(reverse('polls:index'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "no_polls_message")
        self.assertQuerysetEqual(r.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions published in the past are shown
        """
        q = create_question(question_text="Past question.", days=-30)
        r = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            r.context['latest_question_list'],
            [q]
        )

    def test_future_question(self):
        """
        Questions published in the future are NOT shown
        """
        q = create_question(question_text="Future question.", days=30)
        r = self.client.get(reverse('polls:index'))
        self.assertContains(r, "no_polls_message")
        self.assertQuerysetEqual(r.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        """
        If future and past questions exist, only past ones are shown
        """
        q = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        r = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            r.context['latest_question_list'],
            [q],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        q1 = create_question(question_text="Past question 1.", days=-30)
        q2 = create_question(question_text="Past question 2.", days=-5)
        r = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            r.context['latest_question_list'],
            [q2, q1],
        )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for pub_date far enough in the past
        """
        fq = Question(pub_date = timezone.now() - datetime.timedelta(days=30))
        self.assertIs(fq.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for pub_date in the future
        """
        fq = Question(pub_date = timezone.now() + datetime.timedelta(days=30))
        self.assertIs(fq.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for pub_date from past day
        """
        fq = Question(pub_date = timezone.now() - datetime.timedelta(hours=12))
        self.assertIs(fq.was_published_recently(), True)
