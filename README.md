# 🎬 Alden Downloader

**Alden Downloader** é um aplicativo desktop desenvolvido em Python para baixar vídeos e áudios do YouTube. Ele oferece uma interface gráfica simples e intuitiva, suporte a múltiplas resoluções, conversão automática via FFmpeg e compatibilidade com qualquer link do YouTube.

## 🚀 Funcionalidades

- 🎥 Baixe vídeos em diversas resoluções (360p, 720p, 1080p, etc)
- 🎧 Extraia áudios em `.mp3` com qualidade otimizada
- 🔗 Suporte a qualquer tipo de URL do YouTube (incluindo playlists e parâmetros como `?si=`, `&list=`, etc.)
- 💻 Interface desenvolvida com `Tkinter`
- 📦 Executável standalone gerado com PyInstaller
- 🛠 Instalador profissional criado com Inno Setup

## 🖼 Captura de Tela

> Em breve uma imagem da interface gráfica

## 📦 Instalação

### ✅ Instalador (Windows)

1. Baixe `Setup_AldenDownloader.exe`
2. Execute o instalador
3. O programa será instalado em `C:\Arquivos de Programas\AldenDownloader`
4. Um atalho será criado na área de trabalho e no menu iniciar

### 🧪 Rodar pelo código-fonte

#### Pré-requisitos

- Python 3.10 ou superior
- `pip install yt-dlp`

#### Execução

```bash
python alden_downloader.py
```

## 🛠 Tecnologias Utilizadas

- Python
- Tkinter
- yt-dlp
- FFmpeg
- PyInstaller
- Inno Setup

## 🔧 Gerando o Executável

```bash
pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --icon=alden.ico --name "AldenDownloader" alden_downloader.py
```

## 📁 Estrutura do Projeto

```
Alden-Downloader/
├── dist/
│   └── AldenDownloader.exe
├── build/
├── alden_downloader.py
├── ffmpeg.exe
├── alden.ico
├── AldenDownloader.spec
└── README.md
```

## 📄 Licença

Distribuído sob a licença MIT.

## 🙋‍♂️ Autor

Desenvolvido por **Gerson Junior**  
[LinkedIn](https://www.linkedin.com)