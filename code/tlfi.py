# -*- coding: utf-8 -*-
import json
import xmltodict
import os
import csv
import re
"""
Sina Ahmadi - July 2021
This script converts TLFi into a josn file where each entry is structured as follows:

{
	"lemma": "",
	"pos": "",
	"gender": "",
	"senses": ["id": "sense/definition"]
}

"""
sense_IDs = list()

def retrieve_pos(tlf_pos):
	"""
	Given a part-of-speech of TLF, return a normalized part-of-speech and possibily gender
	"""
	pos, gender = "", ""
	if False:
		with open("../resources/tlf_pos_mapper.json", "r") as json_file:
			tlf_pos_mapper = json.load(json_file)

		tlf_pos_mapper_inverse = dict()
		for pos in tlf_pos_mapper:
			if pos not in tlf_pos_mapper_inverse:
				tlf_pos_mapper_inverse[pos] = [tlf_pos_mapper[pos]]
			else:
				tlf_pos_mapper_inverse[pos].append(tlf_pos_mapper[pos])

		pos_tags = list()
		with open("../output/extracted/tlfi_all.json", "r") as json_file:
			for dic in json.load(json_file):
				for i in dic:
					if type(i["pos"]) == str:
						# print(i)
						pos_tags.append(i["pos"])

		print(list(set(pos_tags)))
		# print(tlf_pos_mapper_inverse["noun"])

	pos_mapper = {"adj": "adjective", "adv": "adverb", "subst": "noun"} # , "verbe": "verb"
	gender_mapper = {"fém": "feminine", "masc": "masculine"}

	if "verbe" in tlf_pos and "adv" not in tlf_pos:
		pos = "verb"
	else:
		for p in pos_mapper:
			if pos in tlf_pos:
				pos = pos_mapper[p]

		for g in gender_mapper:
			if g in tlf_pos:
				gender = gender_mapper[g]

	return pos, gender

def convert_to_json():
	# Convert XML files of TLFi into JSON
	for file in os.listdir("tlfi-master/xml"):
		if file.endswith(".xml"):
			print(file)
			with open(os.path.join("tlfi-master/xml", file), "r") as f:
					sample = xmltodict.parse(f.read())
					with open(os.path.join("json", file.replace("xml", "json")), 'w') as json_file:  
						json.dump(sample, json_file)

def clean_tlf(text):
	# cleans senses in TLFi
	# ":" at the end to be removed (28/09/2021)
	# remove sense that appear with brackets at the beginning and at the end (!!!)
	if type(text) != str:
		return False
	else:
		text = " ".join(text.replace("\n", " ").replace(",,", "").replace("„", "").replace("`` (", "").split())
		text = re.sub(r" :$", "", text).strip()
		text = re.sub("^\[.*\]$", "", text)
		if len(text) > 5:
			return text
		return False

def extract_def(sync_H_H):
	"""
	The content of the sync tag should be given to this function based on the JSON files of TLFi.
	"""
	senses = dict()
	sense_id, unk_sub_sense_counter = "", -1

	for sync in sync_H_H:
		# print(sync)
		if type(sync) == str:
			continue

		if type(sync) == dict:
			# there is a hierarchy of senses
			# we only process two levels as follows.
			print("hierarchy of senses")
			for subsense in sync:
				if "H" == subsense:
					try:
						supersense_ID = sync["parah"]["da"]["G"]
					except:
						supersense_ID = ""
					if type(sync[subsense]) == list:
						print(" there is no more subsenses")
						# print(sync[subsense])
						print(type(sync[subsense]))
						extraced_senses = extract_def(sync[subsense])
						for i in extraced_senses:
							senses.update({(supersense_ID+i).replace(" ", ""): extraced_senses[i]})
					else:
						print("|||||||||||||")
						# print(sync[subsense])
						# # there is another level of subsenses
						# for subsubsense in sync[subsense]["H"]:
						# 	if "H" == subsense:
						# 		if type(sync[subsense]) == list:
						# 			# there is no more subsenses
						# 			for subsubsense in sync[subsense]:
						# 				# print(extract_def(subsense))
						# 				senses.update(extract_def(subsense))
						# 				# print(subsubsense, type(subsubsense))
						# 				# print(extract_def(subsense))
			
			# continue							

		if "B" in sync:

			if "syntita" in sync["B"]:
				# syntita is used for words where the main entry appears in. In TLFi, such cases are provided in the
				# main entry, making it difficult to distinguish senses from other entries
				# continue
				pass

			if "def" in sync["B"]:
				def_word = "def"
			elif "ind" in sync["B"]:
				def_word = "ind"
			elif "cro" in sync["B"]:
				def_word = "cro"
			else:
				continue

			try:
				sense_id = sync["parah"]["da"]["G"]
				if sense_id in sense_IDs:
					while True:
						if unk_sub_sense_counter in sense_IDs:
							unk_sub_sense_counter -= 1
						else:
							sense_id = "UND"+str(unk_sub_sense_counter)
							break
				
				sense_IDs.append(str(unk_sub_sense_counter.replace("UND", "")))

			except:
				while True:
					if unk_sub_sense_counter in sense_IDs:
						unk_sub_sense_counter -= 1
					else:
						sense_id = "UND"+str(unk_sub_sense_counter)
						sense_IDs.append(unk_sub_sense_counter)
						break

			sense_id = sense_id.replace(" _", "")

			print("\n************************\n sense id is ", sense_id)
			print(def_word, sync["B"][def_word])

			if type(sync["B"][def_word]) == list:
				senses[sense_id] = " ".join([sense["da"]["R"] for sense in sync["B"][def_word]])

			else:
				for sense in sync["B"][def_word]["da"]:
					print("this for, sense", sense, "id", sense_id, sync["B"][def_word]["da"])
					if type(sense) == dict:
						print("sense", sense)
						if len(sense["R"]):
							if type(sense["R"]) == str:
								senses[sense_id] = sense["R"]
							elif type(sense["R"]) == list:
								if False not in [True if type(i) == str else False for i in sense["R"]]:
									senses[sense_id] = " ".join(filter(None, sense["R"]))
								else:
									if "#text" in sense["R"]:
										if type(sense["R"]["#text"]) == str:
											senses[sense_id] = sense["R"]["#text"]
										else:
											senses[sense_id] = " ".join(filter(None, sense["R"]["#text"]))
									else:
										pass
										# senses[sense_id] = " ".join(filter(None, sense["R"]))
									
					
					elif sense == "R":
						print("r-b", sync["B"][def_word]["da"]["R"])
						if type(sync["B"][def_word]["da"]["R"]) == str:
							senses[sense_id] = sync["B"][def_word]["da"]["R"]
						elif type(sync["B"][def_word]["da"]["R"]) == list:
							if False not in [False if type(i) != str else True for i in sync["B"][def_word]["da"]["R"]]:
								senses[sense_id] = " ".join(filter(None, sync["B"][def_word]["da"]["R"]))
						elif type(sync["B"][def_word]["da"]["R"]) == dict:
							senses[sense_id] = sync["B"][def_word]["da"]["R"]["#text"]

	return senses

def extract_tlfi():
	# extracts lemma, part-of-speech, gender, senses and examples from TLFi
	for file in os.listdir("../resources/tlfi_json"):#[0:1]:
		# if file != "t11_5.xm7.json":
		# 	continue
		print("Working on %s"%file)
		if file.endswith(".json"):
			dictionary = list()
			with open(os.path.join("../resources/tlfi_json", file), "r", encoding='utf-8') as json_file:
				dico = json.load(json_file)["dico"]["art"]

				for entry in dico:
					sense_IDs.clear()
					try: #if True:#
						microstructure = {
							"id": "",
							"lemma": "",
							"pos": "",
							"gender": "",
							"senses": {}
						}
						# example to be added
						
						microstructure["id"] = entry["@id"]
						# if microstructure["id"] != "55177":
						# 	# print()
						# 	continue
						senses = dict()
						#  ========================  find lemma
						if "da" not in entry["ved"]["mot"] or "cod" not in entry["ved"]:
							# skip such entries
							continue

						if "R" in entry["ved"]["mot"]["da"]:
							microstructure["lemma"] = entry["ved"]["mot"]["da"]["R"]
							microstructure["pos"] = entry["ved"]["cod"]["da"]["R"]
						elif "I" in entry["ved"]["mot"]["da"]:
							microstructure["lemma"] = entry["ved"]["mot"]["da"]["I"]
							microstructure["pos"] = entry["ved"]["cod"]["da"]["I"]

						if not len(microstructure["lemma"]) or \
							"(" in microstructure["lemma"] or \
							")" in microstructure["lemma"] or \
							"-" in microstructure["lemma"] or \
							", " in microstructure["lemma"].strip() or \
							clean_tlf(microstructure["lemma"]) == False:
								# the entry contains terminological data, e.g. PY(O)- for PARTHÉNOGENÈSE
								continue

						print("+" * 20, microstructure["lemma"], microstructure["id"])
						#  ======================== find senses
						unk_sense_counter = 1
						while True:
							if unk_sense_counter in sense_IDs:
								unk_sense_counter += 1
							else:
								sense_IDs.append(unk_sense_counter)
								break

						if "B" in entry["sync"]["H"] and "def" in entry["sync"]["H"]["B"]:

							if "R" in entry["sync"]["H"]["B"]["def"]["da"]:
								senses["UND_"+str(unk_sense_counter)] = entry["sync"]["H"]["B"]["def"]["da"]["R"]

							if "I" in entry["sync"]["H"]["B"]["def"]["da"]:
								if type(senses["UND_"+str(unk_sense_counter)]) == str:
									if type(entry["sync"]["H"]["B"]["def"]["da"]["I"]) == str:
										print(type(senses["UND_"+str(unk_sense_counter)]))
										senses["UND_"+str(unk_sense_counter)] = senses["UND_"+str(unk_sense_counter)] + " " + entry["sync"]["H"]["B"]["def"]["da"]["I"]
									elif type(entry["sync"]["H"]["B"]["def"]["da"]["I"]) == list:
										senses["UND_"+str(unk_sense_counter)] = senses["UND_"+str(unk_sense_counter)] + " " + " ".join(filter(None, entry["sync"]["H"]["B"]["def"]["da"]["I"]))

								if type(senses["UND_"+str(unk_sense_counter)]) == list:
									if type(entry["sync"]["H"]["B"]["def"]["da"]["I"]) == str:
										senses["UND_"+str(unk_sense_counter)] = " ".join(filter(None, senses["UND_"+str(unk_sense_counter)])) + " " + entry["sync"]["H"]["B"]["def"]["da"]["I"]
									elif type(entry["sync"]["H"]["B"]["def"]["da"]["I"]) == list:
										senses["UND_"+str(unk_sense_counter)] = " ".join(filter(None, senses["UND_"+str(unk_sense_counter)])) + " ".join(filter(None, entry["sync"]["H"]["B"]["def"]["da"]["I"]))

								unk_sense_counter += 1
						# else:
						if "H" not in entry["sync"]["H"]:
							# no senses are provided
							print("no senses found for ", microstructure["lemma"])
							# continue
						else:
							senses.update(extract_def(entry["sync"]["H"]["H"]))

						# print("senses", senses)
						if len(senses):
						# 	if type(senses[0]) == list:
						# 		senses = [item for items in senses for item in items]
							microstructure["lemma"] = microstructure["lemma"].replace(",", "").lower()
							microstructure["pos"], microstructure["gender"] = retrieve_pos(microstructure["pos"])
							if len(microstructure["gender"]):
								microstructure["pos"] = "noun"
							microstructure["senses"] = {s: clean_tlf(senses[s]) for s in senses if clean_tlf(senses[s])} # clean
							# if False not in microstructure["senses"]:
							dictionary.append(microstructure)
							print()
							# for i in microstructure["senses"]:
							# 	print(i, microstructure["senses"][i])

					except:
						print("An exception occurred")

			with open(os.path.join("../output/extracted", file), "w", encoding='utf-8') as json_w:
					json.dump(dictionary, json_w, indent=4, sort_keys=True)

def extract_exe(sync_H_H):
	# Given an entry in TLFi, find the example associated to the sense
	if "exe" in sync_H_H:
		pass

def merge_json_files():
	# merge json files of TLFi. This should be run after extract_tlfi()
	all_entries = list()
	for file in os.listdir("../output/extracted"):
		if file.endswith(".json"):
			print(file)
			with open(os.path.join("../output/extracted", file), "r") as json_file:
				all_entries.append(json.load(json_file))
					
	with open("../output/extracted/tlfi_all.json", 'w', encoding='utf-8') as json_file:
		json.dump(all_entries, json_file, indent=4, sort_keys=True)

def tlfi_lookup(word, pos):
	"""
	Given a word and its part-of-speech, retrieve it on TLF. 
	(23/08/2021) Update this function so that all entries with identical lemma and pos are retrieved.
	"""
	with open("../output/extracted/tlfi_all.json", "r") as json_file:
		for lex in json.load(json_file):
			for entry in lex:
				if pos == "adjective":
					pos = "adverb"
				if word == entry["lemma"].strip().lower():# and pos in entry["pos"]:
					return entry
	return {}

# extract_tlfi()
# merge_json_files()
# print(tlfi_lookup("mur", "noun"))
# print(tlfi_lookup("bannir", "verb"))
# print(tlfi_lookup("unique", "adjective"))
# print(tlfi_lookup("inhabituel", "adjective"))


