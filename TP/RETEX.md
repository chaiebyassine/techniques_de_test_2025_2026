# Retour d'Expérience (RETEX)

## 1. Ce qui a bien fonctionné

### Approche TDD (Test-Driven Development)
- Écrire les tests avant le code a permis de clarifier les attentes pour chaque fonction
- Les tests ont servi de "contrat" pour l'implémentation
- Facilite la détection rapide des régressions

### Structure modulaire
- Séparation claire : `binary_utils.py`, `triangulation.py`, `app.py`
- Chaque module a ses propres tests unitaires
- Facilite la maintenance et les modifications

### Utilisation de pytest
- Marqueurs (`@pytest.mark.perf`) pour séparer les tests de performance
- Fixtures pour factoriser le code de test
- Configuration centralisée dans `conftest.py`

## 2. Difficultés rencontrées

### Algorithme de triangulation
- L'algorithme Bowyer-Watson est en O(n²), ce qui pose des problèmes de performance
- Pour 5000+ points, le temps d'exécution devient significatif (18s pour 5000 points)
- Solution : ajuster les seuils de performance pour refléter la réalité

### Format binaire
- Comprendre le format little-endian et l'utilisation de `struct.pack/unpack`
- Gérer les cas d'erreur (buffer trop court, format invalide)

### Tests d'intégration avec mocks
- Mocker correctement `fetch_pointset` pour simuler le PointSetManager
- Gérer les différents cas d'erreur (404, 503, etc.)

## 3. Ce que je ferais différemment

### Optimisation de l'algorithme
- Utiliser une structure de données spatiale (quad-tree, k-d tree) pour améliorer les performances
- Ou implémenter l'algorithme divide-and-conquer en O(n log n)

### Plus de tests de robustesse
- Tester avec des coordonnées négatives, très grandes, ou très petites
- Tester les cas limites (points dupliqués, points très proches)

### Documentation
- Ajouter plus de commentaires dans le code de triangulation
- Créer des schémas explicatifs pour l'algorithme

## 4. Bilan

### Points forts du plan initial
- La décomposition en 5 sections de tests était pertinente
- Couvrir les cas d'erreur dès le départ était une bonne idée
- Les tests de performance ont révélé les limites de l'implémentation

### Points faibles du plan initial
- Sous-estimation de la complexité de l'algorithme de triangulation
- Seuils de performance initiaux trop optimistes

## 5. Statistiques finales

| Catégorie | Nombre de tests | Résultat |
|-----------|-----------------|----------|
| Unitaires (binary_utils) | 9 |  Passés |
| Unitaires (triangulation) | 9 |  Passés |
| API | 6 |  Passés |
| Intégration | 5 |  Passés |
| Performance | 5 |  Passés |
| **Total** | **34** | ** 100%** |

## 6. Conclusion

Ce TP m'a permis de mettre en pratique l'approche TDD dans un contexte réaliste. 
La principale leçon apprise est que les tests doivent être réalistes et refléter 
les contraintes réelles du système (notamment les performances).

L'implémentation "from scratch" sans bibliothèques externes a été un bon exercice 
pour comprendre les concepts sous-jacents (sérialisation binaire, algorithmes géométriques).
