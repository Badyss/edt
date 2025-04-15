const userModel = require('../models/offerModel');

exports.sectors = async (req, res) => {
  try {
    const sectors = await userModel.sectors(); 
    res.json(sectors); // on retourne les secteurs au format JSON
  } catch (err) {
    console.error("Erreur lors de la récupération des secteurs :", err);
    res.status(500).send("Erreur lors de la récupération des secteurs");
  }
};

exports.offersnumber = async (req, res) => {
  try {
    const offersnumber = await userModel.offersnumber(); 
    res.json({ total_count: offersnumber });
  } catch (err) {
    console.error("Erreur lors de la récupération des secteurs :", err);
    res.status(500).send("Erreur lors de la récupération des secteurs");
  }
};

exports.offers = async (req, res) => {
  try {
    const { page = 1, minSalary, maxSalary, sector, name } = req.query;
    const offers = await userModel.offers({ page, minSalary, maxSalary, sector, name });
    res.json(offers);
  } catch (err) {
    console.error("Erreur lors de la récupération des offres :", err);
    res.status(500).send("Erreur lors de la récupération des offres");
  }
};

exports.getOfferById = async (req, res) => {
  try {
    const offerId = req.params.id; // Récupère l'ID de l'offre depuis les paramètres de la route
    const offer = await userModel.getOfferById(offerId); // Appelle la méthode du modèle
    if (!offer) {
      return res.status(404).json({ error: "Offre non trouvée" });
    }
    res.json(offer); // Retourne l'offre au format JSON
  } catch (err) {
    console.error("Erreur lors de la récupération de l'offre :", err);
    res.status(500).send("Erreur lors de la récupération de l'offre");
  }
};
