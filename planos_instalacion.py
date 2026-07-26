import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ==============================================================================
# CONFIGURACIÓN GLOBAL — Estilo técnico/profesional (plano arquitectónico)
# ==============================================================================

plt.style.use('default')  # Fondo blanco limpio

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.2,
    'figure.figsize': (14, 10),
})

# Colores estilo plano técnico
COLOR_SOMMIER = '#D9D9D9'       # Gris claro
COLOR_COLCHON = '#F0E6D3'       # Beige/crema
COLOR_CARTEL_BASE = '#C8D8E0'   # Celeste grisáceo (acrílico)
COLOR_CARTEL_NEON = '#E02020'   # Rojo neón
COLOR_COTA = '#1A1A1A'          # Negro para cotas
COLOR_COTA_LINE = '#555555'     # Gris oscuro para líneas de cota
COLOR_PERFORACION = '#333333'   # Gris oscuro para perforaciones

DPI_GUARDADO = 300

# ==============================================================================
# MEDIDAS DE LA OBRA (en metros)
# ==============================================================================
# Sommier
SOMMIER_LARGO = 1.90    # m (eje Y en planta)
SOMMIER_ANCHO = 1.00    # m (eje X en planta)
SOMMIER_ALTO  = 0.30    # m

# Colchón (mismas dimensiones de planta que el sommier)
COLCHON_LARGO = 1.90    # m
COLCHON_ANCHO = 1.00    # m
COLCHON_ALTO  = 0.25    # m

# Letrero neón LED
CARTEL_ANCHO = 1.10     # m (110 cm)
CARTEL_ALTO  = 0.22     # m (22 cm)

# Base de acrílico
BASE_ANCHO = 1.12       # m (112 cm)
BASE_ALTO  = 0.24       # m (24 cm)

# Posición del cartel
CARTEL_ALTURA_PISO = 2.00   # m (del piso al borde inferior del cartel)
CARTEL_OFFSET_CABECERA = 0.10  # m (corrido 10cm hacia adentro desde cabecera)

# Perforaciones: 3 en la parte superior de la base de acrílico
N_PERFORACIONES = 3
PERFORACION_RADIO = 0.008  # m (radio visual, ~8mm para que se vea en el plano)

# Patas del sommier
PATA_ALTO = 0.15        # m (15cm)
PATA_DIAMETRO = 0.05    # m (5cm)
N_PATAS = 6             # 4 esquinas + 2 centrales laterales

# Exciters (transductores)
EXCITER_DIAMETRO = 0.05  # m (5cm)
EXCITER_ALTO = 0.02      # m (2cm)

# Bass Shaker BS250
BASS_SHAKER_DIAMETRO = 0.15  # m (15cm)
BASS_SHAKER_ALTO = 0.05      # m (5cm)

# Caja de electrónica (Bela Rev C + Amp TPA3116D2 + fuente)
CAJA_LARGO = 0.25    # m (25cm)
CAJA_ANCHO = 0.20    # m (20cm)
CAJA_ALTO  = 0.08    # m (8cm)

# Espesor del cartel (para vista de perfil)
CARTEL_ESPESOR = 0.03  # m (~3cm acrílico + neón)

# Colores adicionales
COLOR_PATA = '#A0A0A0'          # Gris medio
COLOR_EXCITER = '#FF8C00'       # Naranja
COLOR_BASS_SHAKER = '#8B4513'   # Marrón
COLOR_CAJA = '#4682B4'          # Azul acero
COLOR_CABLE = '#666666'         # Gris para cables


# ==============================================================================
# FUNCIONES AUXILIARES PARA COTAS
# ==============================================================================

def dibujar_cota_horizontal(ax, x1, x2, y, texto, offset=0.08, lado='abajo',
                            color=COLOR_COTA, fontsize=9):
    """Dibuja una cota horizontal con flechas y texto."""
    if lado == 'abajo':
        y_cota = y - offset
        va = 'top'
        y_linea_ext = [y, y_cota - 0.02]
    else:
        y_cota = y + offset
        va = 'bottom'
        y_linea_ext = [y, y_cota + 0.02]

    # Líneas de extensión
    ax.plot([x1, x1], y_linea_ext, color=COLOR_COTA_LINE, linewidth=0.6, linestyle='-')
    ax.plot([x2, x2], y_linea_ext, color=COLOR_COTA_LINE, linewidth=0.6, linestyle='-')

    # Línea de cota con flechas
    ax.annotate('', xy=(x2, y_cota), xytext=(x1, y_cota),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.0))

    # Texto de la cota
    ax.text((x1 + x2) / 2, y_cota, texto,
            ha='center', va=va, fontsize=fontsize, fontweight='bold',
            color=color, backgroundcolor='white',
            bbox=dict(boxstyle='square,pad=0.15', facecolor='white',
                      edgecolor='none', alpha=0.9))


def dibujar_cota_vertical(ax, y1, y2, x, texto, offset=0.08, lado='derecha',
                          color=COLOR_COTA, fontsize=9):
    """Dibuja una cota vertical con flechas y texto."""
    if lado == 'derecha':
        x_cota = x + offset
        ha = 'left'
        x_linea_ext = [x, x_cota + 0.02]
    else:
        x_cota = x - offset
        ha = 'right'
        x_linea_ext = [x, x_cota - 0.02]

    # Líneas de extensión
    ax.plot(x_linea_ext, [y1, y1], color=COLOR_COTA_LINE, linewidth=0.6, linestyle='-')
    ax.plot(x_linea_ext, [y2, y2], color=COLOR_COTA_LINE, linewidth=0.6, linestyle='-')

    # Línea de cota con flechas
    ax.annotate('', xy=(x_cota, y2), xytext=(x_cota, y1),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.0))

    # Texto de la cota
    ax.text(x_cota + 0.02 if lado == 'derecha' else x_cota - 0.02,
            (y1 + y2) / 2, texto,
            ha=ha, va='center', fontsize=fontsize, fontweight='bold',
            color=color, rotation=90,
            backgroundcolor='white',
            bbox=dict(boxstyle='square,pad=0.15', facecolor='white',
                      edgecolor='none', alpha=0.9))


# ==============================================================================
# VISTA 1: PLANO DE PLANTA (TOP-DOWN VIEW)
# ==============================================================================

def generar_vista_planta():
    """Genera la vista de planta (top-down) de la instalación."""
    print("\n--- Generando Vista 1: Plano de Planta ---")

    fig, ax = plt.subplots(figsize=(10, 16))

    # Posición base: el sommier se ubica centrado en X, con cabecera arriba (Y máximo)
    sommier_x0 = 0
    sommier_y0 = 0

    # --- SOMMIER (rectángulo gris claro) ---
    sommier = mpatches.FancyBboxPatch(
        (sommier_x0, sommier_y0), SOMMIER_ANCHO, SOMMIER_LARGO,
        boxstyle="round,pad=0.01",
        facecolor=COLOR_SOMMIER, edgecolor='black', linewidth=1.8
    )
    ax.add_patch(sommier)
    ax.text(SOMMIER_ANCHO / 2, SOMMIER_LARGO / 2 - 0.15, 'SOMMIER',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='#666666', style='italic')

    # --- COLCHÓN (rectángulo beige, levemente más pequeño visualmente) ---
    margen_visual = 0.02  # margen visual para que se vea el borde del sommier
    colchon = mpatches.FancyBboxPatch(
        (sommier_x0 + margen_visual, sommier_y0 + margen_visual),
        COLCHON_ANCHO - 2 * margen_visual, COLCHON_LARGO - 2 * margen_visual,
        boxstyle="round,pad=0.02",
        facecolor=COLOR_COLCHON, edgecolor='#999999', linewidth=1.2,
        linestyle='--'
    )
    ax.add_patch(colchon)
    ax.text(COLCHON_ANCHO / 2, COLCHON_LARGO / 2 + 0.05, 'COLCHÓN',
            ha='center', va='center', fontsize=10, color='#888888')

    # --- CABECERA (indicador) ---
    cabecera_y = SOMMIER_LARGO  # borde superior
    ax.plot([sommier_x0 - 0.05, SOMMIER_ANCHO + 0.05], [cabecera_y, cabecera_y],
            color='#333333', linewidth=0.8, linestyle=':')
    ax.text(SOMMIER_ANCHO / 2, cabecera_y + 0.03, 'CABECERA',
            ha='center', va='bottom', fontsize=9, color='#555555')

    # --- CARTEL LED (vista desde arriba: se ve como una línea/rectángulo fino) ---
    # El cartel cuelga sobre la cabecera, corrido 10cm hacia adentro
    cartel_x0 = (SOMMIER_ANCHO - BASE_ANCHO) / 2  # centrado en X
    cartel_y0 = cabecera_y - CARTEL_OFFSET_CABECERA  # corrido hacia adentro

    # Base de acrílico (vista desde arriba = rectángulo muy fino)
    base_rect = mpatches.Rectangle(
        (cartel_x0, cartel_y0 - 0.03), BASE_ANCHO, 0.03,
        facecolor=COLOR_CARTEL_BASE, edgecolor='black', linewidth=1.2
    )
    ax.add_patch(base_rect)

    # Texto indicador del cartel
    ax.text(SOMMIER_ANCHO / 2, cartel_y0 - 0.015,
            '-- CARTEL LED "LABUROCRACIA" (proyeccion) --',
            ha='center', va='center', fontsize=7, color=COLOR_CARTEL_NEON,
            fontweight='bold')

    # Perforaciones (vistas desde arriba)
    perf_spacing = BASE_ANCHO / (N_PERFORACIONES + 1)
    for i in range(N_PERFORACIONES):
        perf_x = cartel_x0 + perf_spacing * (i + 1)
        perf_y = cartel_y0 + 0.005
        circ = plt.Circle((perf_x, perf_y), 0.008,
                          facecolor='white', edgecolor=COLOR_PERFORACION, linewidth=1.0)
        ax.add_patch(circ)

    # --- PIE DE CAMA (indicador) ---
    ax.plot([sommier_x0 - 0.05, SOMMIER_ANCHO + 0.05], [0, 0],
            color='#333333', linewidth=0.8, linestyle=':')
    ax.text(SOMMIER_ANCHO / 2, -0.03, 'PIE DE CAMA',
            ha='center', va='top', fontsize=9, color='#555555')

    # --- PATAS DEL SOMMIER (proyeccion, circulos punteados) ---
    for cx, cy in posiciones_patas():
        circ_pata = plt.Circle((cx, cy), PATA_DIAMETRO/2,
                               facecolor='none', edgecolor=COLOR_PATA,
                               linewidth=1.0, linestyle='--')
        ax.add_patch(circ_pata)
    # Etiqueta una pata
    patas = posiciones_patas()
    ax.text(patas[0][0], patas[0][1] - 0.05, 'Pata\n(x6)',
            ha='center', va='top', fontsize=6, color=COLOR_PATA)

    # --- TRANSDUCTORES (proyeccion, entre sommier y colchon) ---
    # Exciter L (izquierda, 1/4 del ancho, mitad del largo)
    ex_l = plt.Circle((SOMMIER_ANCHO * 0.25, SOMMIER_LARGO * 0.5),
                       EXCITER_DIAMETRO/2,
                       facecolor=COLOR_EXCITER, edgecolor='black',
                       linewidth=1.0, alpha=0.6)
    ax.add_patch(ex_l)
    ax.text(SOMMIER_ANCHO * 0.25, SOMMIER_LARGO * 0.5, 'Exc\nL',
            ha='center', va='center', fontsize=6, fontweight='bold', color='white')

    # Exciter R (derecha, 3/4 del ancho, mitad del largo)
    ex_r = plt.Circle((SOMMIER_ANCHO * 0.75, SOMMIER_LARGO * 0.5),
                       EXCITER_DIAMETRO/2,
                       facecolor=COLOR_EXCITER, edgecolor='black',
                       linewidth=1.0, alpha=0.6)
    ax.add_patch(ex_r)
    ax.text(SOMMIER_ANCHO * 0.75, SOMMIER_LARGO * 0.5, 'Exc\nR',
            ha='center', va='center', fontsize=6, fontweight='bold', color='white')

    # Bass Shaker BS250 (centrado)
    bs = plt.Circle((SOMMIER_ANCHO * 0.5, SOMMIER_LARGO * 0.5),
                     BASS_SHAKER_DIAMETRO/2,
                     facecolor=COLOR_BASS_SHAKER, edgecolor='black',
                     linewidth=1.0, alpha=0.4)
    ax.add_patch(bs)
    ax.text(SOMMIER_ANCHO * 0.5, SOMMIER_LARGO * 0.5, 'BS250',
            ha='center', va='center', fontsize=7, fontweight='bold',
            color='white')

    # --- CAJA ELECTRONICA (proyeccion, debajo del sommier contra cabecera) ---
    caja_x = (SOMMIER_ANCHO - CAJA_ANCHO) / 2
    caja_y = SOMMIER_LARGO - CAJA_LARGO - 0.03
    caja_rect = mpatches.Rectangle(
        (caja_x, caja_y), CAJA_ANCHO, CAJA_LARGO,
        facecolor=COLOR_CAJA, edgecolor='black', linewidth=1.0,
        alpha=0.3, linestyle='--'
    )
    ax.add_patch(caja_rect)
    ax.text(caja_x + CAJA_ANCHO/2, caja_y + CAJA_LARGO/2,
            'CAJA\nBela+Amp',
            ha='center', va='center', fontsize=6, color=COLOR_CAJA,
            fontweight='bold')

    # Cables (lineas punteadas desde transductores a caja)
    caja_cx = caja_x + CAJA_ANCHO/2
    caja_cy = caja_y + CAJA_LARGO/2
    for tx, ty in [(SOMMIER_ANCHO*0.25, SOMMIER_LARGO*0.5),
                   (SOMMIER_ANCHO*0.75, SOMMIER_LARGO*0.5),
                   (SOMMIER_ANCHO*0.5, SOMMIER_LARGO*0.5)]:
        ax.plot([tx, caja_cx], [ty, caja_cy],
                color=COLOR_CABLE, linewidth=0.6, linestyle=':', alpha=0.4)

    # Cable 220V a pared
    ax.plot([caja_cx, caja_cx], [caja_y + CAJA_LARGO, SOMMIER_LARGO + 0.08],
            color='#E02020', linewidth=1.0, linestyle='-', alpha=0.5)
    ax.text(caja_cx + 0.03, SOMMIER_LARGO + 0.06, '220V',
            fontsize=6, color='#E02020')

    # === COTAS ===

    # Cota horizontal: ancho del sommier/colchón
    dibujar_cota_horizontal(ax, sommier_x0, sommier_x0 + SOMMIER_ANCHO,
                            sommier_y0, f'{SOMMIER_ANCHO:.2f} m',
                            offset=0.15, lado='abajo', fontsize=10)

    # Cota vertical: largo del sommier/colchón
    dibujar_cota_vertical(ax, sommier_y0, sommier_y0 + SOMMIER_LARGO,
                          sommier_x0 + SOMMIER_ANCHO,
                          f'{SOMMIER_LARGO:.2f} m',
                          offset=0.15, lado='derecha', fontsize=10)

    # Cota horizontal: ancho de la base de acrílico
    dibujar_cota_horizontal(ax, cartel_x0, cartel_x0 + BASE_ANCHO,
                            cartel_y0 + 0.02, f'{BASE_ANCHO:.2f} m',
                            offset=-0.12, lado='arriba', fontsize=9)

    # Cota vertical: offset desde cabecera
    if CARTEL_OFFSET_CABECERA > 0:
        ax.annotate('', xy=(SOMMIER_ANCHO + 0.30, cabecera_y),
                    xytext=(SOMMIER_ANCHO + 0.30, cartel_y0),
                    arrowprops=dict(arrowstyle='<->', color='#E02020', lw=0.8))
        ax.text(SOMMIER_ANCHO + 0.35, (cabecera_y + cartel_y0) / 2,
                f'{CARTEL_OFFSET_CABECERA * 100:.0f} cm',
                ha='left', va='center', fontsize=8, color='#E02020',
                fontweight='bold', rotation=90)

    # --- CONFIGURACIÓN DE EJES ---
    ax.set_xlim(-0.35, SOMMIER_ANCHO + 0.55)
    ax.set_ylim(-0.35, SOMMIER_LARGO + 0.25)
    ax.set_aspect('equal')
    ax.set_xlabel('Ancho (m)', fontsize=12)
    ax.set_ylabel('Largo (m)', fontsize=12)
    ax.set_title('VISTA 1 — PLANO DE PLANTA\nInstalación "LABUROCRACIA"',
                 fontsize=16, fontweight='bold', pad=20)

    # Cuadrícula sutil
    ax.grid(True, linestyle=':', alpha=0.3, color='#CCCCCC')
    ax.tick_params(direction='out', length=4)

    # Leyenda
    legend_elements = [
        mpatches.Patch(facecolor=COLOR_SOMMIER, edgecolor='black', label='Sommier'),
        mpatches.Patch(facecolor=COLOR_COLCHON, edgecolor='#999999',
                       linestyle='--', label='Colchón'),
        mpatches.Patch(facecolor=COLOR_CARTEL_BASE, edgecolor='black',
                       label='Base acrílico (cartel LED)'),
        mpatches.Patch(facecolor=COLOR_EXCITER, edgecolor='black',
                       alpha=0.6, label='Exciters L/R'),
        mpatches.Patch(facecolor=COLOR_BASS_SHAKER, edgecolor='black',
                       alpha=0.4, label='Bass Shaker BS250'),
        mpatches.Patch(facecolor=COLOR_CAJA, edgecolor='black',
                       alpha=0.3, label='Caja electrónica'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8,
              frameon=True, fancybox=True, shadow=True)

    # Nota técnica
    ax.text(0.02, 0.02,
            'Escala: medidas en metros | Obra: "LABUROCRACIA"\n'
            'Cartel LED: 110x22cm sobre base acrilico 112x24cm\n'
            'Transductores entre sommier y colchón (proyección)\n'
            'Caja electrónica debajo del sommier (proyección)',
            transform=ax.transAxes, fontsize=7, va='bottom', ha='left',
            color='#888888', style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F8F8',
                      edgecolor='#DDDDDD'))

    plt.tight_layout()
    plt.savefig('vista_1_planta_laburocracia.png', dpi=DPI_GUARDADO,
                bbox_inches='tight', facecolor='white')
    print("  [OK] Guardada: vista_1_planta_laburocracia.png")
    plt.show()


# ==============================================================================
# VISTA 2: ELEVACIÓN LATERAL (SIDE VIEW)
# ==============================================================================

def generar_vista_elevacion():
    """Genera la vista de elevación lateral de la instalación."""
    print("\n--- Generando Vista 2: Elevacion Lateral ---")

    fig, ax = plt.subplots(figsize=(12, 10))

    # En elevacion lateral, eje X = largo (1.90m), eje Y = altura
    # Cabecera a la izquierda (X=0), pie de cama a la derecha (X=1.90)

    # --- PISO ---
    ax.axhline(y=0, color='#444444', linewidth=2.0)
    ax.fill_between([-0.3, SOMMIER_LARGO + 0.3], -0.05, 0,
                    color='#E8E8E8', hatch='///', alpha=0.5)
    ax.text(SOMMIER_LARGO / 2, -0.03, 'NIVEL DE PISO',
            ha='center', va='top', fontsize=8, color='#666666')

    # --- PATAS DEL SOMMIER (vista lateral: se ven 3 patas) ---
    # En vista lateral se ven: esquina trasera, central, esquina delantera
    margen = 0.05 + PATA_DIAMETRO/2
    patas_x_lateral = [margen, SOMMIER_LARGO / 2, SOMMIER_LARGO - margen]
    for px in patas_x_lateral:
        pata = mpatches.Rectangle(
            (px - PATA_DIAMETRO/2, 0), PATA_DIAMETRO, PATA_ALTO,
            facecolor=COLOR_PATA, edgecolor='black', linewidth=0.8
        )
        ax.add_patch(pata)
    ax.text(patas_x_lateral[2] + 0.06, PATA_ALTO / 2, 'Patas\n15cm',
            ha='left', va='center', fontsize=6, color=COLOR_PATA)

    # --- CAJA ELECTRONICA (en el piso, contra cabecera) ---
    caja_x = SOMMIER_LARGO - CAJA_LARGO - 0.03 - CARTEL_OFFSET_CABECERA
    caja_rect = mpatches.Rectangle(
        (caja_x, 0), CAJA_LARGO, CAJA_ALTO,
        facecolor=COLOR_CAJA, edgecolor='black', linewidth=1.0, alpha=0.7
    )
    ax.add_patch(caja_rect)
    ax.text(caja_x + CAJA_LARGO/2, CAJA_ALTO/2, 'Bela+Amp',
            ha='center', va='center', fontsize=6, color='white', fontweight='bold')

    # Cable 220V de caja a pared
    ax.plot([caja_x + CAJA_LARGO, SOMMIER_LARGO + 0.02],
            [CAJA_ALTO/2, CAJA_ALTO/2],
            color='#E02020', linewidth=1.0, linestyle='-', alpha=0.6)

    # --- SOMMIER (ahora sobre las patas) ---
    sommier_y0 = PATA_ALTO
    sommier = mpatches.FancyBboxPatch(
        (0, sommier_y0), SOMMIER_LARGO, SOMMIER_ALTO,
        boxstyle="round,pad=0.005",
        facecolor=COLOR_SOMMIER, edgecolor='black', linewidth=1.8
    )
    ax.add_patch(sommier)
    ax.text(SOMMIER_LARGO / 2, sommier_y0 + SOMMIER_ALTO / 2, 'SOMMIER',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='#666666', style='italic')

    # --- TRANSDUCTORES (entre sommier y colchon, vista de perfil) ---
    trans_y = sommier_y0 + SOMMIER_ALTO  # sobre el sommier

    # Bass Shaker BS250 (centrado, el mas alto)
    bs_x = SOMMIER_LARGO / 2 - BASS_SHAKER_DIAMETRO / 2
    bs_rect = mpatches.Rectangle(
        (bs_x, trans_y), BASS_SHAKER_DIAMETRO, BASS_SHAKER_ALTO,
        facecolor=COLOR_BASS_SHAKER, edgecolor='black', linewidth=0.8, alpha=0.8
    )
    ax.add_patch(bs_rect)
    ax.text(SOMMIER_LARGO / 2, trans_y + BASS_SHAKER_ALTO / 2, 'BS250',
            ha='center', va='center', fontsize=6, color='white', fontweight='bold')

    # Exciter (uno visible en perfil, a 1/4 del largo — el otro queda detras)
    exc_x = SOMMIER_LARGO * 0.25 - EXCITER_DIAMETRO / 2
    exc_rect = mpatches.Rectangle(
        (exc_x, trans_y), EXCITER_DIAMETRO, EXCITER_ALTO,
        facecolor=COLOR_EXCITER, edgecolor='black', linewidth=0.8, alpha=0.8
    )
    ax.add_patch(exc_rect)
    ax.text(exc_x + EXCITER_DIAMETRO/2, trans_y + EXCITER_ALTO + 0.01, 'Exc',
            ha='center', va='bottom', fontsize=5, color=COLOR_EXCITER)

    # Cables desde transductores bajando a caja
    for tx in [SOMMIER_LARGO/2, SOMMIER_LARGO*0.25]:
        ax.plot([tx, caja_x + CAJA_LARGO/2], [trans_y, CAJA_ALTO],
                color=COLOR_CABLE, linewidth=0.6, linestyle='--', alpha=0.4)

    # --- COLCHON (ahora sobre los transductores) ---
    colchon_y0 = trans_y + max(EXCITER_ALTO, BASS_SHAKER_ALTO)
    colchon = mpatches.FancyBboxPatch(
        (0, colchon_y0), COLCHON_LARGO, COLCHON_ALTO,
        boxstyle="round,pad=0.008",
        facecolor=COLOR_COLCHON, edgecolor='#999999', linewidth=1.2
    )
    ax.add_patch(colchon)
    ax.text(COLCHON_LARGO / 2, colchon_y0 + COLCHON_ALTO / 2, 'COLCHON',
            ha='center', va='center', fontsize=10, color='#888888')

    # Altura total cama (desde piso)
    altura_cama = colchon_y0 + COLCHON_ALTO

    # --- PARED (detrás de la cabecera) ---
    pared_x = -0.05
    ax.plot([pared_x, pared_x], [0, CARTEL_ALTURA_PISO + BASE_ALTO + 0.3],
            color='#AAAAAA', linewidth=3.0, solid_capstyle='butt')
    ax.text(pared_x - 0.03, (CARTEL_ALTURA_PISO + BASE_ALTO + 0.3) / 2,
            'P\nA\nR\nE\nD', ha='center', va='center', fontsize=7,
            color='#999999', fontweight='bold')

    # --- BASE DE ACRÍLICO DEL CARTEL (VISTA DE PERFIL) ---
    # En vista lateral, el cartel se ve de PERFIL (de canto).
    # Solo se ve su espesor (~3cm) y su altura (24cm).
    CARTEL_ESPESOR = 0.03  # m (~3cm espesor del acrílico + neón)

    # Posición horizontal: corrido 10cm desde la cabecera (X=0) hacia el interior
    base_x0 = CARTEL_OFFSET_CABECERA
    base_y0 = CARTEL_ALTURA_PISO

    # Base de acrílico (perfil): rectángulo delgado
    base_acrilico = mpatches.Rectangle(
        (base_x0, base_y0), CARTEL_ESPESOR, BASE_ALTO,
        facecolor=COLOR_CARTEL_BASE, edgecolor='black', linewidth=1.5
    )
    ax.add_patch(base_acrilico)

    # Borde rojo del neón LED (visible como línea en el frente del perfil)
    neon_y0 = base_y0 + (BASE_ALTO - CARTEL_ALTO) / 2
    ax.plot([base_x0, base_x0], [neon_y0, neon_y0 + CARTEL_ALTO],
            color=COLOR_CARTEL_NEON, linewidth=2.5, solid_capstyle='round')

    # Etiqueta del cartel (con línea de llamada)
    label_x = base_x0 + CARTEL_ESPESOR + 0.25
    label_y = base_y0 + BASE_ALTO / 2
    ax.annotate('Cartel LED\n"LABUROCRACIA"\n(vista de perfil)\n110x22 cm\nBase: 112x24 cm',
                xy=(base_x0 + CARTEL_ESPESOR, label_y),
                xytext=(label_x, label_y),
                fontsize=8, color='#333333', va='center',
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.0),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8F0',
                          edgecolor='#CCCCCC'))

    # --- LÍNEA DE CUELGUE (en perfil, las 3 perforaciones se superponen) ---
    techo_y = CARTEL_ALTURA_PISO + BASE_ALTO + 0.25
    cuelgue_x = base_x0 + CARTEL_ESPESOR / 2
    ax.plot([cuelgue_x, cuelgue_x], [base_y0 + BASE_ALTO, techo_y],
            color='#AAAAAA', linewidth=0.8, linestyle='--')
    ax.text(cuelgue_x, techo_y + 0.02,
            'Cuelgue (3 puntos\nsuperpuestos en perfil)',
            ha='center', va='bottom', fontsize=7, color='#999999')

    # === COTAS ===

    # Cota vertical: altura del piso al cartel (2.00m)
    dibujar_cota_vertical(ax, 0, CARTEL_ALTURA_PISO,
                          SOMMIER_LARGO + 0.05,
                          f'{CARTEL_ALTURA_PISO:.2f} m',
                          offset=0.12, lado='derecha', fontsize=10)

    # Cota vertical: altura del sommier
    dibujar_cota_vertical(ax, 0, SOMMIER_ALTO,
                          SOMMIER_LARGO + 0.05,
                          f'{SOMMIER_ALTO:.2f} m',
                          offset=0.35, lado='derecha', fontsize=9)

    # Cota vertical: altura del colchón
    dibujar_cota_vertical(ax, SOMMIER_ALTO, SOMMIER_ALTO + COLCHON_ALTO,
                          SOMMIER_LARGO + 0.05,
                          f'{COLCHON_ALTO:.2f} m',
                          offset=0.55, lado='derecha', fontsize=9)

    # Cota vertical: altura total cama
    dibujar_cota_vertical(ax, 0, altura_cama,
                          SOMMIER_LARGO + 0.05,
                          f'{altura_cama:.2f} m\n(total cama)',
                          offset=0.75, lado='derecha', fontsize=9)

    # Cota vertical: altura base acrílico (24cm)
    dibujar_cota_vertical(ax, base_y0, base_y0 + BASE_ALTO,
                          base_x0 + CARTEL_ESPESOR + 0.02,
                          f'{BASE_ALTO * 100:.0f} cm',
                          offset=0.06, lado='derecha', fontsize=8)

    # Cota horizontal: largo del sommier/colchón
    dibujar_cota_horizontal(ax, 0, SOMMIER_LARGO,
                            0, f'{SOMMIER_LARGO:.2f} m',
                            offset=0.12, lado='abajo', fontsize=10)

    # Cota horizontal: espesor del cartel (perfil)
    dibujar_cota_horizontal(ax, base_x0, base_x0 + CARTEL_ESPESOR,
                            base_y0 + BASE_ALTO,
                            f'{CARTEL_ESPESOR * 100:.0f} cm',
                            offset=-0.06, lado='arriba', fontsize=8)

    # Cota horizontal: offset desde cabecera/pared
    if CARTEL_OFFSET_CABECERA > 0:
        ax.annotate('', xy=(base_x0, -0.08),
                    xytext=(0, -0.08),
                    arrowprops=dict(arrowstyle='<->', color='#E02020', lw=0.8))
        ax.text(base_x0 / 2, -0.10,
                f'{CARTEL_OFFSET_CABECERA * 100:.0f} cm',
                ha='center', va='top', fontsize=8, color='#E02020',
                fontweight='bold')

    # --- CONFIGURACIÓN DE EJES ---
    ax.set_xlim(-0.30, SOMMIER_LARGO + 0.95)
    ax.set_ylim(-0.20, techo_y + 0.15)
    ax.set_aspect('equal')
    ax.set_xlabel('Posicion horizontal -- Largo (m)', fontsize=12)
    ax.set_ylabel('Altura (m)', fontsize=12)
    ax.set_title('VISTA 2 -- ELEVACION LATERAL\n'
                 'Instalacion "LABUROCRACIA"',
                 fontsize=16, fontweight='bold', pad=20)

    # Cuadrícula sutil
    ax.grid(True, linestyle=':', alpha=0.3, color='#CCCCCC')
    ax.tick_params(direction='out', length=4)

    # Leyenda
    legend_elements = [
        mpatches.Patch(facecolor=COLOR_SOMMIER, edgecolor='black', label='Sommier (0.30m alto)'),
        mpatches.Patch(facecolor=COLOR_COLCHON, edgecolor='#999999', label='Colchon (0.25m alto)'),
        mpatches.Patch(facecolor=COLOR_CARTEL_BASE, edgecolor='black',
                       label='Base acrilico (perfil ~3cm)'),
        mpatches.Patch(facecolor='none', edgecolor=COLOR_CARTEL_NEON, linewidth=2,
                       label='Neon LED (perfil)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
              frameon=True, fancybox=True, shadow=True)

    # Nota técnica
    ax.text(0.02, 0.02,
            'Escala: medidas en metros | Obra: "LABUROCRACIA"\n'
            'Cartel a 2.00m del piso, centrado sobre cabecera,\n'
            'corrido 10cm hacia el interior del colchon.\n'
            'Vista de perfil: espesor ~3cm (acrilico + neon).',
            transform=ax.transAxes, fontsize=7, va='bottom', ha='left',
            color='#888888', style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F8F8',
                      edgecolor='#DDDDDD'))

    plt.tight_layout()
    plt.savefig('vista_2_elevacion_laburocracia.png', dpi=DPI_GUARDADO,
                bbox_inches='tight', facecolor='white')
    print("  Guardada: vista_2_elevacion_laburocracia.png")
    plt.show()


# ==============================================================================
# FUNCIONES AUXILIARES PARA 3D ISOMETRICA
# ==============================================================================

def dibujar_prisma(ax, x, y, z, dx, dy, dz, color, edgecolor='black',
                   alpha=0.8, linewidth=0.8, label=None):
    """Dibuja un prisma rectangular en 3D."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Definir las 6 caras del prisma
    vertices = [
        [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],       # cara inferior
        [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]  # cara superior
    ]

    caras = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # frente
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # atras
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # izquierda
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # derecha
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # abajo
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # arriba
    ]

    coleccion = Poly3DCollection(caras, alpha=alpha, facecolor=color,
                                  edgecolor=edgecolor, linewidths=linewidth)
    ax.add_collection3d(coleccion)

    if label:
        ax.text(x + dx/2, y + dy/2, z + dz + 0.01, label,
                ha='center', va='bottom', fontsize=7, color='#333333')


def dibujar_cilindro(ax, cx, cy, z_base, radio, altura, color,
                     edgecolor='black', alpha=0.7, n_segments=20, label=None):
    """Dibuja un cilindro en 3D."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Generar puntos del circulo
    theta = np.linspace(0, 2*np.pi, n_segments)
    x_circle = cx + radio * np.cos(theta)
    y_circle = cy + radio * np.sin(theta)

    # Cara superior e inferior
    z_top = z_base + altura
    verts_bottom = list(zip(x_circle, y_circle, [z_base]*n_segments))
    verts_top = list(zip(x_circle, y_circle, [z_top]*n_segments))

    # Dibujar tapas
    ax.add_collection3d(Poly3DCollection([verts_bottom], alpha=alpha,
                                         facecolor=color, edgecolor=edgecolor,
                                         linewidths=0.3))
    ax.add_collection3d(Poly3DCollection([verts_top], alpha=alpha,
                                         facecolor=color, edgecolor=edgecolor,
                                         linewidths=0.3))

    # Pared lateral (aproximada con quads)
    for i in range(n_segments - 1):
        cara = [
            (x_circle[i], y_circle[i], z_base),
            (x_circle[i+1], y_circle[i+1], z_base),
            (x_circle[i+1], y_circle[i+1], z_top),
            (x_circle[i], y_circle[i], z_top),
        ]
        ax.add_collection3d(Poly3DCollection([cara], alpha=alpha * 0.8,
                                             facecolor=color, edgecolor=edgecolor,
                                             linewidths=0.2))

    if label:
        ax.text(cx, cy, z_top + 0.02, label,
                ha='center', va='bottom', fontsize=6, color='#333333')


def posiciones_patas():
    """Retorna las posiciones (cx, cy) de las 6 patas del sommier."""
    margen = 0.05  # distancia del borde
    return [
        # 4 esquinas
        (margen + PATA_DIAMETRO/2, margen + PATA_DIAMETRO/2),
        (SOMMIER_ANCHO - margen - PATA_DIAMETRO/2, margen + PATA_DIAMETRO/2),
        (margen + PATA_DIAMETRO/2, SOMMIER_LARGO - margen - PATA_DIAMETRO/2),
        (SOMMIER_ANCHO - margen - PATA_DIAMETRO/2, SOMMIER_LARGO - margen - PATA_DIAMETRO/2),
        # 2 centrales laterales (a mitad del largo)
        (margen + PATA_DIAMETRO/2, SOMMIER_LARGO / 2),
        (SOMMIER_ANCHO - margen - PATA_DIAMETRO/2, SOMMIER_LARGO / 2),
    ]


def dibujar_componentes_3d(ax):
    """Dibuja todos los componentes de la instalacion en un eje 3D."""

    # === PATAS DEL SOMMIER ===
    for cx, cy in posiciones_patas():
        dibujar_cilindro(ax, cx, cy, 0, PATA_DIAMETRO/2, PATA_ALTO,
                         COLOR_PATA, alpha=0.6)

    # === CAJA DE ELECTRONICA (en el piso, contra cabecera, centrada en X) ===
    caja_x = (SOMMIER_ANCHO - CAJA_ANCHO) / 2
    caja_y = SOMMIER_LARGO - CAJA_LARGO - 0.03  # contra cabecera con un poco de margen
    dibujar_prisma(ax, caja_x, caja_y, 0,
                   CAJA_ANCHO, CAJA_LARGO, CAJA_ALTO,
                   COLOR_CAJA, alpha=0.7, label='Bela+Amp')

    # Cable 220V saliendo de la caja hacia la pared (cabecera)
    cable_x = caja_x + CAJA_ANCHO / 2
    ax.plot([cable_x, cable_x], [caja_y + CAJA_LARGO, SOMMIER_LARGO + 0.05],
            [CAJA_ALTO/2, CAJA_ALTO/2],
            color=COLOR_CABLE, linewidth=1.5, linestyle='-')
    ax.text(cable_x, SOMMIER_LARGO + 0.06, CAJA_ALTO/2, '220V',
            ha='center', fontsize=6, color='#E02020')

    # === SOMMIER ===
    dibujar_prisma(ax, 0, 0, PATA_ALTO,
                   SOMMIER_ANCHO, SOMMIER_LARGO, SOMMIER_ALTO,
                   COLOR_SOMMIER, alpha=0.5, linewidth=1.0)

    # === TRANSDUCTORES (entre sommier y colchon) ===
    z_transductores = PATA_ALTO + SOMMIER_ALTO

    # Exciter L (izquierda, a 1/4 del ancho)
    ex_l_x = SOMMIER_ANCHO * 0.25
    ex_l_y = SOMMIER_LARGO * 0.5
    dibujar_cilindro(ax, ex_l_x, ex_l_y, z_transductores,
                     EXCITER_DIAMETRO/2, EXCITER_ALTO,
                     COLOR_EXCITER, alpha=0.9, label='Exc L')

    # Exciter R (derecha, a 3/4 del ancho)
    ex_r_x = SOMMIER_ANCHO * 0.75
    ex_r_y = SOMMIER_LARGO * 0.5
    dibujar_cilindro(ax, ex_r_x, ex_r_y, z_transductores,
                     EXCITER_DIAMETRO/2, EXCITER_ALTO,
                     COLOR_EXCITER, alpha=0.9, label='Exc R')

    # Bass Shaker (centrado)
    bs_x = SOMMIER_ANCHO * 0.5
    bs_y = SOMMIER_LARGO * 0.5
    dibujar_cilindro(ax, bs_x, bs_y, z_transductores,
                     BASS_SHAKER_DIAMETRO/2, BASS_SHAKER_ALTO,
                     COLOR_BASS_SHAKER, alpha=0.8, label='BS250')

    # Cables de los transductores hacia la caja (lineas)
    z_cable = PATA_ALTO / 2
    for tx, ty in [(ex_l_x, ex_l_y), (ex_r_x, ex_r_y), (bs_x, bs_y)]:
        # Cable baja por dentro hacia la caja
        ax.plot([tx, cable_x], [ty, caja_y + CAJA_LARGO/2],
                [z_transductores, CAJA_ALTO],
                color=COLOR_CABLE, linewidth=0.8, linestyle='--', alpha=0.5)

    # === COLCHON ===
    z_colchon = PATA_ALTO + SOMMIER_ALTO + max(EXCITER_ALTO, BASS_SHAKER_ALTO)
    dibujar_prisma(ax, 0, 0, z_colchon,
                   COLCHON_ANCHO, COLCHON_LARGO, COLCHON_ALTO,
                   COLOR_COLCHON, alpha=0.4, linewidth=1.0)

    # === CARTEL LED (sobre la cabecera) ===
    # El cartel cuelga a 2.00m del piso, centrado en X, corrido 10cm adentro
    cartel_x = (SOMMIER_ANCHO - BASE_ANCHO) / 2
    cartel_y = SOMMIER_LARGO - CARTEL_OFFSET_CABECERA
    cartel_z = CARTEL_ALTURA_PISO

    # Base de acrilico
    dibujar_prisma(ax, cartel_x, cartel_y - CARTEL_ESPESOR/2, cartel_z,
                   BASE_ANCHO, CARTEL_ESPESOR, BASE_ALTO,
                   COLOR_CARTEL_BASE, alpha=0.8, linewidth=1.0)

    # Borde neon LED (como un rectangulo fino en el frente)
    neon_x = cartel_x + (BASE_ANCHO - CARTEL_ANCHO) / 2
    neon_z = cartel_z + (BASE_ALTO - CARTEL_ALTO) / 2
    neon_y = cartel_y - CARTEL_ESPESOR/2 - 0.002

    # Dibujar marco del neon como lineas
    neon_pts_x = [neon_x, neon_x + CARTEL_ANCHO, neon_x + CARTEL_ANCHO, neon_x, neon_x]
    neon_pts_z = [neon_z, neon_z, neon_z + CARTEL_ALTO, neon_z + CARTEL_ALTO, neon_z]
    neon_pts_y = [neon_y] * 5
    ax.plot(neon_pts_x, neon_pts_y, neon_pts_z,
            color=COLOR_CARTEL_NEON, linewidth=2.5)

    # Texto LABUROCRACIA
    ax.text(SOMMIER_ANCHO/2, neon_y - 0.01, cartel_z + BASE_ALTO/2,
            'LABUROCRACIA', ha='center', va='center',
            fontsize=7, color=COLOR_CARTEL_NEON, fontweight='bold')

    # Lineas de cuelgue
    techo_z = cartel_z + BASE_ALTO + 0.15
    perf_spacing = BASE_ANCHO / (N_PERFORACIONES + 1)
    for i in range(N_PERFORACIONES):
        px = cartel_x + perf_spacing * (i + 1)
        py = cartel_y
        ax.plot([px, px], [py, py], [cartel_z + BASE_ALTO, techo_z],
                color='#AAAAAA', linewidth=0.6, linestyle='--')

    # Cable 12V desde caja al cartel
    ax.plot([cable_x, SOMMIER_ANCHO/2],
            [caja_y + CAJA_LARGO, cartel_y],
            [CAJA_ALTO, cartel_z],
            color='#E02020', linewidth=0.8, linestyle=':', alpha=0.6)

    return z_colchon


def configurar_ejes_3d(ax, elev, azim, titulo):
    """Configura los ejes de una vista 3D."""
    ax.set_xlabel('Ancho (m)', fontsize=9, labelpad=5)
    ax.set_ylabel('Largo (m)', fontsize=9, labelpad=5)
    ax.set_zlabel('Altura (m)', fontsize=9, labelpad=5)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)

    ax.view_init(elev=elev, azim=azim)

    # Limites
    x_span = (SOMMIER_ANCHO + 0.15) - (-0.15)
    y_span = (SOMMIER_LARGO + 0.15) - (-0.15)
    z_span = (CARTEL_ALTURA_PISO + BASE_ALTO + 0.20) - (-0.05)

    ax.set_xlim(-0.15, SOMMIER_ANCHO + 0.15)
    ax.set_ylim(-0.15, SOMMIER_LARGO + 0.15)
    ax.set_zlim(-0.05, CARTEL_ALTURA_PISO + BASE_ALTO + 0.20)

    # Mantener la proporción real física (evita que el sommier de 1x1.90m se vea cuadrado)
    ax.set_box_aspect((x_span, y_span, z_span))

    # Estilo
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#DDDDDD')
    ax.yaxis.pane.set_edgecolor('#DDDDDD')
    ax.zaxis.pane.set_edgecolor('#DDDDDD')
    ax.grid(True, alpha=0.2, linestyle=':')
    ax.tick_params(labelsize=7)


# ==============================================================================
# VISTA 3: ISOMETRICA DESDE PIE DE CAMA (frente + lateral)
# ==============================================================================

def generar_vista_iso_frente():
    """Vista isometrica desde la esquina del pie de cama."""
    print("\n--- Generando Vista 3: Isometrica (pie de cama) ---")

    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection='3d')

    dibujar_componentes_3d(ax)
    configurar_ejes_3d(ax, elev=25, azim=-55,
                       titulo='VISTA 3 -- ISOMETRICA (desde pie de cama)\n'
                              'Instalacion "LABUROCRACIA"')

    # Leyenda manual
    legend_elements = [
        mpatches.Patch(facecolor=COLOR_SOMMIER, edgecolor='black', label='Sommier'),
        mpatches.Patch(facecolor=COLOR_COLCHON, edgecolor='black', label='Colchon'),
        mpatches.Patch(facecolor=COLOR_CARTEL_BASE, edgecolor='black', label='Base acrilico'),
        mpatches.Patch(facecolor=COLOR_PATA, edgecolor='black', label='Patas (x6)'),
        mpatches.Patch(facecolor=COLOR_EXCITER, edgecolor='black', label='Exciters L/R'),
        mpatches.Patch(facecolor=COLOR_BASS_SHAKER, edgecolor='black', label='Bass Shaker BS250'),
        mpatches.Patch(facecolor=COLOR_CAJA, edgecolor='black', label='Caja electronica'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8,
              frameon=True, fancybox=True, shadow=True)

    plt.tight_layout()
    plt.savefig('vista_3_iso_frente.png', dpi=DPI_GUARDADO,
                bbox_inches='tight', facecolor='white')
    print("  Guardada: vista_3_iso_frente.png")
    plt.show()


# ==============================================================================
# VISTA 4: ISOMETRICA DESDE CABECERA (se ve el cartel de frente)
# ==============================================================================

def generar_vista_iso_cabecera():
    """Vista isometrica desde la esquina de la cabecera."""
    print("\n--- Generando Vista 4: Isometrica (cabecera) ---")

    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection='3d')

    dibujar_componentes_3d(ax)
    configurar_ejes_3d(ax, elev=20, azim=125,
                       titulo='VISTA 4 -- ISOMETRICA (desde cabecera)\n'
                              'Instalacion "LABUROCRACIA"')

    legend_elements = [
        mpatches.Patch(facecolor=COLOR_SOMMIER, edgecolor='black', label='Sommier'),
        mpatches.Patch(facecolor=COLOR_COLCHON, edgecolor='black', label='Colchon'),
        mpatches.Patch(facecolor=COLOR_CARTEL_BASE, edgecolor='black', label='Base acrilico'),
        mpatches.Patch(facecolor=COLOR_PATA, edgecolor='black', label='Patas (x6)'),
        mpatches.Patch(facecolor=COLOR_EXCITER, edgecolor='black', label='Exciters L/R'),
        mpatches.Patch(facecolor=COLOR_BASS_SHAKER, edgecolor='black', label='Bass Shaker BS250'),
        mpatches.Patch(facecolor=COLOR_CAJA, edgecolor='black', label='Caja electronica'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8,
              frameon=True, fancybox=True, shadow=True)

    plt.tight_layout()
    plt.savefig('vista_4_iso_cabecera.png', dpi=DPI_GUARDADO,
                bbox_inches='tight', facecolor='white')
    print("  Guardada: vista_4_iso_cabecera.png")
    plt.show()


# ==============================================================================
# VISTA 5: ISOMETRICA CENITAL (desde arriba)
# ==============================================================================

def generar_vista_iso_cenital():
    """Vista isometrica cenital (desde arriba, elevacion alta)."""
    print("\n--- Generando Vista 5: Isometrica cenital ---")

    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection='3d')

    dibujar_componentes_3d(ax)
    configurar_ejes_3d(ax, elev=60, azim=-45,
                       titulo='VISTA 5 -- ISOMETRICA CENITAL (desde arriba)\n'
                              'Instalacion "LABUROCRACIA"')

    legend_elements = [
        mpatches.Patch(facecolor=COLOR_SOMMIER, edgecolor='black', label='Sommier'),
        mpatches.Patch(facecolor=COLOR_COLCHON, edgecolor='black', label='Colchon'),
        mpatches.Patch(facecolor=COLOR_CARTEL_BASE, edgecolor='black', label='Base acrilico'),
        mpatches.Patch(facecolor=COLOR_PATA, edgecolor='black', label='Patas (x6)'),
        mpatches.Patch(facecolor=COLOR_EXCITER, edgecolor='black', label='Exciters L/R'),
        mpatches.Patch(facecolor=COLOR_BASS_SHAKER, edgecolor='black', label='Bass Shaker BS250'),
        mpatches.Patch(facecolor=COLOR_CAJA, edgecolor='black', label='Caja electronica'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8,
              frameon=True, fancybox=True, shadow=True)

    plt.tight_layout()
    plt.savefig('vista_5_iso_cenital.png', dpi=DPI_GUARDADO,
                bbox_inches='tight', facecolor='white')
    print("  Guardada: vista_5_iso_cenital.png")
    plt.show()


# ==============================================================================
# EJECUCION
# ==============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  PLANOS TECNICOS -- Instalacion 'LABUROCRACIA'")
    print("=" * 60)

    generar_vista_planta()
    generar_vista_elevacion()
    generar_vista_iso_frente()
    generar_vista_iso_cabecera()
    generar_vista_iso_cenital()

    print("\n Todas las vistas han sido generadas.")
    print("   Archivos guardados:")
    print("   - vista_1_planta_laburocracia.png")
    print("   - vista_2_elevacion_laburocracia.png")
    print("   - vista_3_iso_frente.png")
    print("   - vista_4_iso_cabecera.png")
    print("   - vista_5_iso_cenital.png")

