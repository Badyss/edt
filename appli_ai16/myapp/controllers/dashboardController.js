const dashboardModel = require('../models/dashboardModel');

exports.getAllEntreprises = async (req, res) => {
  try {
    const entreprises = await dashboardModel.getAllEntreprises();
    res.json(entreprises);
  } catch (err) {
    console.error("Erreur dans le controller :", err);
    res.status(500).send("Erreur lors de la récupération des entreprises");
  }
};

exports.getAllRecruteurs = async (req, res) => {
  try {
    const recruteurs = await dashboardModel.getAllRecruteurs();
    res.json(recruteurs);
  } catch (err) {
    console.error('Erreur dans le contrôleur getAllRecruteurs :', err.message);
    res.status(500).send('Erreur lors de la récupération des recruteurs');
  }
};

exports.getAllUsers = async (req, res) => {
  try {
    const users = await dashboardModel.getAllUsers();
    res.json(users);
  } catch (err) {
    console.error('Erreur dans le contrôleur getAllUsers :', err.message);
    res.status(500).send('Erreur lors de la récupération des utilisateurs');
  }
};

exports.deleteUserByEmail = async (req, res) => {
  const { email } = req.body;  // On récupère l'email de la requête POST
  if (!email) {
    return res.status(400).json({ error: 'Email requis' });
  }

  try {
    const result = await dashboardModel.deleteUserByEmail(email);
    res.json(result);
  } catch (err) {
    console.error('Erreur dans le contrôleur deleteUserByEmail :', err.message);
    res.status(500).send('Erreur lors de la suppression de l\'utilisateur');
  }
};

exports.setadminUserByEmail = async (req, res) => {
  const { email } = req.body;  // On récupère l'email de la requête POST
  if (!email) {
    return res.status(400).json({ error: 'Email requis' });
  }

  try {
    const result = await dashboardModel.setadminUserByEmail(email);
    res.json(result);
  } catch (err) {
    console.error('Erreur dans le contrôleur setadminUserByEmail :', err.message);
    res.status(500).send('Erreur lors de la mise à jour de l\'utilisateur');
  }
};

exports.validerRecruteur = async (req, res) => {
  try {
    await dashboardModel.accepterRecruteur(req.body);
    res.json("Recruteur accepté !");
  } catch (err) {
    console.error(err);
    res.status(500).send("Erreur lors de la validation du recruteur");
  }
};

exports.validerEntreprise = async (req, res) => {
  try {
    await dashboardModel.validerEntreprise(req.body);
    res.json({ message: 'Entreprise accepté !' });
  } catch (err) {
    console.error(err);
    res.status(500).send("Erreur lors de la validation de l'Entreprise");
  }
};

exports.supprimerEntreprise = async (req, res) => {
  try {
    await dashboardModel.supprimerEntreprise(req.body);
    res.json({ message: 'Entreprise supprimée !' });
  } catch (err) {
    console.error(err);
    res.status(500).send("Erreur lors de la suppression de l'Entreprise");
  }
};

