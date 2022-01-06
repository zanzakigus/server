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
    emocion_texto = db.Column(db.String, default='no_name')


    _default_fields = [
        "id_emocion",
        "correo",
        "emocion_texto"
    ]
    _hidden_fields = [
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(id_emocion: int, correo: str, emocion_texto: str):
        emotion: EmocionDetectada = EmocionDetectada(id_emocion=id_emocion, correo=correo,
                                                     emocion_texto=emocion_texto)
        db.session.add(emotion)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = EmocionDetectada.query.all()
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
