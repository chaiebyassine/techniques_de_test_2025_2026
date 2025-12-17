

import pytest
import struct
from src.binary_utils import (
    encode_pointset,
    decode_pointset,
    encode_triangles,
    decode_triangles,
)




def test_encode_pointset_taille_attendue():
    points = [(1.0, 2.0), (3.0, 4.0)]
    buf = encode_pointset(points)
    
    taille_attendue = 4 + len(points) * 8
    assert len(buf) == taille_attendue


def test_decode_pointset_restitue_coordonnees():
    buf = struct.pack('<I', 2)           
    buf += struct.pack('<ff', 1.0, 2.0)  
    buf += struct.pack('<ff', 3.0, 4.0) 
    
    points = decode_pointset(buf)
    
    assert len(points) == 2
    assert points[0] == pytest.approx((1.0, 2.0))
    assert points[1] == pytest.approx((3.0, 4.0))


def test_pointset_encode_decode_roundtrip():
    original = [(1.5, 2.5), (3.5, 4.5), (5.5, 6.5)]
    
    buf = encode_pointset(original)
    resultat = decode_pointset(buf)
    
    assert len(resultat) == len(original)
    for i in range(len(original)):
        assert resultat[i] == pytest.approx(original[i])

def test_encode_triangles_taille():
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    
    buf = encode_triangles(points, triangles)
    
    
    taille_attendue = (4 + 3 * 8) + (4 + 1 * 12)
    assert len(buf) == taille_attendue


def test_decode_triangles_indices_valides():
    
    buf = struct.pack('<I', 3)          
    buf += struct.pack('<ff', 0.0, 0.0)
    buf += struct.pack('<ff', 1.0, 0.0)
    buf += struct.pack('<ff', 0.0, 1.0)
    buf += struct.pack('<I', 1)           
    buf += struct.pack('<III', 0, 1, 2)  
    
    points, triangles = decode_triangles(buf)
    
    n = len(points)
    for tri in triangles:
        for indice in tri:
            assert 0 <= indice < n, f"Indice {indice} invalide"


def test_triangles_encode_decode_roundtrip():
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]
    
    buf = encode_triangles(points, triangles)
    result_points, result_triangles = decode_triangles(buf)
    
    assert len(result_points) == len(points)
    assert result_triangles == triangles



def test_decode_buffer_trop_court():
    buf = b'\x01\x00'  
    
    with pytest.raises(Exception):
        decode_pointset(buf)


def test_decode_buffer_incomplet():
    buf = struct.pack('<I', 10)         
    buf += struct.pack('<ff', 1.0, 2.0)  
    
    with pytest.raises(Exception):
        decode_pointset(buf)


def test_mauvais_endianness():
    buf_big_endian = struct.pack('>I', 1)         
    buf_big_endian += struct.pack('>ff', 1.0, 2.0)
    
    try:
        points = decode_pointset(buf_big_endian)
        if len(points) > 0:
            assert points[0] != pytest.approx((1.0, 2.0))
    except Exception:
        pass  
