Lors de mon premier cours d'économie et politiques publiques à la faculté de DSEG (Droit, Sciences Économiques et Gestion) de Nancy, nous avons traité avec notre enseignant samuel ferey de la décentralisation de l'optimum ✨ .
À titre illustratif, nous avons essayé de savoir si, en laissant les agents agir
librement, on pourrait atteindre la mixité sociale. 
Dès lors, nous nous sommes intéressés au modèle de ségrégation publié en 
1971 par Thomas Schelling. Dans une ville constituée de deux types d'habitants (Rouge et bleu 🎎 ), Schelling pose comme hypothèse que chaque 
habitant possède une certaine tolérance en ce qui concerne le voisinage et souhaite un minimum de diversité, mais pas trop non plus. Ainsi, chaque habitant voudrait qu'un pourcentage minimal de ses voisins lui ressemble (ratio de similarité). 
L'espace géographique est représenté par une grille avec des cases qui symbolisent des emplacements habitables et les cases blanches symbolisent les espaces vacants. À chaque itération, les points insatisfaits peuvent choisir de déménager vers des espaces libres choisis aléatoirement. L'équilibre est atteint lorsqu'aucun point ne se déplace, tout le monde étant satisfait de son entourage. Schelling montre alors, en appliquant un peu la théorie des jeux, que la répartition de la population peut évoluer rapidement vers deux situations stables :

🔹 Un mélange de populations (cas minoritaire et peu probable)
🔸 Une ségrégation quasi absolue.

Curieux 🔎, j'ai décidé de refaire cette simulation moi-même 👨‍💻 en utilisant Python 🐍 et les bibliothèques suivantes : 
- NumPy, car elle prend en charge des opérations élémentaires (comme l’addition, la multiplication, etc.) sur l’ensemble du tableau, ce qui simplifie le code et optimise les calculs numériques et les opérations matricielles.
- Tkinter avec ses widgets de texte et de canevas puissants et faciles à utiliser. De plus, j'ai un penchant pour Tkinter, car je l'ai légèrement touché du doigt l'année dernière avec le projet Industriel proposé par une filiale du groupe Ortec Group. 

Dans la première version de ce programme, j'utilisais deux classes en dehors de la classe Application pour l'interface :
- La classe Point pour représenter un point qui pourrait être de couleur bleue ou rouge
- La classe Grille qui avait une liste de points repartis de manière aléatoire au début de la simulation 
Cependant, cette approche est problématique, car à chaque actualisation du programme (qui a lieu toutes les 100 ms), le programme devait vérifier la satisfaction de 2400 objets en déplaçant certains d'entre eux de manière aléatoire. Ce processus étant trop lourd pour être répété avec fluidité, j'ai revu mon approche 💡en gardant une seule classe : La classe Grille, et j'ai plutôt utilisé un tableau NumPy à deux dimensions pour sauvegarder les cases vides avec le chiffre 0, les cases bleus avec le chiffre 1 et les cases rouges avec le chiffre 2.

Bilan : cinq heures de code, sept heures de débogage. 
