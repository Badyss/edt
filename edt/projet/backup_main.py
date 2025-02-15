import requests
import json
from get_token import get_token_from_requests

def fetch_emploi_du_temps(username, password):
    token = get_token_from_requests(username, password)

    if not token :
        return False

    url_emploi_du_temps = "https://webservices.utc.fr/api/v1/edt/getedt"

    headers = {
        "Authorization": token,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url_emploi_du_temps, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            json_data = json.dumps(response_data)  
            json_data = json_data.replace("'", '"')  

            return json_data 
        else:
            return {"error": f"Erreur HTTP {response.status_code}"}
    except requests.RequestException as e:
        return {"error": f"Une erreur s'est produite : {str(e)}"}
