import re
import os
import csv
import sys
import time
import json
import pandas as pd
from functools import reduce

def indexer(directory,out_index_file):
	words_dict = {}
	cwd = os.getcwd()
	os.chdir(cwd)

	for path, subdirs, files in os.walk(directory):
		for file in files:
			print("Reading " + os.path.join(path, file))
			with open(os.path.join(path, file), 'r') as f:
				# filter out special characters
				filtered_text = re.sub(r'[^\w\s]','', f.read().lower()) 
				words = filtered_text.split()
				for word in words:
					# add new word to dictionary
					if word not in list(words_dict.keys()):
						words_dict[word] = {}
						words_dict[word]["filePath"] = []
					words_dict[word]["filePath"].append(os.path.join(f.name).replace("/","\\"))

	with open(out_index_file, "wb") as index:
		index.write(json.dumps(words_dict))

def retriever(text,directory):
	# open index file
	with open(directory, 'r') as f: 
		email_index = json.load(f)

	filtered_text = re.sub(r'[^\w\s]','', text.lower()) 
	words_list = filtered_text.split()

	# retrieve documents with occurences of the text
	occurrence_paths = []
	for word in words_list:
		if word in email_index:
			occurrence_paths.append(set(email_index.get(word)["filePath"]))
		else: occurrence_paths.append(set([]))

	# get intersection of document lists with the text
	return set.intersection(*occurrence_paths)

def main(query,index_file,directory):
	start = time.clock()
	if not os.path.exists(index_file):
		print("Creating index file...")
		dictionary = indexer(directory,index_file)
	else: print("Files indexed!")

	retrieved = retriever(query,index_file)
	# if bool(retrieved):
	print("\nTEXT SEARCHED: " + query)
	print("\nSEARCH RESULTS:")
	for p in retrieved:
		print(p)
	print("\nText found in " + str(len(retrieved)) + " documents.")

	print("\nTime elapsed: " + str(time.clock() - start))

if __name__ == "__main__":
   main(sys.argv[1],sys.argv[2],sys.argv[3])
