# IFprojetoRFID

Arduino e Acessibilidade

# Objetivo: Leitura Simultânea de Dois Leitores RFID (MFRC522) no Raspberry Pi

Este projeto permite conectar **dois sensores RFID MFRC522** ao Raspberry Pi utilizando a comunicação **SPI**, com leitura simultânea. Ideal para testes de autenticação dupla ou projetos que exigem múltiplos pontos de leitura.

---

## 🧰 Materiais necessários

- 1 Raspberry Pi (com Raspbian instalado)
- 2 leitores RFID MFRC522
- 2 tags/cartões RFID

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
sudo apt install python3-pip git
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
MFRC522_1.py
MFRC522_2.py
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

## 🧪 Dica de teste

Para diagnosticar problemas no circuito:

- Teste **cada leitor individualmente**, comentando o outro no código.
- Verifique todas as conexões físicas.
- Use o comando `pinout` para confirmar os GPIOs.

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