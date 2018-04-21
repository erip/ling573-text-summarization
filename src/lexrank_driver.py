from lexrank import LexRankSummarizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def get_docs():
    return ()

if __name__ == "__main__":
    stemmer = PorterStemmer()
    summarizer = LexRankSummarizer(stemmer, threshold=0.1, epsilon=0.1, stop_words=set(stopwords.words('english')))

    docs = get_docs()

    sent_num = 1

    for sent in summarizer.summarize(docs, sent_num):
        print(sent)