from flask import Blueprint, jsonify
import os
import json

bp = Blueprint('session_status', __name__)
STATUS_FOLDER = 'status'

@bp.route('/api/session-status/<sessionId>', methods=['GET'])
def session_status(sessionId):
    status_file = os.path.join(STATUS_FOLDER, f'{sessionId}.json')
    
    if not os.path.exists(status_file):
        return jsonify({'error': 'Session not found'}), 404
    
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    return jsonify(status), 200
