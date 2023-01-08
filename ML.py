import re
from os.path import join
from os import walk
from itertools import groupby
from nltk import ngrams

'''
# On va parcourir ici notre corpus MEGALITE_FR fichier par fichier 
# On peut spécifier le nombre de fichiers de chaque sous-dossier à parcourir dans paths[repertoire][:20] 
(20 la taille à indiquer, si on veut parcourir tous les fichiers il faut juste la laisser [:])
'''
def parcourir():
    dic_path_fichiers = []
    # Cette variable va contenir les liens vers tous les fichiers de MEGALITE_FR
    path_fic = [] 
    # Ici on va extraire les fichiers de chaque répertoire
    for (repertoire, sousRepertoires, fichiers) in walk("MEGALITE_FR"):
        dic_path_fichiers.append({repertoire: fichiers})
    # On va garder que les fichiers 
    dic_path_fichiers = dic_path_fichiers[1:]

    for paths in dic_path_fichiers:
        # On va ici insérer dans la liste les fichiers de chaque sous-dossiers
        for repertoire in paths:
            path_fic.extend([repertoire + "\\" + fic for fic in paths[repertoire][:]])  
    return path_fic

##########################################################################################################################
def get_model(liste_fichiers):
    # Les modèles sont des dictionnaire où chaque clé et le n_gramme et valeur le nombre d'occurence de ce dernier 
    bigramme_model = {}

    # On va parcourir chaque fichier 
    for path in liste_fichiers:
        with open(path, "r", encoding="utf-8") as f:
            '''
            Pour chaque fichier on va le filtrer selon notre choix avec regex
            ( Durant les tests, à chaque fois qu'on trouve un mot inutile pour la phrase et qui se répéte beaucoup on l'enlève)
            ( On a aussi supprimer les caractères suivis d'un point et les numéros latins )
            '''
            s = "".join(
                list(filter(('').__ne__, re.split(r"\d| \w\. |Chapitre|CHAPITRE|chapitre|Oïmé|Boiscoran|Caïn|aîné| [XVI]+ ", "".join(f.readlines())))))

            # On garder les mots alphabétique, ', ?, ., virgule et retour à la ligne
            s = " ".join(
                list(filter(('').__ne__, re.findall(r"\w+’*,{0,1}\?*\.{0,1}\w*|\n", s))))


            def createModel(n_gramme, model):
                """
                groupby permet de regrouper les ngramme : [(n_gramme_1, [n_gramme_1, ..., n_gramme_1]), (n_gramme_2,
                [n_gramme_2, ..., n_gramme_2]), ..]
                """
                for i, j in groupby(sorted(n_gramme)):
                    grammes = " ".join(i)
                    # On va pas garder les n_grammes contenant le \n
                    if "\n" not in grammes:  
                        """
                        Si le n_gramme est déjà dans le modèle alors on incrémente juste le nombre d'occurences 
                        Sinon on l'ajoute dans notre dictionnaire
                         """
                        if i not in model:
                            model[grammes] = len(list(j))
                        else:
                            model[grammes] += len(list(j))

                # Retourner le modèle et le trier par ordre décroissant par rapport aux occurences
                return dict(sorted(model.items(), key=lambda t: t[1], reverse=True))

            """            
            Nous générons les n_grammes avec la bibliothèque nltk qui possède la méthode "ngrams", la méthode possède
             2 argements : 
                Une liste de mots et le n_gramme résultant : 1 pour un-gramme, 2 pour bi-gramme...
            """
            bigramme_model = createModel(ngrams(re.split(' ', s), 2), bigramme_model)
    return bigramme_model

######################################################################################################################
def fichier_ML(model):

   # Ici on va enregistrer le modèle ML dans un fichier 
    with open("model_bi_gramme.txt", "w", encoding="utf-8") as f:
        for key, val in model.items():
            f.write(str(key) + ":" + str(val) + "\n")



####################################################################################################################
# Ici on va générer les phrases 
def genere_ph1(): 
    # La fonction qui va ouvrir le ML et le parcourir ligne par ligne avec readlines
    def parcourir_ML():
        with open("model_bi_gramme.txt", "r", encoding="utf-8") as f:
            return f.readlines()

    # Génération des phrases avec ML, en indiquant le mot de début et la taille 
    def get_ph1(model, mot, taille):

        ph1 = ""  
        # On va boucler par rapport à la taille de la phrase que nous souhaitons généré 
        for _ in range(0, taille):
            for words in model:
                # w : [mot_1, mot_2, :occurence]
                w = re.split(" |:", words)  

                """                
                La première condition permet d'éviter la répétition d'une expression qu'une expression se répète bcp durant la génération 
                    Ensuite on cherche le premier bigramme contenant le mot pour déterminser son suivant
                """
                if (len(re.findall((w[0] + " " + w[1]), ph1)) <= 0) and mot == w[0]:
                    ph1 += mot + " "
                    mot = w[1]
                    # Une fois trouvé, pn arrête la recherche pour le mot i et on passe au suivant
                    break
        return ph1

#######################################################################################################################
# A partir de notre modèle on va créer la phrase en indiquant le mot par lequel va commencer cette phrase.
# La création de la phrase s'effectue par des tranches qu'on va indiquer selon le nombre d'éléments pour chaque ligne.

    phrase = ""
    #premier = input("La phrase va commencer par : ")
    # Ici en indiquant les tranches de la génération de la phrase (numéro de mot par ligne)
    for i in [5, 10, 15]:
      phrase += get_ph1(parcourir_ML(), premier, i)+"\n"
      print(phrase)

# On va stocker la création de la phrase dans le dossier "phrase.txt"
    fichier = open("phrase.txt", "w")
    fichier.write(phrase)
    fichier.close()

######################################################################################################################



if __name__ == '__main__':

    # En indiquant ici le mot de départ de notre phrase
    premier = input("La phrase va commencer par : ")

    # On parcourt notre courpus 
    path = parcourir()

    # On crée le modèle 
    model = get_model(path)

    # On le stocke dans le fichier
    fichier_ML(model)

    # Finalement on génére notre phrase ph2
    genere_ph1()

