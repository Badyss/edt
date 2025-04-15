const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

// Import des routes
const registerRoutes = require('./routes/registerRoutes');
const offersRoutes = require('./routes/offerRoutes');
const dashboardRoutes = require('./routes/dashboardRoutes');

const app = express();

app.use(bodyParser.json());
app.use(cors({
  origin: 'https://ai16.badyss.dev',
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  allowedHeaders: 'Content-Type,Authorization',
}));

// Moteur de vue pour afficher les pages HTML avec EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


app.get('/', (req, res) => {res.render('index');});  //page garde
app.use('/', registerRoutes); //page authentification
app.use('/', offersRoutes); //Page des offres
app.use('/', dashboardRoutes); //Page dashboard


const port = 8300;
app.listen(port, () => {
  console.log(`Serveur lancé sur http://localhost:${port}`);
});

