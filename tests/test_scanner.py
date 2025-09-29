#!/usr/bin/env python3
"""
Tests unitaires pour le scanner de ports TCP
============================================

Tests simples et rapides qui utilisent un serveur local temporaire
pour vérifier le bon fonctionnement du scanner.
"""

import socket
import threading
import time
import sys
import os

# Ajout du répertoire parent au path pour importer scanner
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import scan_port


class TestServer:
    """
    Serveur TCP simple pour les tests.
    Écoute sur un port libre et accepte une connexion.
    """
    
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 0  # 0 = OS choisit un port libre
        self.socket = None
        self.server_thread = None
        self.running = False
        self.actual_port = None
    
    def start(self):
        """Démarre le serveur dans un thread séparé."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        # Récupération du port assigné par l'OS
        self.actual_port = self.socket.getsockname()[1]
        
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Attente que le serveur soit prêt
        time.sleep(0.1)
    
    def _run_server(self):
        """Boucle principale du serveur."""
        while self.running:
            try:
                self.socket.settimeout(1.0)  # Timeout pour pouvoir arrêter
                conn, addr = self.socket.accept()
                conn.close()
            except socket.timeout:
                continue
            except Exception:
                break
    
    def stop(self):
        """Arrête le serveur."""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.server_thread:
            self.server_thread.join(timeout=1.0)
    
    def get_port(self):
        """Retourne le port sur lequel le serveur écoute."""
        return self.actual_port


def test_scan_port_open():
    """
    Test que scan_port détecte correctement un port ouvert.
    """
    # Création et démarrage du serveur de test
    server = TestServer()
    server.start()
    
    try:
        # Test du port ouvert
        port = server.get_port()
        result = scan_port('127.0.0.1', port, timeout=0.5)
        
        # Vérification que le port est détecté comme ouvert
        assert result is True, f"Le port {port} devrait être détecté comme ouvert"
        
        print(f"✓ Test réussi: Port {port} correctement détecté comme ouvert")
        
    finally:
        # Nettoyage: arrêt du serveur
        server.stop()


def test_scan_port_closed():
    """
    Test que scan_port détecte correctement un port fermé.
    """
    # Test d'un port probablement fermé (port élevé mais valide)
    result = scan_port('127.0.0.1', 65535, timeout=0.5)
    
    # Vérification que le port est détecté comme fermé
    assert result is False, "Le port 65535 devrait être détecté comme fermé"
    
    print("✓ Test réussi: Port fermé correctement détecté")


def test_scan_port_invalid_host():
    """
    Test que scan_port gère correctement un hôte invalide.
    """
    try:
        result = scan_port('hostinexistant12345.local', 80, timeout=0.5)
        assert False, "Une exception devrait être levée pour un hôte invalide"
    except Exception as e:
        # Vérification que l'erreur contient des informations utiles
        assert "hostinexistant12345.local" in str(e) or "résoudre" in str(e).lower()
        print("✓ Test réussi: Hôte invalide correctement géré")


def test_scan_port_timeout():
    """
    Test que scan_port respecte le timeout.
    """
    # Test avec un timeout très court sur un port probablement fermé
    start_time = time.time()
    result = scan_port('127.0.0.1', 12345, timeout=0.1)
    end_time = time.time()
    
    # Vérification que le timeout est respecté (avec une marge)
    duration = end_time - start_time
    assert duration < 0.5, f"Le timeout n'a pas été respecté (durée: {duration:.2f}s)"
    # Le port 12345 est probablement fermé, mais on ne fait que vérifier le timeout
    print(f"✓ Test réussi: Timeout respecté ({duration:.2f}s)")


def run_tests():
    """
    Exécute tous les tests et affiche un résumé.
    """
    print("Démarrage des tests du scanner de ports...")
    print("=" * 50)
    
    tests = [
        test_scan_port_open,
        test_scan_port_closed,
        test_scan_port_invalid_host,
        test_scan_port_timeout
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Échec du test {test.__name__}: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Résultats: {passed} tests réussis, {failed} tests échoués")
    
    if failed == 0:
        print("🎉 Tous les tests sont passés avec succès!")
        return True
    else:
        print("❌ Certains tests ont échoué.")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
