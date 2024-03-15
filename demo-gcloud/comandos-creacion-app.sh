#Comandos para la creacion de una app node js usando Express

sudo systemctl stop nginx
mkdir app-nodejs
cd app-nodejs

sudo apt install npm

npm init -y

npm install express

cat << 'EOF' > app.js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hola Mundo desde la maquina virtual');
});

app.listen(80, () => {
    console.log('Servidor escuchando en el puerto 80');
});
EOF
#prueba2