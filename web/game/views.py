from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import json
from CloneResourceMachine.Game import Game
from CloneResourceMachine.InputDetails import InputDetails

LEVEL_PATH = os.path.join(settings.CRM_PATH, 'levels/game.yaml')
# Create your views here.


def home(request):
    return HttpResponse('Hello, World!')


def load_level(request, level):
    game = Game(LEVEL_PATH)
    game.start_new(level, None)
    data = game.to_data()

    return HttpResponse(json.dumps(data))


def gen_input(request, alphabet, count):
    print(alphabet)
    inp = InputDetails({'alphabet': alphabet, 'count': int(count)})
    sample = inp.get_new_sample()

    return HttpResponse(json.dumps({'sample': sample}))


def get_level_input(request, level):
    game = Game(LEVEL_PATH)
    game.start_new(level, None)
    inp = game.current_level.input_details
    sample = inp.get_new_sample()

    return HttpResponse(json.dumps({'sample': sample}))


def load_solution(request, level, key):
    game = Game(LEVEL_PATH)
    game.start_new(level, None)
    prog = game.current_level.get_program(key)

    return HttpResponse(json.dumps({'program': prog.orig_data, 'labels': prog.labels}))

@csrf_exempt
def run_solution(request, level):
    print(f"body: {request.body}")
    print(f"post: {list(request.POST.items())}")

    return HttpResponse(json.dumps({}))




