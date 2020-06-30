import FFT

def readwav(obj, path):
    if obj.readWav(path) is True: # wav를 정상적으로 읽으면
        return True # True 반환
    else: # 못읽은 경우
        obj.startRecord(0, 2.1, path) #녹음을 다시 시작
        return readwav(obj,path) # 다시 읽음

def startfft(obj,path):
    if obj.startFFT() is True: ## fft가 성공하면
        return True #True 반환
    else: #만약 FFT을 정상적으로 수행하지 못한경우
        obj.startRecord(0, 2.1, path) # 녹음부터 다시 수행함
        while readwav(obj, path) is not True: 1 # wav 파일을 정상적으로 불러올 떄까지 반복
        return startfft(obj,path) # 다시 FFT를 수행함

def startFun(obj,path):
    while obj.startRecord(0,2.1,path) is not True: 1 #녹음이 될 때까지 반복
    while readwav(obj,path) is not True: 1 #wav 파일을 정상적으로 불러올 때까지 반복
    while startfft(obj, path) is not True: 1 #fft를 정상적으로 진행할 때까지 반복
    obj.savefftFile(path.split(sep='.')[0] + ".txt") # freq, db를 log(txt)를 남김
    return True

def errrate(theoreticalvalue,measures):
    return 100 - abs((abs(theoreticalvalue-measures)/theoreticalvalue)*100)

def main():
    path = 'C:/Users/2015136133/Desktop/' #경로
    fft1 = FFT.FFT()
    fft2 = FFT.FFT()
    fft3 = FFT.FFT()

    startFun(fft1, path + 'fft1.wav') #FFT 과정을 수행함
    startFun(fft2, path + 'fft2.wav') #FFT 과정을 수행함
    startFun(fft3, path + 'fft3.wav') #FFT 과정을 수행함

    #fft1.showPltFFT()
    #fft2.showPltFFT()
    #fft3.showPltFFT()

    fftavg = [((fft1.fftdata[i] + fft2.fftdata[i] + fft3.fftdata[i]) / 3) for i in range(len(fft1.fftdata))]
    # fft1, 2, 3의 평균값을 fftavg에다 넣어줌
    fft4 = FFT.FFT()
    startFun(fft4,path + 'fft4.wav')

    cnt = 0
    for i in range(len(fft4.fftdata)):
        if errrate(fftavg[i],fft4.fftdata[i]) > 70:
            cnt+=1

    print((cnt/len(fftavg)*100), '% 입니다.')

    FFT.FFT.saveTextFile(fft1.freq, fftavg, path + 'avgfft.txt') #fft 평균을 txt로 저장
    #saveTextFile(freq,db,path)

    #fft1.showPltFFT()
    #fft2.showPltFFT()
    #fft3.showPltFFT()

if __name__ == "__main__":
    main()