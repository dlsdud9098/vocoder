from pydub import AudioSegment
import librosa
import wave

class audio_setting:
    def __init__(self) -> None:
        pass
    
    # 스테레오 -> 모노 변환
    def stero_to_mono(self, file_path):
        # sound = AudioSegment.from_wav("./music_files/tears.wav")
        sound = AudioSegment.from_wav(file_path)
        sound = sound.set_channels(1)
        sound.export(file_path, format="wav")
        
    def sr_change(self, file_path):
        # 음성 파일 불러오기
        y, sr = librosa.load(file_path, sr=None)

        # 리샘플링
        y_resampled = librosa.resample(y, sr, 44100)

        # 결과 저장하기
        librosa.output.write_wav(file_path, y_resampled, sr=44100)
        
    def audio_change(self, paths:list):
        # path = './music_files/wavfile/musicfilesKimKwangSeokAboutThirtyLyricsOnly.wav'
        for path in tqdm(paths, desc='음성 설정중...'):
            with wave.open(path, 'rb') as audio_file:
                # sr(samplingrate 확인)
                sr = audio_file.getframerate()
                # 채널 수 확인(1=모노)
                channels = audio_file.getnchannels()
                # 비트 수 확인(16비트)
                bit_depth = audio_file.getsampwidth() * 8

            if channels == 2:
                self.stero_to_mono(path)
                # print('모노로 변환')
                
            if sr < 44000:
                self.sr_change(path)
                # print('44100Khz로 변환')