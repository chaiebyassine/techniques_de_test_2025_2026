"""Module de triangulation de Delaunay."""


def compute_triangulation(points: list) -> list:
    """
    Calcule la triangulation de Delaunay d'un ensemble de points.

    Args:
        points: Liste de tuples (x, y) représentant les points.
                Minimum 3 points requis.

    Returns:
        list: Liste de tuples (i, j, k) où i, j, k sont les indices
              des sommets de chaque triangle dans la liste points.

    Raises:
        ValueError: Si moins de 3 points sont fournis.

    Example:
        >>> points = [(0, 0), (1, 0), (0.5, 1)]
        >>> triangles = compute_triangulation(points)
        >>> triangles
        [(0, 1, 2)]
    """
    # TODO: implémenter l'algorithme de triangulation
    raise NotImplementedError("compute_triangulation non implémenté")
