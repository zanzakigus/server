from app import app
from flask_sqlalchemy import SQLAlchemy


db_name = 'database.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
db.init_app(app)


if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        # print("turning on foreign keys for connection")
        dbapi_con.execute('pragma foreign_keys=ON')


    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        # print("foreign keys are already on")