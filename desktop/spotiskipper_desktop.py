import customtkinter as ctk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys
from dotenv import load_dotenv
import threading
import time
from PIL import Image
import tkinter as tk
import ctypes
import win32gui
import win32con
import win32api

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        return os.path.dirname(sys.executable)
    else:
        # Se estiver rodando como script Python
        return os.path.dirname(os.path.abspath(__file__))

# Carrega as variáveis de ambiente do arquivo .env
env_path = os.path.join(get_base_path(), '.env')
load_dotenv(env_path)

class SpotiSkipper(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("SPOTSKIPPAR")
        self.geometry("400x600")
        self.configure(fg_color="#000000")
        
        # Define o ícone da janela
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            try:
                # Tenta definir o ícone usando diferentes métodos
                self.after(100, lambda: self.wm_iconbitmap(icon_path))
                self.after(200, lambda: self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=icon_path.replace('.ico', '.png'))))
            except Exception as e:
                print(f"Erro ao definir ícone: {e}")
            
        # Variáveis
        self.auto_skip_enabled = True  # Auto-skip ativado por padrão
        self.seconds_left = 82  # Timer ajustado para 82 segundos
        self.current_track = None
        
        try:
            # Inicializa o cliente Spotify
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                scope='user-modify-playback-state user-read-playback-state user-library-modify'
            ))
            
            # Testa a conexão
            self.sp.current_user()
            
        except Exception as e:
            self.show_error(f"Erro na autenticação: {str(e)}")
            sys.exit(1)

        # Interface
        self.create_widgets()
        
        # Inicia threads de atualização
        self.start_update_threads()

    def create_widgets(self):
        # Container principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="SPOTSKIPPAR",
            font=("Segoe UI", 32, "bold"),
            text_color="#00ff00"
        )
        self.title_label.pack(pady=20)

        # Frame da musica atual
        self.now_playing_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#111111",
            border_color="#00ff00",
            border_width=1,
            corner_radius=10
        )
        self.now_playing_frame.pack(pady=20, padx=20, fill="x")

        self.now_playing_label = ctk.CTkLabel(
            self.now_playing_frame,
            text="Tocando Agora:",
            font=("Segoe UI", 18),
            text_color="#00ff00"
        )
        self.now_playing_label.pack(pady=10)

        self.song_label = ctk.CTkLabel(
            self.now_playing_frame,
            text="Carregando...",
            font=("Segoe UI", 16),
            text_color="#ffffff"
        )
        self.song_label.pack(pady=5)

        self.artist_label = ctk.CTkLabel(
            self.now_playing_frame,
            text="",
            font=("Segoe UI", 14),
            text_color="#888888"
        )
        self.artist_label.pack(pady=5)

        # Botões
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=20)

        self.skip_button = ctk.CTkButton(
            self.buttons_frame,
            text="Pular Música",
            font=("Segoe UI", 14),
            fg_color="#00ff00",
            text_color="#000000",
            hover_color="#00cc00",
            command=self.skip_track
        )
        self.skip_button.pack(pady=10)

        self.hell_yeah_button = ctk.CTkButton(
            self.buttons_frame,
            text="HELL YES!",
            font=("Segoe UI", 14, "bold"),
            fg_color="#ff3300",
            text_color="#ffffff",
            hover_color="#cc2900",
            command=self.hell_yeah
        )
        self.hell_yeah_button.pack(pady=10)

        self.auto_skip_button = ctk.CTkButton(
            self.buttons_frame,
            text="AUTO SKIP: ON",  # Texto inicial ajustado
            font=("Segoe UI", 14),
            fg_color="#00ff00",  # Cor inicial verde
            text_color="#000000",
            hover_color="#00cc00",
            command=self.toggle_auto_skip
        )
        self.auto_skip_button.pack(pady=10)

        self.timer_label = ctk.CTkLabel(
            self.buttons_frame,
            text="",
            font=("Segoe UI", 14),
            text_color="#00ff00"
        )
        self.timer_label.pack(pady=5)

    def update_now_playing(self):
        while True:
            try:
                playback = self.sp.current_playback()
                if playback and playback['item']:
                    track = playback['item']
                    self.current_track = {
                        'id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name']
                    }
                    
                    # Atualiza a interface
                    self.song_label.configure(text=track['name'])
                    self.artist_label.configure(text=track['artists'][0]['name'])
                else:
                    self.song_label.configure(text="Nenhuma música tocando")
                    self.artist_label.configure(text="")
                    self.current_track = None
            except Exception as e:
                print(f"Erro ao atualizar música: {e}")
            
            time.sleep(5)

    def update_timer(self):
        while True:
            if self.auto_skip_enabled and self.current_track:  # Só conta se houver música tocando
                if self.seconds_left <= 10:  # Vermelho nos últimos 10 segundos
                    self.timer_label.configure(text=f"Próximo pulo em: {self.seconds_left}s", text_color="#ff0000")
                else:
                    self.timer_label.configure(text=f"Próximo pulo em: {self.seconds_left}s", text_color="#00ff00")
                
                self.seconds_left -= 1

                if self.seconds_left < 0:
                    # Pula para próxima música automaticamente
                    self.skip_track()
                    self.seconds_left = 82  # Reseta o timer
            else:
                self.timer_label.configure(text="Timer desativado" if not self.auto_skip_enabled else "Aguardando música...", text_color="#888888")
            
            time.sleep(1)

    def skip_track(self):
        try:
            self.sp.next_track()
            self.seconds_left = 82  # Reseta o timer
            self.flash_feedback("#00ff00")  # Feedback verde
        except Exception as e:
            self.show_error(f"Erro ao pular: {str(e)}")

    def hell_yeah(self):
        if self.current_track:
            try:
                # Salva a música nos favoritos
                self.sp.current_user_saved_tracks_add([self.current_track['id']])
                # Pula para próxima
                self.sp.next_track()
                self.seconds_left = 82  # Reseta o timer
                self.flash_feedback("#ff3300")  # Feedback vermelho
            except Exception as e:
                self.show_error(f"Erro: {str(e)}")

    def toggle_auto_skip(self):
        self.auto_skip_enabled = not self.auto_skip_enabled
        
        if self.auto_skip_enabled:
            self.auto_skip_button.configure(text="AUTO SKIP: ON", fg_color="#00ff00")
        else:
            self.auto_skip_button.configure(text="AUTO SKIP: OFF", fg_color="#ff3300")

    def flash_feedback(self, color):
        # Cria um flash de cor na interface para feedback visual
        flash = ctk.CTkFrame(self, fg_color=color)
        flash.place(x=0, y=0, relwidth=1, relheight=1)
        
        def remove_flash():
            flash.destroy()
        
        self.after(200, remove_flash)  # Remove o flash após 200ms

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Erro")
        error_window.geometry("400x200")
        error_window.configure(fg_color="#111111")
        
        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            font=("Segoe UI", 14),
            text_color="#ff0000",
            wraplength=350
        )
        error_label.pack(pady=20, padx=20)
        
        ok_button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        ok_button.pack(pady=10)

    def start_update_threads(self):
        # Thread para atualizar informações da música atual
        now_playing_thread = threading.Thread(target=self.update_now_playing, daemon=True)
        now_playing_thread.start()
        
        # Thread para o timer de auto-skip
        timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        timer_thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = SpotiSkipper()
    app.mainloop()