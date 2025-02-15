import psycopg2
from psycopg2 import sql, OperationalError

# Paramètres de connexion pour l'administrateur
DB_ADMIN = "postgres"
DB_ADMIN_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

# Informations pour le nouvel utilisateur et la base
NEW_USER = "client21"
NEW_PASSWORD = "securepassword123"
NEW_DB_NAME = "client21"

def create_user_and_database():
    try:
        # Connexion en tant qu'administrateur sur la base "postgres"
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_ADMIN,
            password=DB_ADMIN_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True  # Nécessaire pour créer des bases et des utilisateurs
        cur = conn.cursor()
        
        # Création du nouvel utilisateur (si inexistant)
        cur.execute(
            sql.SQL(
                "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = %s) THEN "
                "CREATE USER {} WITH ENCRYPTED PASSWORD %s; END IF; END $$;"
            ).format(sql.Identifier(NEW_USER)),
            [NEW_USER, NEW_PASSWORD]
        )
        print(f"✅ Utilisateur '{NEW_USER}' créé (ou déjà existant).")
        
        # Création de la base de données en assignant NEW_USER comme propriétaire
        cur.execute(
            sql.SQL("CREATE DATABASE {} WITH OWNER {}")
                .format(sql.Identifier(NEW_DB_NAME), sql.Identifier(NEW_USER))
        )
        print(f"✅ Base de données '{NEW_DB_NAME}' créée avec '{NEW_USER}' comme propriétaire.")
        
        cur.close()
        conn.close()
    except OperationalError as e:
        print(f"❌ Erreur dans create_user_and_database: {e}")

def create_table_in_public():
    try:
        # Connexion en tant que NEW_USER à la nouvelle base
        conn = psycopg2.connect(
            dbname=NEW_DB_NAME,
            user=NEW_USER,
            password=NEW_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        # Définir explicitement le search_path sur le schéma public (par défaut)
        cur.execute("SET search_path TO public;")
        cur.execute("SHOW search_path;")
        print("✅ Search_path dans la session :", cur.fetchone())
        
        # Suppression de la table si elle existe déjà
        cur.execute("DROP TABLE IF EXISTS public.test_table;")
        
        # Création d'une table dans le schéma public
        cur.execute("""
            CREATE TABLE public.test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            );
        """)
        print("✅ Table 'test_table' créée avec succès dans le schéma public.")
        
        conn.commit()
        cur.close()
        conn.close()
    except OperationalError as e:
        print(f"❌ Erreur dans create_table_in_public: {e}")

def test_new_user_connection():
    try:
        conn = psycopg2.connect(
            dbname=NEW_DB_NAME,
            user=NEW_USER,
            password=NEW_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"✅ Connexion réussie avec '{NEW_USER}' à '{NEW_DB_NAME}', version : {db_version}")
        cur.close()
        conn.close()
    except OperationalError as e:
        print(f"❌ Erreur de connexion avec '{NEW_USER}' : {e}")

if __name__ == "__main__":
    create_user_and_database()
    create_table_in_public()
    test_new_user_connection()
