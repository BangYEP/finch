from __future__ import print_function
from config import args
from sklearn.utils import shuffle


import numpy as np
import tensorflow as tf


class IMDB:
    def __init__(self):
        self._index_from = 4
        X_tuple = self._load_data()
        word2idx = self._load_word2idx()
        X = self._pad_data(X_tuple, word2idx)
        X_dropped = self._word_dropout(X, args.word_dropout_rate, word2idx)
        X_len = [args.max_len] * len(X)
        self._make_accessible(X, X_dropped, X_len, word2idx)


    def _load_data(self):
        (X_train, _), (X_test, _) = tf.contrib.keras.datasets.imdb.load_data(
            num_words=args.vocab_size, index_from=self._index_from)
        print("Data Loaded")
        return (X_train, X_test)


    def _load_word2idx(self):
        word2idx = tf.contrib.keras.datasets.imdb.get_word_index()
        print("Word Index Loaded")
        word2idx = {k: (v+self._index_from) for k, v in word2idx.items()}
        word2idx['<pad>'] = 0
        word2idx['<start>'] = 1
        word2idx['<unk>'] = 2
        word2idx['<end>'] = 3
        return word2idx


    def _pad_data(self, X_tuple, word2idx):
        padded_tuple = [tf.contrib.keras.preprocessing.sequence.pad_sequences(
            X, args.max_len+1, padding='post', truncating='post', value=word2idx['<pad>']) for X in X_tuple]
        print("Sequence Padded")
        return np.vstack(padded_tuple)[:, 1:]


    def _word_dropout(self, x, dropout_rate, word2idx):
        is_dropped = np.random.binomial(1, dropout_rate, x.shape)
        fn = np.vectorize(lambda x, k: word2idx['<unk>'] if k else x)
        return fn(x, is_dropped)


    def _make_accessible(self, X, X_dropped, X_len, word2idx):
        self._X = X
        self._X_dropped = X_dropped
        self._X_len = X_len
        self.word2idx = word2idx


    def next_batch(self):
        for i in range(0, len(self._X), args.batch_size):
            yield (self._X[i : i + args.batch_size],
                   self._X_dropped[i : i + args.batch_size],
                   self._X_len[i : i + args.batch_size])

    
    def shuffle(self):
        self._X, self._X_dropped = shuffle(self._X, self._X_dropped)


    def update_word_dropout(self):
        self._X_dropped = self._word_dropout(self._X, args.word_dropout_rate, self.word2idx)


def shape_test(d):
    print(d._X.shape, d._X_dropped.shape)


def idx2word_test(d):
    idx2word = {i:w for w,i in d.word2idx.items()}
    print(' '.join(idx2word[idx] for idx in d._X[30000]))


def word_dropout_test(d):
    idx2word = {i:w for w,i in d.word2idx.items()}
    print(' '.join(idx2word[idx] for idx in d._X[20]))
    print(' '.join(idx2word[idx] for idx in d._X_dropped[20]))


def next_batch_test(d):
    X, X_dropped, sequence_len = next(d.next_batch())
    print(X.shape, X_dropped.shape)


def shuffle_test(d):
    d.shuffle()
    idx2word = {i:w for w,i in d.word2idx.items()}
    print(' '.join(idx2word[idx] for idx in d._X[20]))
    print(' '.join(idx2word[idx] for idx in d._X_dropped[20]))


def update_word_dropout_test(d):
    d.update_word_dropout()
    print()
    idx2word = {i:w for w,i in d.word2idx.items()}
    print(' '.join(idx2word[idx] for idx in d._X[20]))
    print(' '.join(idx2word[idx] for idx in d._X_dropped[20]))


def main():
    dataloader = IMDB()
    """
    shape_test(dataloader)
    idx2word_test(dataloader)
    word_dropout_test(dataloader)
    next_batch_test(dataloader)
    shuffle_test(dataloader)
    update_word_dropout_test(dataloader)
    """


if __name__ == '__main__':
    main()
