from flask import Blueprint, jsonify, request
import yt_dlp

bp = Blueprint('get_download_info', __name__)

@bp.route('/api/get-download-info', methods=['GET'])
def get_download_info():
    url = request.args.get('url')
    
    
    ydl_opts = {
        'noplaylist': True,
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    try:
        info = ydl.extract_info(url, download=False)
        response = {
            'id': info.get('id'),
            'title': info.get('title'),
            '_type': info.get('_type'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration'),
            'duration_string': info.get('duration_string'),
            'extractor': info.get('extractor'),
        }
        if info.get('_type', 'video') == 'video':
            formats = info.get('formats', [])
            
            response['detail_formats'] = get_detail_formats(formats)
            response['simple_formats'] = get_simple_formats(info.get('extractor'), formats)
            
            
        
        elif info.get('_type') == 'playlist':
            entries = info.get('entries', [])
            list_items = []
            for entry in entries:
                list_items.append({
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'thumbnail': entry.get('thumbnail'),
                    'original_url': entry.get('original_url')
                })
            response['listItems'] = list_items
        
        elif info.get('_type') == 'multi_video':
            entries = info.get('entries', [])
            multi_items = []
            for entry in entries:
                multi_items.append({
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'thumbnail': entry.get('thumbnail'),
                    'original_url': entry.get('original_url')
                })
            response['multiItems'] = multi_items

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def get_detail_formats(formats):
    formatted_formats = []
    for fmt in formats:
        formatted_formats.append({
            'ext': fmt.get('ext'),
            'format_id': fmt.get('format_id'),
            'url': fmt.get('url'),
            'vcodec': fmt.get('vcodec'),
            'acodec': fmt.get('acodec'),
            'filesize_approx': fmt.get('filesize_approx'),
            'audio_ext': fmt.get('audio_ext'),
            'video_ext': fmt.get('video_ext'),
            'format': fmt.get('format'),
            'resolution': fmt.get('resolution'),
        })
    
    return formatted_formats

def get_simple_formats(extractor, formats):
    detail_formats = get_detail_formats(formats)
    if extractor != 'youtube':
        return detail_formats
    
    
    simple_formats = []
    for fmt in detail_formats:
        
        #find audio only
        
        #find video only
        
        #find low resolution video with audio
        
        #find medium resolution video with audio
        
        #find best resolution video with audio
        
        
        simple_formats.append({

            'friendly_name': 'friendly_name'
        })
    
    return simple_formats



