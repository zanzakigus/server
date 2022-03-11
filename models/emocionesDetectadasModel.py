from datetime import datetime,timezone

from sqlalchemy import ForeignKey, asc
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
    def get_by_period(fecha_ini: str, fecha_fin: str, _correo: str, _tipo: int):
        dt_tuple = tuple([int(x) for x in fecha_ini[:10].split('/')])
        dt_tuple = (dt_tuple[2], dt_tuple[1], dt_tuple[0]) + (00, 00, 00)
        fecha_ini = int(datetime(*dt_tuple).replace(tzinfo=timezone.utc).timestamp())

        dt_tuple = tuple([int(x) for x in fecha_fin[:10].split('/')])
        dt_tuple = (dt_tuple[2], dt_tuple[1], dt_tuple[0]) + (23, 59, 59)
        fecha_fin = int(datetime(*dt_tuple).replace(tzinfo=timezone.utc).timestamp())

        if _tipo is not -1:
            values: [] = EmocionDetectada.query.filter(
                EmocionDetectada.fecha_deteccion.between(fecha_ini, fecha_fin)).filter_by(correo=_correo).filter_by(
                id_emocion=_tipo).order_by(asc(EmocionDetectada.fecha_deteccion)).all()
        else:
            values: [] = EmocionDetectada.query.filter(
                EmocionDetectada.fecha_deteccion.between(fecha_ini, fecha_fin)).filter_by(correo=_correo).order_by(
                asc(EmocionDetectada.fecha_deteccion)).all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id_correo(_correo: str, _tipo: int):
        if _tipo is not -1:
            values: [] = EmocionDetectada.query.filter_by(correo=_correo, id_emocion=_tipo).order_by(
                asc(EmocionDetectada.fecha_deteccion)).all()
        else:
            values: [] = EmocionDetectada.query.filter_by(correo=_correo).order_by(
                asc(EmocionDetectada.fecha_deteccion)).all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def drop_by_user(_id: str):
        emocionDetectadas: [] = EmocionDetectada.get_by_id_correo(_id)
        for emocionDetectada in emocionDetectadas:
            db.session.delete(emocionDetectada)
        db.session.commit()
