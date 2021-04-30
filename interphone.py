import os
import pyaudio
import numpy as np
import time
from scipy.signal import argrelmax
import requests
import datetime
from scipy import signal
import logging
import logging.config
from subfunc import linefunc
from subfunc import logfunc
from subfunc import token

# interphone setting
CHUNK = 2048
RATE = 48000    # sampling rate
dt = 1/RATE
freq = np.linspace(0,1.0/dt,CHUNK)
fn = 1/dt/2;    # nyquist freq
FREQ_HIGH_BASE = 844.16  # high tone frequency
FREQ_LOW_BASE = 680.02   # low tone frequency
FREQ_ERR = 1         # allowable freq error
detect_high = False
detect_low = False
# Lineのアクセスコード
URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS
LINE_MESSAGE = 'インターフォンが鳴ったよ'
# フィルタ係数
FPASS1 = np.array([670, 860]) # 通過域端周波数
FSTOP1 = np.array([600, 950]) # 阻止域端周波数
FPASS2 = np.array([835, 860]) # 通過域端周波数
FSTOP2 = np.array([750, 950]) # 阻止域端周波数
GPASS = 6   # 通過域端最大損失
GSTOP = 30  # 通過域端最小損失

detect_high_time = detect_low_time = datetime.datetime.now() # 高音低音検知時間
THRESHOLD_SECONDS = datetime.timedelta(seconds=1) # 高音低音検知間隔閾値

# ログ設定
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'interphone.log')

# 振幅設定
AMP_MAX = 0.025
AMP_MIN = 0.02

# FFTで振幅最大の周波数を取得する関数
def getMaxFreqFFT(sound, chunk, freq):
    # FFT
    f = np.fft.fft(sound)/(chunk/2)
    f_abs = np.abs(f)
    # ピーク検出
    peak_args = argrelmax(f_abs[:(int)(chunk/2)])
    f_peak = f_abs[peak_args]
    f_peak_argsort = f_peak.argsort()[::-1]
    peak_args_sort = peak_args[0][f_peak_argsort]
    # 最大ピークをreturn
    return freq[peak_args_sort[0]]

# 検知した周波数がインターホンの音の音か判定する関数
def detectDualToneInOctave(freq_in, freq_high_base, freq_low_base, freq_err):
    det_h = det_l = False
    err_h = np.abs(freq_in - freq_high_base)
    err_l = np.abs(freq_in - freq_low_base)
    if err_h < freq_err:
        det_h = True
    elif err_l < freq_err:
        det_l = True

    return det_h, det_l

# BandPassFilter
def bandpass(ndarray, rate, fpass, fstop, gpass, gstop):
    fn = rate/2 # ナイキスト周波数
    wpass = fpass/fn # ナイキスト周波数で正規化 
    wstop = fstop/fn # ナイキスト周波数で正規化
    N, wn = signal.buttord(wpass, wstop, gpass, gstop) # オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, wn, "band") # フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, ndarray) # フィルタリング処理
    
    return y

# メイン関数
if __name__=='__main__':

    logger = logfunc.get_logger(__name__, LOG_TXT)

    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
    
    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            # BandPassFilter
            filtered_ndarray1 = bandpass(ndarray, RATE, FPASS1, FSTOP1, GPASS, GSTOP)
            filtered_ndarray = filtered_ndarray1
            abs_array = np.abs(filtered_ndarray)/32768
            if abs_array.max() > AMP_MIN and abs_array.max() < AMP_MAX :
                # FFTで最大振幅の周波数を取得
                freq_max = getMaxFreqFFT(filtered_ndarray, CHUNK, freq)
                h,l = detectDualToneInOctave(freq_max, FREQ_HIGH_BASE, FREQ_LOW_BASE, FREQ_ERR)
                logger.debug('--------------------')
                if h:
                    detect_high = True
                    logger.info('高音検知！')
                    detect_high_time = datetime.datetime.now()
                    if abs(detect_high_time - detect_low_time) > THRESHOLD_SECONDS:
                        detect_low = False
                        logger.debug('低音フラグリセット')
                if l:
                    detect_low = True
                    logger.info('低音検知！')
                    detect_low_time = datetime.datetime.now()
                    if abs(detect_high_time - detect_low_time) > THRESHOLD_SECONDS:
                        detect_high = False
                        logger.debug('高音フラグリセット')
                dt_now = datetime.datetime.now()
                logger.info('Max Amplitude = %s', round(abs_array.max(), 5))
                logger.info('Max Frequency = %s Hz', round(freq_max, 3))
                # dual tone detected
                if detect_high and detect_low:
                    logger.info('インターホンの音を検知！')
                    linefunc.pushLine(URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
                    time.sleep(30)
                    logger.info('フラグリセット')
                    detect_high = detect_low = False
        except KeyboardInterrupt:
            break
        
    stream.stop_stream()
    stream.close()
    P.terminate()

