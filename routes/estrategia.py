from app import app, request, Estrategia


@app.route('/estrategia', methods=["POST"])
def new_estrategia():
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
    estrategia_texto = payload.get("estrategia_texto")
    nombre_imagen = payload.get("nombre_imagen")
    if estrategia_texto is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (estrategia_texto,nombre_imagen)",
            "status": 406
        }
        return object_to_return, 406
    Estrategia.new(estrategia_texto, nombre_imagen)
    object_to_return = {"message": "OK",
                        "status": 200}
    return object_to_return, 200


@app.route('/estrategia', methods=["GET"])
def get_estrategiaes():
    if request.method != 'GET':
        return {
                   "message": "Not a get method",
                   "status": 400
               }, 400
    estrategias: [] = Estrategia.get_all()
    estrategiasSal: list = []
    for estrategia in estrategias:
        estrategiasSal.append(estrategia.to_dict())
    object_to_return = {"status": 200, "message": estrategiasSal}
    return object_to_return, 200
