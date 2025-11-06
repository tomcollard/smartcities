# Micro sur A0
# LED RGB (NeoPixel) sur D18

from machine import ADC, Pin
import neopixel
import urandom
from time import ticks_ms, ticks_diff, sleep_ms

# init matériel
micro = ADC(26)                  # A0 -> ADC26
led = neopixel.NeoPixel(Pin(18), 1)  # D18 -> 1 LED

SEUIL_SON = 20000                # niveau à partir duquel on dit "y a du son"

# pour le bonus BPM
derniere_detection = ticks_ms()
liste_bpm = []
debut_minute = ticks_ms()

def couleur_aleatoire():
    # couleur random mais pas noire
    r = urandom.getrandbits(8)
    v = urandom.getrandbits(8)
    b = urandom.getrandbits(8)
    if r < 40 and v < 40 and b < 40:
        r = 255
    led[0] = (r, v, b)
    led.write()

def lire_son():
    # valeur brute 0..65535
    return micro.read_u16()

def main():
    global derniere_detection, liste_bpm, debut_minute

    while True:
        val = lire_son()

        # détection d'un pic
        if val > SEUIL_SON:
            now = ticks_ms()
            ecart = ticks_diff(now, derniere_detection)

            # anti double-détection
            if ecart > 200:
                couleur_aleatoire()

                # BPM instantané
                bpm = int(60000 / ecart)
                if 40 < bpm < 220:
                    liste_bpm.append(bpm)

                derniere_detection = now

        # toutes les 60 s -> log BPM moyen
        now = ticks_ms()
        if ticks_diff(now, debut_minute) >= 60000:
            if liste_bpm:
                moyenne = sum(liste_bpm) / len(liste_bpm)
                try:
                    with open("bpm_log.txt", "a") as f:
                        f.write("BPM moyen : {:.1f}\n".format(moyenne))
                except:
                    pass
            liste_bpm = []
            debut_minute = now

        sleep_ms(20)

# démarrage
main()
