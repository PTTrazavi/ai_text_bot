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

#w2v = word2vec.Word2Vec.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../word2vec_model/zh.bin')) #GCP
w2v = word2vec.Word2Vec.load('word2vec_model/zh.bin')
word2id = {k:i for i, k in enumerate(w2v.wv.vocab.keys())}
id2word = {i:k for k, i in word2id.items()}
word2id_len = len(word2id) - 1
print('word2id_len:', word2id_len)

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
    test_df['keyword_flag'], keywords_list = AppendKeywordCheck(test_df)
    #
    # 選取多少詞來當作輸入
    #
    PICK_WORDS = 40
    batch_size = 16  # 若是資料筆數很多，一次讀batch_size筆資料來預測

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
    #
    # Load trained model and feed data to predict
    #
    pred_input = X_pred
    pred_batch_size = batch_size
    output_class = []
    output_probability = []

    with tf.Session() as sess:
        #saver = tf.train.import_meta_graph(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../model/lstm_model.meta')) # GCP
        saver = tf.train.import_meta_graph('./model/lstm_model.meta') # for local
        #saver.restore(sess, tf.train.latest_checkpoint(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../model/'))) # GCP
        saver.restore(sess, tf.train.latest_checkpoint('./model/')) # for local

        graph = tf.get_default_graph()
        # get_tensor_by_name格式:'tf.name_scope/variable name:0'
        inputs = graph.get_tensor_by_name('input_layer/input_data:0')
        class_prob = graph.get_tensor_by_name('output_logits/class_probability:0')
        predict_out = graph.get_tensor_by_name('predict_output/pred_out:0')

        for start in range(0, len(pred_input), pred_batch_size):
            end = min(start + batch_size, len(pred_input))

            x_pred_batch = pred_input[start:end]

            if np.ndim(x_pred_batch)==1:
                x_pred_batch = x_pred_batch.reshape([1,-1])

            #
            # 把剛剛載入的模型拿來用
            #
            pred_result, pred_prob = sess.run([predict_out, class_prob],
                                              feed_dict = {inputs:x_pred_batch})

            output_class.extend(pred_result)
            output_probability.extend(pred_prob)
    # 預測的類別
    y_pred_class = output_class

    # 預測的類別機率值
    output_probability = np.array(output_probability)
    Legal_prob = output_probability[:,0]    # column[0]是class 0的機率
    Violate_prob = output_probability[:,1]  # column[1]是class 1的機率

    # 單一廣告輸出

    return y_pred_class[0], Violate_prob[0], keywords_list
