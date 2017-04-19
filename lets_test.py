# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys
import os
import codecs
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')
	
#generate sample for train test
generated_queries_file = codecs.open("test/p_gen_queries.txt", "w", "utf-8")
#labled file
tagged_test_file = open("test/uet-ner-in.test", "w")
def label(file_name, seed_variables):
	with open(file_name) as file:
		for line in file.readlines():
			if not line == "\n":
				lineStr = line.strip('\n')
				tokens = line.split()
				for v, vals in seed_variables.iteritems():
					for val in vals:
						val = val.strip('\n')
						i = lineStr.find(val)
						if i is not -1:
							valTokens = val.split()
							j = -1
							jj = 0
							for t in tokens:
								if t == valTokens[0]:
									j = jj
									break;
								jj = jj + 1
							#j = tokens.index(valTokens[0]);
							if j == -1:
								print (line)
								print (val)
								print ("@@-1")
							t = 0
							while (t < len(valTokens)):
								t = t + 1
								if j >= len(tokens):
									print (line)
									print (val)
								tokens[j] = tokens[j] + '\t' + v
								j = j + 1
							break;
							
				for token in tokens:
					if len(token.split())==1:
						token = token + '\t' + 'O'
					tagged_test_file.write(token+'\n')
				tagged_test_file.write('\n')

def gen_comb(crr_index, duplicated_vars, crr_line, seed_variables):
	i = 0
	f_val = "@"
	f_i_line = -1
	vals = seed_variables[duplicated_vars[crr_index]]
	for val in vals:
		val = val.strip('\n')
		j = crr_line.find(val)
		if j is not -1:
			f_i_line = j
			f_val = val
			break
		i = i + 1
	if f_i_line is -1:
		if crr_index == len(duplicated_vars)-1:
			generated_queries_file.write(crr_line+'\n')
		else:
			gen_comb(crr_index+1, duplicated_vars, crr_line, seed_variables)	
	else:
		dline = crr_line.replace(f_val, "")
		for val in vals:
			newdline = dline[:f_i_line] + val.strip("\n") + dline[f_i_line:]
			if crr_index == len(duplicated_vars)-1:
				generated_queries_file.write(newdline + "\n")
			else:
				gen_comb(crr_index+1, duplicated_vars, newdline, seed_variables)

def gen_queries(template_queries, duplicated_vars, seed_variables):
	for line in template_queries:
		line = line.strip('\n')
		gen_comb(0, duplicated_vars, line, seed_variables)

template_queries_file = open('p_queries.txt')
#read template queries
template_queries = template_queries_file.readlines()
duplicated_vars = []
#load variable values in p_variables folder
seed_variables = {}
for f in os.listdir('./test/variables'):
	duplicated_vars.append(f)
	with open('test/variables/' + f) as data_f:
		seed_variables[f] = data_f.readlines()	
gen_queries(template_queries, duplicated_vars, seed_variables)
generated_queries_file.close()
label("test/p_gen_queries.txt", seed_variables)
template_queries_file.close()

generated_queries_file = codecs.open("test/n_gen_queries.txt", "w", "utf-8")
template_queries_file = open('n_queries.txt')
#read template queries
template_queries = template_queries_file.readlines()
#load variable values in p_variables folder	
gen_queries(template_queries, duplicated_vars, seed_variables)
generated_queries_file.close()
label("test/n_gen_queries.txt", seed_variables)
template_queries_file.close()

#tagged_test_file.close()

#test new combine context
tagged_test_file = open("test/uet-ner-nc.test", "w")
generated_queries_file = codecs.open("test/nc_gen_queries.txt", "w", "utf-8")
template_queries_file = open('test/contexts/combine.txt')
#read template queries
template_queries = template_queries_file.readlines()
#load variable values in p_variables folder	
gen_queries(template_queries, duplicated_vars, seed_variables)
generated_queries_file.close()
label("test/nc_gen_queries.txt", seed_variables)
template_queries_file.close()

tagged_test_file.close()
#test
subprocess.call(['java', '-cp', 'stanford-ner.jar', 'edu.stanford.nlp.ie.crf.CRFClassifier', '-loadClassifier', 'model/uet-search-ner-new.gz', '-testFile', 'test/uet-ner-in.test'])