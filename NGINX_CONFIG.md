# Configuration Nginx pour l'upload de photos

## Problème
L'erreur "413 Request Entity Too Large" se produit car Nginx bloque les fichiers trop volumineux par défaut (limite par défaut : 1 Mo).

## Solution

### 1. Modifier la configuration Nginx

Sur le serveur de production, vous devez modifier le fichier de configuration Nginx pour augmenter la limite de taille des uploads.

#### Localisation du fichier de configuration
Le fichier se trouve généralement dans :
- `/etc/nginx/sites-available/votre-site` ou
- `/etc/nginx/nginx.conf`

#### Ajouter/modifier la directive `client_max_body_size`

Dans le bloc `server` ou `http` de votre configuration Nginx, ajoutez :

```nginx
server {
    # ... autres configurations ...
    
    # Augmenter la limite de taille des uploads à 10 Mo (ou plus selon vos besoins)
    client_max_body_size 10M;
    
    # ... autres configurations ...
}
```

### 2. Redémarrer Nginx

Après modification, testez la configuration puis redémarrez Nginx :

```bash
# Tester la configuration
sudo nginx -t

# Si le test est OK, recharger Nginx
sudo systemctl reload nginx
# ou
sudo service nginx reload
```

### 3. Vérification

Après redémarrage, les uploads jusqu'à 10 Mo devraient fonctionner.

## Notes

- La limite actuelle dans Django est fixée à **5 Mo** par fichier
- La limite Nginx doit être supérieure ou égale à la limite Django
- Pour des fichiers plus volumineux, augmentez les deux limites de manière cohérente

