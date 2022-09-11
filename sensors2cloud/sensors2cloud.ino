
// Adafruit IO Environmental Data Logger 
// Tutorial Link: https://learn.adafruit.com/adafruit-io-air-quality-monitor
//
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Written by Brent Rubell for Adafruit Industries
// Copyright (c) 2018 Adafruit Industries
// Licensed under the MIT license.
//
// All text above must be included in any redistribution.

/************************** Adafruit IO Configuration ***********************************/

// edit the config.h tab and enter your Adafruit IO credentials
// and any additional configuration needed for WiFi, cellular,
// or ethernet clients.
#include "config.h"

/**************************** Sensor Configuration ***************************************/
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <SensirionI2CScd4x.h>
#include "Adafruit_BME680.h"
#include "Adafruit_VEML6070.h"
#include "Adafruit_seesaw.h"
#include <Multichannel_Gas_GMXXX.h>

GAS_GMXXX<TwoWire> gas;

Adafruit_seesaw ss;

Adafruit_VEML6070 uv = Adafruit_VEML6070();

// BME280 Sensor Definitions
#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

// Instanciate the sensors
Adafruit_BME680 bme; // I2C
SensirionI2CScd4x scd4x;


/**************************** Example ***************************************/
// Delay between sensor reads, in seconds
#define READ_DELAY 25

// DHT22 Data
int temperatureReading;
int pressureReading;
int altitudeReading = 0;
int humidityReading = 0;
int co2Reading = 0;
int uvReading = 0;
int sTempReading = 0;
int moistureReading = 0;
int no2Reading = 0;
int boozeReading = 0;
int vocReading = 0;
int monoxReading = 0;

//int cotwo = 0;
double lat = 25.907337;
double lon = -80.138976;
double ele = 3;


// set up the feeds for the BME280
AdafruitIO_Feed *temperatureFeed = io.feed("temperature");
AdafruitIO_Feed *humidityFeed = io.feed("humidity");
AdafruitIO_Feed *pressureFeed = io.feed("pressure");
AdafruitIO_Feed *co2Feed = io.feed("co2");
AdafruitIO_Feed *uvFeed = io.feed("uv");
AdafruitIO_Feed *soilTempFeed = io.feed("soil");
AdafruitIO_Feed *moistureFeed = io.feed("moisture");
AdafruitIO_Feed *no2Feed = io.feed("no2");
AdafruitIO_Feed *boozeFeed = io.feed("booze");
AdafruitIO_Feed *monoxFeed = io.feed("monox");
AdafruitIO_Feed *vocFeed = io.feed("voc");
void printUint16Hex(uint16_t value) {
    Serial.print(value < 4096 ? "0" : "");
    Serial.print(value < 256 ? "0" : "");
    Serial.print(value < 16 ? "0" : "");
    Serial.print(value, HEX);
}

void printSerialNumber(uint16_t serial0, uint16_t serial1, uint16_t serial2) {
    Serial.print("Serial: 0x");
    printUint16Hex(serial0);
    printUint16Hex(serial1);
    printUint16Hex(serial2);
    Serial.println();
}

void setup() {
  // start the serial connection
  Serial.begin(115200);
  Wire.begin();
  // wait for serial monitor to open
  while (!Serial);

  Serial.println("Adafruit IO Environmental Logger");

  // set up BME280
  setupBME688();

  uint16_t error;
  char errorMessage[256];
  scd4x.begin(Wire);

  uv.begin(VEML6070_1_T);

  gas.begin(Wire, 0x08);
  
  error = scd4x.stopPeriodicMeasurement();
  if (error) {
      Serial.print("Error trying to execute stopPeriodicMeasurement(): ");
      errorToString(error, errorMessage, 256);
      Serial.println(errorMessage);
  }

  uint16_t serial0;
  uint16_t serial1;
  uint16_t serial2;
  error = scd4x.getSerialNumber(serial0, serial1, serial2);
  if (error) {
      Serial.print("Error trying to execute getSerialNumber(): ");
      errorToString(error, errorMessage, 256);
      Serial.println(errorMessage);
  } else {
      printSerialNumber(serial0, serial1, serial2);
  }
  error = scd4x.startPeriodicMeasurement();
  if (error) {
      Serial.print("Error trying to execute startPeriodicMeasurement(): ");
      errorToString(error, errorMessage, 256);
      Serial.println(errorMessage);
  }

  Serial.println("Waiting for first measurement... (5 sec)");

  if (!ss.begin(0x36)) {
    Serial.println("ERROR! seesaw not found");
    while(1) delay(1);
  } else {
    Serial.print("seesaw started! version: ");
    Serial.println(ss.getVersion(), HEX);
  }
  
  // connect to io.adafruit.com
  Serial.print("Connecting to Adafruit IO");
  io.connect();

  // wait for a connection
  while (io.status() < AIO_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }

  // we are connected
  Serial.println();
  Serial.println(io.statusText());
}

void loop() {
  // io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  io.run();
  uint16_t error;
  char errorMessage[256];
  delay(5000);
  uint16_t co2;
  float temperature;
  float humidity;

  float tempC = ss.getTemp();
  uint16_t capread = ss.touchRead(0);
  
  if (! bme.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }

  // Read the temperature from the BME280
  temperatureReading = bme.temperature;

  // convert from celsius to degrees fahrenheit
  temperatureReading = temperatureReading * 1.8 + 32;

  uvReading = uv.readUV();
  Serial.print("UV light level: "); Serial.println(uvReading);

  sTempReading = tempC * 1.8 + 32;
  Serial.print("Soil Temp: "); Serial.print(sTempReading); Serial.println("*F");

  moistureReading = capread;
  Serial.print("Capacitive: "); Serial.println(moistureReading);

  no2Reading = gas.getGM102B();
  Serial.print("no2: "); Serial.println(no2Reading);

  boozeReading = gas.getGM302B();
  Serial.print("booze: "); Serial.println(boozeReading);

  monoxReading = gas.getGM702B();
  Serial.print("co: "); Serial.println(monoxReading);

  vocReading = gas.getGM502B();
  Serial.print("VOC: "); Serial.println(vocReading);
  
  Serial.print("Temperature = "); Serial.print(temperatureReading); Serial.println(" *F");

  // Read the pressure from the BME280
  pressureReading = bme.pressure / 100.0F;
  Serial.print("Pressure = "); Serial.print(pressureReading); Serial.println(" hPa");

  // Read the altitude from the BME280
  altitudeReading = bme.readAltitude(SEALEVELPRESSURE_HPA) + 28;
  Serial.print("Approx. Altitude = "); Serial.print(altitudeReading); Serial.println(" m");
  
  // Read the humidity from the BME280
  humidityReading = bme.humidity;
  Serial.print("Humidity = "); Serial.print(humidityReading); Serial.println("%");
  
  error = scd4x.readMeasurement(co2, temperature, humidity);
  if (error) {
      Serial.print("Error trying to execute readMeasurement(): ");
      errorToString(error, errorMessage, 256);
      Serial.println(errorMessage);
  } else if (co2 == 0) {
      Serial.println("Invalid sample detected, skipping.");
  } else {
      //cotwo = Co2
      co2Reading = (1.8*co2)/10;
      Serial.print("Co2:");
      Serial.print(co2Reading);
      
  }
  // send data to Adafruit IO feeds
  temperatureFeed->save(temperatureReading,  lat, lon, ele);
  humidityFeed->save(humidityReading,  lat, lon, ele);
  pressureFeed->save(pressureReading,  lat, lon, ele);
  co2Feed->save(co2Reading, lat, lon, ele);
  uvFeed->save(uvReading, lat, lon, ele);
  soilTempFeed->save(sTempReading, lat, lon, ele);
  moistureFeed->save(moistureReading, lat, lon, ele);
  no2Feed->save(no2Reading, lat, lon, ele);
  boozeFeed->save(boozeReading, lat, lon, ele);
  monoxFeed->save(monoxReading, lat, lon, ele);
  vocFeed->save(vocReading, lat, lon, ele);
  // delay the polled loop
  delay(READ_DELAY * 1000);
}

// Set up the BME280 sensor
void setupBME688() {
  bool status;
  status = bme.begin();
  if (!status)
  {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);
  Serial.println("BME Sensor is set up!");
}
