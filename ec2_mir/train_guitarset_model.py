from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Conv2D, MaxPool2D, Flatten
from math import floor

import psutil
from keras.callbacks import Callback
from random import shuffle
import numpy as np
from librosa import time_to_frames
import boto3
import os

def download_guitarset_transforms():
    s3_resource = boto3.resource('s3')
    bucketName = 'dakobed-guitarset'
    bucket = s3_resource.Bucket(bucketName)

    s3 = boto3.client('s3')
    with open('guitarset-mean.npy', 'wb') as f:
        s3.download_fileobj('dakobed-guitarset', 'guitarset-mean.npy', f)
    with open('guitarset-variance.npy', 'wb') as f:
        s3.download_fileobj('dakobed-guitarset', 'guitarset-var.npy', f)


    # os.mkdir('data')
    # os.mkdir('data/dakobed-guitarset')
    for fileID in range(360):
        print(fileID)
        os.mkdir('data/dakobed-guitarset/fileID{}/'.format(fileID))
        path = 'data/dakobed-guitarset/fileID{}'.format(fileID)
        cqtfile = 'fileID{}/cqt.npy'.format(fileID)
        annotation_file = 'fileID{}/binary_annotation.npy'.format(fileID)
        bucket.download_file(cqtfile, path + '/cqt.npy')
        bucket.download_file(annotation_file, path + '/annotation.npy')


def generate_annotation_matrix(annotation, frames):
    '''
    This function will return a one hot encoded matrix of notes being played
    The annotation matrix will start w/ note 25 at index 0 and go up to note 100
    The highest and lowest values that I saw in the annotations seemed to be arounnd 29-96 so give a little leeway
    :return:
    '''
    annotation_matrix = np.zeros((48, frames))
    for i,note in enumerate(annotation):
        starting_frame = time_to_frames(note[1])
        duration_frames = time_to_frames(note[2] - note[1])
        note_value = note[0]
        # print('annotation shape {}'.format(annotation_matrix.shape))
        # print("starting frame " + str(starting_frame))
        # print("duration frames " + str(duration_frames))
        # print("int note value " + str(int(note_value)))
        annotation_matrix[int(note_value) - 25][starting_frame:starting_frame + duration_frames] = 1
    return annotation_matrix.T


def load_transform_and_annotation(fileID, binary = True):
    path = 'data/dakobed-guitarset/fileID{}/'.format(fileID)
    # annotation_label = np.load(path+'annotation.npy') if binary else np.load(path+'multivariable_annotation.npy')
    annotation_label = np.load(path + 'binary_annotation.npy') if binary else np.load(path + 'multivariable_annotation.npy')
    cqt = np.load(path+'cqt.npy')
    return cqt, annotation_label


# def load_guitarset_transform_annotation(fileID, binary=True):
#     path = 'data/guitarset/fileID{}/'.format(fileID)
#     annotation_label = np.load(path + 'binary_annotation.npy') if binary else np.load(
#         path + 'multivariable_annotation.npy')
#     cqt = np.load(path + 'cqt.npy')
#     return cqt, annotation_label
#
#
# def load_maestro_transfrom_annotation(fileID):
#     path = 'data/dakobed-maestro/fileID{}/'.format(fileID)
#     annotation = np.load(path+'annotation.npy')
#     cqt = np.load(path+'cqt.npy')
#     return cqt, annotation


def guitarsetGenerator(batchsize, train=True):
    def init_file_queue():
        if train:
            fileQueue = list(range(291))
            fileQueue = set(fileQueue)
            fileQueue = list(fileQueue)
            shuffle(fileQueue)
        else:
            fileQueue = list(range(291,360))
            shuffle(fileQueue)
            fileQueue = set(fileQueue)
        return fileQueue

    def stitch(next_spec, next_annotation):
        '''
        This method will handle the case when the generator reaches the end of one spectogram and stitch together
        the samples from the next.
            Calculate how many samples of the next spectogram I need to grab. Then set the current_spectogra_index to this value
            This method will be called when the spectogram gets pulled off the queue requiring the need to stitch together the spectograms
        '''

        n_samples = batchsize + currentIndex - x.shape[0]  # Number of samples in next spectogram
        prev_n_samples = batchsize - n_samples  # Number of samples in the previous spectogram

        spec1 = x[-prev_n_samples:]
        spec2 = next_spec[:n_samples]
        # print("The shapes of the spec {} and {}".format(spec1.shape, spec2.shape))
        batchx = np.concatenate((spec1, spec2), axis=0)

        annotation1 = y[-prev_n_samples:]
        annotation2 = next_annotation[:n_samples]
        batchy = np.concatenate((annotation1, annotation2), axis=0)

        return batchx, batchy, next_spec, next_annotation, n_samples

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

    welford_mean = np.load('guitarset-mean.npy')
    welford_variance = np.load('guitarset-variance.npy')
    welford_standard_deviation = np.sqrt(welford_variance)

    fileQueue = init_file_queue()
    fileID = fileQueue.pop()
    x, annotation = load_transform_and_annotation(fileID)
    x = (x-welford_mean)/welford_standard_deviation
    x = generate_windowed_samples(x)
    y = generate_annotation_matrix(annotation, x.shape[0])
    currentIndex = 0

    while True:
        if currentIndex > x.shape[0] - batchsize:
            if len(fileQueue) == 0:
                fileQueue = init_file_queue()
            next_spec_id = fileQueue.pop()
            # print("Processing the next fiel with id {}".format(next_spec_id))
            # print("Length of the queue is {}".format(len(fileQueue)))
            nextSpec, annoation = load_transform_and_annotation(next_spec_id)
            nextSpec = generate_windowed_samples(nextSpec)

            nextSpec = (nextSpec - welford_mean) / welford_standard_deviation

            batchx, batchy, x, y, currentIndex = stitch(nextSpec,generate_annotation_matrix(annoation, nextSpec.shape[0]))
            yield batchx.reshape((batchx.shape[0], batchx.shape[1], batchx.shape[2], 1)), batchy
        else:
            batchx = x[currentIndex:currentIndex + batchsize]
            batchy = y[currentIndex:(currentIndex + batchsize)]
            currentIndex = currentIndex + batchsize
            yield batchx.reshape((batchx.shape[0], batchx.shape[1], batchx.shape[2], 1)), batchy


# class CustomCallback(Callback):
#     def on_train_batch_begin(self, batch, logs=None):
#         process = psutil.Process(os.getpid())
#         print("Training start of batch w/ memory usage {}".format(process.memory_info().rss))


def build_model():
    model = Sequential()
    model.add(Conv2D(filters = 64, kernel_size = (3,3), kernel_initializer='normal', activation='relu', padding = 'same',input_shape=( 5,144,1)))
    model.add(MaxPool2D(pool_size =(2,2)))
    model.add(Dropout(.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(.2))
    model.add(Dense(48,kernel_initializer='normal', activation='relu'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model

#download_guitarset_transforms()

batch_size = 32
model = build_model()
num_epochs = 10

model.fit_generator(generator=guitarsetGenerator(32),
                    epochs=num_epochs,
                    steps_per_epoch = floor(8382182/batch_size),
                    verbose=1,
                    use_multiprocessing=True,
                    workers=16,
                    validation_data = guitarsetGenerator(32,False),
                    validation_steps = floor(888281/batch_size),
                    # callbacks=[CustomCallback()],
                    max_queue_size=32)

# model.save('model1.h5')
# s3client = boto3.client('s3')
# with open('model1.h5', "rb") as f:
#     s3client.upload_fileobj(f, 'dakobed-transcriptions', "model{}.h5".format(1))