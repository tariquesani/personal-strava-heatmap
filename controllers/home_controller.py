from bottle import template
import os
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

        return template('views/index.tpl', checklist=checklist)