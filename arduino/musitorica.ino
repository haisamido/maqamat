/**
 * @file musitorica.ino
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2024-04-23
 * 
 * @copyright Copyright (c) 2024
 * @simulation https://wokwi.com/projects/395360264870700033 
 */
#include <LiquidCrystal_I2C.h>
// Define the I2C LCD connection settings
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Replace 0x27 with your LCD I2C address if different

#include <Adafruit_NeoPixel.h>

#include <Keypad.h>
/*#include <Servo.h>*/
#include "SafeState.h"
#include "icons.h"

/* Locking mechanism definitions */
#define SERVO_PIN        6
#define SERVO_LOCK_POS   20
#define SERVO_UNLOCK_POS 90
Servo lockServo;

/* Display */

/* Keypad setup */
const byte KEYPAD_ROWS    = 4;
const byte KEYPAD_COLS    = 4;
byte rowPins[KEYPAD_ROWS] = {5, 4, 3, 2};
byte colPins[KEYPAD_COLS] = {A3, A2, A1, A0};
char keys[KEYPAD_ROWS][KEYPAD_COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, KEYPAD_ROWS, KEYPAD_COLS);

#define SPEAKER_PIN 13

// input
const uint8_t pitch_class_set[] = {0,1,3,5,6};

int number_of_pitches_in_pitch_class = sizeof(pitch_class_set);

// defaults
const float frequency_reference = 330.; // reference frequency, i.e. 0
const int number_of_pitches     = 12;    // equally tempered (e.g. 12 equal temperament)

// NeoPixel : Bracelet
#define PIXEL_COUNT number_of_pitches
#define PIXEL_PIN 6
Adafruit_NeoPixel pitch_bracelet(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

/* SafeState stores the secret code in EEPROM */
SafeState safeState;

// join array elements
// source: https://gist.github.com/abachman/5257b1700cc77a6ebabdff1aeefb3376
String join(uint8_t vals[], char sep, int items) {
  String out = "";
  
  for (int i=0; i<items; i++) {
    out = out + String(vals[i]);
    if ((i + 1) < items) {
      out = out + sep;
    }
  }
  return out;
}

void lock() {
  lockServo.write(SERVO_LOCK_POS);
  safeState.lock();
}

void unlock() {
  lockServo.write(SERVO_UNLOCK_POS);
}

void showStartupMessage() {
  lcd.setCursor(0, 0);
  String message = "   ... MAQAMAT ...";
  
  for (byte i = 0; i < message.length(); i++) {
    lcd.print(message[i]);
    delay(100);
  }
  
  delay(1000);

  lcd.setCursor(0, 1);
  lcd.print("Mode: 1,");
  lcd.setCursor(0, 2);

  String pitch_class_set_string = "{ " + join(pitch_class_set, ', ', number_of_pitches_in_pitch_class) + " }";
  lcd.print(pitch_class_set_string);

  lcd.setCursor(0, 3);

  delay(500);
}

String inputSecretCode() {
  lcd.setCursor(5, 1);
  lcd.print("[____]");
  lcd.setCursor(6, 1);

  String result = "";

  while (result.length() < 4) {
    char key = keypad.getKey();
    if (key >= '0' && key <= '9') {
      lcd.print('*');
      result += key;
    }

  }
  return result;
}

void showWaitScreen(int delayMillis) {
  lcd.setCursor(2, 1);
  lcd.print("[..........]");
  lcd.setCursor(3, 1);

  for (byte i = 0; i < 10; i++) {
    delay(delayMillis);
    lcd.print("=");
  }
}

bool setNewCode() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Enter new code:");

  String newCode = inputSecretCode();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Confirm new code");

  String confirmCode = inputSecretCode();

  if (newCode.equals(confirmCode)) {
    safeState.setCode(newCode);
    return true;
  } else {
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("Code mismatch");
    lcd.setCursor(0, 1);
    lcd.print("Safe not locked!");

    delay(2000);
    return false;
  }
}

void showUnlockMessage() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.write(ICON_UNLOCKED_CHAR);
  lcd.setCursor(4, 0);
  lcd.print("Unlocked!");
  lcd.setCursor(15, 0);
  lcd.write(ICON_UNLOCKED_CHAR);

  delay(1000);
}

void safeUnlockedLogic() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.write(ICON_UNLOCKED_CHAR);
  lcd.setCursor(2, 0);
  lcd.print(" # to lock");
  lcd.setCursor(15, 0);
  lcd.write(ICON_UNLOCKED_CHAR);

  bool newCodeNeeded = true;

  if (safeState.hasCode()) {
    newCodeNeeded = false;

    lcd.setCursor(0, 1);
    lcd.print("  A = new code");

    newCodeNeeded = false;
  }

  auto key = keypad.getKey();
  while (key != 'A' && key != '#') {
    key = keypad.getKey();
  }

  bool readyToLock = true;
  if (key == 'A' || newCodeNeeded) {
    readyToLock = setNewCode();
  }

  if (readyToLock) {
    lcd.clear();
    lcd.setCursor(5, 0);
    lcd.write(ICON_UNLOCKED_CHAR);
    lcd.print(" ");
    lcd.write(ICON_RIGHT_ARROW);
    lcd.print(" ");
    lcd.write(ICON_LOCKED_CHAR);

    safeState.lock();
    lock();
    showWaitScreen(100);
  }
}

void safeLockedLogic() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.write(ICON_LOCKED_CHAR);
  lcd.print(" Safe Locked! ");
  lcd.write(ICON_LOCKED_CHAR);

  String userCode = inputSecretCode();
  bool unlockedSuccessfully = safeState.unlock(userCode);
  showWaitScreen(200);

  if (unlockedSuccessfully) {
    showUnlockMessage();
    unlock();
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Access Denied!");

    showWaitScreen(1000);
  }
}

// https://wokwi.com/projects/395427205943873537
void pitch_bracelet_startup() {
  pitch_bracelet.begin();
  pitch_bracelet.show();
}

void setup() {
  Serial.begin(9600); // open the serial port at 9600 bps:

  lcd.begin(16, 2);

  lcd.init();
  lcd.backlight();  // Optional: turn on backlight\

  delay(10);
  lcd.setCursor(4, 0);

  init_icons(lcd);

  lockServo.attach(SERVO_PIN);

  // for (uint8_t i = 0; i < numTones; i++) {
  //   pinMode(buttonPins[i], INPUT_PULLUP);
  // }
  pinMode(SPEAKER_PIN, OUTPUT);

  /* Make sure the physical lock is sync with the EEPROM state */
  if (safeState.locked()) {
    lock();
  } else {
    unlock();
  }

  // put your setup code here, to run once:

  pitch_bracelet_startup();
  showStartupMessage();

}

// https://github.com/haisamido/maqamat/blob/main/maqamat.py#L62
float frequency_from_cents(float f1 , float cents, float cents_per_octave){
  return f1*pow(2,cents/cents_per_octave);
}

void loop() {

  float frequency;
  float cents;
  
  int pitch_class_step;

  for ( int i = 0; i < number_of_pitches_in_pitch_class; i++) {

    cents            = i*100.0;
    pitch_class_step = pitch_class_set[i];

    // turn on LED on neopixel for the pitch_class_step in question
    pitch_bracelet.setPixelColor(pitch_class_step, 0, 255, 0);
    pitch_bracelet.show();

    Serial.print(pitch_class_step);
    Serial.print("\t");

    // https://github.com/haisamido/maqamat/blob/main/maqamat.py#L62
    frequency = frequency_from_cents(frequency_reference, cents, 1200);

    Serial.print(frequency);
    Serial.println();

    tone(SPEAKER_PIN, frequency);
    delay(500);
    noTone(SPEAKER_PIN);

  }

  if (safeState.locked()) {
    safeLockedLogic();
  } else {
    safeUnlockedLogic();
  }
  Serial.println();
}
