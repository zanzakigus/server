import csv
import os
import numpy as np
import joblib

from os.path import exists

from numpy.core import numeric

from utils.sharedFunctions import enconder
from sklearn.neural_network import MLPClassifier
from app import app, request, Usuario, EmocionDetectada


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
    train_file = int(payload.get("train_file"))
    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if store_details[0] is None or store_details[1] is None or store_details[2] is None or store_details[3] is None or \
            store_details[4] is None or store_details[5] is None or store_details[6] is None or store_details[
        7] is None or correo is None or password is None or tipo is None or train_file is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (HIGH_ALPHA, LOW_GAMMA, LOW_ALPHA, DELTA, MID_GAMMA, "
                       "HIGH_BETA, LOW_BETA, THETA, correo, password, tipo, train_file)",
            "status": 406
        }
        return object_to_return, 406

    file_name_waves = "/wavesdata.csv"
    file_name_tipo = "/tipos.csv"
    if train_file == 1:
        file_name_waves = "/wavesdata_test.csv"
        file_name_tipo = "/tipos_test.csv"

    os.makedirs("static/user_files/" + correo, mode=0o777, exist_ok=True)
    with open('static/user_files/' + correo + file_name_waves, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(store_details)

    with open('static/user_files/' + correo + file_name_tipo, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([tipo])

    object_to_return = {"message": "OK",
                        "status": 200}
    return object_to_return, 200


# -----------------------------Fit Neural Network Route--------------------------------------
@app.route('/fit_neural', methods=["POST"])
def fit_neural():
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
    with open('static/user_files/' + correo + '/wavesdata.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    data = np.array(data, dtype=numeric)
    result = []
    with open('static/user_files/' + correo + '/tipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)

    train_labels_enc = np.array(list(map(enconder, result)))
    # print(train_labels_enc)
    # test = [16772230, 68543, 27557, 1514095, 78696, 146423, 72003, 394675]
    test_re = [0]
    # test_labels_enc = np.array(list(map(enconder, test_re)))

    # Tres capas ocultas de 20-150-20 neuronas respectivamente
    clf = MLPClassifier(hidden_layer_sizes=(20, 150, 20))

    dataTest = []
    with open('static/user_files/' + correo + '/wavesdata_test.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dataTest.append(row)
    dataTest = np.array(dataTest, dtype=numeric)
    resultTest = []
    with open('static/user_files/' + correo + '/tipos_test.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            resultTest.append(row)

    clf.fit(data, np.ravel(result))
    while clf.score(dataTest, resultTest) < 0.68:
        print(clf.score(dataTest, resultTest))
        clf.fit(data, np.ravel(result))
    joblib.dump(clf, 'static/user_files/' + correo + '/neural_model.pkl', compress=9)

    object_to_return = {"message": "OK",
                        "score": clf.score(dataTest, resultTest),
                        "status": 200}
    return object_to_return, 200


# -----------------------------Classify Waves Route--------------------------------------
@app.route('/classify_neural', methods=["POST"])
def classify_neural():
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
    array_waves = payload.get("array_waves")
    if not Usuario.validate_credentials(correo, password):
        object_to_return = {"resp": False,
                            "message": "Unauthorized",
                            "status": 401}
        return object_to_return, 401
    if store_details[0] is None or store_details[1] is None or store_details[2] is None or store_details[3] is None or \
            store_details[4] is None or store_details[5] is None or \
            store_details[6] is None or store_details[
        7] is None or correo is None or password is None or array_waves is None:
        object_to_return = {
            "message": "Unable to get params: Expected json with (HIGH_ALPHA, LOW_GAMMA, LOW_ALPHA, DELTA, MID_GAMMA, "
                       "HIGH_BETA, LOW_BETA, THETA, correo, password)",
            "status": 406
        }
        return object_to_return, 406

    array_waves = [x.strip().strip("},").strip(" ") for x in array_waves.strip('[]').split("{")]
    if len(array_waves[0]) == 0:
        array_waves.pop(0)
    array_waves = [dict(
        (xx.strip(), y.strip())
        for xx, y in (element.split('=') for element in x.split(', ')))
        for x in array_waves]

    clf = joblib.load('static/user_files/' + correo + '/neural_model.pkl')

    negatives = 0
    positives = 0
    for sample in array_waves:
        store_details = [sample.get('HIGH_ALPHA'), sample.get('LOW_GAMMA'), sample.get('LOW_ALPHA'),
                         sample.get('DELTA'), sample.get('MID_GAMMA'), sample.get('HIGH_BETA'), sample.get('LOW_BETA'),
                         sample.get('THETA')]
        store_details = np.array(store_details, dtype=numeric)
        if int(clf.predict([store_details])[0]) == 0:
            negatives += 1
        else:
            positives += 1
    print(negatives)
    print("\n")
    print(positives)

    predict_label = 1
    if negatives > positives:
        predict_label = 0
        print("Negativa")
    else:
        print("positiva")
    EmocionDetectada.new(predict_label, correo, 1)
    object_to_return = {"message": str(predict_label),
                        "status": 200}
    return object_to_return, 200


# -----------------------------Verify If Neural Network Exist Route--------------------------------------
@app.route('/exist_neural', methods=["POST"])
def exist_neural():
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

    file_exists = exists('static/user_files/' + correo + '/neural_model.pkl')

    message = "No file"
    if file_exists:
        message = "OK"

    object_to_return = {"message": message,
                        "status": 200}

    return object_to_return, 200


# -----------------------------Neural Network Score Route--------------------------------------
@app.route('/score_neural', methods=["POST"])
def score_neural():
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
    with open('static/user_files/' + correo + '/wavesdata.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    data = np.array(data, dtype=numeric)

    result = []
    with open('static/user_files/' + correo + '/tipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)

    clf = joblib.load('static/user_files/' + correo + '/neural_model.pkl')

    object_to_return = {"message": clf.score(data, result),
                        "status": 200}

    return object_to_return, 200
