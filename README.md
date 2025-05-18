# 🕹️ SyntPanel

**SyntPanel** é um painel de gerenciamento de servidores Minecraft feito em **Python** com **Flask** e **Socket.IO**, perfeito para rodar em ambientes leves como **Termux com proot-distro Ubuntu**.  
Ele permite upload de arquivos `.jar`, execução do servidor com visualização do terminal, aceite do EULA, e organização dos servidores em pastas.

## ✨ Recursos
- Upload de arquivos `.jar`
- Aceite automático do EULA
- Terminal ao vivo com log do servidor
- Organização por pasta
- Interface leve e funcional

## 🚀 Instalação
```bash
apt update && apt install unzip git python3-venv -y
git clone https://github.com/TheCoderZeus/SyntPanel
cd SyntPanel
python3 -m venv venv
source venv/bin/activate
pip install flask flask-socketio eventlet
python app.py
```

## 🌐 Acesso
Abra `http://localhost:5000` no navegador ou use o IP do seu celular para acessar de outro dispositivo.
