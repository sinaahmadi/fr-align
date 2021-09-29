# -*- coding: utf-8 -*-
import rdflib
import json
from SPARQLWrapper import SPARQLWrapper, JSON

"""
   Sina Ahmadi
   This script runs queries on DBnary's SPARQL endpoint
   found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
"""

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

         OPTIONAL{?form lexinfo:gender ?gender .}
         FILTER(?lang = "fr")
      }
      }
   }
   """
   if len(pos):
      sense_query = sense_query.replace("MOT", word).replace("PRTOFSPEECH", pos)
   else:
      print("Error- POS not provided.")

   # print(sense_query)
   sparql.setQuery(sense_query)
   sparql.setReturnFormat(JSON)
   results = sparql.query().convert()
   return results

def dbnary_lookup(lemma, pos):
   # convert the output of the SPARQL query to a single dictionary with unique keys, i.e. lemma
   # found these pos tags ['noun', 'properNoun', 'verb', 'adjective', 'adverb']
   # lemma = "beau"
   # pos = "adjective"
   gender = ""
   # gender = ""
   entry_wiktionary = dict()
   
   for lexeme in extract_dbnary(lemma, pos)["results"]["bindings"]:
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

   return json.dumps(entry_wiktionary, indent=4)


# print(dbnary_lookup("ignare", "adjective"))
