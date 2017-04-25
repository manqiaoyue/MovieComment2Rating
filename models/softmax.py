import numpy as np
import tensorflow as tf


# just to see if it works
class Softmax(object):
    def __init__(self, sent_length, class_num, embedding_size, l2_lambda):
        self.input_x = tf.placeholder(tf.float32, [None, sent_length, embedding_size], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, class_num], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        l2_loss = tf.constant(0.0)

        with tf.name_scope("flat"):
            self.flatted = tf.reshape(self.input_x, [-1, sent_length * embedding_size])

        with tf.name_scope("linear"):
            weights = tf.get_variable(
                "W",
                shape=[sent_length * embedding_size, class_num],
                initializer=tf.contrib.layers.xavier_initializer())
            bias = tf.Variable(tf.constant(0.1, shape=[class_num]), name="b")
            l2_loss += tf.nn.l2_loss(weights)
            l2_loss += tf.nn.l2_loss(bias)
            self.linear_result = tf.nn.xw_plus_b(self.flatted, weights, bias, name="linear")
            self.predictions = tf.arg_max(self.linear_result, 1, name="predictions")

        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.linear_result, labels=self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_lambda * l2_loss

        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")