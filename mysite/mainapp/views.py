from django.shortcuts import render, redirect
from .models import Tournament,Typesoftour
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm, UserProfileForm,CreateTour
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def tour_list(request):
    context = {
        'tournaments': Tournament.objects.all()
    }

    return render(request, "tour_list.html", context)


def tour(request,id):

    t = Tournament.objects.get(pk=id)

    context = {'tour':t}

    return render(request,"tour.html",context);


def user_profile(request):
    player = request.user.player
    user = request.user
    form = UserProfileForm(instance=player)
    userform = CreateUserForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=player)
        if form.is_valid():
            form.save()
    context = {'form':form,'userform':userform}
    return render(request,"user.html",context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('mainapp:tour_list')
        else:
            messages.info(request, 'Неправильный логин или пароль')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('mainapp:login')


def registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        player_form = UserProfileForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2 != password1:
            messages.info(request,"Пароли не совпадают")
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.info(request,"Пользователь с таким email уже существует")
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.info(request,"Пользователь с таким логином уже существует")
        else:
            if form.is_valid() and player_form.is_valid():
                user = form.save()
                player = player_form.save(commit=False)
                player.user = user
                user.save()
                player.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт ' + username + ' успешно создан')
                return redirect('mainapp:login')

    context = {'form': form}

    return render(request, 'registration.html', context)

@login_required(login_url='mainapp:login')
def create_tour(request):

    if request.method == 'POST':
            logo = request.FILES['logo']
            title = request.POST['title']
            typet =request.POST['type']
            amount = request.POST['amount']
            city = request.POST['city']
            desc = request.POST['label']
            date = request.POST['date']

            tour_info = Tournament(type=Typesoftour.objects.get(name=typet),title=title,description=desc,teamsamount=amount,dateofstart=date,finishedtour=False,islive=False,city=city,image=logo)
            tour_info.save()
            context = {
                'tournaments': Tournament.objects.all()
            }
            return render(request, "tour_list.html", context)
    context = {'types':Typesoftour.objects.all()}

    return render(request,'create_tour.html',context)