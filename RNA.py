import operator
import re
import pandas as pd
from scipy.spatial.distance import cosine, euclidean



# Ici on va récupérer les embeddings sous dataframe, chaque colonne contient le mot et ses dimensions
def get_embedding():
    dict_emb = {}
    with open("embeddings-Fr.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            words = list(filter(('').__ne__, re.split(" |,|\[|\]|\t|\n", line)))
            dict_emb[words[0]] = words[1:]

    dataFrame_emb = pd.DataFrame(dict_emb).astype('float64')

    return dataFrame_emb


# Ici on va transférer la table associative sous forme d'un dictionnaire {'POS': [liste de mots]}
def get_TA():
    dict_TA = {}
    with open("TableAssociative", "r", encoding="utf-8") as f:
        for line in f.readlines():
            pos_words = list(filter(('').__ne__, re.split("\t|\n", line)))
            dict_TA[pos_words[0]] = pos_words[1:]

    # On va le transférer ici sous forme d'un dataframe qui sera stocké sous forme d'un fichier CSV
    dataFrame_TA = pd.concat({k: pd.Series(v) for k, v in dict_TA.items()}, axis=1)

    return dataFrame_TA

# On va récupérer récupérer les pos de chaque mot des phrases généré par le modèl n-grammes
def get_pos_ph1(table_associative):
	liste = []

	print("\nFaites un choix : ")
	print("1. Choisir la phrase généré par ML.")
	print("2. Choisir votre propre phrase.")

	while 1 :
		choix = input("Votre choix : ")
		if choix == "1" :
			with open("phrase.txt", "r") as f:
				print("\nVoici le résultat en utilisant le ML de bi-grammes :") 
				for chaine in f.readlines(): 
					print(chaine)
			# On peut ici ignorer des mots pour respecter bien l'homosytaxisme
			mots = input('\nIgnorer ces mots pour les garder dans (ph2), les mots doivent être séparés par un espace :')
			stopw = mots.split()
			break
		elif choix == "2" :
			phpers = input("\nEntrez votre phrase : ")
			with open("phrase.txt", "w") as f:
				f.write(phpers)
				mots2 = input("\nIgnorez ces mots (mot1 mot2 ...), sinon laissez vide : ")
				stopw = mots2.split()
				break


	with open("phrase.txt", "r") as f:
		for chaine in f.readlines():
			chaine = chaine.split(" ")
			l = []
			for s in chaine:
				# Ici on va pas chercher les POS de stopw
				if s not in stopw :  
					for c in table_associative.columns.values :
						r = table_associative[table_associative[c] == s][c]
						if not r.empty : 
							l.append(c)
							break
				else: 
					l.append(s)
			liste.append(l)
	
	return liste 

# Foction pour récupérer les mots de chaque POS et calculer leur distance par rapport à la Query
# Et prend le mot le plus proche de la Query
def distance(query, table_associative, embbeding, words_POS):
	# Cette liste va contenir la ph2 générée, sous forme d'une liste
    ph2_liste = []
    # Récupération du vecteur de la Queary Q		
    query_data = embbeding[query]  

    # Pour chaque phrase du ph1, on va récupérer les mots optimaux de chaque POS dans la phrase 
    # Pour chaque texte de ph1
    for ph1 in words_POS:
    	# Récupération des mots optimaux de chaque POS dans la phrase
    	# liste des POS      
        words_optimal = []			
        # On va ici parcourir les POS et voir s'ils existent dans la TA, et on va les stocker dans une liste
        for pos in ph1:
        	if pos not in table_associative.columns.values : 
        		words_optimal.append(pos)
        	else : 
        		# si le POS existe dans TA, on récupère ses mots POS : mot...
	            tag_words = table_associative[pos].dropna()
	            # Dictionnaire contenant la distance de chaque mot par rapport à la Query  
	            best_word = {} 

	            # Pour chaque mot du POS
	            for word in tag_words:  	
	                # Ici on regarde si le mot et dans nos embeddings, différent de la Query et n'est pas encore traité
	                if word in embbeding.columns and word != query and word not in words_optimal:
	                	# Calcule de distance entre ce mot et la Query avec cosine, euclidean...
	                    val = cosine(embbeding[word], query_data) 
	                    # on stock la distance dans le dict "word : dist"
	                    best_word[word] = val
	            # Ici on prend la distance min et on stocke le résultat dans la liste
	            if best_word:
	                words_optimal.append(min(best_word.items(), key=operator.itemgetter(1))[0])

        ph2_liste.append(words_optimal)

    return ph2_liste


def set_word_ph1(optimal, words_POS, query):
	text = ""
	for i in range(len(words_POS)): 
		for j in range(len(words_POS[i])) : 
			# On va afficher ici les phrases sans les POS 
			text += optimal[i][j] + " " 
			#text += "*" + words_POS[i][j], "(" + optimal[i][j] + ")" + " " # Afficher les phrases avec tags
		text += "\n"
	print("\nVoici le résultat qui sera stocker dans 'resultat.txt' : ")
	print(text)


	with open("resultat.txt", "w", encoding="utf-8") as f:
	    f.write(text)

if __name__ == '__main__':

    #query = input("Entez la Query : ")
    # Récupérer les vecteurs de mots dans embedding
    embbeding = get_embedding()  
 
    query = input("\nEntez la Query : ")
    if query not in embbeding.columns:
        raise Exception("Query n'existe pas !!")

    # Récupération de la table associative
    table_associative = get_TA()  
    words_POS = get_pos_ph1(table_associative)

    # On va récupérer maintenant les mots de chaque POS et calculer leur distance par rapport à la Query
    # Prendre les mots les plus proches de la Query et afficher le résultat (ph2) sans les POS des mots
    optimal = distance(query=query, table_associative=table_associative, embbeding=embbeding, words_POS=words_POS)
    set_word_ph1(optimal=optimal, words_POS=words_POS, query=query)

