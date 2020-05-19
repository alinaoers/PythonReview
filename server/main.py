import flask
import lib


PORT = 8000


app = flask.Flask("card_server")
card_storage = lib.CardStorage()


@app.route('/create', methods=['POST'])
def create_card():
    sum = int(flask.request.form['sum'])
    card_id = card_storage.create_card(sum)
    return str(card_id)


@app.route('/get_info', methods=['GET'])
def get_info():
    card_id = int(flask.request.form['id']) - 1
    return card_storage.get_info(card_id)


@app.route('/put', methods=['POST'])
def put():
    sum = int(flask.request.form['sum'])
    card_id = int(flask.request.form['id']) - 1
    card_storage.put(card_id, sum)


@app.route('/withdraw', methods=["POST"])
def withdraw():
    sum = int(flask.request.form['sum'])
    card_id = int(flask.request.form['id']) - 1
    card_storage.withdraw(card_id, sum)


def main():
    app.run('::', port=PORT)


if __name__ == '__main__':
    main()
    