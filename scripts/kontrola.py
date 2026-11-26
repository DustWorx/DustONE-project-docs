#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontrola spójności dokumentacji ECU "Dust ONE".

Uruchomienie z katalogu głównego repozytorium:
    python3 scripts/kontrola.py

Sprawdza:
  1. Pokrycie wymagań — każde wymaganie ma wiersz w tabeli traceability i odwrotnie
  2. Liczniki — wartości do wstawiania do dokumentów, zamiast zliczania ręcznego
  3. Odwołania do pozycji otwartych — każde O-nnn użyte w dokumentach istnieje w otwarte.md
  4. Osierocone odwołania do identyfikatorów wycofanych

Kod wyjścia: 0 = spójne, 1 = znalezione rozbieżności.

Powód istnienia: liczniki wpisywane ręcznie rozjechały się z rejestrami
(dokumenty podawały 51 kodów usterek i 107 testów przy rzeczywistych 49 i 99).
"""

import io
import os
import re
import sys

WYMAGANIA = 'wymagania.md'
FIRMWARE = 'firmware.md'
OTWARTE = 'otwarte.md'
PRODUKT = 'produkt.md'
PROCES = 'proces.md'

KATALOGI = ('.', 'diagrams', 'measurements')
ROZSZERZENIA = ('.md', '.mermaid')

# Identyfikator wymagania na początku wiersza tabeli, z opcjonalnym pogrubieniem
RE_WYMAGANIE = r'^\|\s*\*{0,2}((?:ECU|HMI|APP|SYS)-[A-Z]{2,3}-\d{3}[a-z]?)\*{0,2}'

# Pozycja otwarta w wierszu rejestru. Rejestr ma 8 kolumn, więc wymagamy
# co najmniej 5 kresek — inaczej wpis z dwukolumnowego indeksu "Co blokuje
# bramkę G0" na początku pliku zostałby policzony jako druga definicja.
RE_POZYCJA = r'^\|\s*\*{0,2}(O-\d{3})\*{0,2}\s*\|(?:[^|\n]*\|){5,}'

# Identyfikatory wycofane — nie mogą występować poza zapisem o ich usunięciu.
# DTC-SEN-04 NIE jest wycofany: został przeniesiony do wariantów B/C, bo
# czujnik przepustnicy w nich istnieje. Nie wpisywać go tutaj.
WYCOFANE = ['ECU-IGN-008', 'ECU-IGN-003', 'ECU-IGN-004',
            # 25.10.2026: kody zapłonu indukcyjnego i przegrzania zastąpione (AC-CDI, ECU-SAF-020)
            'DTC-IGN-04', 'DTC-IGN-05', 'DTC-SYS-01']
KONTEKST_USUNIECIA = ('usunięt', 'Usunięt', 'wycofan', 'Wycofan', 'OBALONE', 'nieaktualn')

bledy = []


def czytaj(sciezka):
    if not os.path.exists(sciezka):
        bledy.append('BRAK PLIKU: %s' % sciezka)
        return ''
    return io.open(sciezka, encoding='utf-8').read()


def pliki_tekstowe():
    for katalog in KATALOGI:
        if not os.path.isdir(katalog):
            continue
        for nazwa in sorted(os.listdir(katalog)):
            if nazwa.endswith(ROZSZERZENIA):
                yield os.path.join(katalog, nazwa) if katalog != '.' else nazwa


def unikalne(wzorzec, tekst, flagi=re.M):
    return set(re.findall(wzorzec, tekst, flagi))


# --------------------------------------------------------------- 1. pokrycie
def pokrycie(wymagania):
    if '## 20.' not in wymagania:
        bledy.append('Nie znaleziono rozdziału 20 (tabela pokrycia) w %s' % WYMAGANIA)
        return set(), set()

    i = wymagania.index('## 20.')
    zdefiniowane = unikalne(RE_WYMAGANIE, wymagania[:i])
    pokryte = unikalne(RE_WYMAGANIE, wymagania[i:])

    bez_pokrycia = sorted(zdefiniowane - pokryte)
    nadmiarowe = sorted(pokryte - zdefiniowane)

    if bez_pokrycia:
        bledy.append('Wymagania bez wiersza pokrycia: %s' % ', '.join(bez_pokrycia))
    if nadmiarowe:
        bledy.append('Wiersze pokrycia bez wymagania: %s' % ', '.join(nadmiarowe))

    return zdefiniowane, pokryte


# --------------------------------------------------------------- 2. liczniki
def liczniki(wymagania, firmware, otwarte):
    i = wymagania.index('## 20.') if '## 20.' in wymagania else len(wymagania)
    czesc_wymagan = wymagania[:i]

    # Wymagania [B/C] z DO USTALENIA nie blokują G0 MVP-A — blokują bramkę
    # wariantu B/C, realizowanego jako osobna wariacja po MVP-A.
    # Wymagania oznaczone [poza G0] — decyzja Pawła, że wartość ustala się
    # później (np. przed testem prototypu); liczone osobno, nie blokują G0.
    otwarte_wymagania, otwarte_bc, otwarte_pozniej = set(), set(), set()
    for linia in czesc_wymagan.split('\n'):
        if 'DO USTALENIA' in linia:
            m = re.match(RE_WYMAGANIE, linia)
            if m:
                komorka = linia.split('|')[1]
                if '[B/C]' in komorka:
                    cel = otwarte_bc
                elif '[poza G0]' in komorka:
                    cel = otwarte_pozniej
                else:
                    cel = otwarte_wymagania
                cel.add(m.group(1))

    pozycje = unikalne(RE_POZYCJA, otwarte)
    zalozenia = unikalne(r'\|\s*\*{0,2}(Z\d{1,3})\*{0,2}\s*\|', otwarte)

    return {
        'wymagania': len(unikalne(RE_WYMAGANIE, czesc_wymagan)),
        'wymagania otwarte MVP-A (blokują G0)': len(otwarte_wymagania),
        'wymagania otwarte B/C (poza G0)': len(otwarte_bc),
        'wymagania otwarte MVP-A poza G0': len(otwarte_pozniej),
        'kody usterek DTC': len(set(re.findall(r'^\|\s*\*{0,2}(DTC-[A-Z]{3}-\d{2}[a-z]?)\*{0,2}[^|]*\|', firmware, re.M)) - set(WYCOFANE)),  # wiersze macierzy
        'identyfikatory testów': len(unikalne(r'\bT-[A-Z]{2,4}-\d{3}[a-z]?\b', wymagania, 0)),
        'pozycje otwarte': len(pozycje),
        'założenia': len(zalozenia),
    }, sorted(otwarte_wymagania), pozycje, sorted(otwarte_bc), sorted(otwarte_pozniej)


# ------------------------------------------- 3. odwołania do pozycji otwartych
def odwolania(pozycje):
    uzyte = set()
    for sciezka in pliki_tekstowe():
        if os.path.basename(sciezka) == OTWARTE:
            continue
        tekst = io.open(sciezka, encoding='utf-8').read()
        for ident in re.findall(r'\bO-\d{3}\b', tekst):
            uzyte.add(ident)

    wiszace = sorted(uzyte - pozycje)
    if wiszace:
        bledy.append('Odwołania do pozycji, których nie ma w %s: %s'
                     % (OTWARTE, ', '.join(wiszace)))

    tekst_otwarte = io.open(OTWARTE, encoding='utf-8').read()
    duplikaty = [p for p in sorted(pozycje)
                 if len(re.findall(RE_POZYCJA.replace('(O-\\d{3})', p),
                                   tekst_otwarte, re.M)) > 1]
    if duplikaty:
        bledy.append('Identyfikatory użyte więcej niż raz: %s' % ', '.join(duplikaty))

    return uzyte


# ------------------------------------------ 5. kody usterek użyte dwukrotnie
# Wiersz macierzy kodów ma co najmniej 6 kolumn (kod, nazwa, wykrycie, czas,
# klasa, reakcja); krótsze tabele (np. C.1.7) tylko przywołują kody.
RE_WIERSZ_DTC = r'^\|\s*\*{0,2}(DTC-[A-Z]{3}-\d{2}[a-z]?)\*{0,2}\s*\|(?:[^|\n]*\|){5,}'


def kody_dwukrotnie(firmware):
    kody = re.findall(RE_WIERSZ_DTC, firmware, re.M)
    podwojne = sorted({k for k in kody if kody.count(k) > 1})
    if podwojne:
        bledy.append('Kod usterki zdefiniowany w macierzy więcej niż raz: %s' % ', '.join(podwojne))


# ------------------------------------------------- 6. liczniki w README
def readme(licz, pokryte, zdefiniowane):
    if not os.path.exists('README.md'):
        return
    tekst = io.open('README.md', encoding='utf-8').read()
    oczekiwane = {
        'Wymagania z identyfikatorem': str(licz['wymagania']),
        'Pokrycie w tabeli traceability': '%d / %d' % (len(pokryte), len(zdefiniowane)),
        'Kody usterek w macierzy': str(licz['kody usterek DTC']),
        'Identyfikatory testów': str(licz['identyfikatory testów']),
        'Pozycje otwarte': str(licz['pozycje otwarte']),
        'Wymagania bez ustalonej wartości — **blokują G0**': str(licz['wymagania otwarte MVP-A (blokują G0)']),
        'Wymagania bez ustalonej wartości — wariant B/C, poza G0': str(licz['wymagania otwarte B/C (poza G0)']),
        'Wymagania bez ustalonej wartości — MVP-A, poza G0 (decyzja)': str(licz['wymagania otwarte MVP-A poza G0']),
    }
    for etykieta, wartosc in oczekiwane.items():
        m = re.search(r'^\|\s*%s\s*\|\s*([^|]+?)\s*\|' % re.escape(etykieta), tekst, re.M)
        if m and m.group(1).strip('* ') != wartosc:
            bledy.append('README: „%s” = %s, wyliczone %s' % (etykieta, m.group(1).strip(), wartosc))
    m = re.search(r'^\|\s*Założenia \([^)]*\)\s*\|\s*(\d+)\s*\|', tekst, re.M)
    if m and int(m.group(1)) != licz['założenia']:
        bledy.append('README: założenia = %s, wyliczone %d' % (m.group(1), licz['założenia']))


# ------------------------------------------------- 4. osierocone odwołania
def osierocone():
    for sciezka in pliki_tekstowe():
        for nr, linia in enumerate(io.open(sciezka, encoding='utf-8'), 1):
            for ident in WYCOFANE:
                if ident in linia and not any(k in linia for k in KONTEKST_USUNIECIA):
                    bledy.append('%s:%d — odwołanie do wycofanego %s' % (sciezka, nr, ident))


def main():
    if not os.path.exists(WYMAGANIA):
        print('Uruchom z katalogu głównego repozytorium (nie znaleziono %s).' % WYMAGANIA)
        return 1

    wymagania = czytaj(WYMAGANIA)
    firmware = czytaj(FIRMWARE)
    otwarte = czytaj(OTWARTE)

    zdefiniowane, pokryte = pokrycie(wymagania)
    licz, otwarte_wym, pozycje, otwarte_bc, otwarte_pozniej = liczniki(wymagania, firmware, otwarte)
    uzyte = odwolania(pozycje)
    osierocone()
    kody_dwukrotnie(firmware)
    readme(licz, pokryte, zdefiniowane)

    print('LICZNIKI — wartości do wstawienia do dokumentów')
    for k, v in licz.items():
        print('  %-36s %d' % (k, v))
    print('  %-36s %d / %d' % ('pokrycie traceability', len(pokryte), len(zdefiniowane)))
    print('  %-36s %d' % ('pozycje otwarte przywołane w tekście', len(uzyte)))

    print('\nWYMAGANIA OTWARTE (blokują bramkę G0)')
    print('  ' + (', '.join(otwarte_wym) if otwarte_wym else 'brak'))
    print('\nWYMAGANIA OTWARTE B/C (blokują bramkę wariantu B/C, nie G0)')
    print('  ' + (', '.join(otwarte_bc) if otwarte_bc else 'brak'))
    print('\nWYMAGANIA OTWARTE MVP-A POZA G0 (decyzja — wartość ustalana później)')
    print('  ' + (', '.join(otwarte_pozniej) if otwarte_pozniej else 'brak'))

    if bledy:
        print('\nROZBIEŻNOŚCI — %d' % len(bledy))
        for b in bledy:
            print('  ✗ %s' % b)
        return 1

    print('\nSpójność potwierdzona — brak rozbieżności.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
