from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_token_from_requests(username, password):
    options = Options()
    options.binary_location = "/usr/bin/chromium"  # Chemin de Chromium

    # Ajout d'options pour éviter les erreurs de session
    options.add_argument("--headless")  # Mode sans interface graphique
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-software-rasterizer")  
    options.add_argument("--window-size=1920x1080")  
    options.add_argument("--remote-debugging-port=9222")  # Debugging port pour éviter conflits de session

    service = Service("/usr/bin/chromedriver")  # Chemin de ChromeDriver

    seleniumwire_options = {
        'disable_encoding': True,
        'verify_ssl': False  # Ignorer les erreurs SSL si besoin
    }

    driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)

    token = None  # Initialisation du token
    try:
        driver.get("https://cas.utc.fr/cas/login")
        time.sleep(2)

        # Remplir les informations de connexion
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(3)
        
        # Vérification des erreurs d'authentification
        try:
            error_element = driver.find_element(By.ID, "error_general")
            if error_element.is_displayed():
                print("Erreur de connexion : Identifiants incorrects.")
                return None  # Retourne None en cas d'erreur de connexion
        except:
            pass  # Aucun message d'erreur trouvé, on continue

        driver.get("https://ngapplis.utc.fr/dossieretu/")
        time.sleep(5)

        # Récupération du token
        for request in driver.requests:
            if request.method == "GET" and "webservices.utc.fr/api/v1/etudiant/mineurs" in request.url:
                token = request.headers.get("Authorization")
                if token:
                    break

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        driver.quit()

    return token


if __name__ == "__main__":
    # Ajoute ici des valeurs de test si nécessaire
    username = "ton_identifiant"
    password = "ton_mot_de_passe"
    token = get_token_from_requests(username, password)
    print(f"Token récupéré : {token}")
