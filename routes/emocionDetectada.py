from app import app, request, EmocionDetectada


@app.route('/emocion_detectada', methods=["POST"])
def new_emocion_detectada():
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
    id_emocion = payload.get("id_emocion")
    correo = payload.get("correo")
    id_estrategia = payload.get("id_estrategia")
    if id_emocion is None or correo is None or id_estrategia is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (id_emocion, correo, id_estrategia)",
            "status": 406
        }
        return object_to_return, 406
    EmocionDetectada.new(id_emocion, correo, id_estrategia)
    object_to_return = {"message": "OK",
                        "status": 200}
    return object_to_return, 200


@app.route('/emocion_detectada', methods=["GET"])
def get_emociones_detectadas():
    if request.method != 'GET':
        return {
                   "message": "Not a get method",
                   "status": 400
               }, 400

    emocionesDetectadas: [] = EmocionDetectada.get_all()
    emocionesDetectadasSal: list = []
    for emocion in emocionesDetectadas:
        emocionesDetectadasSal.append(emocion.to_dict())
    object_to_return = {"status": 200, "message": emocionesDetectadasSal}
    return object_to_return, 200
