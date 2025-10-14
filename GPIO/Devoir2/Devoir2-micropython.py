from machine import Pin, PWM, ADC
from time import sleep

# --- Broches ---
BUZZER_PIN = 13
POT_PIN = 26

bz = PWM(Pin(BUZZER_PIN))
pot = ADC(POT_PIN)

# --- Notes --- chat gpt 
NOTES = { #calacul a partir de f=440×2**n/12
    "REST": 0,
    "E5": 659, "B4": 494, "C5": 523, "D5": 587, "G4": 392,
    "F5": 698, "A4": 440, "G5": 784, "C5": 523, "A5": 880
}

# --- Mélodie Tetris simplifiée --- chat gpt note
MELODY = [
    ("E5", 1), ("B4", 0.5), ("C5", 0.5), ("D5", 1), ("C5", 0.5), ("B4", 0.5),
    ("A4", 1), ("A4", 0.5), ("C5", 0.5), ("E5", 1), ("D5", 0.5), ("C5", 0.5),
    ("B4", 1), ("B4", 0.5), ("C5", 0.5), ("D5", 1), ("E5", 1),
    ("C5", 1), ("A4", 1), ("A4", 1)
]

TEMPO_BPM = 140  #baptement par minute 
BEAT = 60 / TEMPO_BPM #la duree 

# --- Fonction de lecture ---
def play(note, beats=1):

    freq = NOTES[note]
    #le reset 
    if freq == 0:
        bz.duty_u16(0)
        sleep(BEAT * beats)
        return

    bz.freq(freq) #lire la note
    for _ in range(int(BEAT * beats * 100)):  #si  le potentiometre tourne 
        volume = pot.read_u16()  # lecture du potentiometre (0–65535)
        bz.duty_u16(volume)      # volume en  focntion du potentiometre
        sleep(0.01)

# --- Boucle principale infinie---
try:
    while True:
        for note, beats in MELODY:
            play(note, beats)
        sleep(1)
        
except KeyboardInterrupt:
    bz.duty_u16(0)
    bz.deinit()
