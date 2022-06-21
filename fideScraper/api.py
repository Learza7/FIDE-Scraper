import datetime
from ninja import NinjaAPI
from Models.models import Person
import Models.Scraper
api = NinjaAPI()


@api.get('/hello')
def hello(request):
    return 'Hello world'

@api.get('/update')
def update(request):
    Players = Person.objects.all()
    
    for player in Players:
        if player.rapid_elo:
            continue

        info = Models.Scraper.getPlayerInfo(player.fide_id)

        player.sex = info['sex']
        player.title = info['title']
        player.world_rank = info['world_rank']
        player.continental_rank = info['continental_rank']
        player.national_rank = info['national_rank']
        player.birth_year = info['birth_year']
        

        elo_history = Models.Scraper.getEloHistory(player.fide_id)
        if elo_history:
            print(player.first_name)
            player.standard_elo = elo_history[0]["standard_elo"]
            player.rapid_elo = elo_history[0]["rapid_elo"]
            player.blitz_elo = elo_history[0]["blitz_elo"]
            player.elo_history = elo_history
        
            date = datetime.datetime.strptime(f'{elo_history[0]["date"]} 01', '%Y-%b %d').strftime('%Y-%m-%d')

            player.standard_games_history = Models.Scraper.getGamesHistory(player.fide_id, date, 0)
            player.rapid_games_history = Models.Scraper.getGamesHistory(player.fide_id, date, 1)
            player.blitz_games_history = Models.Scraper.getGamesHistory(player.fide_id, date, 2)
        player.save()

    return 'Done'

@api.get('/player/{fide_id}')
def getPlayerInfo(request, fide_id):
    Player = Person.objects.get(fide_id=fide_id)
    return {
        "first_name": Player.first_name,
        "last_name": Player.last_name,
        "sex": Player.sex,
        "birth_date": Player.birth_date,
        "origin":  Player.origin,
        "totem": Player.totem,
        
        "title": Player.title,
        "standard_elo": Player.standard_elo,
        "rapid_elo": Player.rapid_elo,
        "blitz_elo": Player.blitz_elo,
        "elo_history": Player.elo_history,

        "world_rank": Player.world_rank,
        "continental_rank": Player.continental_rank,
        "national_rank": Player.national_rank,

    
    }



@api.get('/game_history')
def getGameHistory(request, fide_id : int, period : str, time_control : int):
    
    pass


@api.get('/allPlayersInfo')
def getAllPlayers(request):
    return [{
        "first_name": Player.first_name,
        "last_name": Player.last_name,
        "sex": Player.sex,
        "birth_date": Player.birth_date,
        "origin":  Player.origin,
        "totem": Player.totem,
        
        "title": Player.title,
        "standard_elo": Player.standard_elo,
        "rapid_elo": Player.rapid_elo,
        "blitz_elo": Player.blitz_elo,
        "elo_history": Player.elo_history,

        "world_rank": Player.world_rank,
        "continental_rank": Player.continental_rank,
        "national_rank": Player.national_rank,
    }
        for Player in Person.objects.all()
    ]