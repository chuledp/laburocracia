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

## Notas
- No intervenir el lado 220V bajo ningún concepto
- El transformador permanece siempre enchufado; el MOSFET controla el lado 12V DC
- La RPi se alimenta por separado (su propia fuente de 5V)
