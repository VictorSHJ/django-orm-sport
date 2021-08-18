from django.shortcuts import render, redirect
from django.db.models import Count
from .models import League, Team, Player
from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),

	# 1.Todas las ligas de béisbol
		"consulta01": League.objects.filter(sport__icontains='baseball'),
    # 2.Todas las ligas de mujeres
		"consulta02": League.objects.filter(name__icontains='women'),
    # 3.Todas las ligas donde el deporte es cualquier tipo de hockey
		"consulta03": League.objects.filter(sport__icontains='hockey'),
    # 4.Todas las ligas donde el deporte no sea football
		"consulta04": League.objects.exclude(sport__icontains='soccer'),
    # 5.Todas las ligas que se llaman "conferencias"
		"consulta05": League.objects.filter(name__icontains='conference'),
    # 6.Todas las ligas de la región atlántica
		"consulta06": League.objects.filter(name__icontains='atlantic'),
    # 7.Todos los equipos con sede en Dallas
		"consulta07": Team.objects.filter(location__icontains='dallas'),
    # 8.Todos los equipos nombraron los Raptors
		"consulta08": Team.objects.filter(team_name__icontains='raptors'),
    # 9.Todos los equipos cuya ubicación incluye "Ciudad"
		"consulta09": Team.objects.filter(location__icontains='city'),
    # 10.Todos los equipos cuyos nombres comienzan con "T"
		"consulta10": Team.objects.filter(team_name__istartswith='t'),
    # 11.Todos los equipos, ordenados alfabéticamente por ubicación
		"consulta11": Team.objects.order_by('location'),
    # 12.Todos los equipos, ordenados por nombre de equipo en orden alfabético inverso
		"consulta12": Team.objects.order_by('-team_name'),
    # 13.Cada jugador con apellido "Cooper"
		"consulta13": Player.objects.filter(last_name__icontains='cooper'),
    # 14.Cada jugador con nombre "Joshua"
		"consulta14": Player.objects.filter(first_name__icontains='joshua'),
    # 15.Todos los jugadores con el apellido "Cooper" EXCEPTO aquellos con "Joshua" como primer nombre
		"consulta15": Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua'),
    # 16.Ttodos los jugadores con nombre "Alexander" O nombre "Wyatt"	
	#	"consulta16": Player.objects.filter(first_name='Alexander') | Player.objects.filter(first_name='Wyatt'),
		"consulta16": Player.objects.filter(first_name__in=['Alexander','Wyatt']),

    # II. 1. Todos los equipos en la Atlantic Soccer Conference
		"consulta21": Team.objects.filter(league__name='Atlantic Soccer Conference'),
    # II. 2. Todos los jugadores (actuales) en los Boston Penguins
		"consulta22": Player.objects.filter(curr_team__team_name='Penguins', curr_team__location='Boston'),
    # II. 3. Todos los jugadores (actuales) en la International Collegiate Baseball Conference
		"consulta23": Player.objects.filter(curr_team__league__name='International Collegiate Baseball Conference'),
    # II. 4. Todos los jugadores (actuales) en la Conferencia Americana de Fútbol Amateur con el apellido "López"
		"consulta24": Player.objects.filter(curr_team__league__name='American Conference of Amateur Football', last_name='Lopez'),
    # II. 5. Todos los jugadores de fútbol
		"consulta25": Player.objects.filter(curr_team__league__sport='Football'),
    # II. 6. Todos los equipos con un jugador (actual) llamado "Sophia"
		"consulta26": Team.objects.filter(curr_players__first_name='Sophia'),
    # II. 7. Todas las ligas con un jugador (actual) llamado "Sophia"
		"consulta27": League.objects.filter(teams__curr_players__first_name='Sophia'),
    # II. 8. Todos con el apellido "Flores" que NO (actualmente) juegan para los Washington Roughriders
		"consulta28": Player.objects.filter(last_name="Flores").exclude(curr_team__team_name='Roughriders', curr_team__location='Washington'),
    # II. 9. Todos los equipos, pasados y presentes, con los que Samuel Evans ha jugado
		"consulta29": Team.objects.filter(all_players__first_name='Samuel', all_players__last_name='Evans'),
    # II. 10. Todos los jugadores, pasados y presentes, con los gatos tigre de Manitoba
        "consulta30": Player.objects.filter(all_teams__team_name='Tiger-Cats', all_teams__location='Manitoba'), 
    # II. 11. Todos los jugadores que anteriormente estaban (pero que no lo están) con los Wichita Vikings
		"consulta31": Player.objects.filter(all_teams__team_name='Vikings', all_teams__location='Wichita').exclude(curr_team__team_name='Wichita', curr_team__location='Wichita'),
    # II. 12. Cada equipo para el que Jacob Gray jugó antes de unirse a los Oregon Colts
		"consulta32": Team.objects.filter(all_players__first_name='Jacob', all_players__last_name='Gray').exclude(team_name='Colts', location='Oregon'),
    # II. 13. Todos los jugadores llamados "Joshua" que alguna vez han jugado en la Federación Atlántica de Jugadores de Béisbol Amateur
		"consulta33": Player.objects.filter(all_teams__league__name='Atlantic Federation of Amateur Baseball Players', first_name='Joshua'),
    # II. 14. Todos los equipos que han tenido 12 o más jugadores, pasados y presentes. (SUGERENCIA: busque la función annotate de Django).
		"consulta34": Team.objects.annotate(nro_jugadores=Count('all_players')).filter(nro_jugadores__gte=12),
	# II. 15. Todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
		"consulta35": Player.objects.annotate(nro_equipos=Count('all_teams')).order_by('nro_equipos'),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")