#!/usr/bin/env python3
"""Analiza najgorszego przypadku drabinki przycisków HMI (O-035, 9.11.2026).

Węzeł drabinki: Rb (2,2 kΩ, dołączany przy obudzonym HMI) || Rexbias (150 kΩ, stały, budzenie)
od węzła zasilania drabinki; przyciski 1–4 zwierają do masy rezystory R1–R4 (równolegle).
Mierzony stosunek r = U_węzła / U_zasilania_drabinki (dzielniki odcinane w uśpieniu).
Uruchomienie: python3 scripts/drabinka_hmi.py  — kod wyjścia 1, gdy okna nie są rozłączne.
"""
import sys
RB, REXB = 2200.0, 150e3
R = [2260.0, 1500.0, 499.0, 118.0]          # przyciski 1–4, E96, 1 %
TOL = 0.015                                  # 1 % + dryf 100 ppm/K
STYK = (0.0, 10.0)                           # rezystancja styku, Ω
UPLYW = (None, ('masa', 50e3), ('B+', 100e3))
POMIAR = 0.01                                # dwa dzielniki 0,5 %
ADC = 0.001                                  # ułamek zakresu
NAZWA = {1: 'P1', 2: 'P2', 4: 'P3', 8: 'P4'}

def okno(n):
    wc = [i for i in range(4) if n >> i & 1]; v = []
    for sr in (-1, 1):
        for sb in (-1, 1):
            for c in STYK:
                for lk in UPLYW:
                    gd = sum(1 / (R[i] * (1 + sr * TOL) + c) for i in wc)
                    gb = 1 / (RB * (1 - sb * TOL)) + 1 / REXB
                    if lk and lk[0] == 'masa': gd += 1 / lk[1]
                    if lk and lk[0] == 'B+': gb += 1 / lk[1]
                    r = gb / (gb + gd)
                    v += [r * (1 - POMIAR) - ADC, r * (1 + POMIAR) + ADC]
    return min(v), max(v)

W = {n: okno(n) for n in range(16)}
blad = 0; najmniej = 1
for a, ai in {1: 0, 2: 1, 4: 2, 8: 3}.items():
    for b in range(16):
        if a == b or (b >> ai & 1): continue      # kombinacja zawierająca a może czytać się jako a
        gap = max(W[a][0] - W[b][1], W[b][0] - W[a][1]); najmniej = min(najmniej, gap)
        if gap <= 0: print(f'NAKŁADANIE: {NAZWA[a]} i stan {b}'); blad = 1
for b in range(1, 16):
    if W[0][0] <= W[b][1]: print(f'NAKŁADANIE: brak naciśnięcia i stan {b}'); blad = 1
print(f'Minimalny odstęp okien: {najmniej:.4f} zakresu ({najmniej*4096:.0f} LSB)')
r1 = max(R) * (1 + TOL) + STYK[1]; rx = REXB * (1 - TOL)
print(f'Budzenie przy 7 V (tylko Rexbias): węzeł {7*r1/(r1+rx):.2f} V wobec progu 4,0 V')
for n in sorted(W, key=lambda k: -W[k][0]):
    p = '+'.join(NAZWA[1 << i] for i in range(4) if n >> i & 1) or 'brak'
    print(f'  {p:12s} {W[n][0]:.4f} – {W[n][1]:.4f}')
sys.exit(blad)
