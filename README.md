# 🐍 Raspberry Pi Pico W – Projets MicroPython

## 🔧 Description générale
Ce dépôt contient différents projets réalisés avec le **Raspberry Pi Pico W** en **MicroPython**.  
Il sert de base pour expérimenter les **entrées/sorties GPIO**, les **capteurs**, les **afficheurs**, et les **connexions réseau**.

Chaque projet est organisé dans un sous-dossier avec son propre fichier `README.md`, contenant le code, les explications et les ressources nécessaires.

---

## 🧠 À propos du Raspberry Pi Pico W
Le **Raspberry Pi Pico W** est une carte microcontrôleur basée sur le **RP2040** (double cœur ARM Cortex-M0+).  
Elle dispose de **26 broches GPIO** programmables et d’un **module Wi-Fi** intégré.

Caractéristiques principales :
- Microcontrôleur : RP2040 – Dual-core ARM Cortex-M0+
- Fréquence : 133 MHz  
- Mémoire : 264 Ko
- - Stockage : 2 Mo de mémoire flash intégrée  
- Connectivité : Wi-Fi 2.4 GHz (puce Infineon CYW43439)  
- Interfaces : UART, SPI, I2C, ADC, PWM, USB  
- Alimentation : 1,8 V à 5,5 V  
- Programmation : via **MicroPython** ou **C/C++ SDK**

---

## 🧰 Environnement de travail

Les scripts sont développés en **MicroPython** à l’aide de :
- **Thonny IDE** (environnement recommandé pour débuter)
- **SourceTree / GitHub** pour le suivi de version
- **Raspberry Pi Pico W** connecté en USB (mode mass storage)
- **Terminal REPL** pour tester et exécuter le code directement

---

## 🖼️ Brochage du Raspberry Pi Pico W

![Brochage du Raspberry Pi Pico W](./images/pico_pinout.png)

*Cette image montre la correspondance des broches GPIO et leurs fonctions principales (UART, I2C, SPI, PWM, etc.).*

---

## 📁 Organisation du dépôt

Le dépôt est structuré en plusieurs répertoires thématiques, chacun contenant un fichier `README.md` explicatif et les ressources associées (code, datasheets, photos, explications, etc.) :

- **GPIO** : LED simple, bouton-poussoir, interruption  
- **AD-PWM** : lecture de potentiomètre, PWM (LED, musique, servo)  
- **LCD** : fonctions de la librairie, affichage de valeurs  
- **LED_neo** : utilisation des LEDs Neopixel, arc-en-ciel  
- **sensors** : température, humidité, luminosité, PIR  
- **network** : accès réseau via le RPi Pico W  

---

## 🔗 Liens vers les sous-répertoires

- [GPIO](./GPIO/README.md)
- [AD-PWM](./AD-PWM/README.md)
- [LCD](./LCD/README.md)
- [LED neo](./LED_neo/README.md)
- [sensors](./sensors/README.md)
- [network](./network/README.md)

---

## 📚 Ressources

Après chaque opération :
1. Cliquer sur **Commit** pour enregistrer les changements dans GitHub.  
2. Pour créer un nouveau répertoire :  
   - Se placer à la racine du projet  
   - Cliquer sur **Add File → Create new file**  
   - Nommer le fichier `NOM_DU_DOSSIER/README.md`

Exemple :  
`smartcities/GPIO/README.md` → crée le répertoire **GPIO** avec son fichier explicatif.

---

## ✍️ Exemple de lien interne
Pour faire un lien vers un sous-répertoire dans Markdown :  
`[GPIO](./GPIO/README.md)` → [GPIO](./GPIO/README.md)

---

## 🧩 Auteur et contexte
Ce dépôt s’inscrit dans le cadre du projet **SmartCities & IoT** à la **HEPL – Passerelle Ingénieur Industriel option Informatique**.  
Il regroupe des exercices et expériences réalisés en **MicroPython** sur **Raspberry Pi Pico W**, en lien avec les cours d’**électronique** et d’**IoT**.

---

### 🗓️ Dernière mise à jour
Octobre 2025

