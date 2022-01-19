from app import app, request, Emocion


@app.route('/emocion', methods=["POST"])
def new_emocion():
    if request.method != 'POST':
        return "not a post method", 400
    if not request.is_json:
        return "not json", 415
    payload: dict = request.get_json(force=True)
    emocion_texto = payload.get("emocion_texto")
    if emocion_texto is None:
        return "Unable to get params: Expected json with (emocion_texto)", 406
    Emocion.new(emocion_texto)
    object_to_return = {"resp":  True}
    return object_to_return, 200


@app.route('/emocion', methods=["GET"])
def get_emociones():
    if request.method != 'GET':
        return "not a post method", 400
    emociones: [] = Emocion.get_all()
    emocionesSal: list = []
    for emocion in emociones:
        emocionesSal.append(emocion.to_dict())
    object_to_return = {"resp":  True, "contenido": emocionesSal}
    return object_to_return, 200
