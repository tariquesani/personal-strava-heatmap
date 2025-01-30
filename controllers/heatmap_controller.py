from bottle import template
import json
from services.generator_map import generate_heatmap, generate_heatmap_with_time

class HeatmapController:
    def index(self):
        # Load activities from file
        try:
            with open('data/strava_activities.json', 'r') as f:
                activities = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            activities = []
        
        # Generate heatmap
        heatmap_html = generate_heatmap(activities)
        
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)

    
    def time(self):
        # Load activities from file
        try:
            with open('data/strava_activities.json', 'r') as f:
                activities = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            activities = []
        
        # Generate heatmap
        heatmap_html = generate_heatmap_with_time(activities)
        
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)
