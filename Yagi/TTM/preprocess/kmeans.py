import numpy as np
import pandas as pd
from gensim.models import word2vec
from sklearn.cluster import KMeans

K = 10

data = word2vec.Text8Corpus('../data/basket.txt')
model = word2vec.Word2Vec(sentences=data, sg=1, size=200, window=5, negative=5, iter=30, min_count=0)

item_id = np.array(list(model.vocab.keys()))
X = np.vstack([model[item_id[i]] for i in range(len(item_id))])

labels = KMeans(n_clusters=K, init='k-means++', random_state=0).fit_predict(X)

item_table = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/item_analyzed.csv")
df = pd.DataFrame(np.array([item_id, labels]).T, columns=['item_id', 'label'], dtype=np.int)
df = pd.merge(df, item_table, left_on='item_id', right_on='new_item_id', how='left').dropna()

res = df[['item_id_x', 'label']]
res.columns = ['new_item_id', 'label']

res.to_csv('~/Developer/M1/competition/data/item2category_kmeans_%d.csv' %K, index=False)
