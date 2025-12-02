

import pytest
import struct
from unittest.mock import patch, MagicMock




def creer_pointset_binaire(points):
    """Crée un PointSet binaire à partir d'une liste de points."""
    buf = struct.pack('<I', len(points))
    for x, y in points:
        buf += struct.pack('<ff', x, y)
    return buf




@pytest.fixture
def client():
    """Client de test Flask."""
    from src.app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def uuid_valide():
    return "123e4567-e89b-12d3-a456-426614174000"



def test_flux_complet_triangle(client, uuid_valide):
   
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    pointset_binaire = creer_pointset_binaire(points)
    
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
    
    assert response.status_code == 200
    
    data = response.data
    n_points = struct.unpack('<I', data[:4])[0]
    assert n_points == 3


def test_flux_complet_carre(client, uuid_valide):
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    pointset_binaire = creer_pointset_binaire(points)
    
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
    
    assert response.status_code == 200
    
    data = response.data
    n_points = struct.unpack('<I', data[:4])[0]
    assert n_points == 4
    
    offset = 4 + n_points * 8
    n_triangles = struct.unpack('<I', data[offset:offset+4])[0]
    assert n_triangles == 2


def test_triangulator_appelle_pointsetmanager(client, uuid_valide):
    """PLAN: Le Triangulator envoie bien la requête vers le PointSetManager."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    pointset_binaire = creer_pointset_binaire(points)
    
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
        
        mock.assert_called_once()




def test_pointsetmanager_retourne_404(client, uuid_valide):
    """PLAN: Il traite correctement l'erreur (PointSet non trouvé)."""
    with patch('src.app.fetch_pointset') as mock:
        mock.side_effect = Exception("PointSet not found")
        
        response = client.get(f'/triangulation/{uuid_valide}')
    
    assert response.status_code == 404


def test_pointsetmanager_indisponible(client, uuid_valide):
    """PLAN: PointSetManager indisponible → 503."""
    with patch('src.app.fetch_pointset') as mock:
        mock.side_effect = ConnectionError("Service unavailable")
        
        response = client.get(f'/triangulation/{uuid_valide}')
    
    assert response.status_code == 503
