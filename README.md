# IFprojetoRFID

Arduino, Acessibilidade e Comunicação Alternativa

# Objetivo: Brinquedo Interativo para Comunicação de Crianças Autistas

Este projeto permite conectar **dois sensores RFID MFRC522** ao Raspberry Pi utilizando a comunicação **SPI**, com leitura simultânea. O sistema foi adaptado para funcionar como um brinquedo educativo, ajudando crianças autistas a se comunicarem por meio da montagem de frases simples com cartões RFID. Ao aproximar os cartões, o sistema fala a frase formada, promovendo inclusão e aprendizado.

---

## 🧰 Materiais necessários

- 1 Raspberry Pi (com Raspbian instalado)
- 2 leitores RFID MFRC522
- 2 ou mais tags/cartões RFID (quanto mais, melhor!)
- Caixinha de som ou fone de ouvido para saída de áudio

---

## 🔌 Conexões dos sensores

| Pino do MFRC522 | Leitor 1 (CE0)   | Leitor 2 (CE1)   | Função              |
|------------------|------------------|------------------|---------------------|
| **SDA**          | GPIO8  (CE0)     | GPIO7  (CE1)     | Chip Select (SPI)   |
| **SCK**          | GPIO11           | GPIO11           | Clock SPI           |
| **MOSI**         | GPIO10           | GPIO10           | SPI MOSI            |
| **MISO**         | GPIO9            | GPIO9            | SPI MISO            |
| **RST**          | GPIO25           | GPIO24           | Reset (diferente!)  |
| **GND**          | GND              | GND              | Terra               |
| **3.3V**         | 3.3V             | 3.3V             | Alimentação         |

> ⚠️ Os pinos **RST** devem ir para **GPIOs diferentes**. E os leitores devem compartilhar SPI, mas ter CS (SDA) separados: um em CE0 e o outro em CE1.

---

## ⚙️ Habilitar SPI no Raspberry Pi

No terminal:

```bash
sudo raspi-config
```

- Vá em **Interface Options**
- Escolha **SPI**
- Ative a opção
- Reinicie o Raspberry Pi

---

## 📦 Instalar bibliotecas necessárias

No terminal, execute:

```bash
sudo apt update
sudo apt install python3-pip git espeak
pip3 install spidev RPi.GPIO
```

---

## 📁 Preparar arquivos do projeto

Clone o repositório (ou copie os arquivos manualmente):

```bash
git clone <link-do-repositorio>
cd <pasta-do-projeto>
```

Você deve ter os seguintes arquivos:

```
leitor_duplo.py
leitor_teste_voz.py
MFRC522_1.py
MFRC522_2.py
mapeamento_tags.py
```

Cada versão da biblioteca `MFRC522` foi adaptada para funcionar com um leitor diferente:

- `MFRC522_1.py` → usa **CE0 (GPIO8)**
- `MFRC522_2.py` → usa **CE1 (GPIO7)**

---

## ▶️ Executar o código

No terminal:

```bash
python3 leitor_duplo.py
```

Se os dois leitores estiverem corretamente conectados e os cartões forem aproximados, você verá:

```
Leitor 1: UID: [...]
Leitor 2: UID: [...]
RFID 1 e RFID 2 foram reconhecidos!
```

---

## 🗣️ Como funciona a fala automática

Ao aproximar um cartão RFID de cada leitor, o sistema identifica o pronome e a ação, monta a frase e fala automaticamente usando o eSpeak (voz offline). Exemplo:

```
Leitor 1 (Pronome) detectou o UID: [134, 188, 115, 248, 177]
Pronome reconhecido: Eu
Leitor 2 (Ação) detectou o UID: [192, 118, 11, 63, 130]
Ação reconhecida: quero comer
Frase formada: 'Eu quero comer'
```

---

## 🏷️ Como cadastrar novas tags

1. Aproximar a tag do leitor e anotar o UID exibido no terminal.
2. Editar o arquivo `mapeamento_tags.py` e adicionar o UID (com espaços, igual ao print) ao dicionário `pronomes` ou `acoes`.
3. Salvar o arquivo e reiniciar o programa.

Exemplo:
```python
pronomes = {
    "[134, 188, 115, 248, 177]": "Eu",
    "[X, Y, Z, ...]": "Você"
}
acoes = {
    "[192, 118, 11, 63, 130]": "quero comer"
}
```

---

## 💡 Dicas de uso e expansão

- Cole figuras ou símbolos nos cartões para reforço visual.
- Adicione LEDs ou sons para feedback positivo.
- Expanda o vocabulário com mais cartões e frases.
- Pais e terapeutas podem personalizar as frases conforme a necessidade da criança.
- O sistema pode ser adaptado para montar frases com mais de dois cartões (ex: pronome + ação + objeto).

---

## 🛡️ Segurança e acessibilidade

- Use caixas e peças resistentes, sem partes pequenas.
- Certifique-se de que o áudio está audível e o volume adequado.
- O sistema funciona totalmente offline.

---

## Comandos git dentro do repositório IFprojetoRFID

Para baixar atualizações
```
git pull origin main
```

Para enviar atualizações
```
git push origin main
```