from flask import jsonify
from flask_socketio import emit
import os
import subprocess
import threading
from datetime import datetime
from app import app, socketio, UPLOAD_FOLDER

current_process = None
current_server = None

def emit_console(message, type='info', server=None):
    timestamp = datetime.now().strftime('%H:%M:%S')
    prefix = f"[{timestamp}] "
    if server:
        prefix += f"[{server}] "
    
    socketio.emit('terminal_output', {
        'type': type,
        'message': prefix + message,
        'timestamp': timestamp,
        'server': server
    })

@app.route('/eula/<server>')
def accept_eula(server):
    try:
        eula_path = os.path.join(UPLOAD_FOLDER, server, 'eula.txt')
        with open(eula_path, 'w') as f:
            f.write('eula=true\n')
        return jsonify({'success': True, 'message': 'EULA aceita com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start/<server>')
def start_server(server):
    global current_process, current_server
    
    if current_process is not None and current_process.poll() is None:
        return jsonify({'error': 'Já existe um servidor em execução'}), 400

    def run_server():
        global current_process, current_server
        try:
            server_path = os.path.join(UPLOAD_FOLDER, server)
            jar_files = [f for f in os.listdir(server_path) if f.endswith('.jar')]
            
            if not jar_files:
                emit_console(f"Nenhum arquivo .jar encontrado no servidor {server}", 'error', server)
                return
            
            jar_file = jar_files[0]
            eula_file = os.path.join(server_path, 'eula.txt')
            
            if not os.path.exists(eula_file):
                with open(eula_file, 'w') as f:
                    f.write('eula=false\n')
                emit_console(f"Você precisa aceitar a EULA do servidor {server}", 'warning', server)
                return

            with open(eula_file, 'r') as f:
                if 'eula=true' not in f.read().lower():
                    emit_console(f"Você precisa aceitar a EULA do servidor {server}", 'warning', server)
                    return

            current_server = server
            emit_console("Iniciando servidor...", 'system', server)
            emit_console(f"Diretório: {server_path}", 'system', server)
            emit_console(f"Arquivo JAR: {jar_file}", 'system', server)
            
            java_cmd = ["java", "-Xmx1024M", "-jar", jar_file, "nogui"]
            emit_console(f"Comando: {' '.join(java_cmd)}", 'system', server)
            
            process = subprocess.Popen(
                java_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                cwd=server_path,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            current_process = process
            emit_console("Processo iniciado com sucesso", 'system', server)
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    line = line.strip()
                    msg_type = 'server'
                    
                    if 'error' in line.lower() or 'exception' in line.lower():
                        msg_type = 'error'
                    elif 'warn' in line.lower():
                        msg_type = 'warning'
                    elif 'info' in line.lower():
                        msg_type = 'info'
                    
                    emit_console(line, msg_type, server)
            
            if process.returncode != 0:
                emit_console(
                    f"O servidor foi encerrado com código {process.returncode}",
                    'error',
                    server
                )
            else:
                emit_console("Servidor encerrado normalmente", 'info', server)
            
            current_process = None
            current_server = None
            
        except Exception as e:
            emit_console(f"Erro ao executar o servidor: {str(e)}", 'error', server)
            current_process = None
            current_server = None

    threading.Thread(target=run_server, daemon=True).start()
    return jsonify({'success': True, 'message': f'Iniciando servidor {server}'})

@app.route('/stop')
def stop_server():
    global current_process, current_server
    if current_process and current_process.poll() is None:
        try:
            emit_console("Enviando sinal de parada para o servidor...", 'system', current_server)
            current_process.terminate()
            threading.Timer(2, lambda: current_process.kill() if current_process.poll() is None else None).start()
            emit_console("Servidor parado com sucesso", 'system', current_server)
            current_process = None
            current_server = None
            return jsonify({'success': True, 'message': 'Servidor parado com sucesso'})
        except Exception as e:
            return jsonify({'error': f'Erro ao parar o servidor: {str(e)}'}), 500
    return jsonify({'error': 'Nenhum servidor em execução'}), 400

@app.route('/status')
def server_status():
    return jsonify({
        'running': current_process is not None and current_process.poll() is None,
        'current_server': current_server
    })

@socketio.on('connect')
def handle_connect():
    emit_console('Conectado ao terminal', 'system')
    if current_server:
        emit_console(f'Servidor atual: {current_server}', 'system')
        if current_process and current_process.poll() is None:
            emit_console('Status: Servidor em execução', 'info')
        else:
            emit_console('Status: Servidor parado', 'warning')

@socketio.on('console_input')
def handle_console_input(data):
    if current_process and current_process.poll() is None:
        try:
            command = data.get('command', '').strip() + '\n'
            current_process.stdin.write(command)
            current_process.stdin.flush()
            emit_console(f"$ {command.strip()}", 'system', current_server)
        except Exception as e:
            emit_console(f"Erro ao enviar comando: {str(e)}", 'error', current_server)
    else:
        emit_console("Nenhum servidor em execução", 'error') 