# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys
import os
import codecs
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

def gen_template_queries(file, list_context_files):
	for f in list_context_files:
		with open('context_queries/' + f + '.txt') as data_f:
			for q in data_f.readlines():
				file.write(q)
			file.write('\n')

template_p_queries_file = codecs.open('p_queries.txt', 'w', 'utf-8')
template_n_queries_file = codecs.open('n_queries.txt', 'w', 'utf-8')
#read context p queries
list_context_files = ["location"]
gen_template_queries(template_p_queries_file, list_context_files)
template_p_queries_file.close()
#read normal queries
list_context_files = ["combine", "cost", "quality", "time", "type"]
gen_template_queries(template_n_queries_file, list_context_files)
template_n_queries_file.close()

#load variable values
gaz_files = ["cost", "command", "quality", "time", "type"]
seed_variables = {}
for f in gaz_files:
	with open('n_variables/' + f) as data_f:
		seed_variables[f] = data_f.readlines()

#generate gaz file
gaz_file = codecs.open("uet-search-gaz.txt", "w", 'utf-8')
for v, vals in seed_variables.iteritems():
	for val in vals:
		if not val.strip('\n').replace('.', '', 1).isdigit() and not val.strip('\n').isdigit():
			gaz_file.write(v + '\t' + val.strip('\n') + '\n')