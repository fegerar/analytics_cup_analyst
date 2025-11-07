# Source - https://stackoverflow.com/a
# Posted by anurag, modified by fegerar. See post 'Timeline' for change history
# Retrieved 2025-11-07, License - CC BY-SA 4.0

from django.core.management.base import BaseCommand
from skillcorner_opendata.models import Match, Team
from os import system
import json

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')

def fetch_data():
    """Fetches data from external source"""
    system("git clone https://github.com/SkillCorner/opendata ../temp")
    with open("../temp/data/matches.json") as f:
        data = json.load(f)
    system("rm -rf ../temp")
    return data

def clear_data():
    """Deletes all the table data"""
    Match.objects.all().delete()


def create_match(item):
    """Creates a match object combining different elements from the list"""
    home_team_id = item['home_team']['id']
    away_team_id = item['away_team']['id']
    home_team_short_name = item['home_team']['short_name']
    away_team_short_name = item['away_team']['short_name']
    date_time = item['date_time']

    home_team, created = Team.objects.get_or_create(id=home_team_id, short_name=home_team_short_name)
    away_team, created = Team.objects.get_or_create(id=away_team_id, short_name=away_team_short_name)

    match = Match(
        home_team=home_team,
        away_team=away_team,
        date_time=date_time,
        status=item['status'],
        competition_id=item['competition_id'],
        season_id=item['season_id'],
        competition_edition_id=item['competition_edition_id']
    )

    match.save()
    return match


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    data = fetch_data()
    for item in data:
        create_match(item)

