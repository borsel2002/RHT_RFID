#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9   // Example reset pin
#define SS_PIN          10  // Example slave select pin
#define BUZZER_PIN      5   // Buzzer pin

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(9600); // Start serial communication
  SPI.begin();        // Start SPI bus
  mfrc522.PCD_Init(); // Initialize MFRC522

  pinMode(BUZZER_PIN, OUTPUT); // Set buzzer pin as OUTPUT
  Serial.println("RFID Reader Initialized!");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    sendUIDToComputer(mfrc522.uid); // Send UID to server
    mfrc522.PICC_HaltA();           // Stop reading

    if (waitForAccessResponse()) {
      digitalWrite(BUZZER_PIN, HIGH); // Access granted, turn on buzzer
      delay(1000);                    // Buzzer on for 1 second
      digitalWrite(BUZZER_PIN, LOW);  // Turn off buzzer
    }
    delay(1000); // Wait for a second before next read
  }
}

void sendUIDToComputer(MFRC522::Uid uid) {
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.println(); // End of UID
}

bool waitForAccessResponse() {
  while (!Serial.available()) {
    delay(100); // Wait for a response
  }
  return Serial.read() == '1'; // Assuming '1' means access granted
}
