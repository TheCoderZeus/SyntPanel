from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import os
import subprocess
from werkzeug.utils import secure_filename
import threading
import json
import sys
import time
import shutil
from datetime import datetime

UPLOAD_FOLDER = 'servers'
ALLOWED_EXTENSIONS = {'jar', 'zip'}
EDITABLE_EXTENSIONS = {'yml', 'yaml', 'txt', 'properties', 'json', 'conf', 'cfg'}

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
current_process = None
current_server = None

@app.route('/')
def index():
    return render_template('index.html')

from routes.file_routes import *
from routes.server_routes import *

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 