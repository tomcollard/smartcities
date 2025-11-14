import network, ntptime, time
from machine import Pin, PWM

# Wi-Fi 
WIFI_SSID = "FRITZ!Box 7530 CD"
WIFI_PWD  = "91603772275184296859"

# bouton sur D20
# câblé entre GP20 et GND
bouton = Pin(20, Pin.IN, Pin.PULL_UP)
DELAI_REBOND = 300 #30 ms
INTERVAL_DOUBLE = 500     # temps entre 2 clics pour détecter un double clic
dernier_appui = 0
clic_compte = 0

# fuseaux horaires 
FUSEAUX = [1, 2, 0]   # +1 (hiver BE), +2 (été), UTC
index_fuseau = 0

# mode heure
mode_24h = False  # False = 12h, True = 24h

# servo moteur
servo = PWM(Pin(16))
servo.freq(50)

def angle_vers_duty(angle):
    us = 500 + (2000 * angle / 180)
    return int(us * 65535 / 20000)

def definir_angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    servo.duty_u16(angle_vers_duty(angle))

def connecter_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion", end="")
        wlan.connect(SSID, PASSWORD)
        for _ in range(40):
            if wlan.isconnected():
                break
            print(".", end="")
            time.sleep(0.5)
    if wlan.isconnected():
        print("\nConnecté IP :", wlan.ifconfig()[0])
        return True
    else:
        print("\nImpossible de se connecter.")
        return False

def sync_ntp():
    try:
        ntptime.host = "pool.ntp.org"
        ntptime.settime()
        print("Heure synchronisée (UTC) !")
    except:
        print("Erreur NTP, je garde l'heure interne.")

def bouton_action():
    """
    Gère les clics :
    - 1 clic → changement de fuseau
    - double clic → mode 12h/24h
    """
    global dernier_appui, clic_compte, index_fuseau, mode_24h

    if bouton.value() == 0:  # appui
        maintenant = time.ticks_ms()
        if time.ticks_diff(maintenant, dernier_appui) > DELAI_REBOND:
            clic_compte += 1
            dernier_appui = maintenant

    # après un petit délai, on décide si c'était simple ou double clic
    if clic_compte > 0 and time.ticks_diff(time.ticks_ms(), dernier_appui) > INTERVAL_DOUBLE:
        if clic_compte == 1:
            # simple clic → changer fuseau
            index_fuseau = (index_fuseau + 1) % len(FUSEAUX)
            print("→ Fuseau sélectionné :", FUSEAUX[index_fuseau])
        elif clic_compte == 2:
            # double clic → changer mode
            mode_24h = not mode_24h
            if mode_24h:
                print("→ Mode 24 h activé")
            else:
                print("→ Mode 12 h activé")
        clic_compte = 0

def main():
    global index_fuseau, mode_24h

    wifi_ok = connecter_wifi()
    if wifi_ok:
        sync_ntp()

    while True:
        bouton_action()  # surveille les clics

        # lire l'heure UTC
        t = time.localtime()
        an, mo, jr, h, mi, s, _, _ = t

        # appliquer le fuseau choisi
        ts = time.mktime((an, mo, jr, h, mi, s, 0, 0))
        ts += FUSEAUX[index_fuseau] * 3600
        t_loc = time.localtime(ts)

        heure = t_loc[3]
        minute = t_loc[4]
        seconde = t_loc[5]

        # calcul de l’angle du servo selon le mode
        if mode_24h:
            # 0h -> 0°, 12h -> 90°, 24h -> 180°
            angle = int(heure * 180 / 24)
        else:
            # mode 12h : 0° à 180° sur 12 h
            heure_12 = heure % 12
            angle = int(heure_12 * 180 / 12)

        definir_angle(angle)

        print(
            "Heure locale : %02d:%02d:%02d" % (heure, minute, seconde),
            "| Fuseau =", FUSEAUX[index_fuseau],
            "| Mode =", "24h" if mode_24h else "12h",
            "| Angle =", angle, "°"
        )

        time.sleep(0.2)  # rafraîchissement fluide

main()