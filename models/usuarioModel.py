from app import dbSetting, BaseModel
from utils.random import random_word, random_number
from utils.email import send_code_password, send_random_password
from sha3 import sha3_512

db = dbSetting.db


# Modelo de usuario
class Usuario(BaseModel):
    __tablename__ = 'usuario'
    correo = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, default='no_name')
    ap_paterno = db.Column(db.String, default='no_ap_p')
    ap_materno = db.Column(db.String, default='no_ap_m')
    password = db.Column(db.String, default='password')
    salt = db.Column(db.String)
    fecha_nacimiento = db.Column(db.Integer)

    _default_fields = [
        "correo",
        "nombre",
        "ap_paterno",
        "ap_materno",
        "salt",
        "fecha_nacimiento",
    ]
    _hidden_fields = [
        "password",
    ]
    _readonly_fields = [
    ]

    @staticmethod
    def new(correo: str, nombre: str, ap_paterno: str, ap_materno: str, password: str, fecha_nacimiento: int):
        user: Usuario = Usuario(correo=correo, nombre=nombre, ap_paterno=ap_paterno, ap_materno=ap_materno,
                                fecha_nacimiento=fecha_nacimiento)
        user.salt = random_word(15)
        user.password = Usuario.__generate_pass(password, user.salt)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_all():
        values: [] = Usuario.query.all()
        if len(values) == 0:
            return []
        return values

    @staticmethod
    def get_by_id(_id: str):
        values: [] = Usuario.query.filter_by(correo=_id).all()
        if len(values) == 0:
            return None
        return values[0]

    @staticmethod
    def updateInfo(_id: str, nombre: str, ap_paterno: str, ap_materno: str, fecha_nacimiento: int):
        user: Usuario = Usuario.get_by_id(_id)
        user.nombre = nombre
        user.ap_paterno = ap_paterno
        user.ap_materno = ap_materno
        user.fecha_nacimiento = fecha_nacimiento
        #user.password = Usuario.__generate_pass(password, user.salt)
        db.session.commit()
        
    @staticmethod
    def generateEmail(correo: str, nombre: str):
        numbers = random_number(6)
        send_code_password(correo=correo, nombre=nombre, numeros=numbers)
        return numbers
        
    @staticmethod
    def updatePassword(_id: str, password: str):
        user: Usuario = Usuario.get_by_id(_id)
        user.password = Usuario.__generate_pass(password, user.salt)
        db.session.commit()
        
    @staticmethod
    def randomPassword(_id: str):
      user: Usuario = Usuario.get_by_id(_id)
      newPassword = random_word(8)
      user.password = Usuario.__generate_pass(newPassword, user.salt)
      db.session.commit()
      send_random_password(correo=user.correo, nombre=user.nombre, new_password=newPassword)

    @staticmethod
    def drop(_id: int):
        user: Usuario = Usuario.get_by_id(_id)
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def validate_credentials(_correo: str, _password: str):
        user: [] = Usuario.query.filter_by(correo=_correo).all()
        if len(user) == 0:
            return False
        # valid correo
        user: Usuario = user[0]
        encrypted_test = Usuario.__generate_pass(_password, user.salt)
        if user.password == encrypted_test:
            return True
        else:
            return False
    # Método privado para la generación de la contraseña
    @staticmethod
    def __generate_pass(_pass, _salt):
        salted_password: str = _pass + _salt
        return sha3_512(salted_password.encode('utf-8')).hexdigest()