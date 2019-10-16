import sys
from .models import Textupload
#add frame to the image
def texttool(text_by_user):
    if len(text_by_user) > 10:
        result = "ok"
    else:
        result = "no"
    return result

### for jeiba
import os
import tensorflow as tf
#import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
from gensim.models import word2vec
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from .OpenFabLibrary import JeibaCutWords
from .OpenFabLibrary import AppendKeywordCheck

WORD2VEC_DIMENTION = 128
#w2v = word2vec.Word2Vec.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../word2vec_model/CBOW')) #GCP
w2v = word2vec.Word2Vec.load('word2vec_model/CBOW') #for local
word2id = {k:i for i, k in enumerate(w2v.wv.vocab.keys())}
id2word = {i:k for k, i in word2id.items()}
word2id_len = len(word2id) -1
print('word2id_len:', word2id_len)

ii = 0
embedding = np.zeros((word2id_len+1, WORD2VEC_DIMENTION))
for k, v in word2id.items():
    embedding[v] = w2v.wv[k]

def jieba_validation(input_text):
    ad_ID = 0
    ad_Name = "測試產品"
    ad_Class = 0

    ad_Description = input_text

    test_data_df = pd.DataFrame({'ID': [ad_ID],
                                 'Name':[ad_Name],
                                 'Description':[ad_Description],
                                 'Class':[ad_Class]})
    # 斷詞處理
    test_df = JeibaCutWords(test_data_df)
    #test_df = CkipCutWords(test_data_df)

    # 關鍵字檢查
    test_df['keyword_flag'] = AppendKeywordCheck(test_df)
    #
    # 選取多少詞來當作輸入
    #
    PICK_WORDS = 40

    number_of_classes = 2  # 合法、違法廣告
    sample_per_class  = 8

    # epochs            = 200  #100
    batch_size        = number_of_classes * sample_per_class

    docs_pred_id = []
    for doc in test_df['sentence']:
        text = doc[:PICK_WORDS]
        ids = [word2id_len+1]*PICK_WORDS
        ids[:len(text)] = [word2id[w] if w in word2id else word2id_len+1 for w in text]
        docs_pred_id.append(ids)

    # 轉換後的sequence合併到dataframe
    test_df['sentence_seq'] = docs_pred_id
    #print(test_df.head(5))

    x = test_df['sentence_seq'].tolist()
    X_pred = np.array(x)
    y_pred = test_df['class'].as_matrix()
    y_keyword_flag = test_df['keyword_flag'].as_matrix()

    pred_input = X_pred
    pred_batch_size = batch_size
    pred_data = []

    with tf.Session() as sess:
        #saver = tf.train.import_meta_graph(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../model/lstm_model.meta')) # GCP
        saver = tf.train.import_meta_graph('./model/lstm_model.meta') # for local
        #saver.restore(sess, tf.train.latest_checkpoint(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../model/'))) # GCP
        saver.restore(sess, tf.train.latest_checkpoint('./model/')) # for local

        #print(tf.get_collection('training_collection'))  # get_collection返回list，裡面存放訓練模型時候的變數
        #inputs = tf.get_collection("training_collection")[0]
        #predict_ans = tf.get_collection("training_collection")[1]

        graph = tf.get_default_graph()
        # get_tensor_by_name格式:'tf.name_scope/variable name:0'
        inputs = graph.get_tensor_by_name('input_layer/input_data:0')
        predict_ans = graph.get_tensor_by_name('predict_output/pred_ans:0')

        for start in range(0, len(pred_input), pred_batch_size):
            end = min(start + batch_size, len(pred_input))
            #print('start:', start)
            #print('end:', end)

            x_pred_batch = pred_input[start:end]

            if np.ndim(x_pred_batch)==1:
                x_pred_batch = x_pred_batch.reshape([1,-1])

            #
            # 把剛剛載入的模型拿來用
            #
            x_pred = sess.run(predict_ans,
                              feed_dict = {inputs:x_pred_batch})

            pred_data.extend(x_pred)
    #
    # 預測的答案
    #
    y_pred_class = pred_data
    return y_pred_class[0]
