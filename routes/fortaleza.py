from app import app, request, Fortalezas,Usuario


@app.route('/fortalezas', methods=["POST"])
def new_fortalezas():
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
    strengths = payload.get("strengths")
    correo = payload.get("correo")
    password = payload.get("password")
    if strengths is None or correo is None or password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo, password, strengths)",
            "status": 406
        }
        return object_to_return, 406

    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    print(strengths)
    strengths = [x.replace(" ", "") for x in strengths.strip('[]').split(",")]
    Fortalezas.drop_by_user(correo)
    print(strengths)
    for strength in strengths:
        print(strength)
        Fortalezas.new(correo, strength)
    object_to_return = {
        "message": "OK",
        "status": 200
    }
    return object_to_return, 200


@app.route('/fortalezas', methods=["GET"])
def get_fortalezas():
    if request.method != 'GET':
        return {
                   "message": "Not a get method",
                   "status": 400
               }, 400
    payload: dict = request.args.to_dict()
    correo = payload.get("correo")
    password = payload.get("password")
    if password is None or correo is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo, password)",
            "status": 406
        }
        return object_to_return, 406

    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401

    fortalezas: [] = Fortalezas.get_by_user(correo)
    fortalezasSal: list = []
    for fortaleza in fortalezas:
        fortalezasSal.append(fortaleza.to_dict())
    object_to_return = {"status": 200, "message": fortalezasSal}
    return object_to_return, 200
