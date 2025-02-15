import requests
import json
from get_token import get_token_from_requests

def fetch_emploi_du_temps(username, password):
    # Récupérer le token
    token = get_token_from_requests(username, password)

    if not token:
        return False

    # URLs des deux API
    url_emploi_du_temps = "https://webservices.utc.fr/api/v1/edt/getedt"
    url_trombi_one = "https://webservices.utc.fr/api/v1/trombi/one"

    headers = {
        "Authorization": token,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    }

    try:
        response_emploi_du_temps = requests.get(url_emploi_du_temps, headers=headers)
        if response_emploi_du_temps.status_code == 200:
            emploi_du_temps_data = response_emploi_du_temps.json()
        else:
            emploi_du_temps_data = {}

        response_trombi_one = requests.get(url_trombi_one, headers=headers)
        if response_trombi_one.status_code == 200:
            trombi_one_data = response_trombi_one.json()
            specific_data = {
                "nomp": trombi_one_data.get("nomp", ""),
            }
        else:
            specific_data = {}

        # Combiner les deux réponses dans un seul dictionnaire
        combined_data = {
            "emploi_du_temps": emploi_du_temps_data,
            "specific_data": specific_data,
        }

        return json.dumps(combined_data)

    except requests.RequestException as e:
        return {"error": f"Une erreur s'est produite : {str(e)}"}

