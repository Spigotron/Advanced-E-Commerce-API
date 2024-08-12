from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
import os

MIGRATIONS_FOLDER = os.environ.get('MIGRATIONS_FOLDER') or 'migrations'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate(directory=MIGRATIONS_FOLDER)