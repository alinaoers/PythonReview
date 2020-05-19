import requests
import argparse


PORT = 8000
WRONG_ID = -1
DEFAULT_SUM = 0


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=PORT, type=int)

    return  parser


def finish():
    ask = input('Are you sure you want to leave (YES/NO)?')
    if ask == 'YES':
        print('Goodbye!')
        exit()
    elif ask == 'NO':
        print('OK, let\'s continue')
    else:
        print('Incorrect input, but continue')


def check_correct(user_input, name):
    def_val = (WRONG_ID if name == "id" else DEFAULT_SUM)

    if not user_input:
        return def_val
    else:
        try:
            return int(user_input)
        except ValueError:
            print('Incorrect input, assuming default {}'.format(def_val))
            return def_val


def ask_sum():
    user_input = input('How much money do you want to put/withdraw?>')
    return check_correct(user_input, "sum")


def ask_id():
    user_input = input("What's you id?")
    return check_correct(user_input, "id")


def correct_id():
    card_id = ask_id()
    while card_id == WRONG_ID:
        input("Input correct id")
        card_id = ask_id()
    return card_id


def server(main_args):
    return 'http://{}:{}/'.format(main_args.host, main_args.port)


def create_card(main_args):
    card_id = requests.post(server(main_args) + 'create', data=dict(sum=ask_sum())).text
    print('Your ID: {}'.format(card_id))


def get_info(main_args):
    info = requests.get(server(main_args) + 'get_info', data=dict(id=correct_id())).text
    print(info)


def put(main_args):
    requests.post(server(main_args) + 'put', data=dict(
        sum=ask_sum(),
        id=correct_id()
    ))


def withdraw(main_args):
    requests.post(server(main_args) + 'withdraw', data=dict(
        sum=ask_sum(),
        id=correct_id()
    ))


def main():
    parser = create_main_parser()
    main_args = parser.parse_args()
    while True:
        try:
            cmd = input('Input command>')
            if cmd == 'create':
                create_card(main_args)
            elif cmd == 'get info':
                get_info(main_args)
            elif cmd == 'put':
                put(main_args)
            elif cmd == 'withdraw':
                withdraw(main_args)
            elif cmd == 'exit':
                finish()
        except KeyboardInterrupt:
            finish()
            break


if __name__ == '__main__':
    main()
