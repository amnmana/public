from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import items_view, toggle_item_checked

app_name = 'tripapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist/', views.regist, name='regist'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('newtrip/', views.newtrip, name='newtrip'),
    path('new_page/', views.new_page, name='new_page'),
    path('tripdetails/', views.tripdetails, name='tripdetails'),
    path('pictures/', views.pictures, name='pictures'),
    path('locations/', views.locations_view, name='locations'),
    path('locations/delete/<int:location_id>/', views.delete_location, name='delete_location'),
    path('picturesupload/', views.picturesupload, name='picturesupload'),
    path('bulk_delete_pictures/',views.bulk_delete_pictures, name='bulk_delete_pictures'),
    path('items/', views.items_view, name='items_view'),
    path('items/', views.items_view, name='items'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('items/toggle/<int:item_id>/', toggle_item_checked, name='toggle_item_checked'),
    path('memos/', views.memos, name='memos'),
    path('addmemos/', views.addmemos, name='addmemos'),
    path('delete_memo/<int:memo_id>/', views.delete_memo, name='delete_memo'),
    path('portfolio/', views.portfolio, name='portfolio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)