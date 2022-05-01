from datetime import datetime, timezone, timedelta

from app import app, Usuario, request, Fortalezas, EmocionDetectada


# -----------------------------Create User Route--------------------------------------
@app.route('/usuario', methods=["POST"])
def new_usuario():
    if request.method != 'POST':
        object_to_return = {
            "message": "Not a post method",
            "status": 400
        }
        return object_to_return, 400

    if not request.is_json:
        object_to_return = {
            "message": "Not json",
            "status": 415
        }
        return object_to_return, 415

    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    nombre = payload.get("nombre")
    ap_paterno = payload.get("ap_paterno")
    ap_materno = payload.get("ap_materno")
    password = payload.get("password")
    fecha_nacimiento = payload.get("fecha_nacimiento")
    strengths = payload.get("strengths")
    if correo is None or nombre is None or ap_paterno is None or ap_materno is None or password is None or \
            fecha_nacimiento is None or strengths is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password,fecha_nacimiento)",
            "status": 406
        }
        return object_to_return, 406
    Usuario.new(correo, nombre, ap_paterno,
                ap_materno, password, fecha_nacimiento)
    if Usuario.validate_credentials(correo, password):
        strengths = [x.replace(" ", "")
                     for x in strengths.strip('[]').split(",")]
        for strength in strengths:
            Fortalezas.new(correo, strength)
    object_to_return = {
        "message": "OK",
        "status": 200
    }
    return object_to_return, 200


# -----------------------------Get User Route--------------------------------------


@app.route('/usuario', methods=["GET"])
def get_usuario():
    if request.method != 'GET':
        return {
            "message": "Not a get method",
            "status": 400
        }, 400
    payload: dict = request.args.to_dict()
    correo = payload.get("correo")
    password = payload.get("password")
    if correo is None or password is None:
        return {
            "message": "Unable to get params: Expected json with (correo,password)",
            "status": 406
        }, 406
    if not Usuario.validate_credentials(correo, password):
        object_to_return = {
            "message": "Unauthorized",
            "status": 401}
        return object_to_return, 400

    usuario: Usuario = Usuario.get_by_id(correo)
    emocionesDetectadas: [] = EmocionDetectada.get_by_id_correo(correo, 0)

    #current_time = datetime.now().replace(tzinfo=timezone.utc)
    current_time = datetime.now()
    one_week_ago = current_time - timedelta(days=7)
    current_time = str(current_time.day) + "/" + \
        str(current_time.month) + "/" + str(current_time.year)
    one_week_ago = str(one_week_ago.day) + "/" + \
        str(one_week_ago.month) + "/" + str(one_week_ago.year)
    emocionesNegUltimaSem: [] = EmocionDetectada.get_by_period(
        current_time, one_week_ago, correo, 0)

    object_to_return = {
        "contenido": usuario.to_dict(),
        "statistics_week": len(emocionesNegUltimaSem),
        "statistics_all": len(emocionesDetectadas),
        "message": "OK",
        "status": 200}

    return object_to_return, 200


# -----------------------------PUT User Route--------------------------------------


@app.route('/usuario', methods=["PUT"])
def update_usuario():
    if request.method != 'PUT':
        return {
            "message": "Not a put method",
            "status": 400
        }, 400

    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    nombre = payload.get("nombre")
    ap_paterno = payload.get("ap_paterno")
    ap_materno = payload.get("ap_materno")
    password = payload.get("password")
    fecha_nacimiento = payload.get("fecha_nacimiento")

    if correo is None or nombre is None or ap_paterno is None or ap_materno is None or password is None or fecha_nacimiento is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password,fecha_nacimiento)",
            "status": 406
        }
        return object_to_return, 406

    if Usuario.validate_credentials(correo, password):
        Usuario.updateInfo(_id=correo, ap_materno=ap_materno, ap_paterno=ap_paterno,
                           fecha_nacimiento=fecha_nacimiento, nombre=nombre)
        object_to_return = {"message": "OK",
                            "status": 200}
    else:
        object_to_return = {"message": "Unauthorized",
                            "status": 401}

    return object_to_return, 200


# -----------------------------Password Route--------------------------------------


@app.route('/password', methods=["PUT"])
def update_password():
    if request.method != 'PUT':
        return {
            "message": "Not a put method",
            "status": 400
        }, 400

    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    password = payload.get("password")
    new_password = payload.get("new_password")

    if correo is None or password is None or new_password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password,fecha_nacimiento)",
            "status": 406
        }
        return object_to_return, 406

    if Usuario.validate_credentials(correo, password):
        Usuario.updatePassword(_id=correo, password=new_password)
        object_to_return = {"message": "OK",
                            "status": 200}
    else:
        object_to_return = {"message": "Unauthorized",
                            "status": 401}

    return object_to_return, 200


@app.route('/password', methods=["GET"])
def generate_email():
    payload: dict = request.args.to_dict()
    correo = payload.get("correo")
    password = payload.get("password")

    if correo is None or password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre)",
            "status": 406
        }
        return object_to_return, 406

    if Usuario.validate_credentials(correo, password):
        usuario: Usuario = Usuario.get_by_id(correo)
        numbers: str = Usuario.generateEmail(
            correo=correo, nombre=usuario.nombre)

        object_to_return = {"message": "OK",
                            "numbers": numbers,
                            "status": 200}
    else:
        object_to_return = {"message": "Unauthorized",
                            "status": 401}

    return object_to_return, 200


@app.route('/password', methods=["PATCH"])
def random_password():
    payload: dict = request.get_json()
    correo = payload.get("correo")

    if correo is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo)",
            "status": 406
        }
        return object_to_return, 406

    user: Usuario = Usuario.get_by_id(correo)
    if (user == None):
        object_to_return = {
            "message": "Usuario no encontrado",
            "status": "404"
        }
    else:
        Usuario.randomPassword(correo)
        object_to_return = {"message": "OK",
                            "status": 200}

    return object_to_return, 200


# -----------------------------Login Route--------------------------------------


@app.route('/login', methods=["POST"])
def login():
    if request.method != 'POST':
        return {
            "message": "Not a post method",
            "status": 400
        }, 400
    if not request.is_json:
        return {
            "message": "Not json",
            "status": 415
        }, 415
    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    password = payload.get("password")
    if correo is None or password is None:
        return "Unable to get params: Expected json with (correo,password)", 406
    if Usuario.validate_credentials(correo, password):
        object_to_return = {"message": "OK",
                            "status": 200}
    else:
        object_to_return = {"message": "Usuario no encontrado",
                            "status": 401}

    return object_to_return, 200
