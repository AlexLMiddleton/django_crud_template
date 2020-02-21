from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', NewModelListView.as_view(), name='newmodel-list'),
    path('<int:pk>/', NewModelDetailView.as_view(), name='newmodel-detail'),
    path('new/', NewModelCreateView.as_view(), name='newmodel-create'),
    path('edit/<int:pk>/', NewModelUpdateView.as_view(), name='newmodel-edit'),
    path('delete/<int:pk>/', NewModelDeleteView.as_view(), name='newmodel-delete'),
]