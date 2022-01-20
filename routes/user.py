from app import app, Usuario, request


# -----------------------------Create User Route--------------------------------------
@app.route('/usuario', methods=["POST"])
def new_usuario():
    if request.method != 'POST':
        return "not a post method", 400
    if not request.is_json:
        return "not json", 415
    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    nombre = payload.get("nombre")
    ap_paterno = payload.get("ap_paterno")
    ap_materno = payload.get("ap_materno")
    password = payload.get("password")
    fecha_nacimiento = payload.get("fecha_nacimiento")
    if correo is None or nombre is None or ap_paterno is None or ap_materno is None or password is None or fecha_nacimiento is None:
        return "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password," \
               "fecha_nacimiento)", 406
    Usuario.new(correo, nombre, ap_paterno, ap_materno, password, fecha_nacimiento)
    object_to_return = {"resp": True}
    return object_to_return, 200


# -----------------------------Get User Route--------------------------------------
@app.route('/usuario', methods=["GET"])
def get_usuario():
    if request.method != 'GET':
        return "not a post method", 400
    payload: dict = request.args.to_dict()
    correo = payload.get("correo")
    password = payload.get("password")
    if correo is None or password is None:
        return "Unable to get params: Expected json with (correo,password)", 406
    if Usuario.validate_credentials(correo, password):
        new_usuario: Usuario = Usuario.get_by_id(correo)
        object_to_return = {"resp": True,
                            "contenido": new_usuario.to_dict()}
    else:
        object_to_return = {"resp": False}

    return object_to_return, 200


# -----------------------------Login Route--------------------------------------
@app.route('/login', methods=["POST"])
def login():
    if request.method != 'POST':
        return "not a post method", 400
    if not request.is_json:
        return "not json", 415
    payload: dict = request.get_json(force=True)
    correo = payload.get("correo")
    password = payload.get("password")
    if correo is None or password is None:
        return "Unable to get params: Expected json with (correo,password)", 406
    if Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": True}
    else:
        object_to_return = {"resp": False}

    return object_to_return, 200
