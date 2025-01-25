import os
import json
from time import time
from dotenv import load_dotenv

class StravaService:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tokens_file = "services/strava_tokens.json"
        
    def load_tokens(self):
        """Load tokens from file."""
        return json.load(open(self.tokens_file)) if os.path.exists(self.tokens_file) else {}
        
    def save_tokens(self, tokens):
        """Save tokens to file."""
        with open(self.tokens_file, 'w') as f:
            json.dump(tokens, f)
            
    def get_authorization_url(self):
        """Generate the Strava authorization URL"""
        return f"https://www.strava.com/oauth/authorize?client_id={self.client_id}&response_type=code&redirect_uri=http://localhost:8080/sync/exchange_token&scope=activity:read_all&approval_prompt=force"
        
    def get_valid_access_token(self, client):
        """Get or refresh Strava access token."""
        tokens = self.load_tokens()
        
        if not tokens:
            return False
            
        # Refresh token if expired
        if tokens.get("expires_at", 0) <= time():
            print("Refreshing access token...")
            tokens = client.refresh_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=tokens["refresh_token"]
            )
            self.save_tokens(tokens)
            
        client.access_token = tokens["access_token"]
        return True
        
    def handle_authorization_callback(self, client, code):
        """Handle the OAuth callback and save tokens"""
        tokens = client.exchange_code_for_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code
        )
        self.save_tokens(tokens)
        
    def fetch_activities(self, client, start_date, end_date):
        """Fetch and format Strava activities."""
        return [{
            "id": activity.id,
            "name": activity.name,
            "start_date": activity.start_date_local.isoformat(),
            "start_lat": activity.start_latlng.lat if activity.start_latlng else None,
            "start_lng": activity.start_latlng.lon if activity.start_latlng else None,
            "distance": activity.distance,
            "moving_time": activity.moving_time,
            "elapsed_time": activity.elapsed_time,
            "type": activity.type.root,
            "average_speed": activity.average_speed,
            "map": activity.map.summary_polyline if hasattr(activity, 'map') else None
        } for activity in client.get_activities(after=start_date, before=end_date)
        if hasattr(activity, 'map') and activity.map.summary_polyline] 

    def get_activity_date_range(self):
        """Get the date range of stored activities.
        
        Returns:
            tuple: (start_date, end_date) as ISO format strings, or (None, None) if no activities
        """
        try:
            with open('data/strava_activities.json', 'r') as f:
                activities = json.load(f)
                
            if not activities:
                return None, None
                
            # Sort activities by start_date
            sorted_activities = sorted(activities, key=lambda x: x['start_date'])
            
            # Get earliest and latest dates
            start_date = sorted_activities[0]['start_date'].split('T')[0]  # Get just the date part
            end_date = sorted_activities[-1]['start_date'].split('T')[0]
            
            return start_date, end_date
            
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None 