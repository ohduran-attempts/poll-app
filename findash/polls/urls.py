from django.urls import path
from . import views

# namespace will differentiate app urls from other app urls with the same name.
app_name= 'polls'
# paths within the app
urlpatterns = [
    # /polls
    path('',views.IndexView.as_view(), name='index'),
    # /polls/5
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),
    # /polls/5/results
    path('<int:pk>/results',views.ResultsView.as_view(), name='results'),
    # /polls/5/vote
    path('<int:question_id>/vote',views.vote, name='vote'),
]
