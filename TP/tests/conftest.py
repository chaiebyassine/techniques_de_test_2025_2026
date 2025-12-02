"""
Configuration pytest partagée pour tous les tests.
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def pytest_configure(config):
    """Configuration des marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "perf: marque les tests de performance (désélectionnés par défaut)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modifie la collection de tests :
    - Exclut les tests @pytest.mark.perf sauf si explicitement demandés
    """
    if config.getoption("-m"):
        # Si un marqueur est spécifié, ne pas modifier
        return
    
    skip_perf = pytest.mark.skip(reason="Tests de perf exclus par défaut. Utilisez: pytest -m perf")
    for item in items:
        if "perf" in item.keywords:
            item.add_marker(skip_perf)
