#!/usr/bin/env python
"""
Script de vérification de la santé du déploiement SDI Store
Utilisation: python health_check.py
"""

import os
import sys
import socket
import time
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError

class HealthChecker:
    def __init__(self):
        self.checks = []
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def check_port(self, host, port, name):
        """Vérifier si un port est accessible"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                self.checks.append(('✓', f'{name} (port {port})', 'OK'))
                return True
            else:
                self.checks.append(('✗', f'{name} (port {port})', 'Non-accessible'))
                return False
        except Exception as e:
            self.checks.append(('✗', f'{name} (port {port})', str(e)))
            return False
    
    def check_http(self, url, name):
        """Vérifier la réponse HTTP"""
        try:
            response = urlopen(url, timeout=5)
            status = response.status
            if status == 200:
                self.checks.append(('✓', f'{name}', f'HTTP {status}'))
                return True
            else:
                self.checks.append(('✗', f'{name}', f'HTTP {status}'))
                return False
        except URLError as e:
            self.checks.append(('✗', f'{name}', f'Erreur HTTP: {str(e)[:50]}'))
            return False
        except Exception as e:
            self.checks.append(('✗', f'{name}', f'Erreur: {str(e)[:50]}'))
            return False
    
    def check_file(self, path, name):
        """Vérifier l'existence d'un fichier"""
        if Path(path).exists():
            size = Path(path).stat().st_size
            self.checks.append(('✓', f'{name}', f'{size} bytes'))
            return True
        else:
            self.checks.append(('✗', f'{name}', 'Manquant'))
            return False
    
    def check_env(self, key, name):
        """Vérifier une variable d'environnement"""
        if os.getenv(key):
            value = os.getenv(key)[:20] + '...' if len(os.getenv(key)) > 20 else os.getenv(key)
            self.checks.append(('✓', f'{name}', f'Défini'))
            return True
        else:
            self.checks.append(('✗', f'{name}', 'Non défini'))
            return False
    
    def run_checks(self):
        """Exécuter tous les contrôles"""
        print("\n" + "="*60)
        print("Vérification de la santé - SDI Store")
        print("="*60)
        
        # Charger .env
        if Path('.env').exists():
            from dotenv import load_dotenv
            load_dotenv('.env')
        
        # 1. Ports
        print("\n📡 Vérification des ports...")
        self.check_port('127.0.0.1', 8000, 'Django Daphne')
        self.check_port('127.0.0.1', 80, 'Nginx HTTP')
        self.check_port('127.0.0.1', 443, 'Nginx HTTPS')
        self.check_port('127.0.0.1', 5432, 'PostgreSQL')
        self.check_port('127.0.0.1', 6379, 'Redis')
        
        # 2. Services HTTP
        print("\n🌐 Vérification des services HTTP...")
        self.check_http('http://localhost:8000/', 'Django Root')
        self.check_http('http://localhost:8000/admin/', 'Django Admin')
        self.check_http('http://localhost/', 'Nginx Proxy')
        
        # 3. Fichiers
        print("\n📁 Vérification des fichiers...")
        self.check_file('sdi_market/manage.py', 'manage.py')
        self.check_file('sdi_market/db.sqlite3', 'Base de données SQLite')
        self.check_file('.env', 'Fichier .env')
        self.check_file('docker-compose.yml', 'docker-compose.yml')
        
        # 4. Variables d'environnement
        print("\n🔑 Vérification des variables d'environnement...")
        self.check_env('DJANGO_SECRET_KEY', 'DJANGO_SECRET_KEY')
        self.check_env('DEBUG', 'DEBUG')
        self.check_env('ALLOWED_HOSTS', 'ALLOWED_HOSTS')
        self.check_env('DATABASE_URL', 'DATABASE_URL')
        self.check_env('REDIS_URL', 'REDIS_URL')
        
        # 5. Docker
        print("\n🐳 Vérification Docker...")
        import subprocess
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                container_count = len([l for l in result.stdout.split('\n')[1:] if l.strip()])
                self.checks.append(('✓', 'Docker', f'{container_count} conteneurs actifs'))
            else:
                self.checks.append(('✗', 'Docker', 'Erreur connexion'))
        except Exception as e:
            self.checks.append(('✗', 'Docker', str(e)[:30]))
        
        # Afficher résultats
        self.print_results()
    
    def print_results(self):
        """Afficher les résultats formatés"""
        print("\n" + "="*60)
        print("Résultats")
        print("="*60)
        
        for symbol, check, result in self.checks:
            print(f"{symbol} {check:<35} {result}")
        
        # Résumé
        passed = sum(1 for s, _, _ in self.checks if s == '✓')
        total = len(self.checks)
        
        print("\n" + "-"*60)
        print(f"Total: {passed}/{total} contrôles réussis")
        
        if passed == total:
            print("✓ Système en bonne santé!")
            return 0
        else:
            print(f"⚠ {total-passed} problème(s) détecté(s)")
            return 1


if __name__ == '__main__':
    checker = HealthChecker()
    exit_code = checker.run_checks()
    sys.exit(exit_code)
