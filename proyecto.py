import os
import random
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from TikTokApi import TikTokApi
import logging

class MovieToonsApp:
    def __init__(self, master):
        self.master = master
        master.title("MovieToons")

        # Encabezado
        self.label_header = tk.Label(master, text="MovieToons", font=("Arial", 16))
        self.label_header.pack()

        # Marco para la selección de archivos de video
        frame_video = tk.Frame(master)
        frame_video.pack(side="left")

        # Selección de archivos de video
        self.label_video = tk.Label(frame_video, text="Selecciona los archivos de video:")
        self.label_video.pack()
        self.button_video = tk.Button(frame_video, text="Seleccionar videos", command=self.seleccionar_videos)
        self.button_video.pack()

        # Marco para la selección de archivo de audio
        frame_audio = tk.Frame(master)
        frame_audio.pack(side="right")

        # Selección de archivo de audio
        self.label_audio = tk.Label(frame_audio, text="Selecciona el archivo de audio:")
        self.label_audio.pack()
        self.button_audio = tk.Button(frame_audio, text="Seleccionar audio", command=self.seleccionar_audio)
        self.button_audio.pack()

        # Botón de ejecución
        self.button_ejecutar = tk.Button(master, text="Ejecutar", command=self.ejecutar_codigo)
        self.button_ejecutar.pack()

        # Botón para subir a TikTok
        self.button_subir_tiktok = tk.Button(master, text="Subir a TikTok", command=self.subir_a_tiktok)
        self.button_subir_tiktok.pack()

        # Botón para cerrar la aplicación
        self.button_cerrar = tk.Button(master, text="Cerrar", command=self.cerrar_aplicacion)
        self.button_cerrar.pack()

    def seleccionar_videos(self):
        self.rutas_videos = filedialog.askopenfilenames(title="Seleccionar videos", filetypes=(("Archivos de video", "*.mp4 *.mov"), ("Todos los archivos", "*.*")))

    def seleccionar_audio(self):
        self.ruta_audio = filedialog.askopenfilename(title="Seleccionar audio", filetypes=(("Archivos de audio", "*.mp3"), ("Todos los archivos", "*.*")))

    def cortar_fragmento_aleatorio(self, video_path):
        clip = VideoFileClip(video_path)
        duracion_total = clip.duration
        inicio = random.uniform(0, duracion_total - 12)
        final = inicio + 12
        subclip = clip.subclip(inicio, final)
        # Eliminar el audio del subclip
        subclip = subclip.set_audio(None)
        return subclip

    def unir_videos(self, videos):
        return concatenate_videoclips(videos)

    def agregar_audio(self, video, audio_path):
        audio_clip = AudioFileClip(audio_path)
        # Ajustar la duración del audio al video
        audio_clip = audio_clip.subclip(0, min(audio_clip.duration, 36))
        video = video.set_audio(audio_clip)
        return video

    def guardar_video(self, video, carpeta):
        nombre_video = f"pb{len(os.listdir(carpeta)) + 1}.mp4"
        video.write_videofile(os.path.join(carpeta, nombre_video), fps=24)
        print(f"Video guardado como: {nombre_video}")

    def ejecutar_codigo(self):
        if not hasattr(self, 'rutas_videos') or not hasattr(self, 'ruta_audio'):
            print("Debes seleccionar al menos un video y un audio.")
            return

        # Obtener lista de archivos de video
        videos = [VideoFileClip(video_path) for video_path in self.rutas_videos]

        # Cortar un fragmento aleatorio de 12 segundos para cada video
        clips = [self.cortar_fragmento_aleatorio(video_path) for video_path in self.rutas_videos]

        # Unir los videos
        video_final = self.unir_videos(clips)

        # Agregar audio al video final
        video_final_con_audio = self.agregar_audio(video_final, self.ruta_audio)

        # Guardar el video final en la carpeta de videoyt
        carpeta_videoyt = os.path.join(os.path.dirname(__file__), "videoyt")
        self.guardar_video(video_final_con_audio, carpeta_videoyt)

    def subir_a_tiktok(self):
        # Ejemplo de uso de TikTokApi
        api = TikTokApi(logger_name="tiktok_api_logger", logging_level=logging.DEBUG)
        user_info = api.getUserByName(username="cypriants")
        print(user_info)

    def cerrar_aplicacion(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieToonsApp(root)
    root.mainloop()
