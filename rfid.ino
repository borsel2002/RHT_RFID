#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN1         9          // Ana kapı için RC522 reset pini
#define SS_PIN1          10         // Ana kapı için RC522 slave select pini
#define RST_PIN2         8          // Ofis kapısı için RC522 reset pini
#define SS_PIN2          11         // Ofis kapısı için RC522 slave select pini
#define RST_PIN3         6          // DJ odası kapısı için RC522 reset pini
#define SS_PIN3          2          // DJ odası kapısı için RC522 slave select pini

#define BUZZER_PIN1      5          // Buzzer pini 1
#define BUZZER_PIN2      6          // Buzzer pini 2
#define BUZZER_PIN3      7          // Buzzer pini 3

MFRC522 mfrc522_main(SS_PIN1, RST_PIN1); // MFRC522 örneklerini oluştur
MFRC522 mfrc522_office(SS_PIN2, RST_PIN2);
MFRC522 mfrc522_djroom(SS_PIN3, RST_PIN3);

void setup() {
  Serial.begin(9600);   // Seri iletişimi başlat
  SPI.begin();          // SPI bus'ını başlat
  mfrc522_main.PCD_Init();   // MFRC522'yi başlat
  mfrc522_office.PCD_Init();
  mfrc522_djroom.PCD_Init();

  pinMode(BUZZER_PIN1, OUTPUT); // Buzzer pinlerini OUTPUT olarak ayarla
  pinMode(BUZZER_PIN2, OUTPUT);
  pinMode(BUZZER_PIN3, OUTPUT);

  Serial.println("RFID Okuyucuları Başlatıldı!");
}

void loop() {
  // Ana kapı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_main, "Ana Kapı", BUZZER_PIN1);
  // Ofis kapısı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_office, "Yayın Odası", BUZZER_PIN2);
  // DJ odası kapısı RFID okuyucusunu kontrol et
  checkRFID(mfrc522_djroom, "DJ Odası", BUZZER_PIN3);

  delay(1000); // Bir sonraki kartı okumadan önce bir saniye bekle
}

void checkRFID(MFRC522 &rfidReader, const char* doorName, int buzzerPin) {
  if (rfidReader.PICC_IsNewCardPresent() && rfidReader.PICC_ReadCardSerial()) {
    Serial.print(doorName);
    Serial.print(" kapısı için UID okundu: ");
    printUID(rfidReader.uid);
    // UID'yi seri port üzerinden bilgisayara gönder
    sendUIDToComputer(rfidReader.uid, doorName);
    // Bilgisayardan erişim izni yanıtını bekle
    bool accessGranted = waitForAccessResponse();
    if (accessGranted) {
      Serial.println("Erişim İzni Onaylandı!");
      // Buzzer'ı 1 saniye boyunca aç
      digitalWrite(buzzerPin, HIGH);
      delay(1000);
      digitalWrite(buzzerPin, LOW);
    } else {
      Serial.println("Erişim İzni Reddedildi!");
    }
    rfidReader.PICC_HaltA();  // Okumayı durdur
  }
}

void sendUIDToComputer(MFRC522::Uid uid, const char* doorName) {
  // UID'yi seri monitöre yazdır
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.print(","); // UID ve kapı adı arasında ayırıcı olarak virgül kullan
  Serial.println(doorName); // Kapı adını gönder
}

bool waitForAccessResponse() {
  // Bilgisayardan yanıt gelene kadar bekle
  while (!Serial.available()) {
    delay(100);
  }
  // Bilgisayardan gelen yanıtı oku
  String response = Serial.readStringUntil('\n');
  response.trim(); // Başındaki ve sonundaki boşlukları temizle
  return response.equals("1"); // Eğer yanıt "1" ise erişim izni verilmiş demektir
}

void printUID(MFRC522::Uid uid) {
  // UID'yi seri monitöre yazdır
  for (byte i = 0; i < uid.size; i++) {
    Serial.print(uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(uid.uidByte[i], HEX);
  }
  Serial.println();
}
