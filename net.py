import tensorflow as tf
import numpy as np
import os
import time

# suppress GPU optimization error
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# location of training data
path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org'
                                                          '/data/shakespeare.txt')

# read in the text
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# get the set of characters in the text
vocab = sorted(set(text))

# create lookup tables going from characters to indices and the reverse
char_to_index = {char: index for index, char in enumerate(vocab)}
index_to_char = np.array(char_to_index)

# translate the text from characters to indices
coded_text = np.array([char_to_index[char] for char in text])

# set the lengths of our inputs and epochs
sequence_length = 100
epoch_length = len(text) // (sequence_length + 1)

# create training data
dataset = tf.data.Dataset.from_tensor_slices(coded_text)

sequences = dataset.batch(sequence_length + 1, drop_remainder=True)


def make_source_and_target(sequence):
    """split the sequence into a source and a target; 'Hello' goes to 'Hell' and 'ello'"""
    source = sequence[:-1]
    target = sequence[1:]
    return source, target


dataset = sequences.map(make_source_and_target)

# everyone loves arbitrary constants
BATCH_SIZE = 64
BUFFER_SIZE = 10000

# shuffle the data and split into batches
dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    """build the RNN model"""
    return tf.keras.Sequential([
         tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
         tf.keras.layers.GRU(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
         tf.keras.layers.Dense(vocab_size)])


model = build_model(len(vocab), 256, 1024, BATCH_SIZE)


def loss(labels, logits):
    """calculate the loss, i.e. the distance from expected"""
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


# configure the training
model.compile(optimizer='adam', loss=loss)

# set the checkpoint callback to record checkpoints
checkpoint_prefix = os.path.join('./checkpoints', '{epoch}')
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix, save_weights_only=True)

# train the model
history = model.fit(dataset, epochs=10, callbacks=[checkpoint_callback])

