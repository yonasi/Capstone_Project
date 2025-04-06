from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contacts/<int:id>/activities/', views.ContactActivitiesListView.as_view(), name='contact-activities-list'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'), #created on april6
]