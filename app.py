from bottle import Bottle, run, static_file, template
import json
from services.generator_map import generate_heatmap

app = Bottle()

# Routes for static files (CSS, JS, images)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='static/')

# Route for home page
@app.route('/')
def index():
    return template('views/index')

# Route to display the heatmap
@app.route('/heatmap')
def heatmap():
    # Load activity data
    with open('data/strava_activities.json', 'r') as f:
        activities = json.load(f)
    
    # Generate heatmap
    heatmap_html = generate_heatmap(activities)
    
    # Return the HTML to display in a template
    return template('views/heatmap', map=heatmap_html)

# Start the app
if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True, reloader=True)
