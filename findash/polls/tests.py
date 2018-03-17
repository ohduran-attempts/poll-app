"""Test suite."""
from django.test import TestCase
from django.urls import reverse
import datetime
from django.utils import timezone
from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given text, and
    published the given number of days offset to now (negative for past).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Test Cases."""

    def test_was_published_recently_with_question_in_future(self):
        """
        was_published_recently().
        It must return false for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertFalse(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was was_published_recently().
        It must return True for questions whose pub_date is within the day.
        """
        time = timezone.now() - datetime.timedelta(
                                    hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """Index View Question Tests."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        # API response is OK
        self.assertEqual(response.status_code, 200)
        # A message is included
        self.assertContains(response, "No polls are available.""")
        # Context is an empty list
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are on index."""
        # Create a question in the past
        create_question(question_text="Past question.", days=-30)
        # Get the response when I call the index view
        response = self.client.get(reverse('polls:index'))
        # The question is in there
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>'])

    def test_future_question(self):
        """Questions with a pub_date in the future are NOT on index."""
        # Create a question in the future
        create_question(question_text="Future question.", days=30)
        # Get the response when I call the index view
        response = self.client.get(reverse('polls:index'))
        # The response includes the 'not available message'
        self.assertContains(response, "No polls are available.")
        # Context is an empty list
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        """
        Even if both past and future questions exist,
        only past questions are displayed.
        """
        # Create a past and a future question
        create_question(question_text="Future question.", days=30)
        create_question(question_text="Past question.", days=-30)
        # Get the response when I call the index view
        response = self.client.get(reverse('polls:index'))
        # Only the past question is in there
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>'])

    def test_multiple_past_questions(self):
        """Index must display multiple questions."""
        # Create two questions in the past
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-31)
        # Get the response when I call the index view
        response = self.client.get(reverse('polls:index'))
        # All past questions are there
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 1.>', '<Question: Past question 2.>']
        )


class QuestionDetailViewTests(TestCase):
    """Detail View Questions Tests."""

    def test_future_question(self):
        """Details for a future question return 404."""
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Details for a future question are shown."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text
