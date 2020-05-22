import flask
import lib


PORT = 8000
DEFAULT_HOST = 'localhost'


app = flask.Flask("card_server")
card_storage = lib.CardStorage()


@app.route('/create', methods=['POST'])
def create_card():
    card_sum = int(flask.request.form['sum'])
    card_id = card_storage.create_card(card_sum)
    return str(card_id)


@app.route('/get_info', methods=['GET'])
def get_info():
    card_id = int(flask.request.form['id'])
    return card_storage.get_info(card_id)


@app.route('/put', methods=['POST'])
def put():
    card_sum = int(flask.request.form['sum'])
    card_id = int(flask.request.form['id'])
    card_storage.put(card_id, card_sum)


@app.route('/withdraw', methods=["POST"])
def withdraw():
    card_sum = int(flask.request.form['sum'])
    card_id = int(flask.request.form['id'])
    card_storage.withdraw(card_id, card_sum)


def main():
    app.run(DEFAULT_HOST, port=PORT)


if __name__ == '__main__':
    main()
