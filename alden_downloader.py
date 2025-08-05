import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os
import sys

class AldenDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Alden Downloader")
        self.root.geometry("640x500")
        self.root.resizable(False, False)

        self.url = tk.StringVar()
        self.save_path = tk.StringVar()
        self.format_type = tk.StringVar(value="video")
        self.available_formats = []
        self.selected_format = tk.StringVar()

        self.ffmpeg_path = self.get_ffmpeg_path()
        self.build_interface()

    def get_ffmpeg_path(self):
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        ffmpeg = os.path.join(base, 'ffmpeg.exe')
        if not os.path.exists(ffmpeg):
            messagebox.showerror("Erro", "ffmpeg.exe não encontrado na pasta do aplicativo.")
        return ffmpeg

    def build_interface(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="🔗 URL do YouTube:").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.url, width=80).pack(pady=5)

        options = ttk.Frame(frame)
        options.pack(anchor="w", pady=5)
        ttk.Radiobutton(options, text="🎥 Vídeo", variable=self.format_type, value="video").pack(side="left", padx=5)
        ttk.Radiobutton(options, text="🎧 Áudio", variable=self.format_type, value="audio").pack(side="left", padx=5)

        ttk.Button(frame, text="📋 Listar formatos", command=self.list_formats).pack(pady=10)

        ttk.Label(frame, text="📐 Escolha o formato / resolução:").pack(anchor="w")
        self.format_menu = ttk.OptionMenu(frame, self.selected_format, "")
        self.format_menu.pack(pady=5, fill="x")

        ttk.Button(frame, text="📁 Selecionar pasta", command=self.select_folder).pack(pady=10)
        ttk.Label(frame, textvariable=self.save_path, foreground="gray").pack(anchor="w")

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=20)

        self.status_label = ttk.Label(frame, text="", foreground="blue")
        self.status_label.pack()

        ttk.Button(frame, text="⬇️ Baixar", command=self.start_download_thread).pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)

    def list_formats(self):
        url = self.url.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Insira uma URL válida.")
            return

        try:
            self.available_formats.clear()
            menu = self.format_menu["menu"]
            menu.delete(0, "end")

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'noplaylist': True,
                'no_color': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])

                best_audio = None
                best_audio_bitrate = 0

                # Procurar o melhor áudio disponível
                for f in formats:
                    if f.get("vcodec") == "none" and f.get("acodec") != "none":
                        abr = f.get("abr", 0)
                        if abr > best_audio_bitrate:
                            best_audio = f['format_id']
                            best_audio_bitrate = abr

                # Listar vídeos com ou sem áudio e juntar com o melhor áudio
                for f in formats:
                    has_video = f.get("vcodec") != "none"
                    has_audio = f.get("acodec") != "none"

                    if self.format_type.get() == "video" and has_video:
                        resolution = f.get("height", "?")
                        ext = f.get("ext", "")
                        video_id = f["format_id"]
                        final_format = f"{video_id}+{best_audio}" if not has_audio else video_id
                        label = f"{video_id} - {resolution}p {ext} {'(sem áudio)' if not has_audio else ''}"
                        self.available_formats.append((label, final_format))
                        menu.add_command(label=label, command=lambda val=label: self.selected_format.set(val))

                    elif self.format_type.get() == "audio" and not has_video and has_audio:
                        label = f"{f['format_id']} - {f.get('abr', '??')}kbps {f['ext']}"
                        self.available_formats.append((label, f['format_id']))
                        menu.add_command(label=label, command=lambda val=label: self.selected_format.set(val))

                if self.available_formats:
                    self.selected_format.set(self.available_formats[0][0])
                    messagebox.showinfo("Sucesso", f"{len(self.available_formats)} formatos encontrados!")
                else:
                    raise Exception("Nenhum formato encontrado.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar formatos:\n{e}")

    def start_download_thread(self):
        thread = threading.Thread(target=self.download)
        thread.start()

    def download(self):
        url = self.url.get().strip()
        folder = self.save_path.get().strip()
        selected_label = self.selected_format.get()

        if not url or not folder or not selected_label:
            messagebox.showerror("Erro", "Preencha todos os campos antes de baixar.")
            return

        format_id = None
        for label, fid in self.available_formats:
            if selected_label == label:
                format_id = fid
                break

        self.status_label.config(text="Iniciando download...")
        self.progress["value"] = 0

        def hook(d):
            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0.0%').strip().replace('%', '')
                try:
                    percent = float(percent_str)
                    self.progress["value"] = percent
                    self.status_label.config(text=f"Progresso: {percent:.1f}%")
                except:
                    pass
            elif d['status'] == 'finished':
                self.progress["value"] = 100
                self.status_label.config(text="Download completo!")
                messagebox.showinfo("Sucesso", "Download finalizado com sucesso!")

        ydl_opts = {
            'ffmpeg_location': self.ffmpeg_path,
            'format': format_id,
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [hook],
            'quiet': True,
            'no_color': True
        }

        if self.format_type.get() == "audio":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['merge_output_format'] = 'mp4'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no download:\n{e}")
            self.status_label.config(text="Erro no download")

if __name__ == "__main__":
    root = tk.Tk()
    app = AldenDownloader(root)
    root.mainloop()
