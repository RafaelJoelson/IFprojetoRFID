# --- Mapeamento de UIDs para Palavras ---
# Associe o UID da sua tag RFID a uma palavra.
# O UID é a lista de números que aparece no terminal quando você escaneia a tag.
# Exemplo: se o UID da tag "Eu" for [56, 163, 15, 23, 89], o dicionário ficará:
# pronomes = {"[56, 163, 15, 23, 89]": "Eu"}

pronomes = {
    "[134, 188, 115, 248, 177]": "Eu",
    "UID_DA_TAG_VOCE": "Você",
    "UID_DA_TAG_ELE": "Ele"
    # Adicione mais pronomes e seus UIDs aqui
}

acoes = {
    "[192, 118, 11, 63, 130]": "quero comer",
    "UID_DA_TAG_BANHO": "quero tomar banho",
    "UID_DA_TAG_BRINCAR": "quero brincar"
    # Adicione mais ações e seus UIDs aqui
}