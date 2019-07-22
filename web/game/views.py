from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import json
from CloneResourceMachine.Game import Game


# Create your views here.


def home(request):
    return HttpResponse('Hello, World!')


def load_level(request, level):
    level_path = os.path.join(settings.CRM_PATH, 'levels/game.yaml')
    game = Game(level_path)
    game.start_new(level, None)

    data = game.to_data()

    return HttpResponse(json.dumps(data))


def gen_input(request, alphabet, count):
    pass

