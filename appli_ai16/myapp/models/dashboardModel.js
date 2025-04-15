const client = require('../config/database'); 


exports.getAllEntreprises = async () => {
  try {
    const query = `
      SELECT 
          e.siren, 
          e.nom_complet, 
          e.type, 
          e.adresse, 
          e.ville, 
          e.statut,
          COUNT(r.email) AS nombre_recruteurs
      FROM Entreprises e
      LEFT JOIN Recruteurs r ON e.siren = r.entreprise
      GROUP BY e.siren, e.nom_complet, e.type, e.adresse, e.ville, e.statut;
    `;
    const result = await client.query(query);
    return result.rows;
  } catch (err) {
    console.error('Erreur lors de la récupération des entreprises :', err.stack);
    throw new Error("Erreur lors de la récupération des entreprises");
  }
};

exports.getAllRecruteurs = async () => {
  const query = `
    SELECT 
        r.email, 
        u.prenom, 
        u.nom, 
        u.telephone, 
        u.date_creation, 
        r.statut,
        e.nom_complet AS entreprise_nom,
        e.siren AS entreprise_siren
    FROM Recruteurs r
    JOIN Utilisateurs u ON r.email = u.email
    JOIN Entreprises e ON r.entreprise = e.siren;
  `;
  try {
    const result = await client.query(query);
    return result.rows;
  } catch (err) {
    console.error('Erreur dans getAllRecruteurs :', err.stack);
    throw new Error("Erreur lors de la récupération des recruteurs");
  }
};

// 🔹 Requête pour les utilisateurs
exports.getAllUsers = async () => {
  const query = `
    SELECT 
        Utilisateurs.email, 
        Utilisateurs.prenom, 
        Utilisateurs.nom, 
        Utilisateurs.telephone, 
        Utilisateurs.date_creation,
        CASE
            WHEN Administrateurs.email IS NOT NULL THEN 'Administrateur'
            WHEN Candidats.email IS NOT NULL THEN 'Candidat'
            WHEN Recruteurs.email IS NOT NULL THEN 'Recruteur'
            ELSE 'Inconnu'
        END AS user_type
    FROM Utilisateurs
    LEFT JOIN Candidats ON Candidats.email = Utilisateurs.email
    LEFT JOIN Administrateurs ON Administrateurs.email = Utilisateurs.email
    LEFT JOIN Recruteurs ON Recruteurs.email = Utilisateurs.email
    ORDER BY Utilisateurs.date_creation DESC;
  `;
  try {
    const result = await client.query(query);
    return result.rows;
  } catch (err) {
    console.error('Erreur dans getAllUsers :', err.stack);
    throw new Error("Erreur lors de la récupération des utilisateurs");
  }
};

exports.deleteUserByEmail = async (email) => {
  try {
    // Démarrer la transaction
    await client.query('BEGIN');

    // Exécuter chaque requête de suppression séparément
    await client.query('DELETE FROM Candidats WHERE email = $1;', [email]);
    await client.query('DELETE FROM Recruteurs WHERE email = $1;', [email]);
    await client.query('DELETE FROM Administrateurs WHERE email = $1;', [email]);
    await client.query('DELETE FROM Utilisateurs WHERE email = $1;', [email]);

    // Committer la transaction si tout s'est bien passé
    await client.query('COMMIT');

    return { success: true, message: `Utilisateur avec l'email ${email} supprimé.` };
  } catch (err) {
    // Annuler la transaction en cas d'erreur
    await client.query('ROLLBACK');
    console.error('Erreur dans deleteUserByEmail :', err.stack);
    throw new Error("Erreur lors de la suppression de l'utilisateur");
  }
};

exports.setadminUserByEmail = async (email) => {
  try {
    
    await client.query('INSERT INTO Administrateurs (email) VALUES ($1);', [email]);

    return { success: true, message: `Utilisateur avec l'email ${email} administrauter.` };
  } catch (err) {
    console.error('Erreur dans deleteUserByEmail :', err.stack);
    throw new Error("Erreur lors de la suppression de l'utilisateur");
  }
};


exports.accepterRecruteur = async ({ email }) => {
  await client.query("BEGIN");

  const result = await client.query(
    "SELECT entreprise FROM Recruteurs WHERE email = $1",
    [email]
  );

  if (result.rowCount === 0) {
    throw new Error("Aucun recruteur trouvé avec cet email");
  }

  const siren = result.rows[0].entreprise;

  await client.query(
    "UPDATE Recruteurs SET statut = 'accepté' WHERE email = $1",
    [email]
  );
  await client.query(
    "UPDATE Entreprises SET statut = 'accepté' WHERE siren = $1",
    [siren]
  );

  await client.query("COMMIT");
};

exports.validerEntreprise = async ({ siren }) => {
  try {
    await client.query("BEGIN");

    await client.query(
      "UPDATE Entreprises SET statut = 'accepté' WHERE siren = $1",
      [siren]
    );

    await client.query("COMMIT");
    return { message: 'Entreprise acceptée avec succès.' };
  } catch (error) {
    await client.query("ROLLBACK");
    console.error('Erreur validerEntreprise:', error);
    throw error; 
  }
};

exports.supprimerEntreprise = async ({ siren }) => {
  try {
    await client.query("BEGIN");

    await client.query(
      "DELETE FROM Entreprises WHERE siren = $1", 
      [siren]
    );

    await client.query("COMMIT");
    return { message: 'Entreprise supprimée avec succès.' };
  } catch (error) {
    await client.query("ROLLBACK");
    console.error('Erreur supprimerEntreprise:', error);
    throw error;
  }
};
