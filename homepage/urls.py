from django.urls import path, include

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('__debug__/', include('debug_toolbar.urls')),
]