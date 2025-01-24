from bottle import template
import json
from services.generator_map import generate_heatmap

class HeatmapController:
    def index(self):
        # Load activity data
        with open('data/strava_activities.json', 'r') as f:
            activities = json.load(f)
        
        # Generate heatmap
        heatmap_html = generate_heatmap(activities)
        
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)

    def show(self):
        # new action
        return template('views/show_heatmap.tpl') 