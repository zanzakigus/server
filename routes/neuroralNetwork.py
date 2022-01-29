import csv
import os
from os.path import exists

import numpy as np
import joblib

from utils.sharedFunctions import enconder
from sklearn.neural_network import MLPClassifier
from app import app, request, Usuario


# -----------------------------Receive Data Waves Route--------------------------------------
@app.route('/waves_data', methods=["POST"])
def waves_data():
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
    store_details = [payload.get('HIGH_ALPHA'), payload.get('LOW_GAMMA'), payload.get('LOW_ALPHA'),
                     payload.get('DELTA'), payload.get('MID_GAMMA'), payload.get('HIGH_BETA'), payload.get('LOW_BETA'),
                     payload.get('THETA')]
    correo = payload.get("correo")
    password = payload.get("password")
    tipo = payload.get("tipo")
    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if store_details[0] is None or store_details[1] is None or store_details[2] is None or store_details[3] is None or \
            store_details[4] is None or store_details[5] is None or \
            store_details[6] is None or store_details[7] is None or correo is None or password is None or tipo is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (HIGH_ALPHA, LOW_GAMMA, LOW_ALPHA, DELTA, MID_GAMMA, "
                       "HIGH_BETA, LOW_BETA, THETA, correo, password, tipo)",
            "status": 406
        }
        return object_to_return, 406

    os.makedirs("../static/user_files/" + correo, mode=0o777, exist_ok=False)
    with open('../static/user_files/' + correo + '/wavesdata.csv', 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(store_details)

    with open('../static/user_files/' + correo + '/tipos.csv', 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([tipo])
    object_to_return = {"message": "OK",
                        "status": 200}
    return object_to_return, 200


# -----------------------------Fit Neuronal Network Route--------------------------------------
@app.route('/fit_neuronal', methods=["POST"])
def fit_neuronal():
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

    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if correo is None or password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo, password)",
            "status": 406
        }
        return object_to_return, 406

    data = []
    with open('../static/user_files/' + correo + '/wavesdata.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    result = []
    with open('../static/user_files/' + correo + '/tipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)

    train_labels_enc = np.array(list(map(enconder, result)))
    print(train_labels_enc)
    # test = [16772230, 68543, 27557, 1514095, 78696, 146423, 72003, 394675]
    test_re = [0]
    # test_labels_enc = np.array(list(map(enconder, test_re)))

    # Tres capas ocultas de 20-150-20 neuronas respectivamente
    clf = MLPClassifier(hidden_layer_sizes=(20, 2))

    clf.fit(data, result)
    joblib.dump(clf, '../static/user_files/' + correo + '/my_model.pkl', compress=9)
    #    print(request.body);
    # data = {
    #    "score": clf.score(data, result),
    #    "age": 20,
    #    "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"]
    # }

    object_to_return = {"message": "OK",
                        "status": 200}
    return object_to_return, 200


# -----------------------------Classify Waves Route--------------------------------------
@app.route('/classify_neuronal', methods=["POST"])
def classify_neuronal():
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
    store_details = [payload.get('HIGH_ALPHA'), payload.get('LOW_GAMMA'), payload.get('LOW_ALPHA'),
                     payload.get('DELTA'), payload.get('MID_GAMMA'), payload.get('HIGH_BETA'), payload.get('LOW_BETA'),
                     payload.get('THETA')]
    correo = payload.get("correo")
    password = payload.get("password")
    tipo = payload.get("tipo")
    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if store_details[0] is None or store_details[1] is None or store_details[2] is None or store_details[3] is None or \
            store_details[4] is None or store_details[5] is None or \
            store_details[6] is None or store_details[7] is None or correo is None or password is None or tipo is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (HIGH_ALPHA, LOW_GAMMA, LOW_ALPHA, DELTA, MID_GAMMA, "
                       "HIGH_BETA, LOW_BETA, THETA, correo, password, tipo)",
            "status": 406
        }
        return object_to_return, 406

    clf = joblib.load('../static/user_files/' + correo + '/my_model.pkl')

    predict_label = clf.predict([store_details])[0]

    object_to_return = {"message": str(predict_label),
                        "status": 200}
    return object_to_return, 200


# -----------------------------Verify If Neuronal Network Exist Route--------------------------------------
@app.route('/exist_neuronal', methods=["POST"])
def exist_neuronal():
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

    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if correo is None or password is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (correo, password)",
            "status": 406
        }
        return object_to_return, 406

    file_exists = exists('../static/user_files/' + correo + '/my_model.pkl')

    message = "No file"
    if file_exists:
        message = "OK"

    object_to_return = {"message": message,
                        "status": 200}

    return object_to_return, 200
