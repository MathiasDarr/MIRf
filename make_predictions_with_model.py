import keras
import numpy as np
import matplotlib.pyplot as plt

def generate_windowed_samples(spec):
    '''
    This method creates the context window for a sample at time t, Wi-2, Wi-1, Wi, Wi+1,Wi+2
    '''
    windowed_samples = np.zeros((spec.shape[0], 5, spec.shape[1]))
    for i in range(spec.shape[0]):
        if i <= 1:
            windowed_samples[i] = np.zeros((5, spec.shape[1]))
        elif i >= spec.shape[0] - 2:
            windowed_samples[i] = np.zeros((5, spec.shape[1]))
        else:
            windowed_samples[i, 0] = spec[i - 2]
            windowed_samples[i, 1] = spec[i - i]
            windowed_samples[i, 2] = spec[i]
            windowed_samples[i, 3] = spec[i + 1]
            windowed_samples[i, 4] = spec[i + 2]
    return windowed_samples


def preprocess(mean, std, spectogram):

    spec = generate_windowed_samples(spectogram - mean) / std
    return np.expand_dims(spec, axis=-1)
model =  keras.models.load_model('data/model1.h5')

plt.plot(list(model.history.values())[0],'k-o')
plt.show()

mean = np.load('data/guitarset-mean.npy')
var = np.load('data/guitarset-var.npy')
std = np.sqrt(var)

for i in range(360):
    cqt = np.load('data/dakobed-guitarset/fileID1/cqt.npy')
    annotation = np.load('data/dakobed-guitarset/fileID1/binary_annotation.npy')


windowed_spectogram = preprocess(mean, std, cqt)

score = model.evaluate(windowed_spectogram, annotation.T )



probabilities = model.predict_proba(windowed_spectogram)

tslice = probabilities[23,:]
plt.plot(tslice)
plt.show()