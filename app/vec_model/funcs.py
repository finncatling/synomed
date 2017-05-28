import os
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


probs = pd.read_csv(os.path.join('data', 'word_probs.csv'))

w2v = pd.read_table(os.path.join('data', 'w2v.csv.csv'))
w2v.columns = [0]
w2v = w2v[0].str.split(expand=True)
w2v.set_index(0, inplace=True)
w2v = w2v.astype(float)

icd10 = pd.read_csv(os.path.join('data', 'icd10.csv'))
icd10_emb_exploded = pd.read_csv('data/icd10_emb_exploded.csv')
icd10_emb_exploded.set_index(icd10.code, inplace=True)
icd10_emb_exploded.drop('code', axis=1, inplace=True)

# get rid of any codes with zero embeddings
drop = icd10_emb_exploded[np.sum(icd10_emb_exploded,1)==0].index
icd10_emb_exploded.drop(drop, inplace=True)


def query_emb(query, w2v=w2v, probs=probs):
    q_tokens = word_tokenize(query)

    query_emb = np.zeros(200)
    a = 10**-4

    for token in q_tokens:
        try:
            word_emb = w2v.loc[token].values
        except KeyError:
            word_emb = np.zeros(200)

        try:
            word_p = probs.loc[probs['word'] == token, 'prob'].values[0]
        except IndexError:
            word_p = 1.104473e-07

        query_emb += (a / (a + word_p)) * word_emb

    return query_emb / len(q_tokens)


def princi(q_emb, icd10=icd10_emb_exploded):
    pca = PCA(n_components=1)

    q_emb2 = pd.DataFrame(q_emb).T
    q_emb2 = q_emb2.astype(float)
    q_emb2.index.name = "code"
    q_emb2 = q_emb2.T
    q_emb2.columns = icd10.columns
    icd_and_q = icd10.append(q_emb2)
    pca.fit(icd_and_q.values)
    u = pca.components_.T
    output_embs = (icd_and_q.values.T -
                   np.dot(np.dot(u, u.T), icd_and_q.values.T))
    return output_embs


def parse_input(q_input):
    q_input = [x.lower() for x in q_input]
    q_emb = np.zeros([len(q_input), 200])
    for x in range(len(q_input)):
        q_emb[x, :] = query_emb(q_input[x])
    return princi(q_emb)


def find_codes(
    q_input,
    n_neighbours=5,
    icd10_emb_exploded=icd10_emb_exploded,
    icd10=icd10
):
    final_embs = parse_input(q_input)
    q_emb = final_embs[:, icd10_emb_exploded.shape[0]:].T

    nn = NearestNeighbors(n_neighbors=n_neighbours)
    nn.fit(final_embs[:, :icd10_emb_exploded.shape[0]].T)

    output = []
    for j in range(len(q_input)):
        dict1 = {}
        query = q_emb[j, :]
        distances, indexes = nn.kneighbors(
            query.reshape(1, final_embs.shape[0])
        )
        dict1["search"] = q_input[j]

        # denom = np.sum(np.e**distances[0])

        for i in range(len(distances[0])):
            dict1[i] = {}
            dict1[i]['code'] = icd10.loc[indexes[0][i], ['code']].values[0]
            dict1[i]['description'] = icd10.loc[indexes[0][i], ['description']].values[0]
            dict1[i]['distance'] = distances[0][i]

            # dict1[i]['percent'] = np.e**distances[0][i] / denom
            # percent = 100 - 100 * distances[0][i] / 3

            if distances[0][i] > 3:
                dict1[i]['percent'] = 0
            else:
                dict1[i]['percent'] = 100 - 100 * distances[0][i] / 3

        output.append(dict1)

    return output
