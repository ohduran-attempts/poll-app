"""Admin registry."""
from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):  # displayed as a table
    """Adding choices when creating a Question."""

    model = Choice
    extra = 2  # number of minimum choices


class QuestionAdmin(admin.ModelAdmin):
    """Question Admin class."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']

    # Change list
    list_display = ('question_text', 'pub_date', 'was_published_recently')


admin.site.register(Question, QuestionAdmin)
