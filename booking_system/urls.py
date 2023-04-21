from django.urls import path, re_path
from . import views as system_views

urlpatterns = [
    path('', system_views.MainView.as_view(), name='main_page'),
    re_path(r'^room/new/$', system_views.NewRoom.as_view(), name='new_room'),
    re_path(r'^all-rooms/$', system_views.AllRooms.as_view(), name='all_rooms'),
    re_path(r'^room/delete/(?P<room_id>\d+)/$', system_views.DeleteRoom.as_view(), name='delete_room'),
    re_path(r'^room/modify/(?P<room_id>\d+)/$', system_views.EditRoom.as_view(), name='edit_room'),
    re_path(r'^room/reserve/(?P<room_id>\d+)/$', system_views.ReserveRoom.as_view(), name='room_reservation'),
    re_path(r'^room/info/(?P<room_id>\d+)/$', system_views.InfoRoom.as_view(), name='room_info'),
    path('search/', system_views.SearchRoom.as_view(), name='search_room'),
]
