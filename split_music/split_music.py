from pydub import AudioSegment
import librosa
import librosa.display
import soundfile as sf
import os
from glob import glob
import soundfile as sf
import numpy as np
import wave
import math
from tqdm import tqdm

class split_sound:
    def __init__(self) -> None:
        pass
    
    def split_sudio(self, file_path, split_num, idx=0):
        # Load audio file
        # filename = './music_files/IU_input.wav'
        file_name = os.path.basename(file_path)
        y, sr = librosa.load(file_path, sr=None)

        # 8초 간격으로 자르기
        split_time = split_num

        with wave.open(file_path, 'rb') as wave_file:
            # 샘플링 레이트, 채널 수, 샘플 수 정보 가져오기
            framerate = wave_file.getframerate()
            n_frames = wave_file.getnframes()

            # 음성 파일 길이 계산 (초 단위)
            duration = n_frames / float(framerate)
            duration = int(math.ceil(duration))
            
        end = int(duration/split_time)

        for i in range(end):
            start = i * split_time
            end = start + split_time

            # 분할된 파일의 경로와 파일 이름 지정
            output_filename = f"./music_download/split_files/split_{i+idx}.wav"

            # 분할된 파일을 저장
            sf.write(output_filename, y[start*sr:end*sr], sr)
        
        # os.system(f'del "./music_download/split_files/{file_name}"')
        os.remove(file_path)
        return i+idx
    
    def delete_no_voice(self, file_path):
        # Load audio file
        # filename = './music_files/original.wav'
        file_name = os.path.basename(file_path)
        audio = AudioSegment.from_file(file_path)

        # Remove silent parts
        audio_filtered = audio.strip_silence(silence_thresh=-30)

        
        # Save the output
        audio_filtered.export(f'./music_download/split_files/{file_name}', format='wav')
        
    def run(self, split_num = 8):
        files = glob('./music_download/spleeter vocals/*.wav')
        for path in tqdm(files, desc='전체적으로 앞, 뒤 무음 제거'):
            self.delete_no_voice(path)
            
        # 10초 간격으로 분리하기
        files = glob('./music_download/split_files/*.wav')
        idx = 0
        for file in tqdm(files, desc='간격으로 음성파일 분리중...'):
            if idx == 0:
                idx = self.split_sudio(file, split_num)
            else:
                idx = self.split_sudio(file, split_num, idx)
            
        # split_voice('./music_files/train_files/vocals.wav')
        print('분리')

        # 자른 파일 모두 앞 뒤로 무음 제거
        files = glob('./music_download/split_files/*.wav')
        for file in tqdm(files, desc='무음 제거중...'):
            self.delete_no_voice(file)
            
            with wave.open(file, 'rb') as wave_file:
                # 샘플링 레이트, 채널 수, 샘플 수 정보 가져오기
                framerate = wave_file.getframerate()
                n_frames = wave_file.getnframes()

                # 음성 파일 길이 계산 (초 단위)
                duration = n_frames / float(framerate)
                duration = int(math.ceil(duration))
                    
            if duration < 3:
                del file
                print(f'{duration}초 이므로 파일 삭제')