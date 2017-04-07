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

    print stopwords
    for f in files:
        with open(join(inputdir, f), 'r') as f_handle:
            data = f_handle.readlines()[0]
            text_list.append(data)
            print "Raw data is:"
            print data
            print "Sanitized data is:"
            data = sanitizeData_(data, stopwords)
            print data
            raw_input('...')

    return text_list

def sanitizeData_(data_str, stopwords):
    """ Internal function to sanitize the input data.
    """
    out = data_str.translate(string.maketrans(string.punctuation, OUTTAB))
    out = out.lower()
    out = ' '.join([word for word in out.split() if word not in stopwords])
    return out
