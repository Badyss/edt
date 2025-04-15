const express = require('express');
const router = express.Router();
const registerController = require('../controllers/registerController');


router.get('/login', (req, res) => { res.render('login'); });  
router.get('/register', registerController.afficherFormulaire);
router.post('/candidate_registration', registerController.inscrireCandidat);
router.post('/recruiter_registration', registerController.inscrireRecruteur);
router.post('/login', registerController.login);

module.exports = router;
