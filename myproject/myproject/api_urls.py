from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('', include('articles.urls')),
    path('', include('books.urls')),
]