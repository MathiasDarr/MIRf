import os
import numpy as np
import librosa
import jams
import boto3
import json
from numpy import format_float_positional


def jam_to_notes_matrix(jam_file):
    annotation = (jams.load(jam_file)).annotations
    # annotation['value'] = annotation['value'].apply(round_midi_numers)
    lowE = annotation[1]
    A = annotation[3]
    D = annotation[5]
    G = annotation[7]
    B = annotation[9]
    highE = annotation[11]
    notes = []
    for i,string in enumerate([lowE, A, D,G,B, highE]):
        for datapoint in string.data:
            notes.append([datapoint[0], datapoint[1], datapoint[2], i])
    notes.sort(key=lambda x: x[0])
    return np.asarray(notes, dtype=np.float32)


def notes_matrix_to_annotation(notes, nframes):
    binary_annotation_matrix = np.zeros((48, nframes))
    full_annotation_matrix = np.zeros((48,nframes, 6))
    for note in notes:
        starting_frame = librosa.time_to_frames(note[0])
        duration_frames = librosa.time_to_frames(note[1])
        ending_frame = starting_frame + duration_frames
        note_value, string = int(note[2])-35, int(note[3])
        binary_annotation_matrix[note_value ,starting_frame:ending_frame] = 1
        full_annotation_matrix[note_value , starting_frame:ending_frame, string]  = 1
    return binary_annotation_matrix, full_annotation_matrix


def annotation_audio_file_paths(audio_dir='data/guitarset/audio/', annotation_dir='data/guitarset/annotations' ):

    audio_files = os.listdir(audio_dir)
    audio_files = [os.path.join(audio_dir, file) for file in audio_files]
    annotation_files = os.listdir(annotation_dir)
    annotation_files = [os.path.join(annotation_dir, file) for file in annotation_files]

    file_pairs = []
    for annotation in annotation_files:
        annotation_file = annotation.split('/')[-1].split('.')[0]
        for audio_file in audio_files:
            if audio_file.split('/')[-1].split('.')[0][:-4] == annotation_file:
                file_pairs.append((audio_file, annotation))
    return file_pairs


class Transcription:
    def __init__(self, wav, jam, fileID):
        notes = jam_to_notes_matrix(jam)
        self.fileID = fileID
        y, sr = librosa.load(wav)
        tempo, beat_times = librosa.beat.beat_track(y, sr=sr, start_bpm=60, units='time')
        self.beats = [float(format_float_positional(beat, 3)) for beat in beat_times]
        self.assign_notes_to_measures(notes)
        self.processMeasures()
        self.generate_transcription_json()


    def processMeasures(self):
        measures = []
        for i, notes in enumerate(self.measures_notes):
            try:
                measures.append(Measure(notes, i))
            except Exception as e:
                print(e)
        self.measures = measures

    def getMeasures(self):
        return self.measures

    def assign_notes_to_measures(self, notes):
        measures_end_times = self.beats[0::4]
        nmeasures = len(self.beats) // 4
        if len(self.beats) % 4 != 0:
            nmeasures += 1
        measures = [[] for i in range(nmeasures)]
        measure_index = 0
        current_measure_end = measures_end_times[measure_index]

        for note in notes:
            note[0] = format_float_positional(note[0], 2)

        for note in notes:
            if note[0] > current_measure_end:
                measure_index += 1
                if measure_index >= len(measures):
                    break
                measures[measure_index].append((note))
                current_measure_end = measures_end_times[measure_index]
            else:
                measures[measure_index].append(list(note))
        self.measures_notes = measures

    def generate_transcription_json(self):
        transcription = []
        for m, measure in enumerate(self.measures):
            notes = measure.notes
            beats = measure.note_beats
            durations = measure.note_durations
            for i in range(len(notes)):
                note_dictionary = {'measure':str(m),'midi': str(notes[i][2]), 'string': str(notes[i][3]), 'beat':str(beats[i])}
                transcription.append(note_dictionary)
        with open('data/dakobed-guitarset/fileID{}/transcription.json'.format(self.fileID), 'w') as outfile:
            json.dump(transcription, outfile)
        bucket = 'dakobed-guitarset'
        s3 = boto3.client('s3')
        with open('data/dakobed-guitarset/fileID{}/transcription.json'.format(self.fileID), "rb") as f:
            s3.upload_fileobj(f, bucket, 'fileID{}/transcription.json'.format(self.fileID, self.fileID))


class Measure:
    def __init__(self, notes, index):
        start_of_measure = notes[0][0]
        end_of_measure = notes[-1][0]
        measureduration = notes[-1][0] -notes[0][0]
        sixteenth_note_duration = measureduration/16
        sixteenth_note_buckets = np.linspace(start_of_measure, end_of_measure, 16)

        # This will only be relevant when I am processing piano transcriptions.  An array containing the
        # durations of 1/16, 1/8th, 1/4, quarter dot, 1/2, 1/2 dot & whote notes for this measure.  I w

        note_durations = np.array([sixteenth_note_duration, sixteenth_note_duration*2, sixteenth_note_duration*4,
                                   sixteenth_note_duration*6, sixteenth_note_duration * 8, sixteenth_note_duration * 12,
                                   sixteenth_note_duration*16])

        processed_note_beats = []
        processed_note_durations = []

        for note in notes:
            absolute_val_beat_times_array = np.abs(sixteenth_note_buckets - note[0])
            note_beat = absolute_val_beat_times_array.argmin()
            processed_note_beats.append(note_beat)

            absolute_val_note_durations_array = np.abs(note_durations - note[1])
            duration = absolute_val_note_durations_array.argmin()
            processed_note_durations.append(duration)

        self.note_durations = processed_note_durations
        self.note_beats = processed_note_beats
        self.notes = notes


def process_wav_jam_pair(jam, wav, i):
    bucket = 'dakobed-guitarset'
    s3 = boto3.client('s3')
    os.mkdir('data/dakobed-guitarset/fileID{}'.format(i))

    y, sr = librosa.load(wav)
    cqt_raw = librosa.core.cqt(y, sr=sr, n_bins=144, bins_per_octave=36, fmin=librosa.note_to_hz('C2'), norm=1)
    magphase_cqt = librosa.magphase(cqt_raw)
    cqt = magphase_cqt[0].T
    notes = jam_to_notes_matrix(jam)

    binary_annotation, multivariate_annotation = notes_matrix_to_annotation(notes, cqt.shape[0])

    for file, array, s3path in [('data/dakobed-guitarset/fileID{}/cqt.npy'.format(i), cqt, 'fileID{}/cqt.npy'.format(i)),
                                ('data/dakobed-guitarset/fileID{}/binary_annotation.npy'.format(i), binary_annotation,'fileID{}/binary_annotation.npy'.format(i)),
                                ('data/dakobed-guitarset/fileID{}/multivariate_annotation.npy'.format(i), multivariate_annotation,'fileID{}/multivariate_annotation.npy'.format(i))]:
        np.save(file, arr=array)
        with open(file, "rb") as f:
            s3.upload_fileobj(f, bucket, s3path)
    with open(wav, "rb") as f:
        s3.upload_fileobj(f, bucket, "fileID{}/audio.wav".format(i))


def insert_guitarset_data_dynamo(dynamoDB, title, fileID):

    print("Processing fileID {}".format(fileID))

    try:
        dynamoDB.put_item(
            TableName="DakobedGuitarSet",
            Item={
                "fileID" : {"S":str(fileID)},
                "title": {"S":title}
            }
        )
    except Exception as e:
        print(e)



def save_transforms_and_annotations():
    dynamoDB = boto3.client('dynamodb', region_name='us-west-2')
    files = annotation_audio_file_paths()
    for fileID in range(len(files)):

        wav = files[fileID][0]
        jam = files[fileID][1]
        title = wav.split('/')[-1].split('.wav')[0][3:-4]
        insert_guitarset_data_dynamo(dynamoDB, title, fileID)
        process_wav_jam_pair(jam, wav, fileID)
        tab = Transcription(wav, jam, fileID)
        print("Processed filepair " + str(fileID))



save_transforms_and_annotations()