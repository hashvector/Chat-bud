from django.shortcuts import render
from .models import Room


def index(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'core/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'core/room.html', context)