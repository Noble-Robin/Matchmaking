# Projet Serveur Matchmaking

### Première étapes : Création de la VM serveur 

Visualistation du reseaux 
![alt text](img/image.png)

Notre réseaux est composé d'un serveur et de 2 pc. Le serveur est utilisé pour faire communiquer les 2 pc entre eux et les 2 pc sont des pc de joueurs sur lesquel le jeux est installé et qui joue l'un contre l'autre sachant que le serveur et chaque pc peuvnent etre sur des réseaux différents.

1 serveur :
    - crée la communication entre les pc

2 pc joueur :
    - jeux installer dessus


# Installation et configuration d'une VM serveur pour le matchmaking

## 1️⃣ Prérequis

Avant de commencer, assure-toi d'avoir :

- Une VM sous **Linux (Ubuntu/Debian recommandé)**
- **Node.js** installé (v16+ recommandé)
- **Ngrok** pour exposer le serveur sur Internet

## 2️⃣ Installation de Node.js et npm

Connecte-toi à ta VM et installe Node.js :

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl ufw
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
```

Configurer le pare-feu :

```bash
sudo ufw allow 22  # SSH
sudo ufw allow 80  # HTTP
sudo ufw allow 443 # HTTPS
sudo ufw allow 3000  # WebSocket
sudo ufw enable
```

Vérifie l'installation :

```bash
node -v  # Affiche la version de Node.js
npm -v   # Affiche la version de npm
```

---

## 3️⃣ Installation du serveur Express + Socket.IO

### 📌 Création du projet

```bash
mkdir matchmaking-server && cd matchmaking-server
npm init -y
```

### 📌 Installation des dépendances

```bash
npm install express socket.io
```

### 📌 Création du fichier `server.js`

```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

let queue = [];

io.on('connection', (socket) => {
    console.log('Un joueur connecté:', socket.id);

    socket.on('join_queue', () => {
        queue.push(socket);
        console.log(`Joueur ${socket.id} ajouté à la file d'attente. Taille de la file: ${queue.length}`);

        if (queue.length >= 2) {
            const player1 = queue.shift();
            const player2 = queue.shift();

            const colors = ['white', 'black'];
            const player1Color = colors[Math.floor(Math.random() * colors.length)];
            const player2Color = player1Color === 'white' ? 'black' : 'white';

            player1.emit('match_found', { opponent: player2.id, color: player1Color });
            player2.emit('match_found', { opponent: player1.id, color: player2Color });

            console.log(`Match trouvé entre ${player1.id} (couleur: ${player1Color}) et ${player2.id} (couleur: ${player2Color})`);
        }
    });

    socket.on('disconnect', () => {
        queue = queue.filter(player => player.id !== socket.id);
        console.log(`Joueur ${socket.id} déconnecté et retiré de la file.`);
    });
});

server.listen(3000, "0.0.0.0", () => console.log("Serveur en écoute sur le port 3000"));
```

---

## 4️⃣ Lancement du serveur

```bash
node server.js
```

Tu devrais voir :

```
Serveur en écoute sur le port 3000
```

Si tu veux que le serveur tourne en arrière-plan :

```bash
npm install -g pm2
pm2 start server.js --name matchmaking
pm2 save
```

---

## 5️⃣ Exposer le serveur avec Ngrok

### 📌 Installation de Ngrok

```bash
snap install ngrok
```

### 📌 Connexion à Ngrok

Connecte toi à ton à ton compte Ngrok et rajoute ton token d'authentification :

```bash
ngrok config add-authtoken $AUTHTOKEN
```

(Ton authtoken est disponible sur [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken))

### 📌 Exposition du serveur

```bash
ngrok http 3000
```

Ngrok fournira une URL comme :

```
Forwarding https://random-subdomain.ngrok.io -> http://localhost:3000
```

Utilise cette URL pour connecter tes clients.

---
