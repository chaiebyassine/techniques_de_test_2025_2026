
import struct


def encode_pointset(points: list) -> bytes:
    
    buf = struct.pack('<I', len(points))
    
    for x, y in points:
        buf += struct.pack('<ff', x, y)
    
    return buf


def decode_pointset(buf: bytes) -> list:
   
    if len(buf) < 4:
        raise ValueError("Buffer trop court")
    
    n_points = struct.unpack('<I', buf[:4])[0]
    
    taille_attendue = 4 + n_points * 8
    if len(buf) < taille_attendue:
        raise ValueError("Buffer incomplet")
    
    points = []
    offset = 4
    for _ in range(n_points):
        x, y = struct.unpack('<ff', buf[offset:offset + 8])
        points.append((x, y))
        offset += 8
    
    return points


def encode_triangles(points: list, triangles: list) -> bytes:
    
    buf = encode_pointset(points)
    
    buf += struct.pack('<I', len(triangles))
    
    for i, j, k in triangles:
        buf += struct.pack('<III', i, j, k)
    
    return buf


def decode_triangles(buf: bytes) -> tuple:
    
    if len(buf) < 4:
        raise ValueError("Buffer trop court")
    
    n_points = struct.unpack('<I', buf[:4])[0]
    taille_pointset = 4 + n_points * 8
    
    if len(buf) < taille_pointset + 4:
        raise ValueError("Buffer incomplet")
    
    points = decode_pointset(buf[:taille_pointset])
    
    offset = taille_pointset
    n_triangles = struct.unpack('<I', buf[offset:offset + 4])[0]
    offset += 4
    
    if len(buf) < offset + n_triangles * 12:
        raise ValueError("Buffer incomplet pour les triangles")
    
    triangles = []
    for _ in range(n_triangles):
        i, j, k = struct.unpack('<III', buf[offset:offset + 12])
        triangles.append((i, j, k))
        offset += 12
    
    return points, triangles

