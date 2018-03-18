"""Model suite."""
from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    """Question Model"""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """print Question."""
        return self.question_text

    def was_published_recently(self):
        """Boolean for the question to appear in Index."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Choice Model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """print Choice."""
        return self.choice_text
