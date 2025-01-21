from django.urls import path
from client.views import ProfileView

urlpatterns = [
    path('profiles/', ProfileView.as_view()),  # List and Create
    path('profiles/<int:pk>/', ProfileView.as_view()),  # Retrieve, Update, Delete
]
