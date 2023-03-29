from pytube import YouTube
import re
import os
from tqdm import tqdm
from glob import glob

class Youtube_to_wav:
    def __init__(self) -> None:
        pass
    
    def yt_audio_download(self, urls:list, path:str ,best_audio = True):
        for url in tqdm(urls, desc='영상 다운로드 중...'):
            yt = YouTube(url)
            streams = yt.streams.filter(only_audio=True, file_extension = 'mp4')
            max_abr = 0
            for stream in streams:
                abr = int(re.findall(r'\d+', stream.abr)[0])
                if abr > max_abr:
                    max_abr = abr
                    max_stream = stream

            max_stream.download(path)
        print('음악 다운로드 성공!')
    
    def video_to_wav(self, urls:list, best_audio=True):
        path = './music_download/original_files/'
        # 음악 다운로드
        self.yt_audio_download(urls, path, best_audio)
        
        files = glob('./music_download/original_files/*.mp4')        
        for file in tqdm(files, desc='mp4 -> wav 작업중...'):
            file_name = os.path.basename(file)[:-4]
            # print(file_name)
            # mp4 -> mp3
            file_name = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", file_name).replace(' ','').replace('musicdownloadoriginalfiles','')+'.mp3'
            
            # print(title)
            os.rename(file, path+file_name)

            # mp3 -> wav
            infile =  path+file_name
            outfile = f'./music_download/wav_files/{os.path.basename(file_name)}.wav'
            
            command = f'ffmpeg -i {infile} -ac 2 -f wav {outfile}'
            os.system(command)
            os.system(f'del {infile}')