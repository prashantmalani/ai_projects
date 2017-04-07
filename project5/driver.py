import read_inputfiles
import os

#train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
#test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
train_path = "/Users/pmalani/ai_projects/project5/aclImdb/train"


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
 	'''Implement this module to extract
	and combine text files under train_path directory into
    imdb_tr.csv. Each text file in train_path should be stored
    as a row in imdb_tr.csv. And imdb_tr.csv should have two
    columns, "text" and label'''


if __name__ == "__main__":
     data = read_inputfiles.readFiles(os.path.join(train_path, 'pos'))
     print data
     pass
