# ref: https://www.youtube.com/watch?v=NoLF7Dlu5mc

from django.urls import path
from . import views

urlpatterns = [
    path('wordlists/', views.get_word_lists),
    path('loadwords/', views.load_words),
    path('checkguess/', views.guess_checker),
]