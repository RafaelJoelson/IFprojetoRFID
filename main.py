import RPi.GPIO as GPIO
import MFRC522_1 as RFID1
import MFRC522_2 as RFID2
import time
import os
import json
import subprocess # Adicionamos o subprocess para o aquecimento

# --- Constantes ---
ESPEAK_PATH = '/usr/bin/espeak'
# --- Funções Auxiliares ---

def carregar_mapeamento(nome_arquivo):
    """Carrega um mapeamento de um arquivo JSON."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de mapeamento '{nome_arquivo}' não encontrado. Um dicionário vazio será usado.")
        return {}

def falar(texto):
    """Gera o áudio a partir do texto usando o comando do sistema eSpeak."""
    print("1. Entrando na função 'falar'. Tentando gerar áudio com eSpeak...")
    try:
        if not texto or not texto.strip():
            print("ERRO: O texto para falar está vazio. Abortando.")
            return

        # Chamada direta e limpa. Não é preciso mais o os.system para evitar problemas
        comando = [
            ESPEAK_PATH, 
            '-v', 'pt-br', 
            '-s', '120',  # Velocidade
            '-a', '150',  # Amplitude
            '-g', '10',   # Gap entre palavras
            texto
        ]
        
        # Usamos subprocess.run no lugar de os.system, que é mais robusto
        # e garante que o caminho absoluto seja usado corretamente.
        subprocess.run(comando, check=True)
        
        print(f"2. eSpeak sintetizou e reproduziu: '{texto}'")
        print("3. Áudio reproduzido.")
    except subprocess.CalledProcessError as e:
        print("\n!!!!!!!!!! ERRO CRÍTICO AO GERAR/TOCAR O ÁUDIO COM eSPEAK !!!!!!!!!!")
        print(f"A EXCEÇÃO FOI: {e}")
        print("Verifique se o eSpeak está instalado corretamente (sudo apt-get install espeak).")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

# conjugações do verbo "querer" para diferentes pronomes
conjugacao_querer = {
    "Eu": "quero",
    "Você": "quer",
    "Ele": "quer",
    "Ela": "quer",
    "Nós": "queremos",
    "Vocês": "querem",
    "Eles": "querem",
    "Elas": "querem"
}

# --- Carregamento de Mapeamentos ---

pronomes = carregar_mapeamento('pronomes.json')
acoes = carregar_mapeamento('acoes.json')

# --- Inicialização ---
reader1 = RFID1.MFRC522()
reader2 = RFID2.MFRC522()

pronome_detectado = None
acao_detectada = None

# --- Sinal de Início com Aquecimento do Áudio ---
print("Sistema iniciando... Executando aquecimento do driver de áudio.")

try:
    # Comando de AQUICIMENTO (Silencioso: -q). Ele só força o ALSA a carregar.
    print("Iniciando aquecimento do eSpeak...")
    # Usamos o timeout de 1 segundo para garantir que não trave, caso algo dê errado
    subprocess.run([ESPEAK_PATH, '-q', ' '], check=False, timeout=1) 
    print("Aquecimento concluído. Aguardando 10 segundos pelo sinal sonoro.")
except Exception as e:
    print(f"AVISO: Falha no aquecimento do eSpeak. O áudio inicial pode ter engasgos. {e}")
    
time.sleep(10) # Pausa de 10 segundos
falar("Olá, estou pronto para formar frases.") # O driver já deve estar ativo agora!

print("Aproxime as etiquetas RFID para formar a frase...")

# --- Loop Principal ---
try:
    while True:
        # Leitor 1 (Pronomes)
        # ... (seu código de leitura RFID) ...
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
        # ... (seu código de leitura RFID) ...
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
            # Busca a conjugação do verbo "querer" para o pronome detectado
            verbo_conjugado = conjugacao_querer.get(pronome_detectado)

            if verbo_conjugado:
                # Forma a frase no novo formato: "Pronome + querer(conjugado) + ação"
                frase_completa = f"{pronome_detectado} {verbo_conjugado} {acao_detectada}"
            else:
                # Fallback para o formato antigo se a conjugação não for encontrada
                print(f"AVISO: Conjugação para o pronome '{pronome_detectado}' não encontrada. Usando formato antigo.")
                frase_completa = f"{pronome_detectado} {acao_detectada}"

            print(f"\n--- FRASE FORMADA --- \n'{frase_completa}'\n---------------------\n")
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