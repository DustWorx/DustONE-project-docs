#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontrola spójności dokumentacji ECU "Dust ONE".

Uruchomienie z katalogu głównego repozytorium:
    python3 skrypty/kontrola.py

Sprawdza:
  1. Pokrycie wymagań — każde wymaganie ma wiersz w tabeli traceability i odwrotnie
  2. Liczniki — wymagania, DTC, testy, pozycje rejestrów (do wstawiania do dokumentów)
  3. Osierocone odwołania do identyfikatorów wycofanych
  4. Zgodność wersji w spisie dokumentów z metrykami plików

Kod wyjścia: 0 = spójne, 1 = znalezione rozbieżności.
Powód istnienia: ustalenie A50 drugiego audytu — liczniki w dokumentach
rozjechały się z rejestrami, bo były wpisywane ręcznie.
"""

import io
import os
import re
import sys

DOK = 'dokumentacja'
PROCES = os.path.join(DOK, 'proces-rozwoju-ecu.md')
WYMAGANIA = os.path.join(DOK, 'wymagania.md')
FIRMWARE = os.path.join(DOK, 'faza2-fw-specyfikacja.md')

# Identyfikator wymagania na początku wiersza tabeli, z opcjonalnym pogrubieniem
RE_WYMAGANIE = r'^\|\s*\*{0,2}((?:ECU|HMI|APP|SYS)-[A-Z]{2,3}-\d{3}[a-z]?)\*{0,2}'

# Identyfikatory wycofane — nie mogą występować poza zapisem o ich usunięciu.
# DTC-SEN-04 NIE jest wycofany: został przeniesiony do wariantów B/C, bo
# czujnik przepustnicy w nich istnieje. Nie wpisywać go tutaj.
WYCOFANE = ['ECU-IGN-008']
KONTEKST_USUNIECIA = ('usunięt', 'Usunięt', 'wycofan', 'Wycofan', 'OBALONE', 'nieaktualn')

# Wiersz historii zmian: "| 2.7 | 2026-09-22 | ...". Historia jest zapisem
# tego, co było, więc odwołania do wycofanych identyfikatorów są w niej
# prawidłowe i nie podlegają kontroli.
RE_HISTORIA = r'^\|\s*\*{0,2}\d+\.\d+\*{0,2}\s*\|\s*\*{0,2}\d{4}-\d{2}-\d{2}'

bledy = []


def czytaj(sciezka):
    if not os.path.exists(sciezka):
        bledy.append('BRAK PLIKU: %s' % sciezka)
        return ''
    return io.open(sciezka, encoding='utf-8').read()


def unikalne(wzorzec, tekst, flagi=re.M):
    return set(re.findall(wzorzec, tekst, flagi))


# --------------------------------------------------------------- 1. pokrycie
def pokrycie(wymagania, proces):
    zdefiniowane = unikalne(RE_WYMAGANIE, wymagania)

    if '## 14' not in proces:
        bledy.append('Nie znaleziono rozdziału 14 (tabela pokrycia) w %s' % PROCES)
        return zdefiniowane, set()

    tabela = proces[proces.index('## 14'):]
    pokryte = unikalne(RE_WYMAGANIE, tabela)

    bez_pokrycia = sorted(zdefiniowane - pokryte)
    nadmiarowe = sorted(pokryte - zdefiniowane)

    if bez_pokrycia:
        bledy.append('Wymagania bez wiersza pokrycia: %s' % ', '.join(bez_pokrycia))
    if nadmiarowe:
        bledy.append('Wiersze pokrycia bez wymagania: %s' % ', '.join(nadmiarowe))

    return zdefiniowane, pokryte


# --------------------------------------------------------------- 2. liczniki
def liczniki(wymagania, proces, firmware):
    otwarte = set()
    for linia in wymagania.split('\n'):
        if 'DO USTALENIA' in linia:
            m = re.match(RE_WYMAGANIE, linia)
            if m:
                otwarte.add(m.group(1))

    return {
        'wymagania': len(unikalne(RE_WYMAGANIE, wymagania)),
        'wymagania otwarte (DO USTALENIA)': len(otwarte),
        'kody usterek DTC': len(unikalne(r'\bDTC-[A-Z]{3}-\d{2}\b', firmware, 0)),
        'identyfikatory testów': len(unikalne(r'\bT-[A-Z]{3}-\d{3}[a-z]?\b', proces, 0)),
        'luki L': len(unikalne(r'\|\s*\*{0,2}(L\d{1,3})\*{0,2}\s*\|', proces)),
        'ryzyka R': len(unikalne(r'\|\s*\*{0,2}(R\d{1,3})\*{0,2}\s*\|', proces)),
        'założenia Z': len(unikalne(r'\|\s*\*{0,2}(Z\d{1,3})\*{0,2}\s*\|', proces)),
    }, sorted(otwarte)


# ------------------------------------------------- 3. osierocone odwołania
def osierocone():
    for katalog in (DOK, 'diagramy', 'pomiary'):
        if not os.path.isdir(katalog):
            continue
        for nazwa in sorted(os.listdir(katalog)):
            if not nazwa.endswith(('.md', '.mermaid')):
                continue
            sciezka = os.path.join(katalog, nazwa)
            for nr, linia in enumerate(io.open(sciezka, encoding='utf-8'), 1):
                if re.match(RE_HISTORIA, linia):
                    continue
                for ident in WYCOFANE:
                    if ident in linia and not any(k in linia for k in KONTEKST_USUNIECIA):
                        bledy.append('%s:%d — odwołanie do wycofanego %s' % (sciezka, nr, ident))


# ------------------------------------------------------------- 4. wersje
def wersje(proces):
    """Wersja w spisie dokumentów musi zgadzać się z metryką pliku."""
    metryki = {}
    for katalog in (DOK, 'archiwum'):
        if not os.path.isdir(katalog):
            continue
        for nazwa in sorted(os.listdir(katalog)):
            if not nazwa.endswith('.md'):
                continue
            tekst = io.open(os.path.join(katalog, nazwa), encoding='utf-8').read(2000)
            m = re.search(r'\*\*Wersja\*\*\s*\|\s*\*{0,2}([0-9]+\.[0-9]+)', tekst)
            if m:
                metryki[nazwa] = m.group(1)

    for nazwa, wersja_pliku in sorted(metryki.items()):
        wzor = r'`%s`[^|]*\|\s*\*{0,2}([0-9]+\.[0-9]+)' % re.escape(nazwa)
        m = re.search(wzor, proces)
        if not m:
            bledy.append('%s — brak wpisu w spisie dokumentów' % nazwa)
        elif m.group(1) != wersja_pliku:
            bledy.append('%s — spis podaje %s, metryka pliku %s'
                         % (nazwa, m.group(1), wersja_pliku))
    return metryki


def main():
    if not os.path.isdir(DOK):
        print('Uruchom z katalogu głównego repozytorium (brak katalogu %s/).' % DOK)
        return 1

    wymagania = czytaj(WYMAGANIA)
    proces = czytaj(PROCES)
    firmware = czytaj(FIRMWARE)

    zdefiniowane, pokryte = pokrycie(wymagania, proces)
    licz, otwarte = liczniki(wymagania, proces, firmware)
    osierocone()
    metryki = wersje(proces)

    print('LICZNIKI — wartości do wstawienia do dokumentów')
    for k, v in licz.items():
        print('  %-36s %d' % (k, v))
    print('  %-36s %d / %d' % ('pokrycie traceability', len(pokryte), len(zdefiniowane)))

    print('\nWERSJE DOKUMENTÓW')
    for nazwa, w in sorted(metryki.items()):
        print('  %-34s %s' % (nazwa, w))

    print('\nWYMAGANIA OTWARTE (blokują bramkę G0)')
    print('  ' + (', '.join(otwarte) if otwarte else 'brak'))

    if bledy:
        print('\nROZBIEŻNOŚCI — %d' % len(bledy))
        for b in bledy:
            print('  ✗ %s' % b)
        return 1

    print('\nSpójność potwierdzona — brak rozbieżności.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
