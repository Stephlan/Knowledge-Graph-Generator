import tensorflow as tf

tf.app.flags.DEFINE_string("train_file", "./Data/...", "Train Data")
tf.app.flags.DEFINE_integer("num_steps", 70, "Cut off Back-propagation as num_step long")
tf.app.flags.DEFINE_integer("num_epoches", 30, "Number of epoches")
tf.app.flags.DEFINE_integer("num_classes", 12, "The total class number")
tf.app.flags.DEFINE_integer("num_gru_neurals", 230, "Number of neurals in a GRU")
tf.app.flags.DEFINE_integer("keep_prob", 0.5, "Probabilty that we keep a node instead of dropping it out")
tf.app.flags.DEFINE_integer("num_forward_layers", 1, "Number of forward layers")
tf.app.flags.DEFINE_integer("num_backward_layers", 1, "Number of backward layers")
tf.app.flags.DEFINE_integer("pos_size", 5, "")
tf.app.flags.DEFINE_integer("pos_num", 123, "")
tf.app.flags.DEFINE_integer("big_num", 50, "")

FLAGS = tf.app.flags.FLAGS
