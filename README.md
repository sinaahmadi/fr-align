# Alignment of French Resources

This repository contains resources and codes to run experiments on aligning the *[Trésor de la Langue Française informatisé](https://www.atilf.fr/ressources/tlfi/)* and the French Wiktionary -- [Wiktionnaire](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil).

## Data Extraction
In addition to [codes/main.py](codes/main.py), two of the provided scripts can be used within other applications and are described as follows:

- [codes/dbnary.py](codes/dbnary.py) retrieves data from Wiktionnaire through [DBnary](http://kaiko.getalp.org/about-dbnary/)'s SPARQL endpoint
- [codes/tlfi.py](codes/tlfi.py) extracts relevant information from TLFi by reaching out to specific tags and paths in the XML files. To reduce complexity in the hierarchy of senses, all senses are flattened and provided at the same level. Extraction of definitions was particularly challenging due to lack of distinction between the definition of the entry versus that of the locution/idioms which also appear in the same entry. For example, *mur* (noun) comes with over 60 definitions in (TLFi)[https://www.cnrtl.fr/definition/mur] among which only a couple of them define the entry and the other, focus on locutions, idioms or multi-word expressions as in "*mur des Lamentations, des Pleurs.*" and "*mur ossaturé*".

In both resources, the microstructure of each entry is reshaped as follows:

- *puissamment* from TLFi (See [https://www.cnrtl.fr/definition/PUISSAMMENT])

```
{
    "gender": "",
    "id": "69866",
    "lemma": "puissamment",
    "pos": "adverb",
    "senses": {
        "A.": "Très, à un degré élevé, avec force.",
        "B.": "Avec efficacité, grandement.",
        "C.": "Avec de la force physique; de façon marquée.",
        "D.": "Avec des moyens puissants, fortement."
    }
} 
```

- *puissamment* from Wiktionnaire (See [https://fr.wiktionary.org/wiki/puissamment])

```
{
    "http://kaiko.getalp.org/dbnary/fra/puissamment__adv__1": {
        "lemma": "puissamment",
        "pos": "adverb",
        "gender": "",
        "senses": {
            "http://kaiko.getalp.org/dbnary/fra/__ws_2_puissamment__adv__1": "Avec force.",
            "http://kaiko.getalp.org/dbnary/fra/__ws_4_puissamment__adv__1": "(Par extension) très.",
            "http://kaiko.getalp.org/dbnary/fra/__ws_1_puissamment__adv__1": "Avec puissance.",
            "http://kaiko.getalp.org/dbnary/fra/__ws_3_puissamment__adv__1": "Extrêmement."
        }
    }
}
```

## Data Annotation

Based on the lemmata used in the [MWSA datasets](https://github.com/elexis-eu/mwsa) (which are based on the English WordNet), we retrieve the synsets associated to the word in the French language based the Open Multilingual WordNet. The is beneficial to carry out cross-lingual word-sense alignment tasks in the future.

The relevant information are then extracted for these words in French as described in the previous section. Given a lemma with identical part-of-speech and gender in TLFi and Wiktionnaire, a combination of all possible definition/sense matches are provided. This way, the annotator can select one of the following relations between every pair of senses in the two resources:
- `none`: the two senses/definitions are not referring to the same concepts, i.e. meanings
- `exact`: the two senses/definitions are semantically identical
- `related`: the two senses/definitions are not referring to the same concepts but are **semantically related**

Here are a few examples:

- `livre` (noun, masculine)

    - proposed relation: **`related`**
        - *Ouvrage imprimé, relié ou broché, non périodique, comportant un assez grand nombre de pages.* (TLF)
        - *Ouvrage qui fait référence à un texte sacré* (Wiktionnaire) 
    - proposed relation: **`exact`**
        - *Assemblage de feuilles en nombre plus ou moins élevé, portant des signes destinés à être lus.* (TLF)
        - *Assemblage de feuilles manuscrites ou imprimées destinées à être lues.* (Wiktionnaire) 
    - proposed relation: **`none`**
        - *Ouvrage constituant un volume imprimé. * (TLF)
        - *Registre destiné à recueillir les signatures et les commentaires des visiteurs.* (Wiktionnaire) 

These type of relations are based on [SKOS's semantic relations](https://www.w3.org/TR/skos-reference/#semantic-relations). It should be noted that the proposed relations are symmetric. Therefore, `R(A, B)` equals with `R(B, A)`, where `R()` refers to the relation between `A` and `B`. 

In order to evaluate the level of (dis)agreement among annotators, we will then calculate an inter-annotator agreement such as [Fleis's Kappa](https://en.wikipedia.org/wiki/Fleiss%27_kappa).


## Alignment techniques


## Experiments








