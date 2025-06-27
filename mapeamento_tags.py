# --- Mapeamento de UIDs para Palavras ---
# Associe o UID da sua tag RFID a uma palavra.
# O UID é a lista de números que aparece no terminal quando você escaneia a tag.
# Exemplo: se o UID da tag "Eu" for [56, 163, 15, 23, 89], o dicionário ficará:
# pronomes = {"[56, 163, 15, 23, 89]": "Eu"}

pronomes = {
    "[134, 188, 115, 248, 177]": "Eu",
    "[196, 212, 82, 115, 49]": "Você",
    "UID_DA_TAG_ELE": "Ele"
    # Adicione mais pronomes e seus UIDs aqui
}

acoes = {
    "[192, 118, 11, 63, 130]": "comer",
    "[246, 116, 127, 248, 5]": "tomar banho",
    "UID_DA_TAG_BRINCAR": "brincar"
    # Adicione mais ações e seus UIDs aqui
}