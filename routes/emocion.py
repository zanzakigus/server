from app import app, request, Emocion


@app.route('/emocion', methods=["POST"])
def new_emocion():
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
    emocion_texto = payload.get("emocion_texto")
    if emocion_texto is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (emocion_texto)",
            "status": 406
        }
        return object_to_return, 406
    Emocion.new(emocion_texto)
    object_to_return = {"resp":  True}
    return object_to_return, 200


@app.route('/emocion', methods=["GET"])
def get_emociones():
    if request.method != 'GET':
        return {
                   "message": "Not a get method",
                   "status": 400
               }, 400
    emociones: [] = Emocion.get_all()
    emocionesSal: list = []
    for emocion in emociones:
        emocionesSal.append(emocion.to_dict())
    object_to_return = {"status": 200, "message": emocionesSal}
    return object_to_return, 200
