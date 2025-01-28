from bottle import template
import os
import json
from stravalib.client import Client
from services.strava_service import StravaService

class HomeController:
    def index(self):
        checklist = {
            'env_file': os.path.exists('services/.env'),
            'strava_credentials': False,
            'data_files': {
                'strava_activities': os.path.exists('data/strava_activities.json'),
                'strava_athlete': os.path.exists('data/strava_athlete.json')
            }
        }

        # Initialize StravaService
        strava_service = StravaService()

        # Validate Strava credentials
        client = Client()
        checklist['strava_credentials'] = strava_service.get_valid_access_token(client)

        athlete = {}
        if checklist['data_files']['strava_athlete']:
            with open('data/strava_athlete.json', 'r') as f:
                athlete = json.load(f)

        return template('views/index.tpl', checklist=checklist, athlete=athlete)