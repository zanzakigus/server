from app import dbSetting, BaseModel

db = dbSetting.db


# Modelo de estrategia
class Estrategia(BaseModel):
    __tablename__ = 'estrategias'
    id_estrategia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto_estrategia = db.Column(db.String, default='no_name')

    _default_fields = [
        "id_estrategia",
        "texto_estrategia",
    ]
    _hidden_fields = [
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(texto_estrategia: str):
        emotion: Estrategia = Estrategia(texto_estrategia=texto_estrategia)
        db.session.add(emotion)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = Estrategia.query.all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id(_id: int):
        values: [] = Estrategia.query.filter_by(id_estrategia=_id).all()
        if len(values) == 0:
            return None
        return values[0]

    @staticmethod
    def update(_id: int, texto_estrategia: str):
        emotion: Estrategia = Estrategia.get_by_id(_id)
        emotion.texto_estrategia = texto_estrategia
        db.session.commit()

    @staticmethod
    def drop(_id: int):
        emotion: Estrategia = Estrategia.get_by_id(_id)
        db.session.delete(emotion)
        db.session.commit()
