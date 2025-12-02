"""
Tests unitaires — Algorithme de triangulation

PLAN.md Section 1:
- Triangle minimal, Carré, Points colinéaires
- Aucun triangle dégénéré (aire ≈ 0)
- Les arêtes ne se croisent pas
- Les indices de sommets valides
"""

import pytest
from src.triangulator.triangulation import compute_triangulation

def test_triangle_minimal():
    points = [(0, 0), (1, 0), (0, 1)]
    triangles = compute_triangulation(points)
    assert len(triangles) == 1


def test_carre():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangles = compute_triangulation(points)
    assert len(triangles) == 2


def test_points_colineaires():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    triangles = compute_triangulation(points)
    assert len(triangles) == 0



def test_indices_sommets_valides():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangles = compute_triangulation(points)
    
    n = len(points)
    for triangle in triangles:
        for indice in triangle:
            assert 0 <= indice < n, f"Indice {indice} hors limite [0, {n-1}]"


def test_aucun_triangle_degenere():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangles = compute_triangulation(points)
    
    for tri in triangles:
        i, j, k = tri
        x1, y1 = points[i]
        x2, y2 = points[j]
        x3, y3 = points[k]
        
        aire = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
        assert aire > 0, f"Triangle dégénéré: aire = {aire}"


def test_aretes_ne_se_croisent_pas():
    points = [(0, 0), (2, 0), (2, 2), (0, 2)]
    triangles = compute_triangulation(points)
    
    aretes = []
    for tri in triangles:
        i, j, k = tri
        aretes.append(tuple(sorted([i, j])))
        aretes.append(tuple(sorted([j, k])))
        aretes.append(tuple(sorted([i, k])))
    
    def segments_se_croisent(p1, p2, p3, p4):
        def signe(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        
        d1 = signe(p3, p4, p1)
        d2 = signe(p3, p4, p2)
        d3 = signe(p1, p2, p3)
        d4 = signe(p1, p2, p4)
        
        return (d1 * d2 < 0) and (d3 * d4 < 0)
    
    for idx1 in range(len(aretes)):
        for idx2 in range(idx1 + 1, len(aretes)):
            a1, a2 = aretes[idx1]
            b1, b2 = aretes[idx2]
            
            if a1 in (b1, b2) or a2 in (b1, b2):
                continue
            
            croise = segments_se_croisent(
                points[a1], points[a2],
                points[b1], points[b2]
            )
            assert not croise, "Deux arêtes se croisent!"


def test_zero_points():
    assert compute_triangulation([]) == []


def test_un_point():
    assert compute_triangulation([(0, 0)]) == []


def test_deux_points():
    assert compute_triangulation([(0, 0), (1, 1)]) == []
