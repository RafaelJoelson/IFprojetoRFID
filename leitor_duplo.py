import RPi.GPIO as GPIO
import MFRC522_1 as RFID1
import MFRC522_2 as RFID2
import time

reader1 = RFID1.MFRC522()
reader2 = RFID2.MFRC522()

rfid1_detectado = False
rfid2_detectado = False

print("Escutando dois leitores RFID...")

try:
    while True:
        # Leitor 1
        (status1, _) = reader1.MFRC522_Request(reader1.PICC_REQIDL)
        if status1 == reader1.MI_OK:
            (status1, uid1) = reader1.MFRC522_Anticoll()
            if status1 == reader1.MI_OK:
                print("Leitor 1: UID:", uid1)
                rfid1_detectado = True

        # Leitor 2
        (status2, _) = reader2.MFRC522_Request(reader2.PICC_REQIDL)
        if status2 == reader2.MI_OK:
            (status2, uid2) = reader2.MFRC522_Anticoll()
            if status2 == reader2.MI_OK:
                print("Leitor 2: UID:", uid2)
                rfid2_detectado = True

        if rfid1_detectado and rfid2_detectado:
            print("RFID 1 e RFID 2 foram reconhecidos!")
            rfid1_detectado = False
            rfid2_detectado = False

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Encerrando...")
    GPIO.cleanup()
