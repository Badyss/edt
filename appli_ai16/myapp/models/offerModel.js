const client = require('../config/database'); 

exports.sectors = async () => {
  try {
    const result = await client.query(
      "SELECT unnest(enum_range(NULL::domaine_offres_enum))::text;"
    );
    return result.rows;
  } catch (err) {
    console.error('Erreur lors de la récupération des secteurs :', err.stack);
    throw new Error("Erreur lors de la récupération des secteurs");
  }
};

exports.offersnumber = async () => {
  const query = `SELECT COUNT(*) AS total_count FROM Offres;`;

  try {
    const result = await client.query(query);
    return result.rows[0].total_count;
  } catch (err) {
    console.error('Erreur lors de la récupération du total des offres:', err);
    throw err;
  }
}

exports.offers = async ({ page, minSalary, maxSalary, sector, name }) => {
  const limit = 10; // Nombre d'offres par page
  const offset = (parseInt(page) - 1) * limit; // Calcul de l'offset en fonction de la page

  if (isNaN(page) || page <= 0) {
    throw new Error('Le paramètre "page" est requis et doit être un nombre positif.');
  }

  let query = `
    SELECT 
        o.*, fp.*, e.nom_complet
    FROM Offres o
    JOIN FichePoste fp
        ON o.fiche_poste_entreprise = fp.entreprise
        AND o.fiche_poste_titre = fp.titre
    JOIN Entreprises e
        ON fp.entreprise = e.siren
    WHERE 1=1
  `;

  const queryParams = [limit, offset];
  let paramCounter = 3; // On commence à 3 car les deux premiers paramètres sont déjà utilisés pour limit et offset

  // Application des filtres
  if (!isNaN(minSalary)) {
    query += ` AND fp.salaire_min >= $${paramCounter}`;
    queryParams.push(minSalary);
    paramCounter++;
  }

  if (!isNaN(maxSalary)) {
    query += ` AND fp.salaire_max <= $${paramCounter}`;
    queryParams.push(maxSalary);
    paramCounter++;
  }

  if (sector) {
    query += ` AND fp.secteur = $${paramCounter}`;
    queryParams.push(sector);
    paramCounter++;
  }

  if (name) {
    query += ` AND (e.nom_complet ILIKE $${paramCounter} OR fp.titre ILIKE $${paramCounter})`;
    queryParams.push(`%${name}%`);
    paramCounter++;
  }

  query += ` LIMIT $1 OFFSET $2`;

  try {
    const result = await client.query(query, queryParams);
    return result.rows;
  } catch (err) {
    console.error('Erreur lors de la récupération des offres:', err);
    throw new Error('Erreur serveur');
  }
};

exports.getOfferById = async (offerId) => {
  const query = `
    SELECT 
        * 
    FROM Offres o
    JOIN FichePoste fp
        ON o.fiche_poste_entreprise = fp.entreprise
        AND o.fiche_poste_titre = fp.titre
    JOIN Entreprises e
        ON fp.entreprise = e.siren
    WHERE o.id = $1;
  `;

  try {
    const result = await client.query(query, [offerId]); // Exécution de la requête avec l'ID passé en paramètre
    if (result.rows.length === 0) {
      return null; // Si aucune offre n'est trouvée, retourne null
    }
    return result.rows[0]; // Retourne la première ligne (l'offre)
  } catch (err) {
    console.error("Erreur lors de la récupération de l'offre :", err);
    throw err; // Lève l'erreur pour qu'elle puisse être capturée dans le contrôleur
  }
};
