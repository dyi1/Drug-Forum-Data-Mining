import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, 
from nltk.corpus import stopwords
import codecs

documents = []
with codecs.open("Master_File_Forums.txt", encoding = 'utf-8', mode= "r") as fid:
   for line in fid:
       documents.append(line)
stoplist = []
x = stopwords.words('english')
for word in x:
    stoplist.append(word)

##Removes Stopwords
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print dictionary
print corpus

tfidf = models.TfidfModel(corpus)
    
    
    
