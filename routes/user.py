from app import app, Usuario


@app.route('/test')
def version():
    Usuario.new_user("nini","onoino","bninin")
    return 'it wosrks!'
