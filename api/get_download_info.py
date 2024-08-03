from flask import Blueprint, jsonify, request
import yt_dlp

bp = Blueprint('get_download_info', __name__)

@bp.route('/api/get-download-info', methods=['GET'])
def get_download_info():
    url = request.args.get('url')
    
    
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    try:
        info = ydl.extract_info(url, download=False)
        response = {
            'id': info.get('id'),
            'title': info.get('title'),
            '_type': info.get('_type', 'video'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration'),
            'duration_string': info.get('duration_string'),
            'extractor': info.get('extractor'),
            'url': url
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
    if extractor == 'youtube':
        simple_formats = []
    
            
        #Best + fastest video
        # simple_formats.append({
        #     'format_description': 'Best + fastest video',
        #     'format_id': 'best',
        #     'ext': None,
        #     'url': None,
        # })
        
        
        #Audio only
        simple_formats.append({
            'format_description': 'Audio only',
            'format_id': 'bestaudio[abr<=128]',
            'ext': None,
            'url': None,
        })
        #SD Video
        simple_formats.append({
            'format_description': 'SD Video',
            'format_id': 'worstvideo/worstaudio',
            'ext': None,
            'url': None,
        })
        
        #HD Video
        simple_formats.append({
            'format_description': 'HD Video',
            'format_id': 'bestvideo[height<=720]+bestaudio/best',
            'ext': None,
            'url': None,
        })
        
        #Best Video
        simple_formats.append({
            'format_description': 'Best Video',
            'format_id': 'bestvideo+bestaudio/best',
            'ext': None,
            'url': None,
        })
            
            
        return simple_formats
    
    else:
        simple_formats = []
        for fmt in formats:
            simple_formats.append({
                'format_description': fmt.get('format'),
               'format_id': fmt.get('format_id'),
                'ext': fmt.get('ext'),
                # 'url': fmt.get('url'),            
            
            })
        return simple_formats
    



