#include <Adafruit_NeoPixel.h>
#include "config.h"

// How many internal neopixels do we have? some boards have more than one!
#define NUMPIXELS        9
bool btn_state = false;


Adafruit_NeoPixel pixels(NUMPIXELS, 35, NEO_GRB + NEO_KHZ800);
AdafruitIO_Feed *led = io.feed("led");


// the setup routine runs once when you press reset:
void setup() {
  Serial.begin(115200);

  while(! Serial);

  Serial.print("Connecting to Adafruit IO");
  io.connect();
  #if defined(NEOPIXEL_POWER)
  // If this board has a power control pin, we must set it to output and high
  // in order to enable the NeoPixels. We put this in an #if defined so it can
  // be reused for other boards without compilation errors
  pinMode(NEOPIXEL_POWER, OUTPUT);
  digitalWrite(NEOPIXEL_POWER, HIGH);

  led->onMessage(handleMessage);

  // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println();
  Serial.println(io.statusText());
  led->get();

   pinMode(37, OUTPUT);

  pixels.begin();
  pixels.setBrightness(100);
  pixels.show();
  #endif
  
    pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
    pixels.setBrightness(100);
    pixels.show();// not so bright
  }

// the loop routine runs over and over again forever:
void loop() {
  // say hi
  io.run();  
  // set color to red
  //pixels.fill(0xFFFFFF);
  Serial.println(digitalReadOutputPin(37));
  delay(2500);
  //if (digitalReadOutputPin(
  //pixels.show();
  //delay(500); // wait half a second

  // turn off
  //pixels.fill(0x000000);
  //pixels.show();
  //delay(500); // wait half a second
}

int digitalReadOutputPin(uint8_t pin)
{
  uint8_t bit = digitalPinToBitMask(pin);
  uint8_t port = digitalPinToPort(pin);
  if (port == NOT_A_PIN) 
    return LOW;

  return (*portOutputRegister(port) & bit) ? HIGH : LOW;
}

void handleMessage(AdafruitIO_Data *data) {
  Serial.print("received <- ");

  if(data->toPinLevel() == HIGH){
    pixels.fill(0xFFFFFF);
    pixels.show();
    Serial.println("HIGH");
  }
  else {
    Serial.println("LOW");
    pixels.fill(0x000000);
    pixels.show();
  }
  digitalWrite(37, data->toPinLevel());
}
