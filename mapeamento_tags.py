
import json
import time
import RPi.GPIO as GPIO
import MFRC522_1 as RFID

# Funções auxiliares para manipulação de arquivos JSON
def carregar_tags(nome_arquivo):
    """Carrega as tags de um arquivo JSON. Se o arquivo não existir, retorna um dicionário vazio."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_tags(nome_arquivo, tags):
    """Salva as tags em um arquivo JSON com formatação."""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(tags, f, indent=4, ensure_ascii=False)

def ler_uid_da_tag():
    """Inicializa o leitor RFID, lê o UID de uma tag e o retorna como string."""
    leitor = RFID.MFRC522()
    print("\nAproxime a tag do leitor 1...")
    uid_lido = None
    while uid_lido is None:
        status, _ = leitor.MFRC522_Request(leitor.PICC_REQIDL)
        if status == leitor.MI_OK:
            status, uid = leitor.MFRC522_Anticoll()
            if status == leitor.MI_OK:
                uid_lido = str(uid)
                print(f"Tag detectada! UID: {uid_lido}")
        time.sleep(0.5)
    return uid_lido

# Função principal para gerenciar o mapeamento
def gerenciar_mapeamento():
    """Menu principal para cadastro de tags de ação e pronome."""
    while True:
        print("\n--- Gerenciamento de Tags RFID ---")
        print("1. Cadastrar Tag de Ação")
        print("2. Cadastrar Tag de Pronome")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome_arquivo = 'acoes.json'
            tipo_tag = 'ação'
        elif escolha == '2':
            nome_arquivo = 'pronomes.json'
            tipo_tag = 'pronome'
        elif escolha == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue

        # Lógica de cadastro
        nome = input(f"Digite o nome do(a) {tipo_tag}: ")
        uid = ler_uid_da_tag()
        
        tags = carregar_tags(nome_arquivo)

        if uid in tags:
            print(f"A tag {uid} já está cadastrada como '{tags[uid]}'.")
            resposta = input("Deseja atualizar o nome? (s/n): ").lower()
            if resposta == 's':
                tags[uid] = nome
                salvar_tags(nome_arquivo, tags)
                print(f"Tag atualizada com sucesso para '{nome}'!")
            else:
                print("Atualização cancelada.")
        else:
            tags[uid] = nome
            salvar_tags(nome_arquivo, tags)
            print(f"Tag '{nome}' cadastrada com sucesso!")

if __name__ == "__main__":
    try:
        gerenciar_mapeamento()
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
    finally:
        GPIO.cleanup()
