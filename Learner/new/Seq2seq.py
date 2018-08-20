import tensorflow as tf
import numpy as np
import config

# Train Configurations
NUM_STEPS = config.FLAGS.num_steps
NUM_EPOCHES = config.FLAGS.num_epoches
NUM_CLASSES = config.FLAGS.num_classes

# GRU Configurations
NUM_GRU_NEURALS = config.FLAGS.num_gru_neurals
KEEP_PROB = config.FLAGS.keep_prob
NUM_FORWARD_LAYER = config.FLAGS.num_forward_layer
NUM_BACKWARD_LAYER = config.FLAGS.num_backward_layer

# Attention Configurations
POS_SIZE = config.FLAGS.pos_size
POS_NUM = config.FLAGS.pos_num
BIG_NUM = config.FLAGS.big_num

class Networks:
    def __init__(self, is_training, word_embeddings_in):
        # X (batches, step, inputs)
        # Y (num_classes)
        # "num_steps": Cut off Back-propagation - to feed num_steps inputs for each iteration
        self.is_trainning = is_training
        self.setPlaceHolders()
        self.calcEmbeddings(word_embeddings_in)
        self.setGRU()


    def setPlaceHolders(self):  # Out: all the placeHolders
        self.input_word = tf.placeholder(dtype = tf.int32, shape = [None, NUM_STEPS], name = 'input_word')
        self.input_pos1 = tf.placeholder(dtype = tf.int32, shape = [None, NUM_STEPS], name = 'input_pos1')
        self.input_pos2 = tf.placeholder(dtype = tf.int32, shape = [None, NUM_STEPS], name = 'input_pos2')
        self.input_y = tf.placeholder(dtype = tf.int32, shape = [None, NUM_CLASSES], name = 'input_y')
        self.total_shape = tf.placeholder(dtype = tf.int32, shape = [BIG_NUM + 1], name = 'total_shape')
        self.total_num = self.total_shape[-1]
    
    def calcEmbeddings(self, word_embeddings_in):   # Out: inputs_forward & inputs_backward
        with tf.device('/gpu:0'):
            with tf.variable_scope('Embedding'):
                word_embedding = tf.get_variable(initializer = word_embeddings_in, name = 'word_embeddings')
                pos1_embedding = tf.get_variable('pos1_embedding', shape = [POS_NUM, POS_SIZE])
                pos2_embedding = tf.get_variable('pos2_embedding', shape = [POS_NUM, POS_SIZE])
                self.inputs_forward = tf.concat(axis = 2, values = [ tf.nn.embedding_lookup(word_embedding, self.input_word),
                                                                tf.nn.embedding_lookup(pos1_embedding, self.input_pos1),
                                                                tf.nn.embedding_lookup(pos2_embedding, self.input_pos2) ])
                self.inputs_backward = tf.concat(axis = 2, values = [ tf.nn.embedding_lookup(word_embedding, tf.reverse(self.input_word, [1])),
                                                                tf.nn.embedding_lookup(pos1_embedding, tf.reverse(self.input_pos1, [1])),
                                                                tf.nn.embedding_lookup(pos2_embedding, tf.reverse(self.input_pos2, [1])) ])
    def setGRU(self):   # Out: outputs_forward & outputs_backward
        # Bidirectional GRU
        # Basic GRU
        gru_cell_forward = tf.contrib.rnn.GRUCell(num_units = NUM_GRU_NEURALS)
        gru_cell_backward = tf.contrib.rnn.GRUCell(num_units = NUM_GRU_NEURALS)
        # Dropouts
        if KEEP_PROB < 1:   # Otherwise there's no need for dropping
            gru_cell_forward = tf.contrib.rnn.DropoutWrapper(gru_cell_forward, output_keep_prob = KEEP_PROB)
            gru_cell_backward = tf.contrib.rnn.DropoutWrapper(gru_cell_backward, output_keep_prob = KEEP_PROB)
        # Stack GRUs
        cell_forward = tf.contrib.rnn.MultiRNNCell([gru_cell_forward] * NUM_FORWARD_LAYER)
        cell_backward = tf.contrib.rnn.MultiRNNCell([gru_cell_backward] * NUM_BACKWARD_LAYER)

        # Bi-GRU layer forward
        outputs_forward = []
        state_forward = cell_forward.zero_state(self.total_num, tf.float32) # init
        with tf.variable_scope('GRU_FORWARD') as scope:
            for step in range(NUM_STEPS):
                if step > 0:
                    scope.reuse_variables()
                (cell_output_forward, state_forward) = cell_forward(self.inputs_forward[:, step, :], state_forward)
                outputs_forward.append(cell_output_forward)

        # Bi-GRU layer backward
        state_backward = cell_backward.zero_state(self.total_num, tf.float32) # init
        outputs_backward = []
        with tf.variable_scope('GRU_FORWARD') as scope:
            for step in range(NUM_STEPS):
                if step > 0:
                    scope.reuse_variables()
                (cell_output_backward, state_backward) = cell_backward(self.inputs_forward[:, step, :], state_backward)
                outputs_backward.append(cell_output_backward)

        self.outputs_forward = tf.reshape(tf.concat(axis = 1, values = outputs_forward), [self.total_num, NUM_STEPS, NUM_GRU_NEURALS])
        self.outputs_backward = tf.reverse(tf.reshape(tf.concat(axis = 1, values = outputs_backward), [self.total_num, NUM_STEPS,NUM_GRU_NEURALS]), [1])

    def setAttention(self):
        attention_w = tf.get_variable('attention_omega', [NUM_GRU_NEURALS, 1])
        sen_a = tf.get_variable('attention_A', [NUM_GRU_NEURALS])
        sen_r = tf.get_variable('query_r', [NUM_GRU_NEURALS, 1])
        relation_embedding = tf.get_variable('relation_embedding', [NUM_CLASSES, NUM_GRU_NEURALS])
        sen_d = tf.get_variable('bias_d', [NUM_CLASSES])
        
        sen_repre = []
        sen_alpha = []
        sen_s = []
        sen_out = []
        self.prob = []
        self.predictions = []
        self.loss = []
        self.accuracy = []
        self.total_loss = 0.0

        # word-level attention layer
        output_h = tf.add(self.outputs_forward, self.outputs_backward)
        attention_r = tf.reshape(tf.matmul(tf.reshape(tf.nn.softmax(
            tf.reshape(tf.matmul(tf.reshape(tf.tanh(output_h), [self.total_num * NUM_STEPS, NUM_GRU_NEURALS]), attention_w),
                       [self.total_num, NUM_STEPS])), [self.total_num, 1, NUM_STEPS]), output_h), [self.total_num, NUM_GRU_NEURALS])

        # sentence-level attention layer
        for i in range(BIG_NUM):
            sen_repre.append(tf.tanh(attention_r[self.total_shape[i]: self.total_shape[i + 1]]))
            batch_size = self.total_shape[i + 1] - self.total_shape[i]

            sen_alpha.append(tf.reshape(tf.nn.softmax(tf.reshape(tf.matmul(tf.multiply(sen_repre[i], sen_a), sen_r), [batch_size])), [1, batch_size]))
            sen_s.append(tf.reshape(tf.matmul(sen_alpha[i], sen_repre[i]), [NUM_GRU_NEURALS, 1]))
            sen_out.append(tf.add(tf.reshape(tf.matmul(relation_embedding, sen_s[i]), [NUM_CLASSES]), sen_d))

            self.prob.append(tf.nn.softmax(sen_out[i]))

            with tf.name_scope("output"):
                self.predictions.append(tf.argmax(self.prob[i], 0, name = "predictions"))

            with tf.name_scope("loss"):
                self.loss.append(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = sen_out[i], labels = self.input_y[i])))
                if i == 0:
                    self.total_loss = self.loss[i]
                else:
                    self.total_loss += self.loss[i]

            with tf.name_scope("accuracy"):
                self.accuracy.append(tf.reduce_mean(tf.reduce_mean(tf.cast(tf.equal(self.predictions[i], tf.argmax(self.input_y[i], 0)), "float"), name = "accuracy")))

            tf.summary.scalar('loss', self.total_loss)

            #regularization
            self.l2_loss = tf.contrib.layers.apply_regularization(regularizer = tf.contrib.layers.l2_regularizer(scale = 0.0001), weights_list = tf.trainable_variables())        

            self.final_loss = self.total_loss + self.l2_loss
            tf.summary.scalar('l2_loss', self.l2_loss)
            tf.summary.scalar('final_loss', self.final_loss)
