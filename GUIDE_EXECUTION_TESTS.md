# Guide d'exécution des tests

Pour exécuter les tests unitaires du scanner de ports :

## 1. 📦 Installation de pytest (si nécessaire)

### Créer un environnement virtuel (recommandé)
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### Installer pytest
```bash
pip install pytest
```

## 2. 🧪 Exécution des tests

### Méthode 1 : Avec pytest (recommandé)
```bash
source venv/bin/activate
pytest tests/test_scanner.py -v
```

### Méthode 2 : Exécution directe
```bash
python3 tests/test_scanner.py
```

## 3. ✅ Résultats attendus

Les tests devraient tous passer et afficher :

- ✅ **Test réussi** : Port X correctement détecté comme ouvert
- ✅ **Test réussi** : Port fermé correctement détecté  
- ✅ **Test réussi** : Hôte invalide correctement géré
- ✅ **Test réussi** : Timeout respecté (X.XXs)

**Résumé :** 4 tests réussis, 0 tests échoués
🎉 **Tous les tests sont passés avec succès !**

## 4. 🔍 Détails des tests

| Test | Description |
|------|-------------|
| `test_scan_port_open` | Crée un serveur local temporaire et vérifie que le scanner détecte correctement le port ouvert |
| `test_scan_port_closed` | Vérifie qu'un port fermé est correctement identifié comme fermé |
| `test_scan_port_invalid_host` | Teste la gestion d'erreur pour un nom d'hôte invalide |
| `test_scan_port_timeout` | Vérifie que le timeout est respecté |

## 5. 🔧 Dépannage

### Problèmes courants :

- **pytest n'est pas installé** → Utilisez la méthode 2 (exécution directe)
- **Tests échouent** → Vérifiez que le port 80 n'est pas utilisé par un autre service sur votre machine
- **Conflits de ports** → Les tests utilisent des ports aléatoires pour éviter les conflits

### Solutions :

```bash
# Vérifier l'installation de pytest
pip list | grep pytest

# Exécuter les tests en mode verbeux pour plus de détails
pytest tests/test_scanner.py -v -s

# Exécuter un test spécifique
pytest tests/test_scanner.py::test_scan_port_open -v
```

## 6. 🛡️ Sécurité des tests

Les tests sont conçus pour être :
- **Rapides** (< 2 secondes)
- **Sûrs** (ne scannent que localhost)
- **Isolés** (utilisent des ports temporaires)

## 7. 📊 Exemple de sortie complète

```
=========================================== test session starts ============================================
platform darwin -- Python 3.13.4, pytest-8.4.2
collected 4 items                                                                                          

tests/test_scanner.py::test_scan_port_open PASSED                                                    [ 25%]
tests/test_scanner.py::test_scan_port_closed PASSED                                                  [ 50%]
tests/test_scanner.py::test_scan_port_invalid_host PASSED                                            [ 75%]
tests/test_scanner.py::test_scan_port_timeout PASSED                                                 [100%]

======================================= 4 passed in 6.13s =======================================
```

## 🔗 Voir aussi

- [README.md](README.md) - Documentation complète
- [example_usage.md](example_usage.md) - Exemples d'utilisation
- [EXPLANATION.md](EXPLANATION.md) - Explications pédagogiques
- [tests/test_scanner.py](tests/test_scanner.py) - Code source des tests
