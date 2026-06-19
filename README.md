# Control de LED de alta potencia con MOSFET y Raspberry Pi (PatchboxOS)

Guía para controlar tiras LED o lámparas de 12V/24V desde Pure Data, utilizando un MOSFET de canal N (nivel lógico) y la Raspberry Pi con PatchboxOS.

## ¿Por qué este enfoque?

- **Raspberry Pi + PatchboxOS**: entorno optimizado para audio y control en tiempo real con Pure Data.
- **MOSFET IRLZ44N**: conmuta altas corrientes (hasta ~40A) con solo 3.3V de la RPi, ideal para LEDs de potencia.
- **Pd (Pure Data)**: genera señales de control (encendido/apagado o PWM) que se envían directamente a los pines GPIO.

## Materiales necesarios

| Componente | Especificación |
|------------|----------------|
| Raspberry Pi (3B+/4) | Con PatchboxOS instalado y Pd funcionando |
| MOSFET canal N | IRLZ44N (nivel lógico, Vgs<th = 1–2V) |
| Diodo 1N4007 | Protección contra picos inductivos |
| Resistencia 10kΩ | Pull-down en la puerta (opcional pero recomendada) |
| Resistencia 220Ω–1kΩ | Limitadora de corriente de la puerta (opcional) |
| Fuente externa | 12V o 24V (según tu LED) |
| LED / tira LED | Conectada al drenador del MOSFET |
| Cables y protoboard | Conexiones seguras |

## Diagrama de conexión (ASCII)
