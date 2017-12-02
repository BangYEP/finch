import tensorflow as tf
import numpy as np


class LinearSVMClassifier:
    def __init__(self, n_in, C=1.0, sess=tf.Session()):
        """
        Parameters:
        -----------
        C: float
            Penalty parameter C of the error term
        n_in: int
            Input dimensions
        sess: object
            tf.Session() object 
        """
        self.C = C
        self.n_in = n_in
        self.sess = sess
        self.build_graph()
    # end constructor

    def build_graph(self):
        self.add_input_layer()
        self.add_forward_path() 
        self.add_output_layer()
        self.add_backward_path()
    # end method build_graph


    def add_input_layer(self):
        self.X = tf.placeholder(shape=(None, self.n_in), dtype=tf.float32)
        self.Y = tf.placeholder(shape=[None, 1], dtype=tf.float32)
        self._batch_size = tf.shape(self.X)[0]
    # end method add_input_layer


    def add_forward_path(self):
        with tf.variable_scope('svm'):
            self.logits = tf.layers.dense(self.X, 1)
    # end method add_forward_path


    def add_output_layer(self):
        self.pred = tf.sign(self.logits)
    # end method add_output_layer


    def add_backward_path(self):
        with tf.variable_scope('svm', reuse=True):
            regu_loss = 0.5 * tf.reduce_sum(tf.square(tf.get_variable('dense/kernel')))
        hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros([self._batch_size,1]), 1-self.Y*self.logits))
        self.loss = regu_loss + self.C * hinge_loss
        self.train_op = tf.train.AdamOptimizer().minimize(self.loss)
        self.acc = tf.reduce_mean(tf.cast(tf.equal(self.pred, self.Y), tf.float32))
    # end method add_backward_path


    def fit(self, X, Y, val_data, n_epoch=50, batch_size=100):
        print("Train %d samples | Test %d samples" % (len(X), len(val_data[0])))
        log = {'loss':[], 'acc':[], 'val_loss':[], 'val_acc':[]}
        
        self.sess.run(tf.global_variables_initializer()) # initialize all variables
        for epoch in range(n_epoch):
            for X_batch, Y_batch in zip(self.gen_batch(X, batch_size), # batch training
                                        self.gen_batch(Y, batch_size)):
                _, loss, acc = self.sess.run([self.train_op, self.loss, self.acc],
                                             {self.X:X_batch, self.Y:Y_batch})
            val_loss_list, val_acc_list = [], [] # compute validation loss and acc
            for X_test_batch, Y_test_batch in zip(self.gen_batch(val_data[0], batch_size),
                                                  self.gen_batch(val_data[1], batch_size)):
                v_loss, v_acc = self.sess.run([self.loss, self.acc],
                                              {self.X:X_test_batch, self.Y:Y_test_batch})
                val_loss_list.append(v_loss)
                val_acc_list.append(v_acc)
            val_loss, val_acc = self.list_avg(val_loss_list), self.list_avg(val_acc_list)

            # append to log
            log['loss'].append(loss)
            log['acc'].append(acc)
            log['val_loss'].append(val_loss)
            log['val_acc'].append(val_acc)
            # verbose
            if epoch % 5 == 0:
                print ("%d / %d: train_loss: %.4f train_acc: %.4f | test_loss: %.4f test_acc: %.4f"
                    % (epoch+1, n_epoch, loss, acc, val_loss, val_acc))
            
        return log
    # end method fit


    def predict(self, X_test, batch_size=100):
        if batch_size is None:
            batch_size = len(X_test)
        batch_pred_list = []
        for X_test_batch in self.gen_batch(X_test, batch_size):
            batch_pred = self.sess.run(self.pred, {self.X:X_test_batch})
            batch_pred_list.append(batch_pred)
        return np.vstack(batch_pred_list)
    # end method predict


    def gen_batch(self, arr, batch_size):
        for i in range(0, len(arr), batch_size):
            yield arr[i : i+batch_size]
    # end method gen_batch


    def list_avg(self, l):
        return sum(l) / len(l)
    # end method list_avg
# end class LinearSVMClassifier