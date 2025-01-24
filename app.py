from bottle import Bottle, run, static_file, HTTPError, error, template
import importlib
import os

app = Bottle()

# Routes for static files (CSS, JS, images)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='static/')

# Custom error handler for 404
@app.error(404)
def error404(error):
    return template('views/404.tpl', message=error.body)

# Dynamic controller/action routing
@app.route('/')
@app.route('/<controller>')
@app.route('/<controller>/')
@app.route('/<controller>/<action>')
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
        
    except (ImportError, AttributeError) as e:
        raise HTTPError(404, f"Page not found: {controller}/{action}")

# Start the app
if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True, reloader=True)
