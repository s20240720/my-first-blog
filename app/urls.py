from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book/<int:pk>/', views.bookdetail, name='book_detail'),
    path('book/<int:pk>/', views.requestlibrarydata, name='requestlibrarydata'),
    path('register/author/', views.RegisterAuthorView.as_view(), name='registerauthor'),
    path('register/book/', views.RegisterBookView.as_view(), name='registerbook'),
    path('writing/log/', views.WritingLogView.as_view(), name='writinglog'),
    path('update/log/<int:pk>/', views.UpdateLogView.as_view(), name='updatelog'),
    path('update/book/<int:pk>/', views.UpdateBookView.as_view(), name='updatebook'),
    path('delete/log/<int:pk>/', views.deletelog, name='deletelog'),
    path('delete/book/<int:pk>/', views.deletebook, name='deletebook'),
    path('writing/thisbooklog/<int:book_id>', views.writingthisbooklog, name='writingthisbooklog'),
]