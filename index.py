import pytube
import os
import subprocess
from moviepy.editor import *

def download_video(url):
    yt = pytube.YouTube(url)

    unique_options = set()

    for stream in yt.streams.filter(type="video", progressive=True).order_by('resolution'):
        resolution = int(stream.resolution[:-1]) if stream.resolution[:-1].isdigit() else 0
        if resolution <= 720:
            unique_options.add((stream.resolution, stream.fps))


    print("Opções disponíveis para download:")
    for idx, (resolution, fps) in enumerate(unique_options, 1):
        print(f"{idx}. {resolution} {fps}FPS")

    choice = input("Selecione a opção desejada: ")

    choice_idx = int(choice) - 1

    if 0 <= choice_idx < len(unique_options):
        chosen_resolution, chosen_fps = list(unique_options)[choice_idx]
        print(f"\nBaixando {chosen_resolution} {chosen_fps}FPS...")
        video = yt.streams.filter(type="video", resolution=chosen_resolution, progressive=True).first()
        video.download()
        print("Download do vídeo concluído.")
    else:
        print("Opção inválida.")

def download_audio(url):
    yt = pytube.YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    mp4_filename = audio.default_filename  
    out_file = audio.download(output_path='.')  

    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 
    print("Download concluído.")

def download_playlist(url, file_format='mp4'):
    from pytube import Playlist

    playlist = Playlist(url)

    print(f"Baixando a playlist: {playlist.title}")
    for video in playlist.videos:
        print(f'Baixando: {video.title}...')
        if file_format == 'mp3':
            download_audio(video.watch_url)
        elif file_format == 'mp4':
            download_video(video.watch_url)
        else:
            print("Formato de arquivo não suportado.")
    print("Download da playlist concluído.")

def main():
    while True:
        menu = """
        .------- Bem Vindo ao Storm Menu -------.
        |                                       |
        | 1. Baixar um vídeo do youtube         |
        | 2. Baixar um áudio do youtube         |
        | 3. Baixar uma playlist do youtube     |
        | 4. Sair                               |
        |                                       |
        '---------------------------------------'
        """

        opcao = input(menu)

        if opcao == '1':
            video_url = input("Insira o link do vídeo: ")
            download_video(video_url)
        elif opcao == '2':
            audio_url = input("Insira o link do vídeo: ")
            download_audio(audio_url)
        elif opcao == '3':
            playlist_url = input("Insira o link da playlist: ")
            file_format = input("Escolha o formato dos arquivos (mp3 ou mp4): ")
            download_playlist(playlist_url, file_format)
        elif opcao == '4':
            break
        else:
            print("Opção inválida. Por favor, escolha entre 1 e 5.")

if __name__ == "__main__":
    main()
