from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app import app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, EDITABLE_EXTENSIONS, current_server
import shutil

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_editable_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EDITABLE_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    server_name = request.form.get('server_name')
    
    if not server_name:
        return jsonify({'error': 'Nome do servidor é obrigatório'}), 400
    
    server_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(server_name))
    os.makedirs(server_path, exist_ok=True)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(server_path, filename))
        return jsonify({'success': True, 'message': 'Arquivo enviado com sucesso'})
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

@app.route('/upload-file/<path:path>', methods=['POST'])
def upload_to_directory(path):
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if not file:
        return jsonify({'error': 'Arquivo inválido'}), 400
    
    try:
        target_dir = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(target_dir):
            return jsonify({'error': 'Diretório não encontrado'}), 404
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(target_dir, filename))
        return jsonify({'success': True, 'message': 'Arquivo enviado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/servers')
def list_servers():
    try:
        servers = []
        if os.path.exists(UPLOAD_FOLDER):
            for server in os.listdir(UPLOAD_FOLDER):
                server_path = os.path.join(UPLOAD_FOLDER, server)
                if os.path.isdir(server_path):
                    jar_files = [f for f in os.listdir(server_path) if f.endswith('.jar')]
                    servers.append({
                        'name': server,
                        'type': 'directory',
                        'path': server,
                        'has_jar': len(jar_files) > 0
                    })
        return jsonify(servers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/servers/<path:path>')
def list_files(path):
    try:
        full_path = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(full_path):
            return jsonify({'error': 'Caminho não encontrado'}), 404

        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            items.append({
                'name': item,
                'type': 'directory' if is_dir else 'file',
                'path': os.path.join(path, item).replace('\\', '/'),
                'is_editable': not is_dir and is_editable_file(item)
            })
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file/<path:path>', methods=['GET', 'POST'])
def handle_file(path):
    try:
        full_path = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(full_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        if not is_editable_file(full_path):
            return jsonify({'error': 'Tipo de arquivo não suportado para edição'}), 400

        if request.method == 'GET':
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content

        elif request.method == 'POST':
            content = request.json.get('content')
            if content is None:
                return jsonify({'error': 'Conteúdo não fornecido'}), 400

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return jsonify({'success': True, 'message': 'Arquivo salvo com sucesso'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:path>')
def download_file(path):
    try:
        full_path = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/delete/<path:path>', methods=['DELETE'])
def delete_item(path):
    try:
        full_path = os.path.join(UPLOAD_FOLDER, path)
        
        if not os.path.exists(full_path):
            return jsonify({'error': 'Arquivo ou pasta não encontrado'}), 404
            
        if os.path.isfile(full_path):
            os.remove(full_path)
            return jsonify({'success': True, 'message': 'Arquivo deletado com sucesso'})
        elif os.path.isdir(full_path):
            if current_server and current_server == path.split('/')[0]:
                return jsonify({'error': 'Não é possível deletar um servidor em execução'}), 400
            shutil.rmtree(full_path)
            return jsonify({'success': True, 'message': 'Pasta/Servidor deletado com sucesso'})
            
    except Exception as e:
        return jsonify({'error': f'Erro ao deletar: {str(e)}'}), 500 