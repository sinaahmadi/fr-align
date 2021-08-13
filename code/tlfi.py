# -*- coding: utf-8 -*-
import json
import xmltodict
import os
import string
import csv
import shortuuid
shortuuid.set_alphabet(string.digits)

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

	pos_mapper = {"adv": "adverb", "adj": "adjective", "subst": "noun", "verbe": "verb"}
	gender_mapper = {"fém": "feminine", "masc": "masculine"}

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
	if type(text) != str:
		return False
	return " ".join(text.replace("\n", " ").replace(",,", "").replace("„", "").split())

def extract_def(sync_H_H):
	"""
	The content of the sync tag should be given to this function based on the JSON files of TLFi.
	"""
	senses = dict()
	sense_id, unk_sense_counter = "", -1

	for sync in sync_H_H:
		# print(sync)
		if type(sync) == str:
			continue

		if "B" not in sync:
			print("ERROR")

			if type(sync) == dict:
				# there is a hierarchy of senses
				# we only process two levels as follows.
				print("yes")
				for subsense in sync:
					if "H" == subsense:
						if type(sync[subsense]) == list:
							print(" there is no more subsenses")
							# print(subsense)
							print(type(sync[subsense]))
							senses.update(extract_def(sync[subsense]))
						else:
							print("|||||||||||||")
							# there is another level of subsenses
							for subsubsense in sync[subsense]["H"]:
								if "H" == subsense:
									if type(sync[subsense]) == list:
										# there is no more subsenses
										for subsubsense in sync[subsense]:
											# print(extract_def(subsense))
											senses.update(extract_def(subsense))
											# print(subsubsense, type(subsubsense))
											# print(extract_def(subsense))
			
			continue							

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
		except:
			sense_id = "UND"+str(unk_sense_counter)
			unk_sense_counter -= 1

		sense_id = sense_id.replace(" _", "")
		print("sense id is ", sense_id)

		print(def_word, sync["B"][def_word])
		if type(sync["B"][def_word]) == list:
			senses[sense_id] = " ".join([sense["da"]["R"] for sense in sync["B"][def_word]])

		else:
			for sense in sync["B"][def_word]["da"]:
				print("this for, sense", sense, sense_id, sync["B"][def_word]["da"])
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

def extract_exe(sync_H_H):
	# Given an entry in TLFi, find the example associated to the sense
	if "exe" in sync_H_H:
		pass

def extract_tlfi():
	# extracts lemma, part-of-speech, gender, senses and examples from TLFi
	for file in os.listdir("../resources/tlfi_json"):#[0:1]:
		print("Working on %s"%file)
		if file.endswith(".json"):
			dictionary = list()
			with open(os.path.join("../resources/tlfi_json", file), "r", encoding='utf-8') as json_file:
				dico = json.load(json_file)["dico"]["art"]

				for entry in dico:
					print()
					try: #if True:
						microstructure = {
							"id": "",
							"lemma": "",
							"pos": "",
							"gender": "",
							"senses": {}
						}
						# example to be added
						
						microstructure["id"] = entry["@id"]
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
							microstructure["senses"] = {s: clean_tlf(senses[s]) for s in senses} # clean
							# if False not in microstructure["senses"]:
							dictionary.append(microstructure)

					except:
						print("An exception occurred")

			with open(os.path.join("../output/extracted", file), "w", encoding='utf-8') as json_w:
					json.dump(dictionary, json_w, indent=4, sort_keys=True)

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
	"""
	with open("../output/extracted/tlfi_all.json", "r") as json_file:
		for lex in json.load(json_file):
			for entry in lex:
				if word == entry["lemma"].strip().lower() and pos == entry["pos"]:
					return entry
	return {}
# extract_tlfi()
# merge_json_files()



