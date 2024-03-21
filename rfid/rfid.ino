#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN1         9          // Main door RC522 reset pin
#define SS_PIN1          10         // Main door RC522 slave select pin
#define RST_PIN2         3          // Office door RC522 reset pin
#define SS_PIN2          4          // Office door RC522 slave select pin
#define RST_PIN3         5          // DJ room door RC522 reset pin
#define SS_PIN3          6          // DJ room RC522 slave select pin

#define BUZZER_PIN1      2          // Buzzer pin 1
#define BUZZER_PIN2      3          // Buzzer pin 2
#define BUZZER_PIN3      4          // Buzzer pin 3

MFRC522 mfrc522_main(SS_PIN1, RST_PIN1);   // Create MFRC522 instance for main door
MFRC522 mfrc522_office(SS_PIN2, RST_PIN2); // Create MFRC522 instance for office door
MFRC522 mfrc522_djroom(SS_PIN3, RST_PIN3); // Create MFRC522 instance for DJ room door

void setup() {
  Serial.begin(9600);   // Start serial communication
  SPI.begin();          // Start SPI bus
  mfrc522_main.PCD_Init();   // Initialize MFRC522 for main door
  mfrc522_office.PCD_Init(); // Initialize MFRC522 for office door
  mfrc522_djroom.PCD_Init(); // Initialize MFRC522 for DJ room door

  pinMode(BUZZER_PIN1, OUTPUT); // Set buzzer pin for main door as OUTPUT
  pinMode(BUZZER_PIN2, OUTPUT); // Set buzzer pin for office door as OUTPUT
  pinMode(BUZZER_PIN3, OUTPUT); // Set buzzer pin for DJ room as OUTPUT

  Serial.println("RFID Readers Initialized!");
}

void loop() {
  // Check each RFID reader
  checkRFID(mfrc522_main, "Main Door", BUZZER_PIN1);
  checkRFID(mfrc522_office, "Office Door", BUZZER_PIN2);
  checkRFID(mfrc522_djroom, "DJ Room", BUZZER_PIN3);

  delay(1000); // Wait a second before reading the next card
}

void checkRFID(MFRC522 &rfidReader, const char* doorName, int buzzerPin) {
  if (rfidReader.PICC_IsNewCardPresent() && rfidReader.PICC_ReadCardSerial()) {
    Serial.print(doorName);
    Serial.print(" door UID read: ");
    printUID(rfidReader.uid);
    sendUIDToComputer(rfidReader.uid, doorName);
    bool accessGranted = waitForAccessResponse();
    if (accessGranted) {
      Serial.println("Access Granted!");
      digitalWrite(buzzerPin, HIGH);
      delay(1000);
      digitalWrite(buzzerPin, LOW);
    } else {
      Serial.println("Access Denied!");
    }
    //rfidReader.PICC_HaltA();  // Stop reading
  }
}

void sendUIDToComputer(MFRC522::Uid uid, const char* doorName) {
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.print(","); // Use comma as separator between UID and door name
  Serial.println(doorName); // Send door name
}

bool waitForAccessResponse() {
  while (!Serial.available()) {
    delay(100);
  }
  String response = Serial.readStringUntil('\n');
  response.trim();
  return response.equals("1"); // If response is "1" then access is granted
}

void printUID(MFRC522::Uid uid) {
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.println();
}
