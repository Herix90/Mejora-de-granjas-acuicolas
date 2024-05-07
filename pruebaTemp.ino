#include <OneWire.h>

int DS18S20_Pin = 2; // Pin de señal del sensor DS18S20 en el pin digital 2

// Configuración del chip de temperatura (I/O)
OneWire ds(DS18S20_Pin);  // en el pin digital 2

void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  float temperatura = obtenerTemperatura();
  Serial.println(temperatura);

  delay(100); // utilizado para ralentizar la salida y facilitar la lectura
}

float obtenerTemperatura(){
  // Devuelve la temperatura de un sensor DS18S20 en grados Celsius

  byte datos[12];
  byte direccion[8];

  if ( !ds.search(direccion)) {
      // no hay más sensores en la cadena, reiniciar la búsqueda
      ds.reset_search();
      return -1000;
  }

  if ( OneWire::crc8( direccion, 7) != direccion[7]) {
      Serial.println("¡El CRC no es válido!");
      return -1000;
  }

  if ( direccion[0] != 0x10 && direccion[0] != 0x28) {
      Serial.print("Dispositivo no reconocido");
      return -1000;
  }

  ds.reset();
  ds.select(direccion);
  ds.write(0x44,1); // iniciar conversión, con alimentación parásita al final

  byte presente = ds.reset();
  ds.select(direccion);
  ds.write(0xBE); // Leer Scratchpad

  for (int i = 0; i < 9; i++) { // necesitamos 9 bytes
    datos[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = datos[1];
  byte LSB = datos[0];

  float lecturaTemp = ((MSB << 8) | LSB); // utilizando complemento a dos
  float sumaTemperatura = lecturaTemp / 16;

  return sumaTemperatura;
}
