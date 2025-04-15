const express = require('express');
const router = express.Router();
const dashboardController = require('../controllers/dashboardController');

router.get('/dashboard', (req, res) => { res.render('dashboard');});
router.get('/entreprises', dashboardController.getAllEntreprises);
router.get('/recruteurs', dashboardController.getAllRecruteurs);
router.get('/Users', dashboardController.getAllUsers);
router.post('/deluser', dashboardController.deleteUserByEmail);
router.post('/setadmin', dashboardController.setadminUserByEmail);
router.post('/validerRecruteur', dashboardController.validerRecruteur );
router.post('/validerEntreprise', dashboardController.validerEntreprise );
router.post('/supprimerEntreprise', dashboardController.supprimerEntreprise );

module.exports = router;
