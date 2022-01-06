from app import dbSetting, BaseModel

db = dbSetting.db


# Modelo de emocion
class Emocion(BaseModel):
    __tablename__ = 'emociones'
    id_emocion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emocion_texto = db.Column(db.String, default='no_name')

    _default_fields = [
        "id_emocion",
        "emocion_texto",
    ]
    _hidden_fields = [
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(emocion_texto: str):
        emotion: Emocion = Emocion(emocion_texto=emocion_texto)
        db.session.add(emotion)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = Emocion.query.all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id(_id: int):
        values: [] = Emocion.query.filter_by(id_emocion=_id).all()
        if len(values) == 0:
            return None
        return values[0]

    @staticmethod
    def update(_id: int, emocion_texto: str):
        emotion: Emocion = Emocion.get_by_id(_id)
        emotion.emocion_texto = emocion_texto
        db.session.delete(emotion)
        db.session.commit()

    @staticmethod
    def drop(_id: int):
        emotion: Emocion = Emocion.get_by_id(_id)
        db.session.delete(emotion)
        db.session.commit()
