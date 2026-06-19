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



> **Nota:** La tierra de la RPi y la de la fuente externa **deben** estar unidas (GND común). Sin esta conexión, el MOSFET no conmutará correctamente.

## Esquema eléctrico detallado

- **Puerta (G)**: conectada al GPIO de la RPi (ej. pin 18) a través de una resistencia de 220Ω (protege el pin y reduce oscilaciones).
- **Drenador (D)**: conectado al cátodo del LED (o al lado negativo de la carga); el ánodo del LED va a +Vcc (12/24V).
- **Fuente (S)**: conectada a GND común (tanto de la RPi como de la fuente externa).
- **Diodo en antiparalelo**: colocado entre Drenador y +Vcc (cátodo hacia +Vcc) para proteger el MOSFET si la carga es inductiva (motores, relés). Para LEDs puros no es estrictamente necesario, pero no estorba.
- **Resistencia pull‑down de 10kΩ** entre puerta y fuente: asegura que el MOSFET esté apagado cuando la RPi arranca o si el GPIO queda en alta impedancia.

## Configuración de Pure Data

### 1. Encendido/apagado básico (señal digital)

En Pd, usa el objeto `[gpio]` si está disponible en PatchboxOS (suele venir con el paquete `pd-gpio`). Si no, puedes usar `[shell]` para llamar a comandos del sistema (`gpio -g write 18 1`).

**Ejemplo con [gpio] (recomendado):**





