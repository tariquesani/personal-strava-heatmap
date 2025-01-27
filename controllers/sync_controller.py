from bottle import template, request, redirect, route
from datetime import datetime, timedelta
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
        # Handle form submission
        if request.method == 'POST':
            return self.sync()
        # Ensure we have valid authentication
        if not self.strava_service.get_valid_access_token(self.client):
            return redirect('/sync/authorize')
            
        # Get the date range of existing activities
        start_date, end_date = self.strava_service.get_activity_date_range()
        return template('views/sync/index.tpl', start_date=start_date, end_date=end_date)
        
    def sync(self):
        """Handle the sync request"""
        try:
            # Get date parameters from form
            start_date = datetime.strptime(request.forms.get('start_date'), "%Y-%m-%d")
            end_date_input = request.forms.get('end_date')
            end_date = datetime.today() if not end_date_input else datetime.strptime(end_date_input, "%Y-%m-%d")
                        
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

    def inc(self):
        """Handle incremental sync request"""
        try:
            # Ensure we have valid authentication
            if not self.strava_service.get_valid_access_token(self.client):
                return redirect('/sync/authorize')

            # Get existing activities
            existing_activities = []
            if os.path.exists('data/strava_activities.json'):
                with open('data/strava_activities.json', 'r') as f:
                    existing_activities = json.load(f)

            # Get the last synced date
            if not existing_activities:
                return redirect('/sync')  # Redirect to full sync if no activities exist
                
            # Sort activities by start_date and get the latest date
            sorted_activities = sorted(existing_activities, key=lambda x: x['start_date'])
            last_sync_date = datetime.fromisoformat(sorted_activities[-1]['start_date'].replace('Z', '+00:00'))
            
            # Add one second to avoid duplicate activity
            start_date = last_sync_date + timedelta(seconds=1)
            end_date = datetime.today()
            
            # Fetch new activities
            new_activities = self.strava_service.fetch_activities(self.client, start_date, end_date)
            
            # Combine existing and new activities
            all_activities = existing_activities + new_activities
            
            # Save to data file
            os.makedirs('data', exist_ok=True)
            with open('data/strava_activities.json', 'w') as f:
                json.dump(all_activities, f, indent=4)
                
            return template('views/sync/success.tpl', activity_count=len(new_activities))
            
        except Exception as e:
            return template('views/sync/error.tpl', error=str(e)) 
        
    def athlete(self):
        # Ensure we have valid authentication
        if not self.strava_service.get_valid_access_token(self.client):
            return redirect('/sync/authorize')
        
        athlete = self.strava_service.fetch_athlete(self.client)
        return template('views/athlete.tpl', athlete=athlete)
                

