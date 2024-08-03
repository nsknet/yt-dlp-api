import json
from flask import Blueprint, jsonify, request, send_file
import os

bp = Blueprint('download_file', __name__)
STATUS_FOLDER = 'status'

@bp.route('/api/download-file/<sessionId>', methods=['GET'])
def download_file(sessionId):
    status_file = os.path.join(STATUS_FOLDER, f'{sessionId}.json')
    
    if not os.path.exists(status_file):
        return jsonify({'error': 'Session not found'}), 404
    
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    if status['step'] != 'Finished':
        return jsonify({'error': 'File download not complete yet'}), 400
    
    file_path = status.get('fileName')
    fileName = request.args.get('fileName')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    if fileName:
        # Extract the extension from the file_path
        ext = os.path.splitext(file_path)[1]
        # Create the new file name with the given name and original extension
        custom_file_name = f"{fileName}{ext}"
    else:
        custom_file_name = os.path.basename(file_path)

    return send_file(file_path, as_attachment=True, download_name=custom_file_name)

