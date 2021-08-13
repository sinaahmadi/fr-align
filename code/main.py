# -*- coding: utf-8 -*-

import random
import json
from nltk.corpus import wordnet
import tlfi as tlfi
import dbnary as dbnary

"""
Sina Ahmadi - July 2021 - ATILF
Alignment of French resources, namely TLFi and Wiktionnaire

"""
wordnet_pos_mapper = {
	"verb": "v",
	"adjective": "a",
	"noun": "n",
	"adverb": "r"
}

def retrieve_WordNet_lemmata(word, pos, source_lang="eng", target_lang="fra"):
	"""
	Given a word in the source language, it retrieves the synsets
	associated to the word in the target language based the Open Multilingual Wordnet.
	"""
	senses = [synset.lemma_names(target_lang) for synset in wordnet.synsets(word, pos=pos, lang=source_lang)]
	return [item for subsenses in senses for item in subsenses]

def extract_mwsa_lemmata():
	"""
	Based on the lemmata used in the MWSA task (English data), extract French entries for our task.
	See https://github.com/elexis-eu/mwsa
	"""
	target_lemmata = dict()
	with open("../resources/mwa_en_lemmata.tsv", "r") as f: 
		frequent_words = {i.split("\t")[0]: i.split("\t")[1] for i in f.read().split("\n")}

	for word in frequent_words:
		word_senses = retrieve_WordNet_lemmata(word, wordnet_pos_mapper[frequent_words[word]])
		if len(word_senses):
			target_lemmata[word] = (word_senses[0], frequent_words[word])

	return target_lemmata

def convert_to_ontolex(microstructure):
	# convert json file into Ontolex-Lemon
	# print(microstructure)
	lemma, pos, senses = microstructure["lemma"], microstructure["pos"], microstructure["senses"]
	if "id" not in microstructure:
		lemma_id = "fr_" + shortuuid.uuid()[0:5]
	else:
		lemma_id = "fr_" + microstructure["id"]
	ontolex = """<http://elex.is/mwsa/#lemma_id> a ontolex:LexicalEntry ; 
		rdfs:label "lemma_label"@fr ;
		lexinfo:partOfSpeech   lexinfo:POS_tag ;
		""".replace("lemma_id", lemma_id).replace("lemma_label", lemma).replace("POS_tag", pos)

	senses_ids, sense_defs= list(), list()
	for sense in senses:
		if type(sense) == str:
			sense_id = lemma_id + "_" + shortuuid.uuid()[0:5]
			senses_ids.append("<http://elex.is/mwsa/#" + sense_id + ">")
			sense_defs.append("<http://elex.is/mwsa/#?id_sense> skos:definition \"?def\"@fr .".replace("?def", sense.replace("\"", "\\\"")).replace("?id_sense", sense_id))

	if len(senses_ids):
		ontolex = ontolex + "ontolex:sense " + ", ".join(senses_ids) + ".\n"
		ontolex = ontolex + "\n".join(sense_defs)

		return ontolex

	# if the microstructure is detected without any sense, return nothing
	return ""

def find_common_lemma(tlfi, wiktionary):
	# given tlfi and wiktionary, find common lemmat that exist in the two resources
	common = list()

def create_naisc_input(file_name):
	"""
	Given the extracted information from DBnary or TLFi, create a ttl file compatible with Naisc's input format
	"""
	prefixes = """
	@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
	@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .

	"""

	if False:
		# convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
		# found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
		wiktionary = dict()
		with open("fr_wiktionaire_10k.json", "r") as f:
			for lexeme in json.load(f)["results"]["bindings"]:
				lemma = lexeme["label"]["value"]
				pos = lexeme["pos"]["value"].split("#")[-1]
				if lemma + "_" + pos not in wiktionary:
					wiktionary[lemma + "_pos" + pos] = {"pos": pos, "senses": [lexeme["definition"]["value"]]}
				else:
					wiktionary[lemma + "_pos" + pos]["senses"].append(lexeme["definition"]["value"])

		wiktionary_file = list()
		for entry in wiktionary:
			wiktionary[entry]["lemma"] = entry.split("_pos")[0]
			wiktionary_file.append(convert_to_ontolex(wiktionary[entry]))

		with open("fr_wiktionaire_10k.ttl", "w") as f:
			f.write(prefixes + "\n\n".join(wiktionary_file))

	else:
		tlf_file = list()
		for file in os.listdir("extracted"):
			if file.endswith(".json"):
				print(file)
				with open(os.path.join("extracted", file), "r") as json_file:
					for entry in json.load(json_file):
						if type(entry["lemma"]) == str and \
							type(entry["pos"]) == str and \
							entry["pos"] in tlf_pos_mapper and \
							" " not in entry["lemma"] and \
							"," not in entry["lemma"] and \
							len(entry["senses"]):
								# print(entry["lemma"])
								# entry["lemma"] + "_" + tlf_pos_mapper[entry["pos"]]
								entry["pos"] = tlf_pos_mapper[entry["pos"]]
								tlf_file.append(convert_to_ontolex(entry))
								# 1707236 headwords were found using this (03/08/2021)
		
		tlf_file = list(set(tlf_file))
		with open("tlf_all_cleaned_converted.ttl", "w") as f: #encoding='utf-8'
			f.write(prefixes + "\n\n".join(tlf_file))

def create_annotation_sheet(wiktionnaire, tlfi):
	# Given the retrieved data from both resources, create a sheet (tsv) for annotation
	pass

if __name__ == '__main__':
	"""
	Based on the lemmata used in the MWSA datasets (those of the English WordNet),
	extract synsets based on the French WordNet. Select 100 of them randomly and 
	create a dataset with common entries for evaluation purposes
	"""

	wiktionary, tlfi_dict = list(), list()
	for word in list(extract_mwsa_lemmata().values())[200: 300]: # random selection
		# print("Processing", word)

		lemma = word[0]
		pos = word[1]

		
		# lemma = "continuum"
		# pos = "noun"
		# gender = "masculine"

		# Look up TLFi
		entry_tlfi = tlfi.tlfi_lookup(lemma, pos)
		
		# Setting gender
		if pos == "noun" and "gender" in entry_tlfi: 
			gender = entry_tlfi["gender"]
		elif pos == "noun" and "gender" not in entry_tlfi:
			continue
		elif pos != "noun":
			gender = ""

		# print(lemma, pos, gender)
		# print(entry_tlfi)
		# exit()

		# Look up Wiktionnaire
		# convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
		entry_wiktionary = dict()
   
		for lexeme in dbnary.extract_dbnary(lemma, pos)["results"]["bindings"]:
		  if lexeme["lexeme"]["value"] not in entry_wiktionary:
		     if "gender" not in lexeme or (len(lexeme["gender"]["value"]) and lexeme["gender"]["value"].split("#")[-1] == gender):
		        entry_wiktionary[lexeme["lexeme"]["value"]] = {
		        "lemma": lemma,
		        "pos": pos,
		        "gender": gender,
		        "senses": {lexeme["sense"]["value"]: lexeme["definition"]["value"]}
		        }
		  else:
		     if "gender" not in lexeme or len(lexeme["gender"]["value"]) and lexeme["gender"]["value"].split("#")[-1] == gender:
		        entry_wiktionary[lexeme["lexeme"]["value"]]["senses"].update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})

		# print(entry_tlfi)
		# print(entry_wiktionary)
		if len(entry_tlfi) and len(entry_wiktionary):
			tlfi_dict.append(entry_tlfi)
			wiktionary.append(entry_wiktionary)

			print("%s|%s|%s\n%s\n%s"%(lemma, pos, gender, entry_tlfi["id"], list(entry_wiktionary.keys())[0]))
			for s_1 in entry_tlfi["senses"]:
				for s_2 in entry_wiktionary[list(entry_wiktionary.keys())[0]]["senses"]:
					print("\t%s\t%s\t\t%s\t%s"%(s_1, entry_tlfi["senses"][s_1], entry_wiktionary[list(entry_wiktionary.keys())[0]]["senses"][s_2], s_2))
			
			print()

	print(len(tlfi_dict) == len(wiktionary))
	with open("../output/wiktionnaire_annotation.json", "w", encoding='utf-8') as f:
		json.dump(wiktionary, f, indent=4, sort_keys=True)

	with open("../output/tlfi_annotation.json", "w", encoding='utf-8') as f:
		json.dump(tlfi_dict, f, indent=4, sort_keys=True)
	