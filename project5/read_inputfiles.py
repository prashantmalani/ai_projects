from os import listdir
from os.path import isfile, join
import string

OUTTAB = ' ' * len(string.punctuation)

def readFiles(inputdir):
    """ Helper function to read all the files in a particular dir into lines
    lines of text in a list.
    Returns:
        List containing all the files in strings
    """
    files = [f for f in listdir(inputdir) if isfile(join(inputdir, f))]
    text_list = []

    # Read in stopwords
    stopwords = []
    with open('stopwords.en.txt', 'r') as f:
        data = f.read()
        stopwords = data.split()

    # Read files one by one.
    for f in files:
        file_str = readFile_(join(inputdir, f), stopwords)
        text_list.append(file_str)
    return text_list

def readFile_(inputpath, stopwords):
    data = ""
    with open(inputpath, 'r') as f_handle:
        data = f_handle.readlines()[0]
        data = sanitizeData_(data, stopwords)
    return data

def sanitizeData_(data_str, stopwords):
    """ Internal function to sanitize the input data.
    """
    out = data_str.translate(string.maketrans(string.punctuation, OUTTAB))
    out = out.lower()
    out = ' '.join([word for word in out.split() if word not in stopwords])
    out = out.decode('unicode_escape').encode('ascii','ignore')
    return out

def sanitizeString(data_str):
    # Sanitization is performed in place
    stopwords = []
    with open('stopwords.en.txt', 'r') as f:
        data = f.read()
        stopwords = data.split()
    return sanitizeData_(data_str, stopwords)
