
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
    path('level/<level>/solution/<key>', views.load_solution, name='load_solution'),
    path('level/<level>/run', views.run_solution, name='run_solution'),
    path('level/<level>/input', views.get_level_input, name='get_level_input'),
    path('input/alphabet/<alphabet>/count/<count>', views.gen_input, name='gen_input'),
    path('admin/', admin.site.urls),
]
