# -*- coding: utf-8 -*-

import random
from nltk.corpus import wordnet

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


def extract_lemmata():
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


prefixes = """
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .


"""

for word in list(extract_lemmata().values())[200: 300]: # random selection
	
exit()




# if False:
# 	# convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
# 	# found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
# 	wiktionary = dict()
# 	with open("fr_wiktionaire_10k.json", "r") as f:
# 		for lexeme in json.load(f)["results"]["bindings"]:
# 			lemma = lexeme["label"]["value"]
# 			pos = lexeme["pos"]["value"].split("#")[-1]
# 			if lemma + "_" + pos not in wiktionary:
# 				wiktionary[lemma + "_pos" + pos] = {"pos": pos, "senses": [lexeme["definition"]["value"]]}
# 			else:
# 				wiktionary[lemma + "_pos" + pos]["senses"].append(lexeme["definition"]["value"])

# 	wiktionary_file = list()
# 	for entry in wiktionary:
# 		wiktionary[entry]["lemma"] = entry.split("_pos")[0]
# 		wiktionary_file.append(convert_to_ontolex(wiktionary[entry]))

# 	with open("fr_wiktionaire_10k.ttl", "w") as f:
# 		f.write(prefixes + "\n\n".join(wiktionary_file))

# else:
# 	tlf_file = list()
# 	for file in os.listdir("extracted"):
# 		if file.endswith(".json"):
# 			print(file)
# 			with open(os.path.join("extracted", file), "r") as json_file:
# 				for entry in json.load(json_file):
# 					if type(entry["lemma"]) == str and \
# 						type(entry["pos"]) == str and \
# 						entry["pos"] in tlf_pos_mapper and \
# 						" " not in entry["lemma"] and \
# 						"," not in entry["lemma"] and \
# 						len(entry["senses"]):
# 							# print(entry["lemma"])
# 							# entry["lemma"] + "_" + tlf_pos_mapper[entry["pos"]]
# 							entry["pos"] = tlf_pos_mapper[entry["pos"]]
# 							tlf_file.append(convert_to_ontolex(entry))
# 							# 1707236 headwords were found using this (03/08/2021)
	
# 	tlf_file = list(set(tlf_file))
# 	with open("tlf_all_cleaned_converted.ttl", "w") as f: #encoding='utf-8'
# 		f.write(prefixes + "\n\n".join(tlf_file))	