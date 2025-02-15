import psycopg2
from psycopg2 import sql, OperationalError

# Paramètres pour la connexion en tant qu'admin
DB_ADMIN = "postgres"
DB_ADMIN_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

# Informations pour la nouvelle base de données et utilisateur
NEW_DB_NAME = "client_21db46"
NEW_USER = "client_21user46"
NEW_PASSWORD = "securepassword123"


def create_database_and_user():
    try:
        # Connexion à PostgreSQL en tant qu'admin
        connection = psycopg2.connect(
            dbname="postgres",
            user=DB_ADMIN,
            password=DB_ADMIN_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        connection.autocommit = True  # Activation de l'autocommit pour CREATE DATABASE

        cursor = connection.cursor()

        # Création de la base de données
        cursor.execute(sql.SQL(f"CREATE DATABASE {NEW_DB_NAME};"))
        print(f"✅ Base de données '{NEW_DB_NAME}' créée avec succès.")

        # Création du nouvel utilisateur avec mot de passe
        cursor.execute(sql.SQL(f"CREATE USER {NEW_USER} WITH ENCRYPTED PASSWORD %s;"), [NEW_PASSWORD])
        print(f"✅ Utilisateur '{NEW_USER}' créé avec succès.")

        # Attribution de tous les privilèges nécessaires
        cursor.execute(sql.SQL(f"""
            GRANT ALL ON DATABASE {NEW_DB_NAME} TO {NEW_USER};
	    GRANT USAGE, CREATE ON SCHEMA public TO {NEW_USER};
            GRANT ALL ON SCHEMA public TO {NEW_USER};
	    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {NEW_USER};
        """))

        print(f"✅ Tous les privilèges nécessaires accordés à '{NEW_USER}' sur '{NEW_DB_NAME}'.")

        # Fermeture des connexions
        cursor.close()
        connection.close()

    except OperationalError as e:
        print(f"❌ Erreur : {e}")


def setup_quota_management():
    try:
        # Connexion à la base de données nouvellement créée
        connection = psycopg2.connect(
            dbname=NEW_DB_NAME,
            user=DB_ADMIN,
            password=DB_ADMIN_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Création de la table `db_quota`
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS db_quota (
                user_id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                used_size_mb NUMERIC DEFAULT 0,
                max_size_mb NUMERIC NOT NULL
            );
        """)
        print("✅ Table 'db_quota' créée.")

        # Insérer un quota de 500MB pour `client_user`
        cursor.execute("""
            INSERT INTO db_quota (username, max_size_mb)
            VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (NEW_USER, 500))
        print(f"✅ Quota de 500MB ajouté pour '{NEW_USER}'.")

        # Création de la fonction `check_db_quota()` (en cas de besoin)
        cursor.execute("""
            CREATE OR REPLACE FUNCTION check_db_quota()
            RETURNS void AS $$
            DECLARE
                user_used_size NUMERIC;
                user_max_size NUMERIC;
            BEGIN
                -- Obtenir la taille utilisée de la base de données
                SELECT SUM(pg_total_relation_size(oid)) / 1024 / 1024
                INTO user_used_size
                FROM pg_class
                WHERE relkind = 'r';

                -- Obtenir la taille maximale autorisée
                SELECT max_size_mb INTO user_max_size
                FROM db_quota
                WHERE username = 'client_user';

                -- Vérifier si l'utilisateur dépasse le quota
                IF user_used_size > user_max_size THEN
                    EXECUTE 'REVOKE INSERT ON ALL TABLES IN SCHEMA public FROM client_user';
                ELSE
                    EXECUTE 'GRANT INSERT ON ALL TABLES IN SCHEMA public TO client_user';
                END IF;

                -- Mettre à jour la table db_quota avec la taille actuelle
                UPDATE db_quota SET used_size_mb = user_used_size WHERE username = 'client_user';
            END;
            $$ LANGUAGE plpgsql;
        """)
        print("✅ Fonction 'check_db_quota()' créée.")

        # Empêcher `client_user` de modifier la table `db_quota`
        cursor.execute(sql.SQL(f"REVOKE ALL ON db_quota FROM {NEW_USER};"))
        cursor.execute(sql.SQL(f"GRANT SELECT ON db_quota TO {NEW_USER};"))
        print(f"✅ '{NEW_USER}' ne peut que lire 'db_quota'.")

        # Fermeture de la connexion
        cursor.close()
        connection.close()

    except OperationalError as e:
        print(f"❌ Erreur lors de la configuration du quota : {e}")

def test_new_user_connection():
    try:
        # Connexion avec le nouvel utilisateur
        connection = psycopg2.connect(
            dbname=NEW_DB_NAME,
            user=NEW_USER,
            password=NEW_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Vérifier la connexion
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"✅ Connexion réussie avec {NEW_USER} à {NEW_DB_NAME}, version : {db_version}")

        # Vérifier le quota actuel
        cursor.execute("SELECT * FROM db_quota WHERE username = %s;", (NEW_USER,))
        quota_info = cursor.fetchone()
        print(f"📊 Quota actuel de '{NEW_USER}' : {quota_info}")

        # Fermeture
        cursor.close()
        connection.close()

    except OperationalError as e:
        print(f"❌ Erreur de connexion avec {NEW_USER} : {e}")

if __name__ == "__main__":
    create_database_and_user()
    setup_quota_management()
    test_new_user_connection()
