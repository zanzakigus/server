from flask import Flask, request, json


app = Flask(__name__)

# import db setting and models
from models import dbSetting
from models.baseModel import BaseModel
from models.usuarioModel import Usuario
from models.emocionesModel import Emocion
from models.emocionesDetectadasModel import EmocionDetectada
from models.estrategiasModel import Estrategia

# import declared routes
from routes import user
from routes import emocion
from routes import emocionDetectada




@app.route('/')
def hello_world():  # put application's code here
    return json.dumps({'message': 'Hello World!!'}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
