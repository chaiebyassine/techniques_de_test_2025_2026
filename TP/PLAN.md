# TODO
## 1. Tests unitaires — Algorithme de triangulation

Pourquoi :
Vérifier que l’algorithme de triangulation produit des résultats mathématiquement corrects et cohérents, quelle que soit la configuration des points d’entrée.

Comment :
Les tests seront réalisés sur des ensembles de points simples et représentatifs :
Triangle minimal ,Carré ,Points colinéaires 
Vérifications supplémentaires :
Aucun triangle dégénéré (aire ≈ 0).
Les arêtes ne se croisent pas.
Les indices de sommets des triangles sont valides.

## 2.Tests unitaires — serialization binaire

Pourquoi :
S’assurer que les conversions entre les structures Python et leur format binaire sont correctes et conformes à la spécification.
Ces tests garantissent la compatibilité entre le Triangulator et les autres services.

Comment :

Pour les PointSet :
Vérifier qu’un encodage produit un binaire de la taille attendue 
Le décodage doit restituer les mêmes coordonnées .

Pour les Triangles :
Vérifier la partie “sommets” (identique à PointSet).
Vérifier la partie “triangles” :
Les indices doivent toujours référencer des sommets existants.

Cas d’erreur à tester :
Tampon binaire incomplet ou trop court.
Mauvais type d’encodage ou endianness incorrecte.

## 3. Tests API — Contrat du Triangulator

Pourquoi :
Vérifier que le service respecte bien la spécification OpenAPI (triangulator.yml) et se comporte correctement en cas d’entrée valide ou invalide.

Comment :
Cas normal (happy path) :
Requête HTTP avec un PointSetID valide.
Le contenu doit être un binaire valide représentant des Triangles.

Cas d’erreur :
PointSetID inconnu ,Contenu non supporté ,Mauvais header Accept .

## 4. Tests d’intégration — Flux complet simulé

Pourquoi :
Vérifier que le Triangulator fonctionne correctement dans son environnement global, c’est-à-dire en interaction avec le Client et le PointSetManager.

Comment :
Simulation (mock) du PointSetManager à l’aide d’un serveur HTTP factice.
Pour un PointSetID donné, le mock renvoie un PointSet binaire correct.

Vérifier que :
Le Triangulator envoie bien la requête vers le PointSetManager.
Il traite correctement la réponse ou l’erreur.
Il calcule la triangulation et renvoie une réponse binaire valide au client.

## 5. Tests de performance
Pourquoi :
La triangulation et la conversion binaire peuvent être coûteuses en temps.
Ces tests servent à mesurer les performances et fixer des seuils acceptables.

Comment :
Tests effectués sur des ensembles de points de tailles croissantes (ex : 1 000, 5 000, 10 000 points).
Mesure du temps de calcul de la triangulation et du temps d’encodage/décodage binaire.
Ces tests seront marqués avec @pytest.mark.perf pour pouvoir être exécutés séparément des tests unitaires.
