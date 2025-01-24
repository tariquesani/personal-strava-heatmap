from bottle import template, request, redirect, route
from datetime import datetime
import json
import os
from stravalib.client import Client
from services.strava_service import StravaService

class SyncController:
    def __init__(self):
        self.strava_service = StravaService()
        self.client = Client()
        
    def index(self):
        """Show the sync form page"""
        if request.method == 'POST':
            return self.sync()
        return template('views/sync/index.tpl')
        
    def sync(self):
        """Handle the sync request"""
        try:
            # Get date parameters from form
            start_date = datetime.strptime(request.forms.get('start_date'), "%Y-%m-%d")
            end_date_input = request.forms.get('end_date')
            end_date = datetime.today() if not end_date_input else datetime.strptime(end_date_input, "%Y-%m-%d")
            
            # Ensure we have valid authentication
            if not self.strava_service.get_valid_access_token(self.client):
                return redirect('/sync/authorize')
            
            # Fetch and save activities
            activities = self.strava_service.fetch_activities(self.client, start_date, end_date)
            
            # Save to data file
            os.makedirs('data', exist_ok=True)
            with open('data/strava_activities.json', 'w') as f:
                json.dump(activities, f, indent=4)
                
            return template('views/sync/success.tpl', activity_count=len(activities))
            
        except Exception as e:
            return template('views/sync/error.tpl', error=str(e))
            
    def authorize(self):
        """Start the Strava OAuth flow"""
        auth_url = self.strava_service.get_authorization_url()
        return redirect(auth_url)
        
    def exchange_token(self):
        """Handle the OAuth callback"""
        code = request.query.get('code')
        if code:
            self.strava_service.handle_authorization_callback(self.client, code)
            return redirect('/sync')
        return redirect('/sync') 