import tkinter as tk
from tkinter import colorchooser
import serial
import time

# Configuration de la communication série avec l'Arduino
# Remplacez 'COM3' par le port série correspondant sur votre machine (ex: '/dev/ttyACM0' sous Linux)
try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
    # Petite pause pour laisser le temps à l'Arduino de se réinitialiser
    time.sleep(2)
except serial.SerialException as e:
    print("Erreur lors de l'ouverture du port série :", e)
    exit()

def choisir_couleur():
    # Ouvre la boîte de dialogue de sélection de couleur
    couleur, hex_color = colorchooser.askcolor()
    if couleur:
        # Extraction des composantes RGB (arrondies en entiers)
        r, g, b = [int(c) for c in couleur]
        print(f"Couleur choisie : R={r} G={g} B={b}")
        try:
            # Envoi des valeurs RGB sous forme de 3 octets
            arduino.write(bytes([r, g, b]))
        except Exception as e:
            print("Erreur lors de l'envoi sur le port série :", e)

# Configuration de l'interface Tkinter
root = tk.Tk()
root.title("Contrôle des yeux du robot")

bouton = tk.Button(root, text='Choisir une couleur', command=choisir_couleur, font=("Helvetica", 14))
bouton.pack(pady=20, padx=20)

root.mainloop()
