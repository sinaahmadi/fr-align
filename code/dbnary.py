# -*- coding: utf-8 -*-
import rdflib
import json
from SPARQLWrapper import SPARQLWrapper, JSON

def extract_dbnary(word, pos):
	sparql = SPARQLWrapper("http://kaiko.getalp.org/sparql")

	sense_query = """
	SELECT ?lexeme ?label ?pos ?gender ?sense ?definition
	WHERE {
	?sense a ontolex:LexicalSense ;
	skos:definition ?def .
	?def rdf:value ?definition .
	FILTER(lang(?definition) = "fr")
	{
	SELECT ?lexeme ?label ?pos ?gender ?sense WHERE {
	  	   VALUES ?label {'MOT'@fr}
	  	   VALUES ?pos {<http://www.lexinfo.net/ontology/2.0/lexinfo#PRTOFSPEECH>} 
	  	   ?lexeme a ontolex:Word , ontolex:LexicalEntry ;
	  	   rdfs:label ?label ;
	  	   ontolex:canonicalForm ?form ;
	           lime:language ?lang ;
	  	   lexinfo:partOfSpeech   ?pos ;
	  	   ontolex:sense  ?sense .
	   
	  	   FILTER(?lang = "fr")
	  	   OPTIONAL{?form lexinfo:gender ?gender}

	}
	}
	}
	"""

	sparql.setQuery(sense_query.replace("MOT", word).replace("PRTOFSPEECH", pos))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results

# sense_query = """
# SELECT ?lexeme ?label ?pos ?sense ?definition
# WHERE {
# ?sense a ontolex:LexicalSense ;
# skos:definition ?def .
# ?def rdf:value ?definition .
# FILTER(lang(?definition) = "fr")
# {
# SELECT ?lexeme ?label ?pos ?sense WHERE {
#   	   ?lexeme a ontolex:Word , ontolex:LexicalEntry ;
#   	   rdfs:label ?label ;
#            lime:language ?lang ;
#   	   lexinfo:partOfSpeech   ?pos ;
#   	   ontolex:sense  ?sense .
#   	   FILTER(?lang = "fr")
# }
# }
# } """

# qres = g.query(knows_query)

# print(len(qres))
# # for row in qres:
# #     print(f"{row.lexeme} {row.label} {row.pos} {row.sense} {row.definition}")

# extract_dbnary()


json_dbnary = """
{
   "head":{
      "link":[
         
      ],
      "vars":[
         "lexeme",
         "label",
         "pos",
         "sense",
         "definition"
      ]
   },
   "results":{
      "distinct":false,
      "ordered":true,
      "bindings":[
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_1_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Au singulier) Ce qui est bon, ce qui favorise l'équilibre, l'épanouissement d'un individu, d'une collectivité ou d'une entreprise humaine."
            }
         },
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_2_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Au singulier) Probité, vertu."
            }
         },
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_3_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Droit de propriété) Toute chose d'utilité pratique et de valeur financière."
            }
         },
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_3a_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Courant) Chose, matérielle ou immatérielle, qui appartient en propre à une personne."
            }
         },
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_3b_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Vieilli) Maison de campagne, propriété rurale."
            }
         },
         {
            "lexeme":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/bien__nom__1"
            },
            "label":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"bien"
            },
            "pos":{
               "type":"uri",
               "value":"http://www.lexinfo.net/ontology/2.0/lexinfo#noun"
            },
            "sense":{
               "type":"uri",
               "value":"http://kaiko.getalp.org/dbnary/fra/__ws_4_bien__nom__1"
            },
            "definition":{
               "type":"literal",
               "xml:lang":"fr",
               "value":"(Spécialement) (Canada) (Désuet) Terre, bien immobilier en campagne."
            }
         }
      ]
   }
}
"""

wiktionary = dict()

lemma = "bien"
pos = "noun"

# convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
# found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
for lexeme in json.loads(json_dbnary)["results"]["bindings"]:
	if lexeme["lexeme"]["value"] not in wiktionary:
		wiktionary[lexeme["lexeme"]["value"]] = {"pos": pos, "senses": {lexeme["sense"]["value"]: lexeme["definition"]["value"]}}
	else:
		wiktionary[lexeme["lexeme"]["value"]]["senses"].update({lexeme["sense"]["value"]: lexeme["definition"]["value"]})

print(wiktionary)
exit()

wiktionary_file = list()
for entry in wiktionary:
	wiktionary[entry]["lemma"] = entry.split("_pos")[0]
	wiktionary_file.append(convert_to_ontolex(wiktionary[entry]))

# with open("fr_wiktionaire_10k.ttl", "w") as f:
# 	f.write(prefixes + "\n\n".join(wiktionary_file))
