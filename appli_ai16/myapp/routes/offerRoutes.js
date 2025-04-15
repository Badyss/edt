const express = require('express');
const router = express.Router();
const offersController = require('../controllers/offerController');

router.get('/sectors', offersController.sectors);
router.get('/Offersnumber', offersController.offersnumber);
router.get('/Offers', offersController.offers);
router.get('/Offer/:id', offersController.getOfferById);


module.exports = router;
