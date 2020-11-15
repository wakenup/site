from django.db import models

from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
#1 Тип турнира
#2 Турнир
#3 Команды
#4 Игроки
#5 Турнир-команда
#6 Игра


class Typesoftour(models.Model):

    name = models.CharField(max_length=255,verbose_name="Тип турнира")
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):

    type = models.ForeignKey(Typesoftour,verbose_name="Тип",on_delete=models.CASCADE)
    title = models.CharField(max_length=255,verbose_name="Название")
    # slug = models.SlugField(unique=True)
    description = models.TextField()
    teamsamount = models.IntegerField()
    dateofstart = models.DateTimeField(verbose_name="Дата начала турнира")
    finishedtour = models.BooleanField(default=False)
    islive = models.BooleanField(default=False)
    city = models.CharField(verbose_name="Город проведения",max_length=255)
    image = models.ImageField(null=True,blank=True,default='cup.jpg')
    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'img/cup.jpg'
        return url


class Team(models.Model):
    # captain = models.ForeignKey(Player, verbose_name="Капитан команды",on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name="Название команды")
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    # user = models.ForeignKey(User,verbose_name="Пользователь",on_delete=models.CASCADE)
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    # firstname = models.CharField(max_length=255,verbose_name="Имя")
    # lastname = models.CharField(max_length=255,verbose_name="Фамилия")
    phone = models.CharField(max_length=100,null=True,blank=True)
    avatar = models.ImageField(null=True,blank=True,default='blankuser.jpg')

    def __str__(self):
        return "Игрок {} {}".format(self.user.first_name,self.user.last_name)


class PlayerTeam(models.Model):
    player = models.ForeignKey(Player,verbose_name="Игрок",on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name="Команда", on_delete=models.CASCADE)

class Tourteam(models.Model):
    team = models.ForeignKey(Team,verbose_name="Команда",on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament,verbose_name="Турнир",on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    captain = models.ForeignKey(Player,verbose_name="Капитан",on_delete=models.CASCADE)

    def __str__(self):
        return "Команда {} принимает участие в турнире {}".format(self.team,self.tournament)

class Game(models.Model):

    tournament = models.ForeignKey(Tournament,verbose_name="Турнир",on_delete=models.CASCADE)
    teamone = models.ForeignKey(Team,verbose_name="Первая команда",on_delete=models.CASCADE,related_name="firstteam")
    teamtwo = models.ForeignKey(Team,verbose_name="Вторая команда",on_delete=models.CASCADE,related_name="secondteam")

    goalsteamone = models.PositiveIntegerField(default=0)
    goalsteamtwo = models.PositiveIntegerField(default=0)
    dateofstart = models.DateTimeField()

    def __str__(self):
        pass
