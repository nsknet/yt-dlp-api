from flask import Blueprint, jsonify, request
import yt_dlp

bp = Blueprint('get_download_json', __name__)

@bp.route('/api/get-download-json', methods=['GET'])
def get_download_info():
    url = request.args.get('url')
    
    
    ydl_opts = {
        'noplaylist': True,
    }    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    try:
        info = ydl.extract_info(url, download=False)
        return jsonify(info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
