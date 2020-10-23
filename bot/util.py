import sys
from .models import Textupload
#add frame to the image
def texttool(text_by_user):
    if len(text_by_user) > 10:
        result = "ok"
    else:
        result = "no"
    return result

#for pdf generator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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
word2id_len = len(word2id)
print('word2id_len:', word2id_len)

def jieba_validation(input_text):
    ad_ID = 0
    ad_Name = "測試產品"
    ad_Class = 0

    ad_Description = input_text

    # 單一廣告輸入
    test_data_df = pd.DataFrame({'ID': [ad_ID],
                                'Name':[ad_Name],
                                'Description':[ad_Description],
                                'Class':[ad_Class]})
    # 斷詞處理
    test_df = JeibaCutWords(test_data_df)

    # 關鍵字檢查
    test_df['keyword_flag'], keywords_list = AppendKeywordCheck(test_df)
    # 選取多少詞來當作輸入
    PICK_WORDS = 80  # 選前面80個詞當作輸入，這個長度要跟訓練模型的長度一樣

    docs_pred_id = []
    for doc in test_df['sentence']:
        text = doc[:PICK_WORDS]
        ids = [word2id_len]*PICK_WORDS
        ids[:len(text)] = [word2id[w] if w in word2id else word2id_len for w in text] # <OOV> is 50101
        docs_pred_id.append(ids)

    # 轉換後的sequence合併到dataframe
    test_df['sentence_seq'] = docs_pred_id

    x = test_df['sentence_seq'].tolist()
    x_pred = np.array(x)

    # Load trained model and feed data to predict
    model = tf.keras.models.load_model('./model/tf2_lstm_model')
    probability = model.predict(x_pred)

    if probability < 0.5:  # 合法
        keywords_list = []  # 合法廣告不用列出違規關鍵字
        return 0, probability[0][0], keywords_list
    else:  # 違法
        return 1, probability[0][0], keywords_list
