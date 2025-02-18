from flask import Flask, request, jsonify
from database import DatabaseManager
import jwt
import datetime
import uuid

app = Flask(__name__)
db = DatabaseManager()

SECRET_KEY = uuid.uuid4().hex

@app.route('/register_server', methods=['POST'])
def register_server():
    server_data = {
        'id': str(uuid.uuid4()),
        'hostname': request.json['hostname'],
        'ip': request.remote_addr,
        'os_type': request.json['os_type'],
        'capabilities': request.json['capabilities'],
        'last_seen': datetime.datetime.utcnow().isoformat(),
        'token': jwt.encode(
            {'server_id': str(uuid.uuid4()), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)},
            SECRET_KEY,
            algorithm='HS256'
        )
    }
    db.add_server(server_data)
    return jsonify({'token': server_data['token']})

@app.route('/get_servers', methods=['GET'])
def get_servers():
    return jsonify(db.get_all_servers())

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=5000, 
        ssl_context=('cert.pem', 'key.pem')
    ) 