

def compute_triangulation(points: list) -> list:
    
    n = len(points)
    
    if n < 3:
        return []
    
    if _sont_colineaires(points):
        return []
    
    triangles = _bowyer_watson(points)
    
    return triangles


def _sont_colineaires(points: list) -> bool:
    if len(points) < 3:
        return True
    
    x0, y0 = points[0]
    x1, y1 = points[1]
    
    for i in range(2, len(points)):
        x2, y2 = points[i]
        aire = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(aire) > 1e-10:
            return False
    
    return True


def _bowyer_watson(points: list) -> list:
   
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy) * 2
    
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    p1 = (mid_x - delta_max, mid_y - delta_max)
    p2 = (mid_x + delta_max, mid_y - delta_max)
    p3 = (mid_x, mid_y + delta_max)
    
    all_points = list(points) + [p1, p2, p3]
    n = len(points)
    
    triangles = [(n, n + 1, n + 2)]
    
    for i in range(n):
        point = points[i]
        triangles = _ajouter_point(all_points, triangles, i, point)
    
    resultat = []
    for tri in triangles:
        if tri[0] < n and tri[1] < n and tri[2] < n:
            resultat.append(tri)
    
    return resultat


def _ajouter_point(all_points: list, triangles: list, idx: int, point: tuple) -> list:
    mauvais_triangles = []
    
    for tri in triangles:
        if _point_dans_cercle_circonscrit(all_points, tri, point):
            mauvais_triangles.append(tri)
    
    polygone = []
    for tri in mauvais_triangles:
        for j in range(3):
            arete = (tri[j], tri[(j + 1) % 3])
            partagee = False
            for autre_tri in mauvais_triangles:
                if autre_tri == tri:
                    continue
                for k in range(3):
                    autre_arete = (autre_tri[k], autre_tri[(k + 1) % 3])
                    if (arete[0] == autre_arete[1] and arete[1] == autre_arete[0]):
                        partagee = True
                        break
                if partagee:
                    break
            if not partagee:
                polygone.append(arete)
    
    for tri in mauvais_triangles:
        triangles.remove(tri)
    
    for arete in polygone:
        nouveau_tri = (arete[0], arete[1], idx)
        triangles.append(nouveau_tri)
    
    return triangles


def _point_dans_cercle_circonscrit(all_points: list, triangle: tuple, point: tuple) -> bool:
    i, j, k = triangle
    ax, ay = all_points[i]
    bx, by = all_points[j]
    cx, cy = all_points[k]
    px, py = point
    
    ax_ = ax - px
    ay_ = ay - py
    bx_ = bx - px
    by_ = by - py
    cx_ = cx - px
    cy_ = cy - py
    
    det = (
        (ax_ * ax_ + ay_ * ay_) * (bx_ * cy_ - cx_ * by_) -
        (bx_ * bx_ + by_ * by_) * (ax_ * cy_ - cx_ * ay_) +
        (cx_ * cx_ + cy_ * cy_) * (ax_ * by_ - bx_ * ay_)
    )
    
    orientation = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    
    if orientation > 0:
        return det > 0
    else:
        return det < 0

