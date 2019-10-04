from urllib.request import Request
from urllib.request import urlopen
from yahoo_oauth import OAuth2
import urllib.request
import json
from bs4 import BeautifulSoup
from .constants import FORMAT
from .models import PlayerModel
from .player import Player

# ALL PLAYERS http://fantasy.espn.com/apis/v3/games/ffl/seasons/2018/players?scoringPeriodId=0&view=players_wl
# ALL FREE AGENTS http://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/336358?scoringPeriodId=0&view=kona_player_info
# Pro League organization info https://site.web.api.espn.com/apis/site/v2/teams?region=us&lang=en&leagues=nfl%2Cnba%2Cmlb%2Cnhl
# Pro team schedule http://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/?view=proTeamSchedules
# Roster at a given week http://fantasy.espn.com/apis/v3/games/ffl/seasons/2018/segments/0/leagues/336358?forTeamId=9&scoringPeriodId=13&view=mRoster
RATINGS_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1172646?forTeamId=1&view=mRoster"
S_G_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/803723?forTeamId=1&view=mRoster"
DYNASTY_URL = "https://www.fleaflicker.com/nfl/leagues/195647/teams/1318827"
RUGBY_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1259927?forTeamId=13&view=mRoster"
YAHOO_URL = "https://fantasysports.yahooapis.com/fantasy/v2/team/nfl.l.1166377.t.12/roster/players"
PHI_DELT_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/667520?forTeamId=3&view=mRoster"
PPR_LEAGUE_ESPN_URLS = [RATINGS_URL, S_G_URL]
PPR_LEAGUE_FLEAFLICKER_URLS = [DYNASTY_URL]
HALF_LEAGUE_URLS = [RUGBY_URL]
STANDARD_LEAGUE_URLS = [YAHOO_URL, PHI_DELT_URL]
ESPN_URLS = [RATINGS_URL, S_G_URL, RUGBY_URL]

players = []

qb_tiers = []
rb_tiers = []
wr_tiers = []
te_tiers = []
flex_tiers = []


def login_to_yahoo():
    global oauth
    oauth = OAuth2(None, None, from_file='./backend/oauth2yahoo.json')
    if not oauth.token_is_valid():
        oauth.refresh_access_token()


def clear_tier_arrays():
    rb_tiers.clear()
    wr_tiers.clear()
    te_tiers.clear()
    flex_tiers.clear()


def get_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return BeautifulSoup(page, "html.parser")


def get_player_list():
    print(DYNASTY_URL)
    soup = get_soup(DYNASTY_URL)

    player_list = soup.find_all('div', attrs={'class': 'player-name'})

    for row in player_list:
        players.append(Player(str(row.find('a').getText())))

    for espn_url in ESPN_URLS:
        with urllib.request.urlopen(espn_url) as url:
            print(espn_url)
            data = json.loads(url.read().decode())

            player_list = data['teams'][0]['roster']['entries']

            for player in player_list:
                print(player['playerPoolEntry']['player']['fullName'])
                players.append(Player(player['playerPoolEntry']['player']['fullName']))

    login_to_yahoo()

    print(YAHOO_URL)
    response = oauth.session.get(YAHOO_URL, params={'format': 'json'})
    data = response.json()

    player_list = data['fantasy_content']['team'][1]['roster']['0']['players']
    player_list.pop('count')

    for player in player_list:
        print(player_list[player]['player'][0][2]['name']['first']
              + " "
              + player_list[player]['player'][0][2]['name']['last'])


def get_ppr_tiers():
    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_QB.txt")
    [qb_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB-PPR.txt")
    [rb_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR-PPR.txt")
    [wr_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE-PPR.txt")
    [te_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_FLX-PPR.txt")
    [flex_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]


def get_half_tiers():
    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB-HALF.txt")
    [rb_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR-HALF.txt")
    [wr_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE-HALF.txt")
    [te_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_FLX-HALF.txt")
    [flex_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]


def get_standard_tiers():
    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB.txt")
    [rb_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR.txt")
    [wr_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE.txt")
    [te_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]

    soup = get_soup("https://s3-us-west-1.amazonaws.com/fftiers/out/text_FLX.txt")
    [flex_tiers.append(row[8:].split(',')) for row in str(soup).splitlines()]


def get_tiers(format):
    if format == FORMAT.PPR:
        get_ppr_tiers()
    elif format == FORMAT.HALF:
        get_half_tiers()
    elif format == FORMAT.STANDARD:
        get_standard_tiers()


def map_ppr_players_to_tiers():
    for index, tier in enumerate(qb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.ppr_position_tier = index

    for index, tier in enumerate(rb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.ppr_position_tier = index

    for index, tier in enumerate(wr_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.ppr_position_tier = index

    for index, tier in enumerate(te_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.ppr_position_tier = index

    for index, tier in enumerate(flex_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.ppr_flex_tier = index


def map_half_players_to_tiers():
    for index, tier in enumerate(qb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.half_position_tier = index

    for index, tier in enumerate(rb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.half_position_tier = index

    for index, tier in enumerate(wr_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.half_position_tier = index

    for index, tier in enumerate(te_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.half_position_tier = index

    for index, tier in enumerate(flex_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.half_flex_tier = index


def map_standard_players_to_tiers():
    for index, tier in enumerate(qb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.standard_position_tier = index

    for index, tier in enumerate(rb_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.standard_position_tier = index

    for index, tier in enumerate(wr_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.standard_position_tier = index

    for index, tier in enumerate(te_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.standard_position_tier = index

    for index, tier in enumerate(flex_tiers, start=1):
        for player in players:
            if any(player.name in tier_player for tier_player in tier):
                player.standard_flex_tier = index


def map_players_to_tiers(format):
    if format == FORMAT.PPR:
        map_ppr_players_to_tiers()
    elif format == FORMAT.HALF:
        map_half_players_to_tiers()
    elif format == FORMAT.STANDARD:
        map_standard_players_to_tiers()


def clear_players_with_no_tier():
    for player in players:
        if player.ppr_position_tier == -1 and player.ppr_flex_tier == -1 \
                and player.half_position_tier == -1 and player.half_flex_tier == -1\
                and player.standard_position_tier == -1 and player.standard_flex_tier == -1:
            players.remove(player)
            if get_player(player.name):
                found_player = get_player(player.name)
                found_player.delete()


def get_player(name):
    try:
        return PlayerModel.objects.get(name=name)
    except PlayerModel.DoesNotExist:
        return False


def update_players():
    print("updating player list")

    get_player_list()
    get_tiers(FORMAT.PPR)
    map_players_to_tiers(FORMAT.PPR)

    clear_tier_arrays()
    get_tiers(FORMAT.HALF)
    map_players_to_tiers(FORMAT.HALF)

    clear_tier_arrays()
    get_tiers(FORMAT.STANDARD)
    map_players_to_tiers(FORMAT.STANDARD)

    clear_players_with_no_tier()

    for player in set(players):
        if get_player(player.name):
            found_player = get_player(player.name)
            found_player.name = player.name
            found_player.ppr_position_tier = player.ppr_position_tier
            found_player.ppr_flex_tier = player.ppr_flex_tier
            found_player.half_position_tier = player.half_position_tier
            found_player.half_flex_tier = player.half_flex_tier
            found_player.standard_position_tier = player.standard_position_tier
            found_player.standard_flex_tier = player.standard_flex_tier

            found_player.save()
            print("Saved player: " + found_player.name)
        else:
            staged_player = PlayerModel(
                name = player.name,
                ppr_position_tier = player.ppr_position_tier,
                ppr_flex_tier = player.ppr_flex_tier,
                half_position_tier = player.half_position_tier,
                half_flex_tier = player.half_flex_tier,
                standard_position_tier = player.standard_position_tier,
                standard_flex_tier = player.standard_flex_tier,
            )
            staged_player.save()
            print("Saved player: " + player.name)
