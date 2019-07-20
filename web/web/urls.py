"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from game import views

# GET level/<level> => load a level (with an empty program)
# GET level/<level>/input => generate new input
# POST leve/<level>/run => send program to level, run it, return results
# GET level/<level>/solution/<sol_name> => load a named solution
# ... more later ...

urlpatterns = [
    path('', views.home, name='home'),
    path('level/<level>', views.load_level, name='load_level'),
    path('admin/', admin.site.urls),
]
