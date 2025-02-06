from bottle import template
import json
from services.map_service import generate_heatmap, generate_heatmap_with_time, generate_heatmap_one_ata_time
from bottle import redirect

class HeatmapController:
    def load_activities(self):
        try:
            with open('data/strava_activities.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            redirect('/sync') # Will this work reliably?
            return []

    def index(self):
        activities = self.load_activities()
        # Generate heatmap
        heatmap_html = generate_heatmap(activities)
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)

    def time(self):
        activities = self.load_activities()
        # Generate heatmap
        heatmap_html = generate_heatmap_with_time(activities)
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)

    def single(self):
        activities = self.load_activities()
        # Generate heatmap
        heatmap_html = generate_heatmap_one_ata_time(activities)
        # Return the HTML to display in a template
        return template('views/heatmap.tpl', map=heatmap_html)
