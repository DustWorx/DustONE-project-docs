#!/usr/bin/env python3
"""Bilans czarnej skrzynki (O-042): strumien danych, podzial W25Q64, RAM, zuzycie pamieci.

Kanaly i czestotliwosci to propozycja (firmware.md F.1) - po zmianie tabeli
KANALY skrypt przelicza wszystko. Kod wyjscia 1, gdy podzial pamieci nie miesci
sie w 8 MB albo zywotnosc pierscienia < 5000 h pracy silnika.
"""
import sys

# (nazwa, bajty na probke, Hz)
KANALY = [
    ('naglowek ramki: znacznik czasu 4 B + licznik 2 B', 6, 100),
    ('obroty, wyprzedzenie zadane, kat iskry przechwycony', 6, 100),
    ('napiecie kondensatora, szczyt wzbudzajacego', 4, 100),
    ('stany: maszyna stanow, synchronizacja, kill, START, flagi DTC', 6, 100),
    ('akcelerometr 3 osie x 16 bit', 6, 200),
    ('temperatury cieczy i powietrza, akumulator, VDD5, VSOUT1', 10, 10),
    ('bieg, predkosc kola, cisnienie, temperatura ECU', 8, 10),
]
SEKTOR = 4096                 # B, kasowanie W25Q64
STRONA = 256                  # B, programowanie
PRZED, PO = 10.0, 5.0         # s, ECU-LOG-006
ZDARZENIA = 16                # slotow na zdarzenia
PIERSCIEN_S = 8 * 60          # s, dlugosc pierscienia ciaglego
CYKLE = 100_000               # kasowan na sektor (karta rodziny W25Q)
PAMIEC = 8 * 1024 * 1024

def main():
    bps = sum(b * hz for _, b, hz in KANALY)
    print(f'Strumien: {bps} B/s = {bps/1024:.2f} kB/s')
    for n, b, hz in KANALY:
        print(f'  {n:58s} {b:3d} B x {hz:4d} Hz = {b*hz:5d} B/s')
    zd = bps * (PRZED + PO)
    zd_sekt = -(-int(zd) // SEKTOR) * SEKTOR
    pier = -(-int(bps * PIERSCIEN_S) // SEKTOR) * SEKTOR
    podzial = [
        ('pierscien ciagly (ostatnie %d min pracy)' % (PIERSCIEN_S // 60), pier),
        ('zdarzenia: %d x %.0f s (%d kB po zaokragleniu do sektorow)' % (ZDARZENIA, PRZED + PO, zd_sekt // 1024), ZDARZENIA * zd_sekt),
        ('dziennik usterek i zdarzen (rekordy 32 B)', 256 * 1024),
        ('mapy: 3 profile x 2 kopie x 16 kB', 3 * 2 * 16 * 1024),
        ('profil granic, konfiguracja, rekord transakcji: po 2 kopie', 6 * SEKTOR),
        ('liczniki (dziennik z wyrownywaniem zuzycia)', 64 * 1024),
        ('histogram ECU-LOG-009', 2 * SEKTOR),
    ]
    uzyte = sum(v for _, v in podzial)
    print(f'\nPodzial W25Q64 ({PAMIEC // 1024 // 1024} MB):')
    for n, v in podzial:
        print(f'  {n:62s} {v/1024:8.0f} kB')
    print(f'  {"razem":62s} {uzyte/1024:8.0f} kB  ({100*uzyte/PAMIEC:.0f} %), rezerwa {(PAMIEC-uzyte)/1024/1024:.1f} MB')
    zycie_h = CYKLE * pier / bps / 3600
    print(f'\nZuzycie pierscienia: kazdy sektor kasowany co {pier/bps/60:.1f} min pracy silnika;'
          f' {CYKLE} cykli = {zycie_h:,.0f} h pracy silnika')
    ram = 2 * STRONA * 4
    print(f'RAM: bufor stron {ram} B (podwojny, 4 strony) - przed zanikiem zasilania traci sie najwyzej '
          f'{4*STRONA/bps*1000:.0f} ms danych')
    ok = uzyte <= PAMIEC and zycie_h >= 5000
    print('\nOK' if ok else '\nPRZEKROCZENIE')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
