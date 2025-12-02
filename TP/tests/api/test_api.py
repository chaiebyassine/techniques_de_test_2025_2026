

import pytest
import struct
from unittest.mock import patch



@pytest.fixture
def client():
    """Crée un client de test Flask."""
    from src.app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def uuid_valide():
    """UUID valide pour les tests."""
    return "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture
def pointset_binaire():
    """Crée un PointSet binaire valide (3 points = triangle)."""
    buf = struct.pack('<I', 3)
    buf += struct.pack('<ff', 0.0, 0.0)
    buf += struct.pack('<ff', 1.0, 0.0)
    buf += struct.pack('<ff', 0.0, 1.0)
    return buf




def test_requete_valide_retourne_200(client, uuid_valide, pointset_binaire):
    """PLAN: Requête HTTP avec un PointSetID valide → 200."""
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
        
        assert response.status_code == 200


def test_requete_valide_retourne_binaire(client, uuid_valide, pointset_binaire):
    """PLAN: Le contenu doit être un binaire valide."""
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
        
        assert response.content_type == 'application/octet-stream'
        assert len(response.data) > 0


def test_reponse_contient_triangles(client, uuid_valide, pointset_binaire):
    """PLAN: Le contenu représente des Triangles valides."""
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(f'/triangulation/{uuid_valide}')
        
        data = response.data
        assert len(data) >= 8  
        
        n_points = struct.unpack('<I', data[:4])[0]
        assert n_points == 3




def test_pointsetid_inconnu_retourne_404(client, uuid_valide):
    """PLAN: PointSetID inconnu → 404."""
    with patch('src.app.fetch_pointset') as mock:
        mock.side_effect = Exception("Not found")
        
        response = client.get(f'/triangulation/{uuid_valide}')
        
        assert response.status_code == 404


def test_uuid_invalide_retourne_400(client):
    """PLAN: UUID invalide → 400."""
    uuid_invalide = "pas-un-uuid"
    
    response = client.get(f'/triangulation/{uuid_invalide}')
    
    assert response.status_code == 400


def test_mauvais_header_accept(client, uuid_valide, pointset_binaire):
    """PLAN: Mauvais header Accept → erreur ou ignoré."""
    with patch('src.app.fetch_pointset') as mock:
        mock.return_value = pointset_binaire
        
        response = client.get(
            f'/triangulation/{uuid_valide}',
            headers={'Accept': 'text/html'}
        )
        
        assert response.status_code in [200, 406]
