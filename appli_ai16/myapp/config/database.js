// config/database.js
const { Client } = require('pg');

const client = new Client({
  user: 'postgres',
  host: '192.168.1.153',
  database: 'stripe-example',
  password: 'postgres',
  port: 5432,
});

client.connect()
  .then(() => console.log('Connecté à la base de données'))
  .catch(err => {
    console.error('Erreur de connexion à la base de données', err.stack);
    process.exit(1); // Arrêter le processus en cas d'erreur de connexion
  });

module.exports = client;
