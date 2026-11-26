#!/usr/bin/env python3
"""Bilans rozmiaru profilu map i RAM na 3 profile (O-067, pytanie Pawla 26.11.2026).

Profil = komplet map jednego trybu jazdy (np. STD, RACE, WET; ECU-IGN-039, maks. 3).
Komorki map int16 (zaplon 0,1 deg, dawka 0,01 ms / VE 0,1 %), cele AFR i pompa oleju uint8;
osie int16. Siatki to propozycja - po zmianie tabel skrypt przelicza wszystko.
Kod wyjscia 1, gdy RAM ECU przekracza granice SYS-RES-001 (50 % z 128 KB).
"""
import sys

def mapa(n_x, n_y=1, b=2):
    """Bajty mapy: komorki + osie (int16)."""
    return n_x * n_y * b + 2 * n_x + (2 * n_y if n_y > 1 else 0)

def krzywa(n=16):
    return mapa(n)

NAGLOWEK = 64  # wersja formatu, nazwa profilu 16 znakow, granice, CRC-32, numer sekwencji

def profil_a():
    """MVP-A: gaznik, AC-CDI, bez TPS - zaplon tylko od obrotow (ECU-IGN-020)."""
    return [
        ('zaplon od obrotow (32 pkt)', mapa(32)),
        ('korekta zaplonu: temp. cieczy', krzywa()),
        ('korekta zaplonu: temp. powietrza', krzywa()),
        ('ogranicznik: prog, histereza, metoda', 16),
        ('progi wentylatora', 8),
        ('naglowek, CRC', NAGLOWEK),
    ]

def profil_bc(nx=32, ny=20):
    """B/C: wtrysk TPI/TBI, TPS - mapy obroty x obciazenie."""
    return [
        (f'dawka / VE {nx}x{ny}', mapa(nx, ny)),
        (f'zaplon {nx}x{ny}', mapa(nx, ny)),
        (f'kat wtrysku {nx}x{ny}', mapa(nx, ny)),
        (f'cel AFR {nx}x{ny} (uint8)', mapa(nx, ny, 1)),
        (f'pompa oleju {nx}x{ny} (uint8, TPI)', mapa(nx, ny, 1)),
        ('12 krzywych korekt (rozgrzewanie, po starcie, temp., cisnienie, przyspieszenie, czas martwy, rozruch, zaplon)', 12 * krzywa()),
        ('ogranicznik, wentylator', 24),
        ('naglowek, CRC', NAGLOWEK),
    ]

# RAM ECU z budzetu (scripts/budzet_wykonalnosci.py) bez pozycji map
RAM_BEZ_MAP = (19.5, 30.5)   # KB min, max
GRANICA_RAM = 64.0           # KB, SYS-RES-001

def pokaz(nazwa, pozycje):
    print(nazwa)
    for n, b in pozycje:
        print(f'  {n:70s} {b:6d} B')
    s = sum(b for _, b in pozycje)
    print(f'  {"razem":70s} {s:6d} B = {s/1024:.2f} KB')
    return s

def main():
    a = pokaz('Profil MVP-A', profil_a())
    bc = pokaz('\nProfil B/C (siatka 32 x 20)', profil_bc())
    limit = 8 * 1024
    print(f'\nLimit profilu {limit//1024} KB: MVP-A {100*a/limit:.0f} %, B/C {100*bc/limit:.0f} %')
    ok = bc <= limit
    print('\nRAM ECU - 3 profile + bufor zapisu (4 bufory po limicie profilu):')
    mapy = 4 * limit / 1024
    lo, hi = RAM_BEZ_MAP[0] + mapy, RAM_BEZ_MAP[1] + mapy
    print(f'  pozostaly RAM {RAM_BEZ_MAP[0]:.1f}-{RAM_BEZ_MAP[1]:.1f} KB + mapy {mapy:.0f} KB = {lo:.1f}-{hi:.1f} KB, granica {GRANICA_RAM:.0f} KB')
    ok &= hi <= GRANICA_RAM
    print(f'  rzeczywiste zuzycie map: MVP-A {4*a/1024:.1f} KB, B/C {4*bc/1024:.1f} KB')
    print('\nOK' if ok else '\nPRZEKROCZENIE')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
