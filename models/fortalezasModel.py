from sqlalchemy import ForeignKey

from app import dbSetting, BaseModel

db = dbSetting.db


# Modelo de Fortalezas
class Fortalezas(BaseModel):
    __tablename__ = 'fortalezas'
    correo = db.Column(db.String, ForeignKey('usuario.correo'), primary_key=True)
    fortaleza_texto = db.Column(db.String, primary_key=True)

    _default_fields = [
        "correo",
        "fortaleza_texto",
    ]
    _hidden_fields = [
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(correo: str, fortaleza_texto: str):
        strength: Fortalezas = Fortalezas(correo=correo, fortaleza_texto=fortaleza_texto)
        db.session.add(strength)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = Fortalezas.query.all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id(_correo: str, fortaleza_texto: str):
        values: [] = Fortalezas.query.filter_by(correo=_correo, fortaleza_texto=fortaleza_texto).all()
        if len(values) == 0:
            return None
        return values[0]

    @staticmethod
    def get_by_user(_correo: str):
        values: [] = Fortalezas.query.filter_by(correo=_correo).all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def update(_correo: str, fortaleza_texto_old: str, fortaleza_texto_new: str):
        strength: Fortalezas = Fortalezas.get_by_id(_correo, fortaleza_texto_old)
        strength.fortaleza_texto = fortaleza_texto_new
        db.session.commit()

    @staticmethod
    def drop_by_user(_correo: correo):
        values: [] = Fortalezas.get_by_user(_correo)
        for value in values:
            db.session.delete(value)
            db.session.commit()
