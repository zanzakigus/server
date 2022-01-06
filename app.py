from flask import Flask

app = Flask(__name__)

# import db setting and models
from models import dbSetting
from models.usuarioModel import Usuario


# import declared routes
from routes import user

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
