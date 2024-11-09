import os
from flask import Flask
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='static')
app.url_map.strict_slashes = False


app.jinja_options = app.jinja_options.copy()
app.jinja_options.update({
    'trim_blocks': True,
    'lstrip_blocks': True
})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = \
    os.getenv("SECRET_KEY", None)
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

app.config['LINE_BOT_API'] = os.getenv("LINE_BOT_API", None)
app.config['HANDLER'] = os.getenv("HANDLER", None)
app.config['WEATHER_TOKEN'] = os.getenv("WEATHER_TOKEN", None)
app.config['LINK'] = os.getenv("LINK", None)


from app import views  # noqa

