from django.shortcuts import redirect, render
from django.template import context
from .models import Room
from .form import RoomForm

def index(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'core/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'core/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'core/room_form.html', context)



def editRoom(request, pk):
    room =Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form }
    return render(request, 'core/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj':room}
