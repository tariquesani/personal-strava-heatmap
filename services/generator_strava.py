import json
import os
import signal
import webbrowser
from time import time
from datetime import datetime
from threading import Thread
from stravalib.client import Client
from bottle import Bottle, request, run
from dotenv import load_dotenv

# Load environment config
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKENS_FILE = "strava_tokens.json"
OUTPUT_FILE = "../data/strava_activities.json"

# Initialize Bottle app and global auth state
app = Bottle()
auth_code = None
bottle_thread = None


def load_tokens():
    """Load tokens from file."""
    return json.load(open(TOKENS_FILE)) if os.path.exists(TOKENS_FILE) else {}


def save_tokens(tokens):
    """Save tokens to file."""
    json.dump(tokens, open(TOKENS_FILE, 'w'))


def stop_bottle_server():
    """Force stop the Bottle server."""
    if bottle_thread:
        print("Stopping Bottle server...")
        os._exit(0)


# Set up graceful shutdown on Ctrl+C
signal.signal(signal.SIGINT, lambda sig, frame: stop_bottle_server())


def get_valid_access_token(client):
    """Get or refresh Strava access token."""
    global auth_code
    tokens = load_tokens()

    # Handle first-time authentication
    if not tokens:
        print("Starting authentication flow...")
        global bottle_thread
        bottle_thread = Thread(target=lambda: run(
            app, host="localhost", port=8080), daemon=True)
        bottle_thread.start()

        auth_url = f"https://www.strava.com/oauth/authorize?client_id={
            CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8080/exchange_token&scope=activity:read_all&approval_prompt=force"
        webbrowser.open(auth_url)

        while not auth_code:
            pass  # Wait for auth callback
        tokens = client.exchange_code_for_token(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=auth_code)
        save_tokens(tokens)

    # Refresh token if expired
    if tokens.get("expires_at", 0) <= time():
        print("Refreshing access token...")
        tokens = client.refresh_access_token(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=tokens["refresh_token"])
        save_tokens(tokens)

    client.access_token = tokens["access_token"]


@app.route("/exchange_token")
def exchange_token():
    """Callback endpoint for Strava OAuth."""
    global auth_code
    auth_code = request.query.code
    return "Authorization successful! You can close this window."


def fetch_activities(client, start_date, end_date):
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


def main():
    client = Client()
    try:
        get_valid_access_token(client)

        # Get date range from user
        start_date = datetime.strptime(
            input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d")
        # end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d")
        end_date = datetime.today() if not (end_date_input := input(
            "Just press enter for today or Enter end date (YYYY-MM-DD): ").strip()) else datetime.strptime(end_date_input, "%Y-%m-%d")

        # Fetch and save activities
        print("Fetching activities...")
        activities = fetch_activities(client, start_date, end_date)
        json.dump(activities, open(OUTPUT_FILE, 'w'), indent=4)
        print(f"Saved {len(activities)} activities to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        stop_bottle_server()


if __name__ == "__main__":
    main()
