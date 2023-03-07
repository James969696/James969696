from flask import Flask, request, jsonify

app = Flask(__name__)
port = 5051

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json['data']
    command = data['command']
    message = data['message']
    response = message + '¯\_(ツ)_/¯'
    return jsonify({'data': {'command': command, 'message': response}})




@app.route('/register', methods=['POST'])
def register():
    data = request.json['data']
    command = data['command']
    server_url = data['server_url']
    # Save the mapping of command to server_url in a JSON file called "serverMapping.json"
    with open('serverMapping.json', 'r') as f:
        server_mapping = json.load(f)
    server_mapping[command] = server_url
    with open('serverMapping.json', 'w') as f:
        json.dump(server_mapping, f)
    # Return a JSON response indicating success
    return jsonify({'data': {'command': command, 'message': 'saved'}})


@app.route('/message', methods=['POST'])
def message():
    data = request.json['data']
    message = data['message']
    command = ''
    if message.startswith('/'):
        command, message = message.split(' ', 1)
        command = command[1:]
        # Check if there is a server registered for this command
        with open('serverMapping.json', 'r') as f:
            server_mapping = json.load(f)
        if command in server_mapping:
            # Forward the message to the appropriate server
            server_url = server_mapping[command]
            execute_endpoint = server_url + '/execute'
            response = requests.post(execute_endpoint, json={'data': {'command': command, 'message': message}})
            message = response.json


if __name__ == '__main__':
    app.run(port=port, debug=True)