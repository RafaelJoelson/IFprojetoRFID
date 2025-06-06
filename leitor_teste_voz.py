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
# NOVA VERSÃO PARA DIAGNÓSTICO
def falar(texto):
    """Gera o áudio a partir do texto e o reproduz."""
    print("1. Entrando na função 'falar'. Tentando gerar áudio...")
    try:
        if not texto or not texto.strip():
            print("ERRO: O texto para falar está vazio. Abortando.")
            return

        tts = gTTS(text=texto, lang='pt-br')
        print(f"2. Objeto gTTS criado. Tentando salvar o arquivo 'frase.mp3'...")
        
        tts.save("frase.mp3")
        print("3. Arquivo 'frase.mp3' salvo com sucesso!")

        pygame.mixer.music.load("frase.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            continue
            
        print("4. Áudio reproduzido.")
        os.remove("frase.mp3")
        print("5. Arquivo temporário removido.")

    except Exception as e:
        print("\n!!!!!!!!!! ERRO CRÍTICO AO GERAR/TOCAR O ÁUDIO !!!!!!!!!!")
        print(f"A EXCEÇÃO FOI: {e}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

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
            time.sleep(5) # Pausa para evitar repetições imediatas

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEncerrando o programa...")
finally:
    GPIO.cleanup()
    pygame.quit()