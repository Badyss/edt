const client = require('../config/database');

exports.creerCandidat = async ({ prenom, nom, email, telephone, mot_de_passe }) => {
  await client.query("BEGIN");
  await client.query(
    "INSERT INTO Utilisateurs (email, prenom, nom, mot_de_passe, telephone) VALUES ($1, $2, $3, $4, $5)",
    [email, prenom, nom, mot_de_passe, telephone]
  );
  await client.query("INSERT INTO Candidats (email) VALUES ($1)", [email]);
  await client.query("COMMIT");
};

exports.creerRecruteur = async ({ prenom, nom, email, telephone, mot_de_passe, siren, nom_complet, secteur, adresse, ville }) => {
  await client.query("BEGIN");
  await client.query(
    "INSERT INTO Utilisateurs (email, prenom, nom, mot_de_passe, telephone) VALUES ($1, $2, $3, $4, $5)",
    [email, prenom, nom, mot_de_passe, telephone]
  );
  await client.query(
    "INSERT INTO Entreprises (siren, nom_complet, type, adresse, ville) VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING",
    [siren, nom_complet, secteur, adresse, ville]
  );
  await client.query(
    "INSERT INTO Recruteurs (email, entreprise, statut) VALUES ($1, $2, 'en attente')",
    [email, siren]
  );
  await client.query("COMMIT");
};

exports.seconnecter = async (email, password) => {
  try {
    const result = await client.query('SELECT * FROM Utilisateurs WHERE email = $1', [email]);

    if (result.rowCount === 0) {
      return null;  
    }

    const user = result.rows[0];

    if (user.mot_de_passe !== password) {
      return null;  
    }

    return user;

  } catch (err) {
    console.error('Erreur lors de la connexion :', err.stack);
    throw new Error("Erreur lors de la connexion");
  }
};