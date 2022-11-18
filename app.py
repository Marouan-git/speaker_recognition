from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os 
import glob
import os
import joblib, librosa
import numpy as np
import pandas as pd
import scipy
import scipy.signal

def latest_wav():
    list_of_files = glob.glob('./wav_files/*.wav') # * means all if need specific format then *.csv
    path_latest_wav = max(list_of_files, key=os.path.getctime)

    return path_latest_wav


def generate_dataset(audio, sr=22050):
    # generate Mel spectrogram
    spec = librosa.feature.melspectrogram(audio, sr=sr)

    # generate DataFrame from spectrogram (columns: frequencies, rows: analysis frames)
    X = pd.DataFrame(np.transpose(spec))
    return X

def remove_silence(signal):
    # extract non-silent intervals from the voice signal
    voice_intervals = librosa.effects.split(signal, frame_length=2048, top_db=35, hop_length=512)
    voice_no_silence = np.array([])
    slices = [signal[interval[0]:interval[1]] for interval in voice_intervals]
    voice_no_silence = np.concatenate(slices)
    return voice_no_silence

def pass_band_filter(sound, sr_sound=22050):
    # design a filter to remove the background noise using scipy.signal.iirfilter
    b, a = scipy.signal.iirfilter(1, [128, 2048], btype="bandpass", fs=sr_sound)

    # apply the filter using scipy.signal.lfilter
    y_sound_filt = scipy.signal.filtfilt(b, a, sound)
    return y_sound_filt

def pretraitment(sound):
    sound_filtered = pass_band_filter(sound)
    sound_no_silence = remove_silence(sound_filtered)
    return sound_no_silence




UPLOAD_FOLDER = './wav_files'

app = Flask(__name__, template_folder='template')
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')

def webpage():
    return render_template('index.html')

modele = joblib.load("rf_model.joblib")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

   if request.method == 'POST':
    
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        audio, _ = librosa.load(latest_wav())

        # generate the "nutcracker" input data (ignore label series)
        X_eval = generate_dataset(pretraitment(audio), 22050)
        # generate dataset from the audio signal, the samplerate and the label

        predictions = modele.predict(X_eval)
        eval_unique_labels, eval_unique_counts = np.unique(predictions, return_counts=True)
        pred_finale = eval_unique_labels[np.argmax(eval_unique_counts)]
        if str(pred_finale) == "aissa":
            return render_template('aissa.html')
        if str(pred_finale) == "marouan":
            return render_template('marouan.html')
        else:
            return render_template('another.html')
        

