from booking_system.models import Room, RoomReservation
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from datetime import date


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'booking_system/main.html')


class NewRoom(View):
    def get(self, request):
        return render(request, 'booking_system/new_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector') == 'on'

        if not name:
            return HttpResponse('Enter a name of new room')

        if Room.objects.filter(name=name):
            return HttpResponse('The room already exists. Try different name')

        if capacity <= 0:
            return HttpResponse('Capacity must be greater than 0')

        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('main_page')


class AllRooms(View):
    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = date.today() in reservation_dates
        return render(request, 'booking_system/all_rooms.html', {'rooms': rooms})


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
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector') == 'on'

        if not name:
            return HttpResponse('Enter a name of new room')

        if not my_room.name == name:
            if Room.objects.filter(name=name):
                return HttpResponse('The room already exists. Try different name')

        if capacity <= 0:
            return HttpResponse('Capacity must be greater than 0')

        my_room.name = name
        my_room.capacity = capacity
        my_room.projector = projector
        my_room.save()

        return redirect('all_rooms')


class ReserveRoom(View):
    def get(self, request, room_id):
        my_room = Room.objects.get(pk=room_id)
        return render(request, 'booking_system/reserve_room.html', {'room': my_room,
                                                                    'reservations': my_room.roomreservation_set.all()})

    def post(self, request, room_id):
        my_room = Room.objects.get(pk=room_id)
        date_ = request.POST.get('date')
        comment = request.POST.get('comment')

        if RoomReservation.objects.filter(room=my_room, date=date_):
            return HttpResponse(f'The room is already reserved at {date_}')

        if date_ < str(date.today()):
            return HttpResponse('Can not make reservation in past')

        RoomReservation.objects.create(date=date_, comment=comment, room_id=room_id)

        return redirect('all_rooms')


class InfoRoom(View):
    def get(self, request, room_id):
        my_room = Room.objects.get(pk=room_id)
        return render(request, 'booking_system/room_info.html', {'room': my_room,
                                                                 'reservations': my_room.roomreservation_set.filter(
                                                                     room_id=room_id).order_by('-date')})


class SearchRoom(View):
    def get(self, request):
        name = request.GET.get('name')
        capacity = request.GET.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get('projector') == 'on'

        rooms = Room.objects.all()
        rooms = rooms.filter(projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gt=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = date.today() in reservation_dates

        return render(request, 'booking_system/all_rooms.html', {'rooms': rooms,
                                                                 'date': date.today()})
