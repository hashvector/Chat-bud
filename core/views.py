from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Message, Room, Topic
from .form import RoomForm


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "User name or password does not exist")

    context = {'page':page}
    return render(request, 'core/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

def registerUser(request):
    form = UserCreationForm()
    context = {'form':form}

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        
        else:
            messages.error(request, 'An Error occured during the registration')

    return render(request, 'core/login_register.html', context)

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else  ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = f"{rooms.count()} rooms available" if rooms.count() > 1 else f'{rooms.count()} room available'
    topics = Topic.objects.all()
    room_messages = Message.objects.all()

    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages': room_messages,
        }
    return render(request, 'core/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            host = request.user,
            body = request.POST.get('body'),
            room = room,
        )
        room.participants.add(request.user)
        return redirect('room', room.id)    
    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'core/room.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'core/room_form.html', context)


@login_required(login_url='login')
def editRoom(request, pk):
    room =Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form }
    return render(request, 'core/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    context = {'object': room}
    if request.method == 'POST':
        room.delete()
        return redirect('index')

    return render(request, 'core/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
   
    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)

    context = {'object': message}
    return render(request, 'core/delete.html', context)
