from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time

def get_token_from_requests(username, password):
    options = Options()
    options.add_argument('--headless')  # Mode headless pour ne pas ouvrir l'interface graphique
    options.add_argument('--disable-gpu')  # Désactiver l'accélération matérielle GPU
    options.add_argument('--no-sandbox')  # Désactiver le sandbox pour éviter certains problèmes sur Linux
    options.add_argument('--disable-software-rasterizer')  # Désactiver le rendu logiciel
    options.add_argument('--window-size=1920x1080')  # Définir la taille de la fenêtre (nécessaire en headless)

    seleniumwire_options = {
        'disable_encoding': True,
        'verify_ssl': False  # Ignorer les erreurs SSL si elles se produisent
    }

    driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)

    try:
        driver.get("https://cas.utc.fr/cas/login")

        # Remplir les informations de connexion
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)  # Remplacez par votre identifiant
        password_input.send_keys(password)  # Remplacez par votre mot de passe
        password_input.send_keys(Keys.RETURN)

        time.sleep(3)  
        try:
            error_element = driver.find_element(By.ID, "error_general")
            if error_element.is_displayed():
                return False  # Retourne False si l'erreur est présente
        except:
            pass
        driver.get("https://ngapplis.utc.fr/dossieretu/")
        time.sleep(5)

        # Récupérer le token
        token = None
        for request in driver.requests:
            if request.method == "GET" and "webservices.utc.fr/api/v1/etudiant/mineurs" in request.url:
                token = request.headers.get("Authorization")
                if token:
                    break
        
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        driver.quit()

    return token if token else None


if __name__ == "__main__":
    token = get_token_from_requests()