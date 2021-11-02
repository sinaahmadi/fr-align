# -*- coding: utf-8 -*-

import random
import json
import tlfi as tlfi
import dbnary as dbnary
import string
import shortuuid
from nltk.corpus import wordnet
import rdflib.graph as g
shortuuid.set_alphabet(string.digits)

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

def convert_to_ontolex(microstructure, dataset_name="TLFi"):
	# convert json file into Ontolex-Lemon
	# print(microstructure)
	lemma, pos, senses = microstructure["lemma"], microstructure["pos"], microstructure["senses"]
	
	if dataset_name == "Wiktionnaire":
		lemma_id = microstructure["lemma_id"]
	else:
		lemma_id = "https://www.cnrtl.fr/definition/" + microstructure["id"]
	ontolex = """<lemma_id> a ontolex:LexicalEntry ; 
		rdfs:label "lemma_label"@fr ;
		lexinfo:partOfSpeech   lexinfo:POS_tag ;
		""".replace("lemma_id", lemma_id).replace("lemma_label", lemma).replace("POS_tag", pos)

	if len(microstructure["gender"]):
		ontolex = ontolex + "lexinfo:gender lexinfo:?GENDER ;\n\t\t".replace("?GENDER", microstructure["gender"])

	senses_ids, sense_defs= list(), list()
	for sense in senses:
		if type(sense) == str:
			# sense_id = lemma_id + "_" + shortuuid.uuid()[0:5]
			if dataset_name == "TLFi":
				sense_id = lemma_id + "#" + sense.replace(" ", "").replace("\"", "")
			else:
				sense_id = sense.replace(" ", "").replace("\"", "")
			senses_ids.append("<" + sense_id + ">")
			# sense_defs.append("<http://elex.is/mwsa/#?id_sense> skos:definition \"?def\"@fr .".replace("?def", senses[sense].replace("\"", "\\\"")).replace("?id_sense", sense_id))
			sense_defs.append("\t\t<?id_sense> skos:definition \"?def\"@fr .".replace("?def", senses[sense]).replace("?id_sense", sense_id))

	if len(senses_ids):
		ontolex = ontolex + "ontolex:sense " + ", ".join(senses_ids) + ".\n"
		ontolex = ontolex + "\n".join(sense_defs)

		return ontolex

	# if the microstructure is detected without any sense, return nothing
	return ""

def find_common_lemma(tlfi, wiktionary):
	# given tlfi and wiktionary, find common lemmat that exist in the two resources
	common = list()

def create_naisc_input(dataset_name):
	"""
	Based on the lemmata in TLFi, retrieve data from Wiktionnaire. 
	create a dataset with common entries for trainsing purposes.
	Given the extracted information from DBnary or TLFi, create a ttl file compatible with Naisc's input format
	"""
	prefixes = """@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .
@prefix lime: <http://www.w3.org/ns/lemon/lime#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix contact: <http://www.w3.org/2000/10/swap/pim/contact#> .

<https://sinaahmadi.github.io/> 
  rdf:type contact:Person ;
  contact:fullName "Sina Ahmadi" ;
  contact:homePage <https://sinaahmadi.github.io/>, <https://github.com/sinaahmadi/fr-align> ;
  contact:mailbox <mailto:ahmadi.sina@outlook.com> .

RESNAME a lime:Lexicon ;
	lime:language "fra" ;
	dct:language <http://www.lexvo.org/page/iso639-3/fra> ;
	lime:lexicalEntries "COUNTER"^^xsd:integer ;
	dct:description "?DESC"@en ;
	dct:creator <www.atilf.fr> ;
	dct:created "2021-07-08"^^xsd:date ;
	dct:modified "2021-09-28"^^xsd:date .

# ===========================================================================

"""

	if dataset_name == "Wiktionnaire":
		# convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
		# found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
		# wiktionary = dict()
		wiktionary_file, entry_counter = list(), 0
		with open("../output/naisc/tlf_all_cleaned_converted_1000lines_headwords.txt", "r") as f:
			for entry in f.read().split("\n")[0:20]:
				senses = dict()
				print(entry)
				for lexeme in dbnary.extract_dbnary(entry.split("\t")[0], entry.split("\t")[1])["results"]["bindings"]:
					if len(entry.split("\t")) == 2: # no gender
						lemma = lexeme["label"]["value"]
						pos = lexeme["pos"]["value"].split("#")[-1]
						senses.update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})
						gender = ""

					elif len(entry.split("\t")) == 3 and "gender" in lexeme and entry.split("\t")[2] in lexeme["gender"]["value"]:
						lemma = lexeme["label"]["value"]
						pos = lexeme["pos"]["value"].split("#")[-1]
						gender = lexeme["gender"]["value"].split("#")[-1]
						senses.update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})

					entry_counter += 1
					# print(lexeme)
					print()
					wiktionary_file.append(convert_to_ontolex({"lemma_id": lexeme["lexeme"]["value"], "lemma": lemma, "pos": pos, "gender": gender, "senses": senses}, "Wiktionnaire"))

						
				# print(wiktionary)
				# if lemma + "_" + pos not in wiktionary:
				# 	wiktionary[lemma + "_pos" + pos] = {"pos": pos, "senses": senses}
				# else:
				# 	wiktionary[lemma + "_pos" + pos]["senses"].append(lexeme["definition"]["value"])

		# wiktionary_file = list()
		# for entry in wiktionary:
		# 	wiktionary[entry]["lemma"] = entry.split("_pos")[0]
		# 	wiktionary_file.append(convert_to_ontolex(wiktionary[entry], "Wiktionnaire"))

		prefixes_this = prefixes.replace("?DESC", "Wiktionnaire -- le projet lexicographique de la Wikimedia Foundation").replace("RESNAME", "<https://fr.wikipedia.org/wiki/Wiktionnaire>")
		prefixes_this = prefixes_this.replace("COUNTER", str(entry_counter))
		with open("../output/naisc/fr_wiktionaire_1000lines.ttl", "w") as f:
			f.write(prefixes_this + "\n\n".join(wiktionary_file))

	if dataset_name == "TLFi":
		# convert TLFi to Ontolex-Lemon
		# Retrieve the ID of the annoated entries to be excluded in the dataset
		annotated_IDs = list()
		for sheet in ["../output/annotation/Groupe_2_SA.tsv", "../output/annotation/Groupe_1_BG.tsv"]:
			with open(sheet, "r") as f:
				for i in f.read().split("\n"):
					if "https://www.cnrtl.fr/definition/" in i:
						annotated_IDs.append(i.strip())

		tlf_file, entry_counter = list(), 0
		with open("../output/extracted/tlfi_all.json", "r") as json_file:
			for file in json.load(json_file):
				for entry in file:
					if type(entry["lemma"]) == str and \
						type(entry["pos"]) == str and \
						" " not in entry["lemma"] and \
						"," not in entry["lemma"] and \
						len(entry["senses"]) and \
						"https://www.cnrtl.fr/definition/" + entry["id"] not in annotated_IDs:
							# print(entry["lemma"])
							# entry["lemma"] + "_" + tlf_pos_mapper[entry["pos"]]
							# entry["pos"] = tlf_pos_mapper[entry["pos"]]
							tlf_file.append(convert_to_ontolex(entry))
							entry_counter += 1
		
		tlf_file = list(set(tlf_file))
		prefixes_this = prefixes.replace("?DESC", "Le Trésor de la Language Française Informatisé (TLFi) in Ontolex-Lemon").replace("RESNAME", "<http://atilf.atilf.fr/>")
		prefixes_this = prefixes_this.replace("COUNTER", str(entry_counter))
		with open("../output/naisc/tlf_all_cleaned_converted.ttl", "w") as f: #encoding='utf-8'
			f.write(prefixes_this + "\n\n".join(tlf_file))

def combine_senses(senses_1, senses_2):
	# Given the retrieved senses from both resources, create a combination of senses for for annotation
	# senses_1: TLFi
	# senses_2: Wiktionary
	combined = list()
	for s_1 in senses_1:
		for s_2 in senses_2:
			combined.append("\t%s\t%s\t\t%s\t%s"%(s_1, senses_1[s_1], senses_2[s_2], s_2))
	return "\n".join(combined)

def create_annotation_sheets():
	"""
	Based on the lemmata used in the MWSA datasets (those of the English WordNet),
	extract synsets based on the French WordNet. Select 100 of them randomly and 
	create a dataset with common entries for evaluation purposes
	"""

	wiktionary, tlfi_dict, annotation_sheet = list(), list(), list()
	for word in list(extract_mwsa_lemmata().values())[300:500]: # random selection
		if "\'" in word[0]:# or word[1] != "adjective": #skip multi-word units
			continue
		print("Processing ", word)

		lemma = word[0]
		pos = word[1]

		
		# lemma = "continuum"
		# pos = "noun"
		# gender = "masculine"

		# Look up TLFi
		entry_tlfi = tlfi.tlfi_lookup(lemma, pos)
		
		# Setting gender
		gender = ""
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
				if "gender" not in lexeme or \
					((len(lexeme["gender"]["value"]) and lexeme["gender"]["value"].split("#")[-1] == gender)) or \
						pos == "adjective" or \
						pos == "adverb":
					entry_wiktionary[lexeme["lexeme"]["value"]] = {
					"lemma": lemma,
					"pos": pos,
					"gender": gender,
					"senses": {lexeme["sense"]["value"]: lexeme["definition"]["value"]}
					}
				else:
					if "gender" not in lexeme or len(lexeme["gender"]["value"]) and lexeme["gender"]["value"].split("#")[-1] == gender:
						entry_wiktionary[lexeme["lexeme"]["value"]]["senses"].update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})
			else:
				entry_wiktionary[lexeme["lexeme"]["value"]]["senses"].update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})


		# print(entry_tlfi)
		# print(entry_wiktionary)
		if len(entry_tlfi) and len(entry_wiktionary) and len(entry_tlfi["senses"]) < 18 and len(entry_wiktionary[list(entry_wiktionary.keys())[0]]["senses"]) < 18:
			tlfi_dict.append(entry_tlfi)
			wiktionary.append(entry_wiktionary)

			annotation_sheet.append("%s|%s|%s\n%s\n%s"%(lemma, pos, gender, "https://www.cnrtl.fr/definition/" + entry_tlfi["id"], list(entry_wiktionary.keys())[0]))
			annotation_sheet.append(combine_senses(entry_tlfi["senses"], entry_wiktionary[list(entry_wiktionary.keys())[0]]["senses"]))
			

	print(len(tlfi_dict) == len(wiktionary))
	with open("../output/wiktionnaire_annotation.json", "w", encoding='utf-8') as f:
		json.dump(wiktionary, f, indent=4, sort_keys=True)

	with open("../output/tlfi_annotation.json", "w", encoding='utf-8') as f:
		json.dump(tlfi_dict, f, indent=4, sort_keys=True)

	with open("../output/tlfi_wiktionnaire_align.tsv", "w") as f:
		f.write("\n".join(annotation_sheet))

if __name__ == '__main__':
	create_annotation_sheets()
	# create_naisc_input("TLFi")
	# create_naisc_input("Wiktionnaire")
	