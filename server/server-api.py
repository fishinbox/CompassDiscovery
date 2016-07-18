from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/machines', methods=['GET'])
def list_server():
	"""Get machine."""
	return 'eth0: 00:00:00:00:00:00'

@app.route('/machines', methods=['POST'])
def add_server():
        nics = request.get_json(force=True)#new method since flask 0.10
        print str(nics)
	return 'post ok!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888')
