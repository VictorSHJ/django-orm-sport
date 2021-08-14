from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"consulta01": League.objects.filter(sport__contains='baseball'),
		"consulta02": League.objects.filter(name__contains='women'),
		"consulta03": League.objects.filter(sport__contains='hockey'),
		"consulta04": League.objects.exclude(sport__contains='soccer'),
		"consulta05": League.objects.filter(name__contains='conference'),
		"consulta06": League.objects.filter(name__contains='atlantic'),
		"consulta07": Team.objects.filter(location__contains='dallas'),
		"consulta08": Team.objects.filter(team_name__contains='raptors'),
		"consulta09": Team.objects.filter(location__contains='city'),
		"consulta10": Team.objects.filter(team_name__startswith='t'),
		"consulta11": Team.objects.order_by('location'),
		"consulta12": Team.objects.order_by('-team_name'),
		"consulta13": Player.objects.filter(last_name__contains='cooper'),
		"consulta14": Player.objects.filter(first_name__contains='joshua'),
		"consulta15": Player.objects.filter(last_name__contains='cooper').exclude(first_name__contains='joshua'),
		"consulta16": Player.objects.filter(first_name__contains='alexander') | Player.objects.filter(first_name__contains='wyatt'),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")