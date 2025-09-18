# IFprojetoRFID: Brinquedo Interativo para Comunicação

Este projeto transforma um Raspberry Pi e leitores de RFID em um brinquedo educativo e interativo, projetado para auxiliar na comunicação de crianças no espectro autista. O sistema permite que a criança forme frases simples ("Eu quero brincar") aproximando cartões com figuras de dois leitores RFID. O sistema então vocaliza a frase formada, fornecendo feedback auditivo imediato.

---

## 🧰 Materiais Necessários

- 1 Raspberry Pi (qualquer modelo com 40 pinos GPIO)
- 2 leitores RFID MFRC522
- Tags ou cartões RFID variados
- Uma fonte de áudio (caixa de som ou fone de ouvido com conexão P2)

---

## 🔌 Conexões dos Sensores

Os dois leitores compartilham os pinos de SPI (SCK, MOSI, MISO), mas utilizam pinos de *Chip Select* (SDA/CS) e *Reset* (RST) diferentes.

| Pino do MFRC522 | Leitor 1 (Pronomes) | Leitor 2 (Ações) | Pino Físico (Exemplo) |
|-----------------|---------------------|------------------|-----------------------|
| **SDA (CS)**    | GPIO8 (SPI_CE0)     | GPIO7 (SPI_CE1)  | 24 / 26               |
| **SCK**         | GPIO11 (SPI_SCLK)   | GPIO11 (SPI_SCLK)| 23                    |
| **MOSI**        | GPIO10 (SPI_MOSI)   | GPIO10 (SPI_MOSI)| 19                    |
| **MISO**        | GPIO9 (SPI_MISO)    | GPIO9 (SPI_MISO) | 21                    |
| **RST**         | GPIO25              | GPIO24           | 22 / 18               |
| **GND**         | GND                 | GND              | Qualquer pino GND     |
| **3.3V**        | 3.3V                | 3.3V             | Qualquer pino 3.3V    |

> ⚠️ **Atenção:** É crucial que os pinos `RST` sejam diferentes e que cada leitor use um canal de Chip Select (CE0 e CE1) diferente para que o barramento SPI possa alternar entre eles.

---

## ⚙️ Configuração Inicial do Raspberry Pi

### 1. Habilitar a Interface SPI
No terminal, execute `sudo raspi-config`, vá em `Interface Options` -> `SPI` e selecione `Yes` para ativar. Reinicie o Raspberry Pi após a alteração.

### 2. Instalar Dependências
No terminal, execute os seguintes comandos para instalar as bibliotecas e ferramentas necessárias:

```bash
sudo apt update
sudo apt install python3-pip git espeak -y
pip3 install spidev RPi.GPIO
```

---

## 🚀 Como Usar o Projeto

O projeto é dividido em duas partes principais: cadastrar as tags e executar o programa de comunicação.

### 1. Cadastrando as Tags (Novo Sistema)

Para associar suas tags RFID a palavras (pronomes ou ações), utilize o script de gerenciamento interativo. Ele é mais fácil e seguro do que editar o código manualmente.

**Como executar:**

1.  Abra o terminal no seu Raspberry Pi.
2.  Navegue até a pasta do projeto: `cd /caminho/para/IFprojetoRFID`
3.  Execute o script de mapeamento:
    ```bash
    python3 mapeamento_tags.py
    ```
4.  Siga as instruções no menu para escolher entre cadastrar uma **ação** ou um **pronome**, digitar o nome e aproximar a tag do **leitor 1**.

Os mapeamentos serão salvos nos arquivos `acoes.json` e `pronomes.json`.

> #### ⚠️ **Resolvendo Erros de Permissão no Raspberry Pi**
> Ao executar o script de mapeamento pela primeira vez, você pode encontrar um `PermissionError`. Isso ocorre porque, por padrão, seu usuário pode não ter permissão para criar arquivos na pasta.
>
> - **Solução Rápida:** Execute o script com privilégios de administrador usando `sudo`.
>   ```bash
>   sudo python3 mapeamento_tags.py
>   ```
> - **Solução Recomendada (Permanente):** Torne seu usuário o "dono" da pasta do projeto. Execute este comando **uma vez** e você não precisará mais usar `sudo` para este projeto.
>   ```bash
>   # Substitua 'pi' pelo seu nome de usuário, se for diferente
>   sudo chown -R pi:pi .
>   ```

### 2. Executando o Programa Principal

Após cadastrar suas tags, execute o programa principal para iniciar a comunicação.

1.  No terminal, na pasta do projeto, execute:
    ```bash
    python3 main.py
    ```
2.  O programa irá carregar as tags dos arquivos `.json` e dirá: "Aproxime as etiquetas RFID para formar a frase...".
3.  Aproxime uma tag de pronome do **Leitor 1** e uma tag de ação do **Leitor 2**.
4.  O sistema formará a frase e a falará em voz alta.

**Exemplo de saída:**
```
Leitor 1 (Pronome) detectou o UID: [134, 188, 115, 248, 177]
Pronome reconhecido: Eu

Leitor 2 (Ação) detectou o UID: [246, 55, 126, 248, 71]
Ação reconhecida: brincar

--- FRASE FORMADA --- 
'Eu quero brincar'
---------------------
```

---

## 📂 Estrutura dos Arquivos

- `main.py`: O programa principal que lê as tags e forma as frases.
- `mapeamento_tags.py`: Ferramenta de linha de comando para cadastrar e gerenciar as tags.
- `acoes.json`: Arquivo que armazena o mapeamento de UIDs para tags de "ação".
- `pronomes.json`: Arquivo que armazena o mapeamento de UIDs para tags de "pronome".
- `MFRC522_1.py` / `MFRC522_2.py`: Bibliotecas adaptadas para controlar cada um dos leitores RFID em canais SPI diferentes.
- `leitor_de-teste-de-tag.py`: Script simples para depuração, que detecta e exibe os UIDs nos dois leitores.

---

## 💡 Dicas e Expansão

- **Reforço Visual:** Cole figuras ou pictogramas nos cartões RFID.
- **Feedback Tátil/Visual:** Adicione LEDs que acendem ou motores de vibração para dar feedback quando uma tag é lida corretamente.
- **Expansão do Vocabulário:** O sistema é facilmente expansível. Basta cadastrar mais cartões de pronomes, ações, ou até mesmo objetos para formar frases mais complexas.
