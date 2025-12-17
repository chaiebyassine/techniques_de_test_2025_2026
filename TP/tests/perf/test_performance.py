

import pytest
import time
import random
from src.triangulator.triangulation import compute_triangulation
from src.binary_utils import encode_pointset, decode_pointset


SEUIL_1000 = 2.0
SEUIL_5000 = 30.0
SEUIL_10000 = 120.0


def generer_points(n, seed=42):
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]



@pytest.mark.perf
def test_perf_triangulation_1000_points():
    points = generer_points(1000)
    
    debut = time.perf_counter()
    triangles = compute_triangulation(points)
    duree = time.perf_counter() - debut
    
    print(f"\n[PERF] 1000 points: {duree:.3f}s, {len(triangles)} triangles")
    assert duree < SEUIL_1000


@pytest.mark.perf
def test_perf_triangulation_5000_points():
    points = generer_points(5000)
    
    debut = time.perf_counter()
    triangles = compute_triangulation(points)
    duree = time.perf_counter() - debut
    
    print(f"\n[PERF] 5000 points: {duree:.3f}s, {len(triangles)} triangles")
    assert duree < SEUIL_5000


@pytest.mark.perf
def test_perf_triangulation_10000_points():
    points = generer_points(10000)
    
    debut = time.perf_counter()
    triangles = compute_triangulation(points)
    duree = time.perf_counter() - debut
    
    print(f"\n[PERF] 10000 points: {duree:.3f}s, {len(triangles)} triangles")
    assert duree < SEUIL_10000



@pytest.mark.perf
def test_perf_encode_decode_1000_points():
    points = generer_points(1000)
    
    debut = time.perf_counter()
    buf = encode_pointset(points)
    temps_encode = time.perf_counter() - debut
    
    debut = time.perf_counter()
    result = decode_pointset(buf)
    temps_decode = time.perf_counter() - debut
    
    print(f"\n[PERF] Encode 1000 pts: {temps_encode:.4f}s")
    print(f"[PERF] Decode 1000 pts: {temps_decode:.4f}s")
    
    assert temps_encode < 0.1
    assert temps_decode < 0.1


@pytest.mark.perf
def test_perf_encode_decode_10000_points():
    points = generer_points(10000)
    
    debut = time.perf_counter()
    buf = encode_pointset(points)
    temps_encode = time.perf_counter() - debut
    
    debut = time.perf_counter()
    result = decode_pointset(buf)
    temps_decode = time.perf_counter() - debut
    
    print(f"\n[PERF] Encode 10000 pts: {temps_encode:.4f}s")
    print(f"[PERF] Decode 10000 pts: {temps_decode:.4f}s")
    
    assert temps_encode < 1.0
    assert temps_decode < 1.0
