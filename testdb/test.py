import psycopg2
from psycopg2 import OperationalError

# Paramètres pour la connexion
DB_NAME = "client2"
DB_USER = "client2"
DB_PASSWORD = "securepassword123"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    try:
        # Connexion à la base de données
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Connexion réussie à la base de données.")
        return connection
    except OperationalError as e:
        print(f"❌ Erreur de connexion : {e}")
        return None


def insert_data(connection):
    try:
        cursor = connection.cursor()

        # Création de la table data_table si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_table (
                id SERIAL PRIMARY KEY,
                data_value TEXT NOT NULL
            );
        """)
        print("✅ Table 'data_table' créée ou déjà existante.")

        # Insertion de plusieurs lignes dans data_table
        for i in range(1, 11):  # Insérer 10 lignes
            cursor.execute("INSERT INTO data_table (data_value) VALUES (%s);", (f"Data {i}",))
        print("✅ Données insérées dans 'data_table'.")

        # Valider les modifications
        connection.commit()

    except OperationalError as e:
        print(f"❌ Erreur lors de l'insertion des données : {e}")
    finally:
        cursor.close()


def read_db_quota(connection):
    try:
        cursor = connection.cursor()

        # Lecture des données dans la table db_quota
        cursor.execute("SELECT * FROM db_quota WHERE username = %s;", (DB_USER,))
        quota_info = cursor.fetchone()
        print(f"📊 Informations sur le quota : {quota_info}")

    except OperationalError as e:
        print(f"❌ Erreur lors de la lecture de db_quota : {e}")
    finally:
        cursor.close()


def main():
    # Connexion à la base de données
    connection = connect_to_db()
    
    if connection:
        # Insérer des données dans la table 'data_table'
        insert_data(connection)

        # Lire les informations de la table db_quota après insertion des données
        read_db_quota(connection)

        # Fermeture de la connexion
        connection.close()


if __name__ == "__main__":
    main()
