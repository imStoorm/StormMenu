import pytube
import os
import subprocess
import requests
import shutil
from moviepy.editor import *

REPO_OWNER = 'imStoorm'
REPO_NAME = 'StormMenu'

def verificar_atualizacao():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest'

    response = requests.get(url)

    if response.status_code == 200:
        release_info = response.json()

        nova_versao = release_info['tag_name']
        url_download = release_info['assets'][0]['browser_download_url']

        versao_atual = '1.0.1'  
        if nova_versao != versao_atual:
            print(f'Nova versão disponível: {nova_versao}')
            return True, url_download
        else:
            print('O aplicativo está atualizado.')
    else:
        print('Erro ao verificar atualização:', response.status_code)
    
    return False, ''

def baixar_atualizacao(url_download):
    response = requests.get(url_download, stream=True)
    if response.status_code == 200:
        filename = f'{REPO_NAME}_att.exe'

        with open(filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

        return filename
    else:
        print('Erro ao baixar atualização:', response.status_code)
        return None

def download_video(url, opt):
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
        if opt != 'plist':
            subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
            print("Download concluído.")
            still = input("Deseja continuar usando o aplicativo? (S/N)")
            if still.lower() in ['n', 'no', 'nao']:
                return True

        subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
    else:
        print("Opção inválida.")

def download_audio(url, opt):
    yt = pytube.YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    mp4_filename = audio.default_filename  
    out_file = audio.download(output_path='.')  

    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print("Download concluído.")
    if opt != 'plist':
            subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
            print("Download concluído.")
            still = input("Deseja continuar usando o aplicativo? (S/N)")
            if still.lower() in ['n', 'no', 'nao']:
                return True
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)

def download_playlist(url, file_format='mp4'):

    playlist = pytube.Playlist(url)

    print(f"Baixando a playlist: {playlist.title}")
    for video in playlist.videos:
        print(f'Baixando: {video.title}...')
        if file_format == 'mp3':
            download_audio(video.watch_url, 'plist')
        elif file_format == 'mp4':
            download_video(video.watch_url, 'plist')
        else:
            print("Formato de arquivo não suportado.")

    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
    print("Download da playlist concluído.")
    still = input("Deseja continuar usando o aplicativo? (S/N)")
    if still.lower() in ['n', 'no', 'nao']:
        return

def main():

    atualizacao_disponivel, url_download = verificar_atualizacao()
    if atualizacao_disponivel:
        # Baixa a nova versão do aplicativo
        arquivo_atualizacao = baixar_atualizacao(url_download)
        if arquivo_atualizacao:
            os.remove(sys.argv[0])
            os.rename(f'{REPO_NAME}_att.exe', sys.argv[0])
            print('Aplicativo atualizado com sucesso!')

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
        print(menu)
        opcao = input("Insira a opção que deseja prosseguir:")

        if opcao == '1':
            video_url = input("Insira o link do vídeo: ")
            if download_video(video_url, ''):
                break
        elif opcao == '2':
            audio_url = input("Insira o link do vídeo: ")
            if download_audio(audio_url, ''):
                break
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
