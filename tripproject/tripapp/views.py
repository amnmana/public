from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from .models import Trip
from django.http import JsonResponse
from .forms import LocationForm
from .models import Location
from .forms import PictureForm
from .models import Picture
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Item
from django.shortcuts import get_object_or_404, redirect
from .forms import MemoForm
from .models import Memo
from django.views.decorators.http import require_POST
from .forms import TripForm
from django.http import HttpResponse
from .forms import LoginForm


def home(request):
    return render(request, 'tripapp/home.html')

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('tripapp:mypage')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'tripapp/regist.html', context={
            'regist_form': regist_form,
        }
    )

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('tripapp:mypage')
            else:
                messages.warning(request, 'User is not acctive.')
        else:
            messages.warning(request,'Wrong mailaddress or password.')
    return render(
        request, 'tripapp/user_login.html', context={
            'login_form': login_form,
        }
    )


def user_logout(request):
    logout(request)
    return redirect('tripapp:home')

@login_required

def mypage(request):
    breadcrumbs = [
        {'name': 'マイページ', 'url': reverse('tripapp:mypage')}
    ]
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'tripapp/mypage.html', {'trips': trips, 'breadcrumbs': breadcrumbs})

@login_required
def newtrip(request):
    if request.method == "POST":
        print("POST data:", request.POST)  # POSTデータを出力
        form = TripForm(request.POST)
        if form.is_valid():
            new_trip = form.save(commit=False)
            new_trip.user = request.user
            new_trip.save()
            return redirect('tripapp:mypage')
        else:
            print("Form errors:", form.errors)  # フォームのエラーを出力
            return render(request, 'tripapp/newtrip.html', {'form': form})
    else:
        form = TripForm()
    return render(request, 'tripapp/newtrip.html', {'form': form})

def new_page(request):
    return render(request,'tripapp/new_page.html')

def tripdetails(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    breadcrumbs = [
        {'name': 'マイページ', 'url': reverse('tripapp:mypage')},
        {'name': trip.destination, 'url': reverse('tripapp:tripdetails', kwargs={'trip_id': trip_id})}
    ]
    context = {
        'trip': trip,
        'trip_id': trip_id,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'tripapp/tripdetails.html', context)

@require_POST
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    trip.delete()
    return redirect('tripapp:mypage')

# def mypage(request):
#     new_trip = None
#     session_key = request.session.session_key
#     trip_data = request.session.get('new_trip')
#     if trip_data:
#         new_trip = Trip.objects.create(
#             destination=trip_data['destination'],
#             startDate=trip_data['startDate'],
#             endDate=trip_data['endDate']
#         )
#     trips = Trip.objects.all()
#     return render(request, 'tripapp/mypage.html', {'new_trip': new_trip, 'trips': trips})

# def locations(request):
#     return render(request, 'tripapp/locations.html')

@login_required
def locations_view(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    
    if request.method == "POST":
        names = request.POST.getlist('name[]')
        addresses = request.POST.getlist('address[]')
        print(names, addresses)

        # 名称と住所のペアをデータベースに保存
        for name, address in zip(names, addresses):
            if name and address:  # 空の値を無視
                Location.objects.create(name=name, address=address, trip=trip)

        return redirect('tripapp:locations', trip_id=trip_id)

    locations = Location.objects.filter(trip=trip)  # 修正：旅行に紐づく位置情報のみを取得
    return render(request, 'tripapp/locations.html', {'locations': locations, 'trip_id': trip_id})

def delete_location(request, location_id, trip_id):
    location = Location.objects.get(id=location_id)
    location.delete()
    return redirect('tripapp:locations', trip_id=trip_id)  # ここは前回の修正案に基づいています
    
def pictures(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    
    if request.method == 'POST':
        # フォームデータとファイルを処理
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.trip = trip
            picture.save()  # 写真を保存する
            return redirect('tripapp:pictures', trip_id=trip_id)
        else:
            # フォームのバリデーションエラーを扱う
            pictures = Picture.objects.filter(trip=trip)
            return render(request, 'tripapp/pictures.html', {'form': form, 'pictures': pictures, 'trip_id': trip_id})
    else:
        form = PictureForm()
    
    pictures = Picture.objects.filter(trip=trip)  # 修正：旅行に紐づく写真のみを取得
    return render(request, 'tripapp/pictures.html', {'form': form, 'pictures': pictures, 'trip_id': trip_id})

@require_POST
def bulk_delete_pictures(request, trip_id):
    picture_ids = request.POST.getlist('picture_ids')
    Picture.objects.filter(id__in=picture_ids).delete()
    return redirect('tripapp:pictures', trip_id=trip_id)

#def items(request):
    #return render(request, 'tripapp/items.html')

def items_view(request, trip_id):
    if request.method == "POST":
        names = request.POST.getlist('name')

        for name in names:
            if name:  # 空の値を無視
                Item.objects.create(name=name, trip_id=trip_id, checked=False)
        return redirect('tripapp:items', trip_id=trip_id)

    items = Item.objects.filter(trip_id=trip_id)
    return render(request, 'tripapp/items.html', {'items': items, 'trip_id': trip_id})

def delete_item(request, item_id, trip_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('tripapp:items', trip_id=trip_id)  # ここは前回の修正案に基づいています

def toggle_item_checked(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.checked = not item.checked  # 状態を反転
    item.save()
    return redirect('tripapp:items', trip_id=item.trip_id)

def memos(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    memos = Memo.objects.filter(trip=trip)  # trip_idをtripに修正
    
    context = {
        'memos': memos,
        'trip_id': trip_id,
    }
    return render(request, 'tripapp/memos.html', context)

def addmemos(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)  # 旅行データを取得
    if request.method == "POST":
        form = MemoForm(request.POST, trip=trip)  # trip オブジェクトをフォームに渡す
        if form.is_valid():
            form.save()
            return redirect('tripapp:memos', trip_id=trip_id)
    else:
        form = MemoForm(trip=trip)  # GET リクエスト時にも trip オブジェクトをフォームに渡す
    return render(request, 'tripapp/addmemos.html', {'form': form, 'trip_id': trip_id})

def delete_memo(request, memo_id, trip_id):
    memo = get_object_or_404(Memo, id=memo_id)
    memo.delete()
    return redirect('tripapp:memos', trip_id=trip_id)  # memos のリストページにリダイレクトします

@require_POST
def update_memo(request, trip_id):
    memo_id = request.POST.get('id')
    new_detail = request.POST.get('detail')
    
    try:
        memo = Memo.objects.get(id=memo_id)
        memo.detail = new_detail
        memo.save()
        return JsonResponse({'status': 'success'})
    except Memo.DoesNotExist:
        return JsonResponse({'status': 'failed', 'error': 'Memo does not exist'})
    
def portfolio(request):
    return render(request, 'tripapp/portfolio.html')

def some_view(request):
    breadcrumbs = [
        {'name': 'MyPage', 'url': reverse('mypage')},
        {'name': 'カテゴリー名', 'url': reverse('category_view')},
        {'name': '子カテゴリー名', 'url': reverse('subcategory_view')}
    ]
    return render(request, 'tripapp/some_template.html', {'breadcrumbs': breadcrumbs})