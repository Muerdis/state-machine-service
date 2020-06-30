from flask import Flask, jsonify, abort
from transitions import Machine

app = Flask(__name__)

STATES = {
    'sleep_state': 'Сплю',
    'code_state': 'Пишу код',
    'eat_state': 'Ем печеньки'
}
ACTIONS = {
    'alarm_clock': 'Будильник',
    'tired': 'Устал',
    'hungry': 'Проголодался',
    'refreshing': 'Подкрепился',
    'overeat': 'Объелся'
}
TRANSACTIONS = [
    {'trigger': 'alarm_clock', 'source': 'sleep_state', 'dest': 'code_state'},
    {'trigger': 'tired', 'source': 'code_state', 'dest': 'sleep_state'},
    {'trigger': 'hungry', 'source': 'code_state', 'dest': 'eat_state'},
    {'trigger': 'refreshing', 'source': 'eat_state', 'dest': 'code_state'},
    {'trigger': 'overeat', 'source': 'eat_state', 'dest': 'sleep_state'},
]


class Developer(object):
    pass


developer = Developer()


@app.route('/api/developer/<state>/<action>', methods=['GET'])
def get_state_and_actions(state, action):
    if state not in STATES.keys() or action not in ACTIONS.keys():
        abort(400)

    machine = Machine(developer, states=list(STATES.keys()), transitions=TRANSACTIONS, initial=state)
    try:
        developer.trigger(action)
    except:
        abort(400)

    now_state = developer.state
    available_transactions = list(filter(lambda d: d['source'] == now_state, TRANSACTIONS))
    actions = []
    for av_transaction in available_transactions:
        actions.append({
            'key': av_transaction['trigger'],
            'value': ACTIONS[av_transaction['trigger']]
        })

    response = {
        'now_state': {
            'key': now_state,
            'value': STATES[now_state]
        },
        'actions': actions
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
