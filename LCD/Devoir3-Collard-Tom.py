from machine import Pin, ADC, PWM, I2C
import time
import math

# Configuration des broches
potentiometre = ADC(26)
led = PWM(Pin(15))
led.freq(1000)
buzzer = Pin(16, Pin.OUT)

# Capteur de température (DHT11/DHT22)
from dht import DHT11
capteur_temperature = DHT11(Pin(28))

# Écran LCD I2C - Version corrigée
class LCD_I2C:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        time.sleep_ms(50)
        self.envoyer_sequence_initialisation()
    
    def envoyer_commande(self, cmd):
        """Envoyer une commande au LCD"""
        high_nibble = cmd & 0xF0
        low_nibble = (cmd << 4) & 0xF0
        # Envoyer high nibble
        self.i2c.writeto(self.addr, bytes([high_nibble | 0x04 | 0x08]))
        self.i2c.writeto(self.addr, bytes([high_nibble | 0x00 | 0x08]))
        time.sleep_us(50)
        # Envoyer low nibble
        self.i2c.writeto(self.addr, bytes([low_nibble | 0x04 | 0x08]))
        self.i2c.writeto(self.addr, bytes([low_nibble | 0x00 | 0x08]))
        time.sleep_us(50)
    
    def envoyer_caractere(self, char):
        """Envoyer un caractère au LCD"""
        high_nibble = char & 0xF0
        low_nibble = (char << 4) & 0xF0
        # Envoyer high nibble
        self.i2c.writeto(self.addr, bytes([high_nibble | 0x05 | 0x08]))
        self.i2c.writeto(self.addr, bytes([high_nibble | 0x01 | 0x08]))
        time.sleep_us(50)
        # Envoyer low nibble
        self.i2c.writeto(self.addr, bytes([low_nibble | 0x05 | 0x08]))
        self.i2c.writeto(self.addr, bytes([low_nibble | 0x01 | 0x08]))
        time.sleep_us(50)
    
    def envoyer_sequence_initialisation(self):
        """Séquence d'initialisation du LCD"""
        init_commands = [
            0x33, 0x32,  # Initialisation 4 bits
            0x28,        # Mode 4 bits, 2 lignes
            0x0C,        # Display ON, cursor OFF
            0x06,        # Entry mode
            0x01         # Clear display
        ]
        for cmd in init_commands:
            self.envoyer_commande(cmd)
            time.sleep_ms(5)
        time.sleep_ms(50)
    
    def effacer(self):
        self.envoyer_commande(0x01)
        time.sleep_ms(2)
    
    def afficher_texte(self, ligne, texte):
        """Afficher du texte sur une ligne spécifique"""
        # Positionner le curseur
        if ligne == 0:
            self.envoyer_commande(0x80)
        else:
            self.envoyer_commande(0xC0)
        
        # Tronquer ou compléter avec espaces pour 16 caractères
        texte_formatte = texte[:16]  # Tronquer si trop long
        while len(texte_formatte) < 16:  # Compléter avec espaces si trop court
            texte_formatte += " "
        
        # Écrire le texte
        for caractere in texte_formatte:
            self.envoyer_caractere(ord(caractere))

# Détection et initialisation LCD
def initialiser_lcd():
    """Initialiser le LCD avec détection d'adresse"""
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    
    # Scanner les adresses I2C
    peripheriques = i2c.scan()
    print("Périphériques I2C trouvés:", [hex(addr) for addr in peripheriques])
    
    if not peripheriques:
        print("Aucun périphérique I2C trouvé! Vérifiez les branchements.")
        return None
    
    # Utiliser la première adresse trouvée
    addr = peripheriques[0]
    print(f"Utilisation du LCD à l'adresse: {hex(addr)}")
    
    return LCD_I2C(i2c, addr)

# Initialisation LCD
ecran_lcd = initialiser_lcd()

# Variables globales
alarme_active = False
alarme_clignotante = False
dernier_changement_alarme = 0

def lire_temperature_consigne():
    valeur_pot = potentiometre.read_u16()
    temperature = 15 + (valeur_pot / 65535) * 20
    return round(temperature, 1)

def lire_temperature_ambiante():
    try:
        capteur_temperature.measure()
        temp = capteur_temperature.temperature()
        print(f"Température lue: {temp}°C")
        return temp
    except Exception as e:
        print(f"Erreur capteur: {e}")
        return 25.0

def controler_led(difference):
    if difference > 3:
        # Clignotement rapide pour alarme
        led.duty_u16(30000)
        time.sleep(0.1)
        led.duty_u16(0)
        time.sleep(0.1)
    elif difference > 0:
        # Battement progressif à 0.5 Hz
        for i in range(0, 1000, 50):
            valeur_pwm = int(math.sin(i/100) * 20000 + 20000)
            led.duty_u16(max(0, min(65535, valeur_pwm)))
            time.sleep(0.05)
    else:
        # LED éteinte
        led.duty_u16(0)

def controler_buzzer(difference):
    if difference > 3:
        buzzer.on()
    else:
        buzzer.off()

def mettre_a_jour_affichage(temp_consigne, temp_ambiante, difference):
    global alarme_active, alarme_clignotante, dernier_changement_alarme
    
    if ecran_lcd is None:
        return  # Pas d'affichage si LCD non initialisé
    
    # Ligne 1: Set temperature
    texte_ligne1 = f"Set: {temp_consigne}C"
    ecran_lcd.afficher_texte(0, texte_ligne1)
    
    # Ligne 2: Ambient temperature ou ALARM
    temps_actuel = time.ticks_ms()
    if difference > 3:
        alarme_active = True
        if time.ticks_diff(temps_actuel, dernier_changement_alarme) > 500:
            alarme_clignotante = not alarme_clignotante
            dernier_changement_alarme = temps_actuel
        
        if alarme_clignotante:
            ecran_lcd.afficher_texte(1, "Ambient: ALARM!")
        else:
            texte_ligne2 = f"Ambient: {temp_ambiante}C"
            ecran_lcd.afficher_texte(1, texte_ligne2)
    else:
        alarme_active = False
        alarme_clignotante = False
        texte_ligne2 = f"Ambient: {temp_ambiante}C"
        ecran_lcd.afficher_texte(1, texte_ligne2)

def boucle_principale():
    print("Système de contrôle de température démarré")
    
    # Message d'attente si pas de LCD
    if ecran_lcd is None:
        print("ATTENTION: LCD non détecté, vérifiez les connexions I2C")
    else:
        # Test d'affichage initial
        ecran_lcd.afficher_texte(0, "System Ready!")
        ecran_lcd.afficher_texte(1, "Waiting...")
        time.sleep(2)
    
    while True:
        temperature_consigne = lire_temperature_consigne()
        temperature_ambiante = lire_temperature_ambiante()
        difference_temperature = temperature_ambiante - temperature_consigne
        
        print(f"Set: {temperature_consigne}C, Ambient: {temperature_ambiante}C, Diff: {difference_temperature}C")
        
        controler_led(difference_temperature)
        controler_buzzer(difference_temperature)
        mettre_a_jour_affichage(temperature_consigne, temperature_ambiante, difference_temperature)
        
        time.sleep(1)

if __name__ == "__main__":
    boucle_principale()