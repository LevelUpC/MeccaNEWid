import tkinter as tk
import serial
import time
import pygame

# --- Configuration de la communication série ---
# Remplacez 'COM3' par le port correspondant à votre Arduino
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Temps pour permettre à l'Arduino de se réinitialiser
except serial.SerialException as e:
    print("Erreur lors de l'ouverture du port série :", e)
    exit()

# --- Initialisation de Pygame pour la manette ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Aucune manette détectée. Connectez une manette PS4 et réessayez.")
    exit()

# On utilise la première manette détectée
joystick = pygame.joystick.Joystick(0)
joystick.init()

# --- Fonction pour lire la manette et envoyer les positions ---
def controler_br():
    # Traiter les événements Pygame (obligatoire pour mettre à jour l'état de la manette)
    for event in pygame.event.get():
        pass

    # Récupération des valeurs des axes.
    # Par exemple, on utilise l'axe 0 pour le servo1 et l'axe 1 pour le servo2.
    # Les axes retournent une valeur entre -1 et 1.
    axis0 = joystick.get_axis(0)  # Axe horizontal du joystick gauche par exemple
    axis1 = joystick.get_axis(1)  # Axe vertical du joystick gauche par exemple

    # Conversion de la plage -1 à 1 en position d'angle 0 à 180 degrés.
    pos1 = int((axis0 + 1) * 90)  # -1 -> 0°, +1 -> 180°
    pos2 = int((axis1 + 1) * 90)

    # Construction de la commande à envoyer
    command = f"{pos1} {pos2}\n"
    try:
        arduino.write(command.encode())
    except Exception as e:
        print("Erreur lors de l'envoi sur le port série :", e)

    # Affiche les positions dans la console pour debug
    print(f"Envoi : Servo1 = {pos1}, Servo2 = {pos2}")

    # Replanifier l'actualisation après 100 ms
    root.after(100, controler_br)

# --- Création de l'interface Tkinter ---
root = tk.Tk()
root.title("Contrôle du bras du robot")

label_info = tk.Label(root, text="Utilisez la manette PS4 pour contrôler le bras du robot.", font=("Helvetica", 12))
label_info.pack(pady=10, padx=10)

# Bouton pour quitter proprement l'application
bouton_quitter = tk.Button(root, text="Quitter", command=root.destroy, font=("Helvetica", 12))
bouton_quitter.pack(pady=10)

# Démarrer la boucle de contrôle de la manette
root.after(100, controler_br)
root.mainloop()

# Fermeture du port série à la sortie
arduino.close()
pygame.quit()
