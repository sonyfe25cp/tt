
import itertools
import math
import os
import numpy as np

import tensorflow as tf
from tensorflow.contrib import skflow

##Train data
CORPUS_FILENAME='data/train_data.text'
MAX_DOC_LENGTH=50

#tokensize

def tokenizer(iterator):
  for value in iterator:
    ss = []
    for v in value:
      ss.append(v)
    yield ss

def training_data(path):
  X = []
  fp = open(path, 'r')
  for line in fp.readlines():
    line = line.strip()
    if not line:
      continue
    origin = list(line.decode('utf8'))
    if len(origin) >=50:
      origin = origin[:49]
    X.append(origin + ['<EOS/>'])
  return np.array(X)

def iter_docs(docs):
  for doc in docs:
    n_parts = int(math.ceil(float(len(doc))/MAX_DOC_LENGTH))
    for part in range(n_parts):
      offset_begin = part * MAX_DOC_LENGTH
      offset_end = offset_begin + MAX_DOC_LENGTH
      inp = np.zeros(MAX_DOC_LENGTH, dtype=np.int32)
      out =np.zeros(MAX_DOC_LENGTH, dtype = np.int32)
      inp[:min(offset_end - offset_begin, len(doc) - offset_begin)] = doc[offset_begin:offset_end]
      out[:min(offset_end - offset_begin, len(doc) - offset_begin -1)] = doc[offset_begin+1:offset_end+1]
      yield inp,out
def unpack_xy(iter_obj):
  x, y = intertools.tree(iter_obj)
  return (item[0] for item in X), (item[1] for item in y)

vocab_processor = skflow.preprocessing.VocabularyProcessor(MAX_DOC_LENGTH, min_frequency = 2, tokenizer_fn = tokenizer)

datao = train_data(CORPUS_FILENAME)

vocab_processor.fit(datao)

fp = open('data/vocab.txt', 'w')

for k, v in vocab_processor.vocabulary_.mapping.iteritems():
  fp.write('%s\t%d\n' % (k.encode('utf8'), v))
fp.close()

n_words = len(vocab_processor.vocabulary_)
print('total words: %d' % (n_words))

HIDDEN_SIZE=874

def get_language_model(hidden_size):
  '''returns a language model with given hidden size '''

  def language_model(X, y):
    inputs = skflow.ops.one_hot_matrix(X, n_words)
    inputs = skflow.ops.split_squeeze(1, MAX_DOC_LENGTH, inputs)
    target = skflow.ops.split_squeeze(1, MAX_DOC_LENGTH, y)
  
    encoder_cell = tf.nn.rnn_cell.OutputProjectionWrapper(tf.nn.rnn_cell.GRUCell(hidden_size), n_words)
  
    output, _ = tf.nn.rnn(encoder_cell, inputs, dtype=np.float32)
  
    return skflow.ops.sequence_classifier(output, target)
  return language_model

def exp_decay(global_step):
  return tf.train.expontial_decay(0.001, global_step, 5000, 0.5, staircase=True)


model_path = 'data/address_logs'

if os.path.exists(model_path):
  estimator = skflow.TensorFlowEstimator.restore(model_path)
else:
  estimator = skflow.TensorFlowEstimator(model_fn = get_language_model(HIDDEN_SIZE), nclasses=n_words, optimizer='Adam', learning_rate=exp_decay, steps=16273, batch_size=64, continue_training=True)

while True:
  try:
        perm = np.random.permutation(len(datao))
        datao = datao[perm]
        data = vocab_processor.transform(data)
        X, y =  unpack_xy(iter_docs(data))
        estimator.fit(X, y, logdir=model_path)
        estimator.save(model_path)
  except KeyboardInterrupt:
    estimator.save(model_path)
    break

