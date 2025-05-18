# 🕹️ SyntPanel

**SyntPanel** é um painel de gerenciamento de servidores de jogos (com foco em Minecraft) desenvolvido com **Python**, **Flask** e **Socket.IO**.

Com ele, é possível enviar arquivos `.jar`, iniciar servidores com visualização do terminal em tempo real, aceitar automaticamente o EULA e organizar os servidores em pastas individuais.

---

## ✨ Funcionalidades

- 📂 Upload de arquivos `.jar`
- 📄 Aceite automático do `eula.txt`
- 💬 Terminal ao vivo com logs do servidor
- 🗂️ Organização de arquivos por servidor
- 🖥️ Execução direta de servidores Minecraft
- 🔧 Interface web simples, direta e funcional

---

## 📁 Estrutura do Projeto

```
SyntPanel/
├── app.py                  # Servidor Flask principal
├── templates/
│   └── index.html          # Interface HTML com terminal embutido
├── servers/                # Diretório onde os servidores são armazenados
└── README.md
```

---

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/TheCoderZeus/SyntPanel
   cd SyntPanel
   ```

2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install flask flask-socketio eventlet
   ```

4. Inicie o painel:
   ```bash
   python app.py
   ```
