from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()    # this will create the data.db file - no need for create tables dot py.  it must see them in an import definition.
