# Fichier : tests/conftest.py
import sys
import os
import pytest

# === NOUVELLES LIGNES POUR CORRIGER L'ERREUR D'IMPORTATION ===
# On ajoute le dossier parent (la racine du projet) au chemin de recherche de Python
# pour que les tests puissent trouver le module 'app'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# =============================================================

from app import create_app, db # Cette ligne va maintenant fonctionner

@pytest.fixture()
def app():
    # On crée une instance de l'application avec une configuration de test
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # Base de données en mémoire
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # On s'assure que les tests s'exécutent à l'intérieur du contexte de l'application.
    with app.app_context():
        db.create_all() # On crée les tables
        yield app       # On exécute le test

@pytest.fixture()
def client(app):
    # Crée un client de test pour envoyer des requêtes aux routes
    return app.test_client()