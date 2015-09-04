# -*- coding: utf-8 -*-
import os
startpath = os.path.join("Erowid/", "archive") # Should be ...\archive
CORPUS_PATHS = sorted([os.path.join("Erowid/archive/", directories) for directories in os.listdir(startpath)])
filenames = []
for items in CORPUS_PATHS:
    filenames.append(sorted([os.path.join(CORPUS_PATHS, fn) for fn in os.listdir(items)]))

print filenames