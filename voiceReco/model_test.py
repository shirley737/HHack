'''
General test of NN Classifier for speech recognition.
'''


from sklearn import neighbors
import matplotlib.pyplot as plt
import numpy as np
import random
import pyaudio
import os
import sys
import wave

NUM_NEIGHBORS = 1
L_DISTANCE = 1
CHUNK = 512

duration = 3
filename = "./records/icecream0.wav"
DATA_DIR = "./records"

# clf = neighbors.KNeighborsClassifier(NUM_NEIGHBORS, p=L_DISTANCE)
# clf.fit(x_train, y_train)

class Voice_Rec_NN(object):
    def __init__(self, x_train, y_train):
        self.clf = neighbors.KNeighborsClassifier(NUM_NEIGHBORS, p=L_DISTANCE)
        self.clf.fit(x_train, y_train)

    def predict(self, x):
        return self.clf.predict(x)

def load_data(recordings_dir):
    my_data = []
    my_labels = []
    for filename in os.listdir(recordings_dir):
        if filename.split(".")[-1] != "wav":
            continue
        if filename[0] == 'i':
            label = 0
        elif filename[0] == 'p':
            label = 1
        elif filename[0] == 's':
            label = 2
        else:
            label = 3
        my_labels.append(label)
        with wave.open(os.path.join(recordings_dir, filename), 'rb') as wf:
            fs = wf.getframerate()
            bytes_per_sample = wf.getsampwidth()
            bits_per_sample  = bytes_per_sample * 8
            dtype = 'int{0}'.format(bits_per_sample)
            channels = wf.getnchannels()

            # read data
            audio = np.fromstring(wf.readframes(int(duration*fs*bytes_per_sample/channels)), dtype=dtype)
            audio.shape = (int(audio.shape[0]/channels), channels)
            my_data.append(audio)
    return np.array(my_data), np.array(my_labels)



if __name__ == "__main__":
    data, labels = load_data(DATA_DIR)
    print("P1", data.shape, labels.shape)
    print("P2", len(data), len(labels))

    pdata = list(zip(data, labels))
    random.shuffle(pdata)
    data, labels = zip(*pdata)

#    plt.plot(data[0])
#    plt.show()

    print("P3", len(data), len(labels))

    x_train = np.array(data[:-1])
    y_train = np.array(labels[:-1])

    x_train = np.array([np.squeeze(x) for x in x_train])

    x_test = np.array(data[-1:])
    y_test = np.array(labels[-1:])
    x_test = np.array([np.squeeze(x) for x in x_test])

    mine = Voice_Rec_NN(x_train, y_train)
    print(x_test.shape)
    print(mine.predict(x_test))
    print(y_test)
