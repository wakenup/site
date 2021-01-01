from django.shortcuts import render, redirect
from .models import Tournament, Typesoftour, Team, PlayerTeam, Tourteam, Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm, UserProfileForm, CreateTour
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date


def tour_list(request):
    context = {
        'tournaments': Tournament.objects.all()
    }

    return render(request, "tour_list.html", context)


def teams(request):
    context = {
        'teams': Team.objects.all()
    }

    return render(request, "teams.html", context)


@login_required(login_url='mainapp:login')
def create_team(request):
    if request.method == 'POST':
        logo = request.FILES['logo']
        title = request.POST['title']
        city = request.POST['city']

        team_info = Team(name=title, city=city, image=logo)
        team_info.save()
        pt = PlayerTeam(player=request.user.player, team=team_info, registertotur=True)
        pt.save()
        context = {
            'teams': Team.objects.all()
        }
        return render(request, "teams.html", context)
    context = {}

    return render(request, "create_team.html", context)


@login_required(login_url='mainapp:login')
def tour(request, id):
    t = Tournament.objects.get(pk=id)

    if request.method == 'POST':
        if 'register' in request.POST:
            p = PlayerTeam.objects.get(player=request.user.player)
            check = Tourteam.objects.filter(team=p.team, tournament=t)
            if len(check) != 1:
                if p.registertotur == True:
                    tour_team = Tourteam(team=p.team, tournament=t, captain=p.player)
                    tour_team.save()
                else:
                    print("У вас недостачно прав для регистрации команды на турнир")
            else:
                print("Ваша команда уже зарегистрирована на этот турнир")
        else:
            ft = Team.objects.get(name=request.POST['firsteam'])
            st = Team.objects.get(name=request.POST['secondteam'])
            if request.POST['firstscore'] > request.POST['secondscore']:
                fs = Tourteam.objects.get(tournament=t, team=ft)
                fs.points += 3
                fs.goalsscored += int(request.POST['firstscore'])
                fs.goalsskip += int(request.POST['secondscore'])
                fs.save()
                ss = Tourteam.objects.get(tournament=t, team=st)
                ss.goalsskip += int(request.POST['firstscore'])
                ss.goalsscored += int(request.POST['secondscore'])
                ss.save()
            elif request.POST['firstscore'] < request.POST['secondscore']:
                fs = Tourteam.objects.get(tournament=t, team=st)
                fs.points += 3
                fs.goalsskip += int(request.POST['firstscore'])
                fs.goalsscored += int(request.POST['secondscore'])
                fs.save()
                ss = Tourteam.objects.get(tournament=t, team=ft)
                ss.goalsskip += int(request.POST['firstscore'])
                ss.goalsscored += int(request.POST['secondscore'])
                ss.save()
            else:
                fs = Tourteam.objects.get(tournament=t, team=ft)
                fs.points += 1
                fs.goalsscored += int(request.POST['firstscore'])
                fs.goalsskip += int(request.POST['secondscore'])
                fs.save()
                ss = Tourteam.objects.get(tournament=t, team=st)
                ss.points += 3
                ss.goalsskip += int(request.POST['firstscore'])
                ss.goalsscored += int(request.POST['secondscore'])
                ss.save()

            g = Game(tournament=t, teamone=ft, teamtwo=st,
                     goalsteamone=request.POST['firstscore'], goalsteamtwo=request.POST['secondscore'],
                     dateofstart=date.today())
            g.save()
    teams = []
    teamsoftour = Tourteam.objects.filter(tournament=t)
    for e in teamsoftour:
        teams.append(e.team)
    results = []
    resoftour = Game.objects.filter(tournament=t)
    for i in resoftour:
        results.append(i)

    tables = []

    tablesbd = Tourteam.objects.filter(tournament=t).order_by('points').reverse()

    for a in tablesbd:
        tables.append(a)

    context = {'tour': t, 'teams': teams, 'res': results, 'tables': tables}

    return render(request, "tour.html", context);


def user_profile(request):
    player = request.user.player
    user = request.user
    form = UserProfileForm(instance=player)
    userform = CreateUserForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
    context = {'form': form, 'userform': userform}
    return render(request, "user.html", context)


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
            messages.info(request, "Пароли не совпадают")
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.info(request, "Пользователь с таким email уже существует")
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.info(request, "Пользователь с таким логином уже существует")
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
        typet = request.POST['type']
        amount = request.POST['amount']
        city = request.POST['city']
        desc = request.POST['label']
        date = request.POST['date']

        tour_info = Tournament(type=Typesoftour.objects.get(name=typet), title=title, description=desc,
                               teamsamount=amount, dateofstart=date, finishedtour=False, islive=False, city=city,
                               image=logo)
        tour_info.save()
        context = {
            'tournaments': Tournament.objects.all()
        }
        return render(request, "tour_list.html", context)
    context = {'types': Typesoftour.objects.all()}

    return render(request, 'create_tour.html', context)
