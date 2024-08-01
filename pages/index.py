from flask import Blueprint, jsonify, render_template_string

import yt_dlp
import os
import json
import uuid
import threading


bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    # HTML template for the form
    form_template = '''
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Download</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <style>
        .custom-input {
            width: 80%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">URL Form</h1>
        <form id="urlForm" class="form-inline text-center" method="GET">
            <div class="form-group">
                <label for="url" class="sr-only">Enter URL:</label>
                <input type="text" id="url" name="url" class="form-control custom-input" placeholder="Enter URL" required>
            </div>
            <button type="button" class="btn btn-info" onclick="submitForm('/api/get-download-info')">Info</button>
            <button type="button" class="btn btn-primary" onclick="submitForm('/api/start-download')">Download</button>
        </form>
    </div>

    <script>
        function submitForm(action) {
            const form = document.getElementById('urlForm');
            const url = form.url.value;
            if (url) {
                const newTab = window.open(action + '?url=' + encodeURIComponent(url), '_blank');
                newTab.focus();
            } else {
                alert('Please enter a URL');
            }
        }
    </script>
</body>
</html>

    '''
    
    return render_template_string(form_template)
