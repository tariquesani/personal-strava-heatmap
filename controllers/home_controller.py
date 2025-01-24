from bottle import template

class HomeController:
    def index(self):
        return template('views/index.tpl') 