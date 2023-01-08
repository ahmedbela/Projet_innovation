# Projet_innovation
Génération De Phrases Au Moyen D'énergie Textuelle 
## Génération de phrases à partir de ML-2 et du modèle neuronal

## Prérequis

	Afin de pouvoir compiler le programme sur votre poste, vous devez :
		* Déposer les 2 codes dans un dossier 
		* Télécharger et déposer les ressources dans le même dossier (MEGALITE_FR, TableAssociative, embeddings-Fr.txt)
		* Les ressources sont déposées dans l'e-uapv pour le défie 4.

## Instructions

	1. Compilez le code ML.py afin de générer la phrase ph1 à partir du modèle bi-gramme : 
		* Le programme va vous demander de choisir le mot par lequel la phrase va commencer.

	2. Compilez ensuite le code RNA.py qui va générer une phrase ph2 en utilisant le modèle neuronal en prenant en compte le contexte (Q) :

		* Le programme va vous demander premièrement de choisir la Query (le contexte).

		* Ensuite, il va vous demander de choisir le texte d'entrée (comme input) de ce modèle soit de lui fournir :
			** La phrase générée par le premier modèle (ML-2). 
			** Une phrase choisie par vous même.

		* Pour les 2 choix, vous avez la possibilité d'indiquer les mots que vous voudrez garder fixes entre ph1 et ph2 pour optimiser le résultat et respecter bien l'homosyntaxisme. Si vous voulez calculer la distance de tous les mots par rapport à Q, laissez le choix vide et cliquez sur 'entrée'.
 
