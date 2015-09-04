# -*- coding: utf-8 -*-
import os
startpath = "archive"
corpus_path = sorted([os.path.join("archive/", directories) for directories in os.listdir(startpath)])

filenames = []
for items in corpus_path:
    print items
    swag = [os.path.join(corpus_path, fn) for fn in os.listdir(items)]
    print swag
    #filenames.append(sorted([os.path.join(corpus_path, fn) for fn in os.listdir(items)]))

#print filenames