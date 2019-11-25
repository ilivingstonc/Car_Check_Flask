import os
import models

from flask import Flask, jsonify, g 
from flask_cors import CORS
from resources.cars import car
from resources.users import user
from resources.savedcars import savedcar
from flask_login import LoginManager



DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)
app.secret_key = 'nobueno'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(car, origins=['http://localhost:3000', 'https://car-maintenance-app-react.herokuapp.com'], supports_credentials=True, url_prefix='/api/v1/cars') # adding this line

app.register_blueprint(car, url_prefix='/api/v1/cars')

CORS(user, origins=['http://localhost:3000', 'https://car-maintenance-app-react.herokuapp.com'], supports_credentials=True, url_prefix='/api/v1/user') # adding this line

app.register_blueprint(user, url_prefix='/api/v1/user')

CORS(savedcar, origins=['http://localhost:3000', 'https://car-maintenance-app-react.herokuapp.com'], supports_credentials=True, url_prefix='/api/v1/savedcars') # adding this line

app.register_blueprint(savedcar, url_prefix='/api/v1/savedcars')



if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialized()

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)