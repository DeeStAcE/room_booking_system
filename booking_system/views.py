from booking_system.models import Room
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'booking_system/main.html')


class NewRoom(View):
    def get(self, request):
        return render(request, 'booking_system/new_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        if not name:
            return HttpResponse('Enter a name of new room')

        if Room.objects.filter(name=name):
            return HttpResponse('The room already exists. Try different name')

        try:
            capacity = int(capacity)
        except ValueError:
            return HttpResponse('Capacity must be an integer greater than 0')
        if capacity <= 0:
            return HttpResponse('Capacity must be an integer greater than 0')

        if projector == 'on':
            projector = True
        else:
            projector = False

        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('main_page')


class AllRooms(View):
    def get(self, request):
        return render(request, 'booking_system/all_rooms.html', {'rooms': Room.objects.all()})


class DeleteRoom(View):
    def get(self, request, room_id):
        my_room = Room.objects.get(pk=int(room_id))
        my_room.delete()
        return redirect('all_rooms')


class EditRoom(View):
    def get(self, request, room_id):
        return render(request, 'booking_system/edit_room.html', {'room': Room.objects.get(pk=int(room_id))})

    def post(self, request, room_id):
        my_room = Room.objects.get(pk=int(room_id))
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        print(projector)

        if not name:
            return HttpResponse('Enter a name of new room')

        if not my_room.name == name:
            if Room.objects.filter(name=name):
                return HttpResponse('The room already exists. Try different name')

        try:
            capacity = int(capacity)
        except ValueError:
            return HttpResponse('Capacity must be an integer greater than 0')
        if capacity <= 0:
            return HttpResponse('Capacity must be an integer greater than 0')

        if projector == 'on':
            projector = True
        else:
            projector = False

        my_room.name = name
        my_room.capacity = capacity
        my_room.projector = projector
        my_room.save()

        return redirect('all_rooms')
