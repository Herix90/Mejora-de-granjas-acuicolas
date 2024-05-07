#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ECSensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const char* ssid = "LaboratorioInternet";
const char* password = "Lab2023wifi";

const char* thingspeakApiKey = "IATRAMAOBR743HQX";

const int sensorPinPH = A0;
const int sensorPinOxygen = A1;
const int sensorECPin = 1; 
const int sensorTempPin = 5; 

// Instancias de los sensores
Adafruit_ECSensor ecSensor(sensorECPin);
OneWire oneWire(sensorTempPin);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");

  if (!ecSensor.begin()) {
    Serial.println("Error al iniciar el sensor EC");
    while (1);
  }
  Serial.println("Sensor EC iniciado correctamente");

  sensors.begin();
  sensors.requestTemperatures();
}

void loop() {
  // Lectura y envío de pH
  float ph = readPH(sensorPinPH);
  sendToThingSpeak(ph, "Sensor Ph");

  // Lectura y envío de oxígeno disuelto
  float oxygen = readOxygen(sensorPinOxygen);
  sendToThingSpeak(oxygen, "field2");

  // Lectura de conductividad y temperatura
  float conductivity = ecSensor.getConductivity();
  sensors.waitForTemperature(sensorTempPin); 
  float temperature = sensors.getTempCByIndex(0); 

  // Envía los valores de conductividad y temperatura a ThingSpeak
  sendToThingSpeak(conductivity, "field3");
  sendToThingSpeak(temperature, "field4");

  delay(5000); // 5 sec
}

// Función para leer el valor de pH
float readPH(int pin) {
  int sensorValue = analogRead(pin);
  return (sensorValue * 5.0) / 1024.0 * 3.5; // Calibracion
}

// Función para leer el valor de oxígeno
float readOxygen(int pin) {
  int sensorValue = analogRead(pin);
  return (sensorValue * 5.0) / 1024.0 * 20.0; // Calibracion
}

// Función para enviar datos a ThingSpeak
void sendToThingSpeak(float value, String field) {
  WiFiClient client;
  HTTPClient http = HTTPClient(client);

  String url = "https://api.thingspeak.com/update?api_key=";
  url += thingspeakApiKey;
  url += "&" + field + "=";
  url += String(value);

  http.begin(url);
  int httpCode = http.POST();

  if (httpCode > 0) {
    if (httpCode == 200) {
      Serial.println("Datos enviados a ThingSpeak correctamente");
    } else {
      Serial.print("Error enviando datos a ThingSpeak: ");
      Serial.println(httpCode);
    }
  } else {
    Serial.println("Error de conexión a ThingSpeak");
  }

  http.end();
}
