import flask
import lib


app = flask.Flask("card_server")
card_storage = lib.CardStorage()


@app.route('/create', methods=['POST'])
def create_card():
    sum = int(flask.request.form['sum'])
    id = card_storage.create_card(sum)
    return str(id)


@app.route('/get_info', methods=['GET'])
def get_info():
    id = int(flask.request.form['id']) - 1
    return card_storage.get_info(id)


@app.route('/put', methods=['POST'])
def put():
    sum = int(flask.request.form['sum'])
    id = int(flask.request.form['id']) - 1
    card_storage.put(id, sum)


@app.route('/withdraw', methods=["POST"])
def withdraw():
    sum = int(flask.request.form['sum'])
    id = int(flask.request.form['id']) - 1
    card_storage.withdraw(id, sum)



def main():
    app.run('::', port=8000)



if __name__ == '__main__':
    main()