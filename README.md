# 🕹️ SyntPanel

**SyntPanel** é um painel moderno para gerenciamento de servidores de jogos (foco em Minecraft), feito com **Python**, **Flask** e **Socket.IO**.

Agora com visual glassmorphism/cyberpunk, botões neon, animações suaves e experiência de usuário aprimorada!

---

## ✨ Novidades e Melhorias Recentes

- 🎨 **Novo visual glassmorphism/cyberpunk**: cards translúcidos, blur, gradientes e sombras modernas.
- 🌈 **Botões neon**: animações de brilho e gradiente em todos os botões.
- 🪟 **Modais e tabelas glass**: tudo com efeito translúcido e animações suaves.
- ⚡ **Hover animado** em menus, cards, arquivos e botões.
- 📱 **Responsividade aprimorada**: painel bonito em qualquer tela.
- 🔓 **Sem autenticação**: acesso livre e fácil para testes locais.
- 🧹 **Código CSS otimizado**: fácil de customizar e expandir.
- 🛠️ **Usabilidade**: navegação intuitiva, ícones modernos e feedback visual em todas as ações.

---

## 📺 Funcionalidades

- 📂 Upload de arquivos `.jar` e plugins
- 📄 Aceite automático do `eula.txt`
- 💬 Terminal ao vivo com logs do servidor
- 🗂️ Gerenciador de arquivos integrado
- 🖥️ Execução direta de servidores Minecraft
- ⚡ Interface web moderna, responsiva e animada

---

## 📁 Estrutura do Projeto

```
SyntPanel/
├── src/
│   ├── routes/
│   │   ├── file_routes.py         # Rotas de arquivos
│   │   └── server_routes.py       # Rotas de gerenciamento de servidores
│   ├── static/
│   │   └── css/custom.css         # CSS customizado (tema glass/neon)
│   ├── templates/
│   │   └── index.html             # Interface HTML principal
│   └── app.py                     # Servidor Flask principal
├── servers/                       # Diretório dos servidores gerenciados
```

---

## 🚀 Instalação e Uso

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/TheCoderZeus/SyntPanel
   cd SyntPanel/src
   ```
2. **(Opcional) Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # ou
   source venv/bin/activate # Linux/Mac
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicie o painel:**
   ```bash
   python app.py
   ```
5. **Acesse no navegador:**
   - [http://localhost:5000](http://localhost:5000)

---

## 🖌️ Customização Visual
- Todo o tema está em `src/static/css/custom.css`. Edite para mudar cores, animações e efeitos.
- O HTML principal está em `src/templates/index.html`.
- Para um tema ainda mais ousado, altere as variáveis CSS ou peça sugestões!

---

## 📝 Mudanças Recentes
- Removida autenticação e proteção de rotas para facilitar testes.
- Visual completamente renovado: glassmorphism, neon, animações, hover destacado.
- Melhoria de responsividade e usabilidade geral.
- Código CSS limpo e fácil de editar.

---

## 🤝 Contribuição
Pull requests são bem-vindos! Se quiser sugerir novos temas, recursos ou melhorias, abra uma issue ou envie sua contribuição.

---

## 📸 Screenshots
> ![Capturar](https://github.com/user-attachments/assets/59068c38-8018-408c-9b15-148524f0bfcc)
https://github.com/user-attachments/assets/597fb382-ed23-45d2-bcd1-232e17e969c0


---

## Licença
MIT
