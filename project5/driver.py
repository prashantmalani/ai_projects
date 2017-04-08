import read_inputfiles
import os
import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer

#train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
#test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
train_path = "/Users/pmalani/ai_projects/project5/aclImdb/train"
test_path = '/Users/pmalani/ai_projects/project5/imdb_te.csv'


def imdb_data_preprocess():
    # Read in positive reviews
    pos_data = read_inputfiles.readFiles(os.path.join(train_path, 'pos'))
    neg_data = read_inputfiles.readFiles(os.path.join(train_path, 'neg'))
    with open('imdb_tr.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('', 'text', 'polarity'))
        i = 0
        for line in pos_data:
            writer.writerow((i, line, 1))
            i += 1
        for line in neg_data:
            writer.writerow((i, line, 0))
            i += 1

def get_test_data():
    df = pd.read_csv(test_path)
    raw_data = df[df.columns[1]][:]
    sanitized_data = []
    for line in raw_data:
        sanitized_data.append(read_inputfiles.sanitizeString(line))
    new_df = pd.DataFrame(sanitized_data, columns=['text'])
    return new_df



def unigram_ml():
    # First load data via pandas
    df = pd.read_csv('imdb_tr.csv')
    df = df.iloc[np.random.permutation(len(df))]
    df = df.reset_index(drop=True)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(df["text"])
    Y_train = df["polarity"]
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(X_train_counts, Y_train)
    df_test = get_test_data()
    X_test_counts = count_vect.transform(df_test["text"])
    result = clf.predict(X_test_counts)
    with open('unigram.output.txt', 'w') as f:
        for val in result:
            f.write('%d\n' % val)

def unigram_tfidf_ml():
    # First load data via pandas
    df = pd.read_csv('imdb_tr.csv')
    df = df.iloc[np.random.permutation(len(df))]
    df = df.reset_index(drop=True)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(df["text"])
    Y_train = df["polarity"]

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(X_train_tfidf, Y_train)
    df_test = get_test_data()

    X_test_counts = count_vect.transform(df_test["text"])
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    result = clf.predict(X_test_tfidf)
    with open('unigramtfidf.output.txt', 'w') as f:
        for val in result:
            f.write('%d\n' % val)


if __name__ == "__main__":
     imdb_data_preprocess()
     unigram_ml()
     unigram_tfidf_ml()
     pass
