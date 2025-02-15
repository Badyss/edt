import psycopg2

def get_database_size():
    try:
        # Établir la connexion à la base de données
        conn = psycopg2.connect(
            dbname='stripe-example',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        # Créer un curseur
        cursor = conn.cursor()
        # Exécuter la requête pour obtenir la taille de la base de données
        cursor.execute("\d;")
	#cursor.execute("SELECT pg_size_pretty(pg_database_size('stripe-example'));")
        # Récupérer le résultat
        size = cursor.fetchone()[0]
        # Afficher la taille
        print(f"La taille de la base de données est : {size}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

get_database_size()
