#!/usr/bin/env python3
"""
Scanner de ports TCP minimal
============================

Auteur: Cursor
Date: 2024
Licence: MIT

AVERTISSEMENT LÉGAL:
====================
Ce scanner ne doit être utilisé QUE sur des machines que vous possédez
ou pour lesquelles vous avez une autorisation écrite explicite.

Toute utilisation non autorisée est ILLÉGALE et relève de la responsabilité
de l'utilisateur. L'utilisation de cet outil sur des systèmes sans permission
peut constituer une violation de la loi sur la cybersécurité.

Description:
============
Scanner de ports TCP simple utilisant des connexions socket standard.
Utilise le threading pour améliorer les performances tout en restant simple.
"""

import socket
import argparse
import concurrent.futures
import time
from contextlib import closing
from typing import List


def scan_port(host: str, port: int, timeout: float) -> bool:
    """
    Scanne un port unique en tentant une connexion TCP.
    
    Args:
        host: Adresse IP ou nom d'hôte à scanner
        port: Numéro de port à tester
        timeout: Délai d'attente en secondes pour la connexion
        
    Returns:
        True si le port est ouvert, False sinon
    """
    try:
        # Création d'un socket TCP
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            # Configuration du timeout pour éviter les blocages
            sock.settimeout(timeout)
            
            # Tentative de connexion au port
            result = sock.connect_ex((host, port))
            
            # connect_ex retourne 0 si la connexion réussit
            return result == 0
            
    except socket.gaierror:
        # Erreur de résolution DNS
        raise Exception(f"Impossible de résoudre l'hôte: {host}")
    except Exception as e:
        # Autres erreurs réseau
        raise Exception(f"Erreur lors du scan du port {port}: {e}")


def scan_range(host: str, start: int, end: int, timeout: float, workers: int) -> List[int]:
    """
    Scanne une plage de ports en utilisant le threading pour améliorer les performances.
    
    Args:
        host: Adresse IP ou nom d'hôte à scanner
        start: Port de début de la plage
        end: Port de fin de la plage (inclus)
        timeout: Délai d'attente par connexion
        workers: Nombre de threads à utiliser
        
    Returns:
        Liste des ports ouverts, triés par numéro
    """
    ports_ouverts = []
    
    # Création du pool de threads pour scanner en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # Soumission de toutes les tâches de scan
        futures = {
            executor.submit(scan_port, host, port, timeout): port 
            for port in range(start, end + 1)
        }
        
        # Traitement des résultats au fur et à mesure
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                if future.result():
                    ports_ouverts.append(port)
            except Exception as e:
                # En cas d'erreur, on continue avec les autres ports
                print(f"Erreur sur le port {port}: {e}")
    
    # Tri des ports ouverts par numéro
    return sorted(ports_ouverts)


def parse_args():
    """
    Parse les arguments de ligne de commande.
    
    Returns:
        Namespace contenant les arguments parsés
    """
    parser = argparse.ArgumentParser(
        description="Scanner de ports TCP minimal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python3 scanner.py -t 127.0.0.1
  python3 scanner.py -t example.com -s 20 -e 25
  python3 scanner.py -t 192.168.1.1 -s 1 -e 1024 --timeout 0.5 --workers 20

AVERTISSEMENT: Utilisez uniquement sur des machines autorisées!
        """
    )
    
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Adresse IP ou nom d\'hôte à scanner (obligatoire)'
    )
    
    parser.add_argument(
        '-s', '--start',
        type=int,
        default=1,
        help='Port de début (défaut: 1)'
    )
    
    parser.add_argument(
        '-e', '--end',
        type=int,
        default=1024,
        help='Port de fin (défaut: 1024)'
    )
    
    parser.add_argument(
        '--timeout',
        type=float,
        default=1.0,
        help='Timeout par connexion en secondes (défaut: 1.0)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=50,
        help='Nombre de threads (défaut: 50)'
    )
    
    return parser.parse_args()


def main():
    """
    Fonction principale qui orchestre le scan et affiche les résultats.
    """
    # Parsing des arguments
    args = parse_args()
    
    # Validation des arguments
    if args.start < 1 or args.start > 65535:
        print("Erreur: Le port de début doit être entre 1 et 65535")
        return
    
    if args.end < 1 or args.end > 65535:
        print("Erreur: Le port de fin doit être entre 1 et 65535")
        return
    
    if args.start > args.end:
        print("Erreur: Le port de début ne peut pas être supérieur au port de fin")
        return
    
    if args.workers < 1 or args.workers > 200:
        print("Erreur: Le nombre de workers doit être entre 1 et 200")
        return
    
    # Affichage des informations de scan
    print(f"Scan de {args.target} sur les ports {args.start}-{args.end}")
    print(f"Timeout: {args.timeout}s, Workers: {args.workers}")
    print("-" * 50)
    
    # Mesure du temps de début
    debut = time.time()
    
    try:
        # Exécution du scan
        ports_ouverts = scan_range(
            args.target, 
            args.start, 
            args.end, 
            args.timeout, 
            args.workers
        )
        
        # Mesure du temps de fin
        fin = time.time()
        duree = fin - debut
        
        # Affichage des résultats
        if ports_ouverts:
            print("Ports ouverts trouvés:")
            for port in ports_ouverts:
                print(f"Port {port} ouvert")
        else:
            print("Aucun port ouvert trouvé")
        
        # Résumé
        total_ports = args.end - args.start + 1
        print(f"\nRésumé: {len(ports_ouverts)} ports ouverts sur {total_ports} scannés en {duree:.2f}s")
        
    except Exception as e:
        print(f"Erreur lors du scan: {e}")
        return


if __name__ == "__main__":
    main()
