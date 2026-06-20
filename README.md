# Circuito MOSFET — Laburocracia

## Componentes
- MOSFET N-channel: IRL520N o IRLZ44N
- Resistencia gate: 1kΩ
- Resistencia pull-down: 10kΩ

## Conexiones

| Pin MOSFET | Conectar a |
|------------|------------|
| Gate | GPIO 17 RPi vía resistencia 1kΩ |
| Source | GND común (RPi + negativo transformador 12V) |
| Drain | Negativo del cartel LED |

### Pull-down en Gate
```
GPIO ──── 1kΩ ──── Gate
                   Gate ──── 10kΩ ──── GND
```

## Diagrama completo

```
220V ──── transformador ──── 12V+ ──── cartel (+)
                                       cartel (−) ──── Drain
                                                        Source ──── GND común
                             12V− ────────────────────────────────────┘
                                                                       └──── GND RPi
```

## Principio de operación
- **Gate = 0V** (GPIO LOW): MOSFET abierto, circuito cortado, cartel apagado
- **Gate = 3.3V** (GPIO HIGH): MOSFET cerrado, corriente fluye Drain→Source, cartel encendido
- La corriente del cartel fluye: `12V+ → cartel → Drain → Source → GND`
- El GND de la RPi y el GND del transformador deben estar unidos en Source

## Software — Patchbox OS + Pure Data

### Sistema operativo
- **Patchbox OS** (basado en Raspberry Pi OS) — viene con PD preinstalado y optimizado para audio en tiempo real
- Descarga: https://blokas.io/patchbox-os/

### Control GPIO desde PD
Usar el external **`rpi_gpio`**, que en Patchbox OS está disponible sin compilar manualmente.

Sintaxis en el patch:
```
[rpi_gpio 17 1(   ← enciende GPIO 17
[rpi_gpio 17 0(   ← apaga GPIO 17
```

### Lógica del patch PD
```
[adc~]
  |
[env~]          ← detector de envolvente
  |
[> 80]          ← umbral (ajustar según el audio)
  |
[rpi_gpio 17]   ← controla el GPIO del MOSFET
```

## Notas
- No intervenir el lado 220V bajo ningún concepto
- El transformador permanece siempre enchufado; el MOSFET controla el lado 12V DC
- La RPi se alimenta por separado (su propia fuente de 5V)

---

## Hardware de audio — componentes a comprar

### Ya tenés
| Componente | Especificación |
|------------|----------------|
| Amplificador TPA3116D2 2.1 | 24V, 50W x2 (L/R) + 100W (SUB), 4 ohm |
| Bass shaker Sinustec BS250 | 100W RMS, 4 ohm, 30-100 Hz |

### Comprar
| Componente | Cantidad | Especificación |
|------------|----------|----------------|
| [Fuente de alimentación](https://www.mercadolibre.com.ar/fuente-switching-ac-220v-salida-dc-24v-9a-step-down-acdc/up/MLAU305969109) | 1 | 24V, 6A continuos / 9A pico mínimo |
| Exciters (transductores full range) | 2 | 50mm, 4 ohm, 25W RMS |
| Condensadores bipolares | 2 | 47µF, 25V o 50V — van en serie con cada exciter para filtrar graves |
| Cable audio | 1 | Miniplug 3.5mm macho a macho, 1.5-2m |
| Cable de conexión | 2m | 18-20 AWG rojo y negro |
| [Placa de sonido USB — Ditron SK-USB.EXT](https://www.mercadolibre.com.ar/placa-de-sonido-externa-usb-ditron-71-para-pc-y-notebook/p/MLA29399488) | 1 | Ditron SK-USB.EXT |
| MOSFET | 1 | IRL520N o IRLZ44N |
| Resistencia | 1 | 1kΩ |
| Resistencia pull-down | 1 | 10kΩ |

### Opcional
| Componente | Para qué sirve |
|------------|----------------|
| Condensador electrolítico 4700µF / 35V | En paralelo a la salida de la fuente, filtra picos de corriente |
| Fusible 6A corte lento | Protección entre fuente y amplificador |
| Terminales de horquilla | Conexiones más seguras en borneras del amp |

### Esquema de conexión audio
```
Fuente 24V → Amplificador TPA3116D2
RPi (USB DAC Ditron) → entrada audio amplificador
Amp SALIDA L → [47µF] → Exciter L
Amp SALIDA R → [47µF] → Exciter R
Amp SALIDA SUB → Bass shaker BS250 (directo, sin condensador)
```
