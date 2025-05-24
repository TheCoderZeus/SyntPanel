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
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
current_process = None
current_server = None


@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir config.json do novo local
@app.route('/config.json', methods=['GET', 'POST'])
def config_json():
    config_path = os.path.join(config_dir, 'config.json')
    if request.method == 'POST':
        try:
            data = request.get_json()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        with open(config_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'application/json'}

from routes.file_routes import *
from routes.server_routes import *

# Exemplo de agendamento de tarefa: backup diário às 2h
# schedule_task('backup_diario', lambda: print('Backup!'), '0 2 * * *')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    print('Painel iniciado com autenticação, logging, agendamento e docs automáticas!')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 