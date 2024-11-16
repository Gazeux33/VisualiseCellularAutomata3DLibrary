 ## Instance Batching :
Regroupe les cubes similaires pour le rendu par lots
Utilise un buffer d'instances pour réduire les appels de rendu
Pré-calcule les matrices de transformation


## Frustum Culling :
Ne rend que les cubes visibles dans le champ de vision
Calcule et met à jour les plans du frustum de vue
Teste rapidement si un cube est visible


## Spatial Partitioning :
Divise l'espace en grille pour accélérer les requêtes spatiales
Ne vérifie que les cubes dans les cellules proches du joueur
Réduit le nombre de tests de visibilité


## Optimisations de Mémoire :
Utilise numpy pour les calculs matriciels efficaces
Réutilise les buffers pour éviter les allocations
Flag "dirty" pour éviter les mises à jour inutiles