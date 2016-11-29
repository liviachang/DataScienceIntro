from __future__ import division
from pymongo import MongoClient
import sys
import numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.preprocessing import normalize

def get_texts(coll):
    texts = []
    for doc in coll.find():
        strs = doc['content']
        strs = ' '.join(strs)
        texts.append(strs)
    return texts

def get_collections(db_nm='nyt_dump', tbl_nm='articles'):
    client = MongoClient()
    db = client[db_nm]
    coll = db[tbl_nm]
    return coll

def tokenize(texts):
    tokens = []
    for txt in texts:
        ## convert to the lower case
        data = txt.lower()
        data = word_tokenize(data)
        tokens.append(data)
    return tokens

def strip_stopwords(tokens_all):
    stop_wds = stopwords.words('english')
    tokens = []
    for ta in tokens_all:
      tokens.append( [t for t in ta if t not in stop_wds] )
    return tokens

def stem(tokens, option=['PORTER', 'SNOWBALL', 'WORDNET'][2]):
    # reference:
    # http://stackoverflow.com/questions/1787110/what-is-the-true-difference-between-lemmatization-vs-stem
    stem_tks = []
    if (option=='PORTER'):
        stem_tool = PorterStemmer()
    elif (option=='SNOWBALL'):
        stem_tool = SnowballStemmer('english')
    elif (option=='WORDNET'):
        stem_tool = WordNetLemmatizer()

    for t_lst in tokens:
        if option in ['PORTER', 'SNOWBALL']:
            stem_tks.append( [stem_tool.stem(t) for t in t_lst] )
        else:
            stem_tks.append( [stem_tool.lemmatize(t) for t in t_lst])
    return stem_tks

def get_bag_of_words(stem_tks):
    stem_tks_lst = []
    for stks in stem_tks:
        stem_tks_lst = stem_tks_lst + stks
    bwds = set(stem_tks_lst)
    bwds = sorted(list(bwds))
    return bwds

def create_dict_bwds(bwds):
    output = {w: bwds.index(w) for w in bwds}
    return output

def get_wd_count(stem_tks, bwds):
    output = []
    for st in stem_tks:
        output.append( [st.count(v) for v in bwds] )
    return np.array(output)

def get_doc_freq(wd_cts):
    doc_freqs = np.sum(wd_cts>0, axis=0)
    return doc_freqs

def normalize_term_freq(wd_cts, doc_freqs):
    n_docs = wd_cts.shape[0]
    idf = np.log( (1+n_docs) /(1+doc_freqs)) + 1
    tfidf = np.multiply(wd_cts, idf)
    tfidf = normalize(tfidf, norm='l2')
    return tfidf



if __name__ == '__main__':
    option = ['manual', 'sklearn'][0]
    
    if (option=='manual'):
        ## load the data
        coll = get_collections()

        ## parse the raw articles to tokens
        texts = get_texts(coll) ## len=999
        tokens_all = tokenize(texts)
        tokens = strip_stopwords(tokens_all)
        stem_tks = stem(tokens)

        ## build the vocab for word counts
        vocab = get_bag_of_words(stem_tks)
        vocab_dict = create_dict_bwds(vocab)

        ## create word counts for each document
        wd_cts = get_wd_count(stem_tks, vocab)
        ## create the document frequencies
        doc_freqs = get_doc_freq(wd_cts)
        ##
        tfidf = normalize_term_freq(wd_cts, doc_freqs)
    elif (option == 'sklearn'):
        vect = CountVectorizer(stop_words='english')
        word_counts = vect.fit_transform(documents)
        ## FIXME



