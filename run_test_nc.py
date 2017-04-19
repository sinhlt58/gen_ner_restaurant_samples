# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import codecs
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')
#test
subprocess.call(['java', '-cp', 'stanford-ner.jar', 'edu.stanford.nlp.ie.crf.CRFClassifier', '-loadClassifier', 'model/uet-search-ner-new.gz', '-testFile', 'test/uet-ner-nc.test'])