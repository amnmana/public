from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import items_view, toggle_item_checked

app_name = 'tripapp'

urlpatterns = [
    path('home', views.home, name='home'),
    path('regist/', views.regist, name='regist'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('newtrip/', views.newtrip, name='newtrip'),
    path('new_page/', views.new_page, name='new_page'),
    # path('tripdetails/', views.tripdetails, name='tripdetails'),
    path('tripdetails/<int:trip_id>/', views.tripdetails, name='tripdetails'),
    path('delete_trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('pictures/<int:trip_id>/', views.pictures, name='pictures'),
    path('locations/<int:trip_id>/', views.locations_view, name='locations'),
    path('locations/delete/<int:location_id>/<int:trip_id>/', views.delete_location, name='delete_location'),
    path('picturesupload/<int:trip_id>/', views.picturesupload, name='picturesupload'),
    path('bulk_delete_pictures/<int:trip_id>/',views.bulk_delete_pictures, name='bulk_delete_pictures'),
    # path('items/<int:trip_id>/', views.items_view, name='items_view'),
    path('items/<int:trip_id>/', views.items_view, name='items'),
    path('item/delete/<int:item_id>/<int:trip_id>/', views.delete_item, name='delete_item'),
    path('items/toggle/<int:item_id>/', toggle_item_checked, name='toggle_item_checked'),
    path('memos/<int:trip_id>/', views.memos, name='memos'),
    path('addmemos/<int:trip_id>/', views.addmemos, name='addmemos'),
    path('delete_memo/<int:memo_id>/<int:trip_id>/', views.delete_memo, name='delete_memo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)