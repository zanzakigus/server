from app import app, Usuario, request


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
    if correo is None or nombre is None or ap_paterno is None or ap_materno is None or password is None or fecha_nacimiento is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password,fecha_nacimiento)",
            "status": 406
        }
        return object_to_return, 406
    
    Usuario.new(correo, nombre, ap_paterno, ap_materno, password, fecha_nacimiento)
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
    if Usuario.validate_credentials(correo, password):
        new_usuario: Usuario = Usuario.get_by_id(correo)
        object_to_return = {"resp": True,
                            "contenido": new_usuario.to_dict(),
                            "message": "OK",
                            "status": 200}
    else:
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}

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
        Usuario.updateInfo(_id=correo, ap_materno=ap_materno, ap_paterno=ap_paterno, fecha_nacimiento=fecha_nacimiento, nombre=nombre)
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
    
    if correo is None or password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo,nombre,ap_paterno,ap_materno,password,fecha_nacimiento)",
            "status": 406
        }
        return object_to_return, 406
    
    if Usuario.validate_credentials(correo, password):
        Usuario.updatePassword(_id=correo, password=password)
        object_to_return = {"message": "OK",
                            "status": 200}
    else:
        object_to_return = {"message": "Unauthorized",
                            "status": 401}

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
        object_to_return = {"message": "Unauthorized",
                            "status": 401}

    return object_to_return, 200
