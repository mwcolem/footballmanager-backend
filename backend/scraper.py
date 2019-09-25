from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from .constants import FORMAT
from .models import PlayerModel
from .player import Player

RATINGS_URL = "https://fantasy.espn.com/football/team?leagueId=1172646&seasonId=2019&teamId=1&fromTeamId=1"
S_G_URL = "https://fantasy.espn.com/football/team?leagueId=803723&teamId=1&seasonId=2019"
DYNASTY_URL = "https://www.fleaflicker.com/nfl/leagues/195647/teams/1318827"
RUGBY_URL = "https://fantasy.espn.com/football/team?leagueId=1259927&seasonId=2019&teamId=13&fromTeamId=13"
PPR_LEAGUE_ESPN_URLS = [RATINGS_URL, S_G_URL]
PPR_LEAGUE_FLEAFLICKER_URLS = [DYNASTY_URL]
HALF_LEAGUE_URLS = [RUGBY_URL]
STANDARD_LEAGUE_URLS = []

LEAGUE_URLS = [RATINGS_URL, S_G_URL, DYNASTY_URL, RUGBY_URL]

players = []

qb_tiers = []
rb_tiers = []
wr_tiers = []
te_tiers = []
flex_tiers = []


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
    for url in LEAGUE_URLS:
        print(url)
        soup = get_soup(url)
        player_list = soup.find_all('td', attrs={'class': 'playertablePlayerName'})

        for row in player_list:
            players.append(Player(str(row.find('a').getText())))


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
