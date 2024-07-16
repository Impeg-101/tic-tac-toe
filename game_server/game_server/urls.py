"""
URL configuration for game_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from tic_tac_toe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/makePlayer', include(views.urls)),
    path("", views.index, name="index"),
    # path('api/create/', views.create_player),
    # path('api/find/', views.find_opponent),
    # path('api/join/', views.join_game),
    # path('api/leave/', views.leave_game),
    # path('api/move/', views.make_move),
    # path('api/undoStep', include(views.urls)),
] 