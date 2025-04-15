const userModel = require('../models/userModel');

exports.afficherFormulaire = (req, res) => {
  res.render('register');
};

exports.inscrireCandidat = async (req, res) => {
  try {
    await userModel.creerCandidat(req.body);
    res.send("Candidat inscrit !");
  } catch (err) {
    res.status(500).send("Erreur lors de l'inscription");
  }
};

exports.inscrireRecruteur = async (req, res) => {
  try {
    await userModel.creerRecruteur(req.body);
    res.send("Recruteur inscrit !");
  } catch (err) {
    res.status(500).send("Erreur lorsnon  de l'inscription");
  }
};

exports.login = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await userModel.seconnecter(email, password);

    if (!user) {
      return res.status(400).json({ success: false, message: "Identifiants incorrects" });
    }

    res.json({ success: true, message: "Connexion réussie" });

  } catch (err) {
    console.error('Erreur lors de la connexion :', err.stack);
    res.status(500).json({ success: false, message: "Erreur serveur" });
  }
};
