from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def process_message():
    data = request.get_json(force=True)
    message = data['data']
    if message.startswith('/'):
        command, _, message = message[1:].partition(' ')
        response_data = {'command': command, 'message': message}
    else:
        response_data = {'command': None, 'message': message}
    response = {'data': json.dumps(response_data)}
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
