from app import app, Usuario, request


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
    object_to_return = {"resp":  True}
    return object_to_return, 200


@app.route('/login', methods=["POST"])
def login():
    if request.method != 'POST':
        return "not a post method", 400
    if not request.is_json:
        return "not json", 415
    payload: dict = request.get_json(force=True)

    print(request.args.get("Pass"))
    correo = payload.get("correo")
    password = payload.get("password")
    if correo is None or password is None:
        return "Unable to get params: Expected json with (correo,password)", 406
    object_to_return = {"resp":  True}
    return object_to_return, 200
