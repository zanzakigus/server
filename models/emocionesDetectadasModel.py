from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import dbSetting, BaseModel
from app import Emocion
from app import Usuario

db = dbSetting.db


# Modelo de emocion detectada
class EmocionDetectada(BaseModel):
    __tablename__ = 'emociones_detectadas'
    id_emocion = db.Column(db.Integer, ForeignKey('emociones.id_emocion'), primary_key=True)
    correo = db.Column(db.String, ForeignKey('usuario.correo'), primary_key=True)
    id_estrategia = db.Column(db.String, ForeignKey('estrategias.id_estrategia'), primary_key=True)
    fecha_deteccion = db.Column(db.Integer, primary_key=True, default=int(round((datetime.now()).timestamp())))

    _default_fields = [
        "id_emocion",
        "correo",
        "fecha_deteccion"
    ]
    _hidden_fields = [
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(id_emocion: int, correo: str, id_estrategia: int):
        emotion: EmocionDetectada = EmocionDetectada(id_emocion=id_emocion, correo=correo, id_estrategia=id_estrategia)
        db.session.add(emotion)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = EmocionDetectada.query.all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_period(fecha_ini: str, fecha_fin: str, _correo: str):
        dt_tuple = tuple([int(x) for x in fecha_ini[:10].split('/')])
        dt_tuple = (dt_tuple[2], dt_tuple[1], dt_tuple[0]) + (00, 00, 00)
        fecha_ini = int(datetime(*dt_tuple).timestamp())
        dt_tuple = tuple([int(x) for x in fecha_fin[:10].split('/')]) + (00, 00, 00)
        dt_tuple = (dt_tuple[2], dt_tuple[1], dt_tuple[0]) + (00, 00, 00)
        fecha_fin = int(datetime(*dt_tuple).timestamp())
        print(fecha_fin)
        values: [] = EmocionDetectada.query.filter(
            EmocionDetectada.fecha_deteccion.between(fecha_ini, fecha_fin)).filter_by(correo=_correo).all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id_correo(_correo: str):
        values: [] = EmocionDetectada.query.filter_by(correo=_correo).all()
        if len(values) == 0:
            return None
        return values[0]

    @staticmethod
    def drop(_id: str):
        emocionDetectada: EmocionDetectada = EmocionDetectada.get_by_id_correo(_id)
        db.session.delete(emocionDetectada)
        db.session.commit()
