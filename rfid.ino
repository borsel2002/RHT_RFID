#include <SPI.h>
#include <MFRC522.h>
#include <SD.h>
#define RST_PIN1         9          // Ana kapı için RC522 reset pini
#define SS_PIN1          10         // Ana kapı için RC522 slave select pini
#define RST_PIN2         8          // Ofis kapısı için RC522 reset pini
#define SS_PIN2          11         // Ofis kapısı için RC522 slave select pini
#define RST_PIN3         6          // DJ odası kapısı için RC522 reset pini
#define SS_PIN3          2          // DJ odası kapısı için RC522 slave select pini
#define BUZZER_PIN       7          // Buzzer pini
#define SD_CS_PIN        4          // SD kart modülü CS pini
MFRC522 mfrc522_main(SS_PIN1, RST_PIN1); // MFRC522 örneklerini oluştur
MFRC522 mfrc522_office(SS_PIN2, RST_PIN2);
MFRC522 mfrc522_djroom(SS_PIN3, RST_PIN3);
void setup() {
  Serial.begin(9600);   // Seri iletişimi başlat
  SPI.begin();          // SPI bus'ını başlat
  mfrc522_main.PCD_Init();   // MFRC522'yi başlat
  mfrc522_office.PCD_Init();
  mfrc522_djroom.PCD_Init();
  pinMode(BUZZER_PIN, OUTPUT);
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD Kart başlatma başarısız oldu!");
    return;
  }
  Serial.println("SD Kart başlatıldı.");
  Serial.println("RFID Okuyucuları Başlatıldı!");
}
void loop() {
  // Ana kapı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_main, "Ana Kapı");
  // Ofis kapısı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_office, "Yayın Odası");
  // DJ odası kapısı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_djroom, "DJ Odası");
  delay(1000); // Bir sonraki kartı okumadan önce bir saniye bekle
}
void checkRFID(MFRC522 &rfidReader, const char* doorName) {
  if (rfidReader.PICC_IsNewCardPresent() && rfidReader.PICC_ReadCardSerial()) {
    Serial.print("RFID Okuyucu (");
    Serial.print(doorName);
    Serial.print(") - Okunan UID: ");
    printUID(rfidReader.uid);
    // UID'yi listeye karşı kontrol et
    if (checkAccess(rfidReader.uid, doorName)) {
      Serial.println("Erişim İzni Onaylandı!");
      // Buzzer'ı 1 saniye boyunca aç
      digitalWrite(BUZZER_PIN, HIGH);
      delay(1000);
      digitalWrite(BUZZER_PIN, LOW);
    } else {
      Serial.println("Erişim İzni Reddedildi!");
    }
    rfidReader.PICC_HaltA();  // Okumayı durdur
  }
}
bool checkAccess(MFRC522::Uid uid, const char* doorName) {
  // Dosyayı okumak için aç
  File dbFile = SD.open("access_db.txt");
  if (!dbFile) {
    Serial.println("Veritabanı dosyasını açarken hata");
    return false;
  }
  // Dosyayı satır satır oku
  char dbLine[128];
  while (dbFile.available()) {
    dbFile.readBytesUntil('\n', dbLine, sizeof(dbLine));
    // Satırı ayrıştır ve UID'nin eşleşip eşleşmediğini kontrol et
    // ve doğru erişim izinlerine sahip olup olmadığını kontrol et
    char* token = strtok(dbLine, ",");
    if (token && atol(token) == cardUID) {
      // UID bulundu, şimdi erişim izinlerini kontrol et
      while (token) {
        token = strtok(NULL, ",");
        if (token && strcmp(token, doorName) == 0) {
          // Kapı adını buldu, erişim iznini kontrol et
          token = strtok(NULL, ",");
          if (token && atoi(token) == 1) {
            // Erişim izni verildi
            dbFile.close();
            return true;
          }
        }
      }
    }
  }
  // Dosyayı kapat
  dbFile.close();
  // Eğer UID bulunamazsa, erişimi reddet
  return false;
}
void printUID(MFRC522::Uid uid) {
  // UID'yi seri monitöre yazdır
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.println();
}
