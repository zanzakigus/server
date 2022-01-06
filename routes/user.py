from app import app, Usuario


@app.route('/test')
def version():
    Usuario.new("nini","onoino","bninin")
    #Usuario.__generate_pass("1","1")
    return 'it wosrks!'
