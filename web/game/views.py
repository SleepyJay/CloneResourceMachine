from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
from CloneResourceMachine.Game import Game


# Create your views here.


def home(request):
    return HttpResponse('Hello, World!')


def load_level(request, level):
    level_path = os.path.join(settings.CRM_PATH, 'levels/game.yaml')
    game = Game()
    game.load_multi_level_file(level_path)
    game.start_new(level, None)

    print(request)

    return HttpResponse(f'Level {level} Loaded? "{game.current_level.name}" ({settings.CRM_PATH})')

