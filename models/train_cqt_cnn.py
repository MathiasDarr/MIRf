from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Conv2D, MaxPool2D, Flatten, BatchNormalization, Activation
from keras import activations
from math import floor

model = Sequential()
model.add(Conv2D(filters=8, kernel_size=(3, 3), kernel_initializer='normal', activation='relu', padding='same', input_shape=(5, 144, 1)))
model.add(BatchNormalization())
model.add(Activation(activations.relu))
model.add(Conv2D(filters=8, kernel_size=(3, 3), kernel_initializer='normal', activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Activation(activations.relu))
model.add(MaxPool2D(pool_size =(2,2)))
model.add(Dropout(.25))
model.add(Conv2D(filters=8, kernel_size=(3, 3), kernel_initializer='normal', activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Activation(activations.relu))
model.add(MaxPool2D(pool_size =(2,2)))
model.add(Dropout(.25))
model.add(Flatten())

model.compile()
model.summary()

