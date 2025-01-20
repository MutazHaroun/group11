from flask import Flask
from models import db
from routes.auth import auth_blueprint
from routes.entries import entries_blueprint
from utils.db import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydiary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(entries_blueprint, url_prefix='/entries')

if __name__ == '__main__':
    # Run the Flask app on port 8080
    app.run(port=8080, debug=True)
