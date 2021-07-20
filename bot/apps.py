from django.apps import AppConfig
# the model is loaded only once, and not every time the endpoint is called
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

class BotConfig(AppConfig):
    name = 'bot'
    # the model is loaded only once, and not every time the endpoint is called
    Sess = tf.Session()
    Graph = tf.get_default_graph()
    set_session(Sess)
    # model = tf.keras.models.load_model(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../model/tf2_lstm_model')) #GCP
    model = tf.keras.models.load_model('./model/tf2_lstm_model')
    print("loaded model!!!!!")
