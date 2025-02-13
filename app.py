from bottle import Bottle, run, static_file, HTTPError, error, template, BaseTemplate
import importlib
import os
import traceback
import sys
import json

app = Bottle()

# Load Athlete JSON data once at app startup
try:
    with open('data/strava_athlete.json', 'r') as f:
        athlete = json.load(f)
except FileNotFoundError:
    athlete = {"error": "JSON file not found"}
except json.JSONDecodeError:
    athlete = {"error": "Invalid JSON format"}

# Set the default template variables
BaseTemplate.defaults = {'athlete': athlete}

# Routes for static files (CSS, JS, images)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='static/')

# Custom error handler for 404
@app.error(404)
def error404(error):
    return template('views/404.tpl', message=error.body)

# Dynamic controller/action routing
@app.route('/', method=['GET', 'POST'])
@app.route('/<controller>', method=['GET', 'POST'])
@app.route('/<controller>/', method=['GET', 'POST'])
@app.route('/<controller>/<action>', method=['GET', 'POST'])
def dynamic_route(controller='home', action='index'):
    try:
        # Import the controller module
        module_name = f"controllers.{controller}_controller"
        controller_module = importlib.import_module(module_name)
        
        # Get the controller class
        controller_class = getattr(controller_module, f"{controller.capitalize()}Controller")
        controller_instance = controller_class()
        
        # Get and call the action method
        action_method = getattr(controller_instance, action)
        return action_method()
        
    except Exception as e:
        # Log the full error traceback to stderr
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print("Error Details:", error_details, file=sys.stderr)
        
        # Always return a 404 error to the user
        raise HTTPError(404, f"Page not found: {controller}/{action}")

# Start the app
if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True, reloader=True)
