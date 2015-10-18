from gensim import dictionary 

class Corpus(object):
	def __init__(filename):
		self.filename = filename

	def __iter__(self):
		for line in open(filename,'r'):
			yield dictionary.doc2bow(line)
