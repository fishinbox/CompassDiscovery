from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/servers', methods=['GET'])
def list_server():
	"""Get machine."""
	return 'eth0: 00:00:00:00:00:00'

@app.route('/servers', methods=['POST'])
def add_server():
        nics = request.get_json()
        print str(nics)
	return 'post ok!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888')
