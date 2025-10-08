from machine import Pin
from utime import sleep, ticks_ms, ticks_diff

# LED et bouton
led = Pin(15, Pin.OUT)
bouton = Pin(14, Pin.IN, Pin.PULL_DOWN)

# Variables
etat = 1              # 1 = lent, 2 = rapide, 3 = éteint
dernier_appui = 0     # pour l’anti-rebond

while True:
    # Verifie si le bouton est appuyé
    if bouton.value() == 1:
        if ticks_diff(ticks_ms(), dernier_appui) > 300:
            etat += 1
            if etat > 3:
                etat = 1
            dernier_appui = ticks_ms()
            print("etat :", etat)


        # attendre que le bouton soit relâché
        while bouton.value():
            sleep(0.05)

    # Gestion de la LED selon l’état
    if etat == 1:          #clignotement lent
        led.toggle()
        sleep(1.0)
    elif etat == 2:        #clignotement rapide
        led.toggle()
        sleep(0.25)
    else:                  #eteinte
        led.value(0)
        sleep(0.1)
