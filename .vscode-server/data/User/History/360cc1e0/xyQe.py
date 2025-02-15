import subprocess
from gpiozero import LED
import time
import socket

# Définir les LEDs sur les GPIOs 20, 26 et 16
led_system_on = LED(20)
led_ip_configured = LED(26)
led_docker_active = LED(16)

def check_ip_address():
    """Vérifie si une adresse IP est configurée sur la machine."""
    try:
        # Essayer de se connecter à un serveur DNS bien connu (Google DNS)
        socket.create_connection(("8.8.8.8", 53), 2)
        return True
    except OSError:
        return False

def check_docker_status():
    """Vérifie si le service Docker est actif."""
    command = "systemctl is-active docker"
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return output == "active"
    except subprocess.CalledProcessError:
        return False

while True:
    # Allume la LED système (elle sera toujours allumée si le script tourne)
    led_system_on.on()

    # Vérifie si une adresse IP est configurée
    ip_configured = check_ip_address()
    if ip_configured:
        led_ip_configured.on()
    else:
        led_ip_configured.off()

    # Vérifie si le service Docker est actif
    docker_active = check_docker_status()
    if docker_active:
        led_docker_active.on()
    else:
        led_docker_active.off()

    time.sleep(5)  # Modifier la fréquence de vérification
