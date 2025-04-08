from django.conf import settings
from rest_framework.routers import DefaultRouter
from contacts.views import CompanyViewSet, ContactViewSet
from activities.views import ActivityViewSet, ContactActivitiesListView, TaskListView
from users.views import UserRegistrationView, UserLoginView, user_profile_view, PasswordChangeView
from reports import views as reports
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import CustomAPIRoot


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', CustomAPIRoot.as_view(), name='api-root'),
    path('api/', include('contacts.urls')),
    path('api/', include('activities.urls')),
    path('api/', include('reports.urls')),
    path('api/users/', include('users.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)