from app import dbSetting
db = dbSetting.db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    correo = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, default='no_name')
    ap_paterno = db.Column(db.String, default='no_name')

    @staticmethod
    def new_user(correo: str, nombre: str, ap_paterno: str):
        user = Usuario(correo=correo, nombre=nombre, ap_paterno=ap_paterno)
        db.session.add(user)
        db.session.commit()
