from django.urls import path

from .views import ListPostView, CreatePostView, UpdatePostView


urlpatterns = [
    path('', ListPostView.as_view()),
    path('create/', CreatePostView.as_view()),
    path('update/<int:pk>/', UpdatePostView.as_view())
]
