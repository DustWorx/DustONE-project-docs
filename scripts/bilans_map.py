#!/usr/bin/env python3
"""Bilans rozmiaru profilu map i RAM na mapy (O-067, pytanie Pawla 26.11.2026; zmiana 27.11.2026).

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

# W RAM dwa miejsca: profil aktywny + "nastepny" - wspolne dla zmiany profilu z HMI
# (wczytanie z W25Q128) i zapisu z aplikacji (firmware.md D.3, decyzja Pawla 27.11.2026).
# Do 27.11.2026: 3 profile + bufor zapisu (4 miejsca).
MIEJSCA = 2
LIMIT_KB = 8                 # KB, limit profilu

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
    limit = LIMIT_KB * 1024
    print(f'\nLimit profilu {limit//1024} KB: MVP-A {100*a/limit:.0f} %, B/C {100*bc/limit:.0f} %')
    ok = bc <= limit
    from budzet_wykonalnosci import RAM, SZK_APP_RAM, G_RAM, RAM_KB  # pozostaly RAM z budzetu
    bez = [(lo, hi) for n, lo, hi in RAM if not n.startswith('mapy')]
    b_lo, b_hi = SZK_APP_RAM + sum(x for x, _ in bez), SZK_APP_RAM + sum(y for _, y in bez)
    granica = G_RAM * RAM_KB
    print(f'\nRAM ECU - {MIEJSCA} miejsca po limicie profilu (aktywny + nastepny):')
    mapy = MIEJSCA * LIMIT_KB
    lo, hi = b_lo + mapy, b_hi + mapy
    print(f'  pozostaly RAM {b_lo:.1f}-{b_hi:.1f} KB + mapy {mapy:.0f} KB = {lo:.1f}-{hi:.1f} KB, granica {granica:.0f} KB')
    ok &= hi <= granica
    print(f'  rzeczywiste zuzycie map: MVP-A {MIEJSCA*a/1024:.1f} KB, B/C {MIEJSCA*bc/1024:.1f} KB')
    print('\nOK' if ok else '\nPRZEKROCZENIE')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
