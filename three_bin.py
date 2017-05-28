import numpy as np
from datetime import datetime
import pickle

word_vecs = {}
csv_header = "word"
for x in range(1, 201):
    csv_header = csv_header + " V" + str(x)
csv_header = csv_header + "\n"
output_vocab_size=0
#split_at
# in_1 = '/media/hrisheekesh/9092CD7892CD6378/wikipedia-pubmed-and-PMC-w2v.bin'
# out_1 = '/media/hrisheekesh/9092CD7892CD6378/w2v_lower.csv'
# vocab_pkl = '/media/hrisheekesh/9092CD7892CD6378/vocab.pkl'
in_1 = 'data/ignore/wikipedia-pubmed-and-PMC-w2v.bin'
out_1 = 'data/ignore/w2v_2.csv'
vocab_pkl = 'data/vocab.pkl'
with open(vocab_pkl,'rb') as v:
    vocab = pickle.load(v)
    with open(in_1, "rb") as source, open(out_1, 'w', encoding='utf-8') as dest:
        dest.write(csv_header)
        header = source.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in range(vocab_size):
            word = []
            if line%10000==0:
                print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + str(line) + "// " + str(output_vocab_size))
            while True:
                ch = source.read(1)
                if ch == b' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    """print(ch.decode('cp437'))"""
                    word.append(ch.decode('cp437'))
            values = np.fromstring(source.read(binary_len), dtype='float32')
            word2 = word.strip()
            if word2 in vocab:
                dest.write(word + ' ' +  ' '.join(map(str, values))  + "\n")
                output_vocab_size+=1
