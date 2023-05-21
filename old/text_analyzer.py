import string
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import trafilatura
from nltk.corpus import stopwords
from textblob import TextBlob

google_search_result = {
  "organic": [
    {
      "title": "Avocat (fruit) - Wikipédia",
      "link": "https://fr.wikipedia.org/wiki/Avocat_(fruit)",
      "snippet": "L'avocat est le fruit de l'avocatier (Persea americana), un arbre de la famille des Lauraceae, originaire du Mexique. Il en existe trois grandes variétés.",
      "sitelinks": [
        {
          "title": "Histoire",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(fruit)#Histoire"
        },
        {
          "title": "Mode de consommation",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(fruit)#Mode_de_consommation"
        },
        {
          "title": "Composition",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(fruit)#Composition"
        }
      ],
      "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsutp639CKnTMqQhK83cNZ2_1wF1kFPs1rxofnBo2ukmQOzGn_UZxXFeI&s",
      "position": 1
    },
    {
      "title": "Avocat (métier) - Wikipédia",
      "link": "https://fr.wikipedia.org/wiki/Avocat_(m%C3%A9tier)",
      "snippet": "En droit, l'avocat est un juriste dont les fonctions traditionnelles sont de conseiller, représenter, d'assister et de défendre ses clients, ...",
      "attributes": {
        "ROME (France)": "K1903 - Défense et conseil juridique",
        "IDEO (France)": "10308"
      },
      "sitelinks": [
        {
          "title": "Histoire",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(m%C3%A9tier)#Histoire"
        },
        {
          "title": "Par pays",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(m%C3%A9tier)#Par_pays"
        },
        {
          "title": "Chine",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(m%C3%A9tier)#Chine"
        },
        {
          "title": "Europe",
          "link": "https://fr.wikipedia.org/wiki/Avocat_(m%C3%A9tier)#Europe"
        }
      ],
      "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYiaqWYq4x8eMvVYvgx3ppjL2e0KLdhyyb4rh8rXZehD5LE3_yA7nL8iw&s",
      "position": 2
    },
    {
      "title": "Avocat - avocate - Onisep",
      "link": "https://onisep.fr/Ressources/Univers-Metier/Metiers/avocat-avocate",
      "snippet": "Défendre les personnes et les entreprises engagées dans un procès, telle est la principale mission de l'avocat. Il joue aussi un rôle de conseiller pour ...",
      "position": 3
    },
    {
      "title": "avocat.fr | Avocat.fr",
      "link": "https://www.avocat.fr/",
      "snippet": "avocat.fr. 71 000 avocats partout en France pour vous conseiller et vous défendre au quotidien. Je trouve un avocat près de chez moi. L'annuaire des avocats ...",
      "position": 4
    },
    {
      "title": "L'avocat - fruit ou légume ?, valeurs nutritionnelles, calories, santé",
      "link": "https://www.fondation-louisbonduelle.org/legume/avocat/",
      "snippet": "L'avocat est riche en acides gras mono-insaturés · L'avocat est source de vitamine E · Il est disponible toute l'année · Il supporte mal le froid et se mange ...",
      "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQADtZX29ziGGUEISjkxuJooK-H9fWZ7EZnOjDSaSdeR538oerPIqe2_00&s",
      "position": 5
    },
    {
      "title": "Avocat / Avocate : métier, études, diplômes, salaire, formation | CIDJ",
      "link": "https://www.cidj.com/metiers/avocat-avocate",
      "snippet": "L'avocat ou l'avocate représente et défend devant les tribunaux ou les cours des particuliers, des entreprises ou des collectivités.",
      "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqBCOfjbmPj7I3mevR_WxtYCiVl-cuoNpBpPP6k9vOxz2tecfhnaVo3Fo&s",
      "position": 6
    },
    {
      "title": "Fiche métier : Avocat (salaire, formation, qualités requises…)",
      "link": "https://www.leparisien.fr/etudiant/orientation/guide-metiers/metier-avocat/",
      "snippet": "Un avocat est également un orateur de grande qualité. Souvent considéré comme quelqu'un d'éloquent, l'avocat doit convaincre son auditoire en usant d' ...",
      "position": 7
    },
    {
      "title": "Annuaire des avocats de France - Conseil national des barreaux",
      "link": "https://www.cnb.avocat.fr/fr/annuaire-des-avocats-de-france",
      "snippet": "Vous êtes avocat et constatez une anomalie sur votre fiche ? Les données présentées sur cet annuaire proviennent directement des informations enregistrées ...",
      "attributes": {
        "Ville": "Code postal"
      },
      "position": 8
    },
    {
      "title": "Conseil national des barreaux | Accueil - Paris",
      "link": "https://www.cnb.avocat.fr/",
      "snippet": "Vous êtes avocat ? Connectez-vous pour accéder à des contenus exclusifs et à l'ensemble des services en ligne. S'identifier avec e-dentitas.",
      "position": 9
    }
  ],
  "peopleAlsoAsk": [
    {
      "question": "Quels sont les bienfait de l'avocat ?",
      "snippet": "LES BIENFAITS DE L'AVOCAT : POURQUOI EN MANGER ?\nL'avocat est riche en antioxydants. ...\nUne source élevée de fibres. ...\nPour faire le plein de « bons acides gras » ...\nUne excellente source de vitamine B5. ...\nUn bon apport de vitamine B6. ...\nRiche en vitamine K. ...\nUne source non négligeable de phosphore, magnésium et potassium.",
      "title": "L'avocat, un fruit exotique aux nombreux bienfaits",
      "link": "https://www.passeportsante.net/fr/Nutrition/EncyclopedieAliments/Fiche.aspx?doc=avocat_nu"
    },
    {
      "question": "Est-il bon de manger de l'avocat tous les jours ?",
      "snippet": "Consommé quotidiennement, l'avocat aide à prévenir la constipation et facilite\nla digestion grâce à sa teneur en fibres. Il possède aussi un effet coupe-faim\nqui permet de diminuer la sensation de fringale.",
      "title": "Voici ce qu'il se passe si vous mangez de l'avocat tous les jours",
      "link": "https://www.elle.fr/Elle-a-Table/Les-dossiers-de-la-redaction/News-de-la-redaction/Voici-ce-qu-il-se-passe-si-vous-mangez-de-l-avocat-tous-les-jours-3828058"
    },
    {
      "question": "Quel est le salaire d'un avocat ?",
      "snippet": "En début de carrière, un avocat gagne entre 1 800 et 2 700 € brut par mois.\nEnsuite, les rémunérations varient en fonction de chaque situation (renommée,\nactivité, localisation du cabinet). Le revenu moyen mensuel dans la profession\nserait aux alentours de 5 000 €.",
      "title": "Avocat / Avocate : métier, études, diplômes, salaire, formation | CIDJ",
      "link": "https://www.cidj.com/metiers/avocat-avocate"
    },
    {
      "question": "Quels sont les 3 types d'avocats ?",
      "snippet": "En général, on distingue trois catégories d'avocats : les avocats d'affaires,\ndont les clients sont des entreprises ; les pénalistes, qui défendent notamment\nles auteurs présumés de crimes ou délits et les spécialistes des affaires\nciviles (divorces, successions, etc.).",
      "title": "Fiche métier : Avocat·e - Métiers.be",
      "link": "https://metiers.siep.be/metier/avocat/"
    }
  ],
  "relatedSearches": [
    {
      "query": "Avocate ou avocat"
    },
    {
      "query": "Avocat français"
    },
    {
      "query": "Avocat salaire"
    },
    {
      "query": "Avocat gratuit"
    },
    {
      "query": "Avocat prix"
    },
    {
      "query": "Avocat divorce"
    },
    {
      "query": "Avocat arbre"
    },
    {
      "query": "Avocat pénal"
    },
    {
      "query": "Avocat étude"
    },
    {
      "query": "Avocat famille"
    }
  ]
}



urls = [item['link'] for item in google_search_result['organic']]
#get the content of the urls

def get_content(url):
    content = trafilatura.fetch_url(url)
    content =trafilatura.extract(content)
    # content = content.encode('utf-8')
    #add the content to a txt file named content.txt
    with open('content.txt', 'a') as f:
        f.write(content)
    return content


def get_content_list(urls):
    contents = []
    for url in urls:
        try:
            content = get_content(url)
            contents.append(content)
        except Exception:
            print(f"can't get content from url :{url} ")
    return contents



contents = get_content_list(urls)

#convert the list to a string
contents = ' '.join(contents)

# Remove stop words
stop_words = set(stopwords.words('french'))

#il faut aussi supprimer la ponctuation

# Tokenization
tokens = word_tokenize(contents)
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]


blob = TextBlob(" ".join(filtered_tokens))
keywords = blob.noun_phrases
print(keywords)
# Calcul des fréquences des mots
fdist = FreqDist(filtered_tokens)

# Impression des mots les plus fréquents

#remove ponctuation from fdist  
for word in list(fdist):
    if word in string.punctuation:
        del fdist[word]
# il faut aussi retirer les resultats qui ne sont pas des mots


for word in list(fdist):
    if not word.isalpha():
        del fdist[word]

#il faut aussi retirer les mots de type : aussi, donc, etc      

word_list = []

for word, frequency in fdist.most_common(100):
    print(u'{};{}'.format(word, frequency))
    word_list.append(word)
    
#save the output in a file named " word_list.txt"

with open('word_list.txt', 'w') as f:
    for item in word_list:
        f.write("%s " % item)



#identifier les mots les plus pertinents dans votre liste de mots récupérée en utilisant l'algorithme de désambiguation de mots-clés.
#https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/





#sort the keyword by relevancy

#penser à utiliser rake_nltk par la suite


# #visualize the word frequency
fdist.plot(50, cumulative=False)


# from gensim import corpora, models
# from gensim.corpora import Dictionary

# # Define the list of keywords
# keywords = word_list

# # Create a dictionary of keywords
# dictionary = corpora.Dictionary(tokens)

# # Create a bag-of-words representation of the keywords
# corpus = [dictionary.doc2bow(keyword) for keyword in keywords]

# # Train an LSA model on the corpus
# lsa_model = models.LsiModel(corpus, id2word=dictionary, num_topics=1)

# # Sort the keywords by relevance to the language
# sorted_keywords = sorted(keywords, key=lambda x: lsa_model[dictionary.doc2bow([x])][0][1], reverse=True)

# print(sorted_keywords)

