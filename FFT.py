import wave
import scipy.io as sio
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import math
import pyaudio

class FFT():
    def __init__(self):
        self.wavdata = []
        self.fftdata = []
        self.wavfs = None
        self.freq = None
        self.status = None

    def startRecord(self,DEVICE_INDEX=None,RECORD_SECONDS=None,fileName = None):
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                input=True,
                                input_device_index=DEVICE_INDEX,
                                frames_per_buffer=1024)
            print('start : ',fileName.split(sep='/')[-1])
            frames = []

            for i in range(0, int(44100 / 8192 * RECORD_SECONDS)):
                data = stream.read(8192)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            audio.terminate()
            waveFile = wave.open(fileName, 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(44100)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            print('end')
            return True
        except Exception as e:
            print('log:startRecord(): ',e)
            return False

    def readWav(self,fileName):
        try:
            self.wavfs, self.wavdata = sio.wavfile.read(fileName)
            self.status = True
            return True
        except FileNotFoundError as e:
            self.status = False
            print('log:readWav(): ', e)
            return False
        except Exception as e:
            self.status = False
            print('log:readWav(): ', e)
            return None

    def startFFT(self):
        if self.status is False:
            return False
        try:
            nfft = len(self.wavdata)
            k = np.arange(nfft)
            self.freq = (k * self.wavfs / nfft)
            self.freq = self.freq[range(math.trunc(nfft / 2))]
            Y = np.fft.fft(self.wavdata) / nfft
            Y = Y[range(math.trunc(nfft / 2))]
            amplitude_hz = 2 * abs(Y)
            for db in amplitude_hz:
                self.fftdata.append(20 * math.log10(abs(db) / 2))
            return True
        except Exception as e:
            self.status = False
            print('log:startFFT(): ',e)
            return None

    def showPltWav(self,tmin=None,tmax=None,ymin=None,ymax=None):
        try:
            times = np.arange(len(self.wavdata)) / float(self.wavfs)
            plt.plot(times,self.wavdata)
            if tmin is None: tmin = times[0]
            if tmax is None: tmax = times[-1]
            plt.xlim(tmin, tmax)
            plt.ylim(ymin, ymax)
            plt.xlabel('times')
            plt.ylabel('Wavdata')
            plt.grid()
            plt.show()
            return True
        except Exception as e:
            self.status = False
            print('log:showPltWav(): ',e)
            return None

    def showPltFFT(self,ymin=None,ymax=None,xmin=0,xmax = 22050):
        try:
            plt.plot(self.freq, self.fftdata, 'r')  # 2* ???
            plt.xticks(np.arange(0, self.wavfs // 2, (xmax-xmin) / 5))
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            plt.xlabel('frequency($Hz$)')
            plt.ylabel('db')
            plt.grid()
            plt.show()
            return True
        except Exception as e:
            print('log:showPltFFT(): ',e)
            self.status = False
            return None

    def savefftFile(self,path):
        try:
            textfile = open(path, 'w', encoding='utf8')
            for i in range(self.wavfs):
                line = f'fs = {format(self.freq[i], "5.2f")} = db = {format(self.fftdata[i], "5.2f")}\n'
                textfile.write(line)
            textfile.close()
        except Exception as e:
            print('log:savefftFile(): ',e)
            return None

    @staticmethod
    def saveTextFile(freq,db,path):
        try:
            textfile = open(path, 'w', encoding='utf8')
            for i in range(44100):
                line = f'fs = {format(freq[i], ".5f")} = db = {format(db[i], ".5f")}\n'
                textfile.write(line)
            textfile.close()
        except Exception as e:
            print('log:saveTextfile: ', e)
            return None