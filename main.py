import RPi.GPIO as GPIO
import MFRC522_1 as RFID1
import MFRC522_2 as RFID2
import time
import os

# --- Importa os mapeamentos do arquivo externo ---
from mapeamento_tags import pronomes, acoes

# --- Inicialização ---
reader1 = RFID1.MFRC522()
reader2 = RFID2.MFRC522()

pronome_detectado = None
acao_detectada = None

print("Aproxime as etiquetas RFID para formar a frase...")

## Função para Falar com eSpeak

def falar(texto):
    """Gera o áudio a partir do texto usando o comando do sistema eSpeak."""
    print("1. Entrando na função 'falar'. Tentando gerar áudio com eSpeak via sistema...")
    try:
        if not texto or not texto.strip():
            print("ERRO: O texto para falar está vazio. Abortando.")
            return
        # Chama o eSpeak diretamente pelo sistema, idioma pt-br
        comando = f'espeak -v pt-br "{texto}" -s 120'  # Ajuste a velocidade se necessário
        os.system(comando)
        print(f"2. eSpeak sintetizou e reproduziu: '{texto}'")
        print("3. Áudio reproduzido.")
    except Exception as e:
        print("\n!!!!!!!!!! ERRO CRÍTICO AO GERAR/TOCAR O ÁUDIO COM eSPEAK !!!!!!!!!!")
        print(f"A EXCEÇÃO FOI: {e}")
        print("Verifique se o eSpeak está instalado corretamente (sudo apt-get install espeak).")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
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
                else:
                    print(f"Pronome não mapeado para UID: {uid_str1}")

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
                else:
                    print(f"Ação não mapeada para UID: {uid_str2}")

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