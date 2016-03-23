from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/servers', methods=['GET','POST'])
def servers():
    if request.method == 'POST':
    	return 'post ok!'
    else:
    	return 'eth0: 00:00:00:00:00:00'

if __name__ == '__main__':
    app.run()
