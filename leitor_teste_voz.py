import RPi.GPIO as GPIO
import MFRC522_1 as RFID1
import MFRC522_2 as RFID2
import time
from gtts import gTTS
import os
import pygame

# --- Importa os mapeamentos do arquivo externo ---
from mapeamento_tags import pronomes, acoes

# --- Inicialização ---
reader1 = RFID1.MFRC522()
reader2 = RFID2.MFRC522()

pygame.mixer.init()

pronome_detectado = None
acao_detectada = None

print("Aproxime as etiquetas RFID para formar a frase...")

# --- Função para Falar ---
def falar(texto):
    """Gera o áudio a partir do texto e o reproduz."""
    try:
        tts = gTTS(text=texto, lang='pt-br')
        tts.save("frase.mp3")
        pygame.mixer.music.load("frase.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        os.remove("frase.mp3") # Remove o arquivo para não acumular
    except Exception as e:
        print(f"Ocorreu um erro ao tentar falar: {e}")

# --- Loop Principal ---
try:
    while True:
        # Leitor 1 (Pronomes)
        (status1, uid1) = reader1.MFRC522_Request(reader1.PICC_REQIDL)
        if status1 == reader1.MI_OK:
            (status1, uid1) = reader1.MFRC522_Anticoll()
            if status1 == reader1.MI_OK:
                uid_str1 = str(uid1)
                print(f"Leitor 1 (Pronome) detectou o UID: {uid_str1}")
                if uid_str1 in pronomes:
                    pronome_detectado = pronomes[uid_str1]
                    print(f"Pronome reconhecido: {pronome_detectado}")

        # Leitor 2 (Ações)
        (status2, uid2) = reader2.MFRC522_Request(reader2.PICC_REQIDL)
        if status2 == reader2.MI_OK:
            (status2, uid2) = reader2.MFRC522_Anticoll()
            if status2 == reader2.MI_OK:
                uid_str2 = str(uid2)
                print(f"Leitor 2 (Ação) detectou o UID: {uid_str2}")
                if uid_str2 in acoes:
                    acao_detectada = acoes[uid_str2]
                    print(f"Ação reconhecida: {acao_detectada}")

        # Se ambos foram detectados, forma a frase e fala
        if pronome_detectado and acao_detectada:
            frase_completa = f"{pronome_detectado} {acao_detectada}"
            print(f"Frase formada: '{frase_completa}'")
            falar(frase_completa)
            
            # Reseta as variáveis para a próxima leitura
            pronome_detectado = None
            acao_detectada = None
            time.sleep(2) # Pausa para evitar repetições imediatas

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEncerrando o programa...")
finally:
    GPIO.cleanup()
    pygame.quit()