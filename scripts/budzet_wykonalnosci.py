#!/usr/bin/env python3
"""Budzet wykonalnosci (O-067, warunek G0): pamiec programu, RAM, procesor, CAN, W25Q128.

Granice: SYS-RES-001..003 (decyzje Pawla 26.11.2026) - stale od G0.
Warstwa sterownikow (HAL + USB) ZMIERZONA kompilacja szkieletu: scripts/szkielet/build.sh.
Logika aplikacji, czasy obslugi i ramki CAN - SZACUNEK (min, max); po zmianie tabel
skrypt przelicza wszystko. Kod wyjscia 1, gdy gorny szacunek przekracza granice.
HMI: STM32G474RE (512 KB, dwa banki) - bootloader 32 KB, sloty po 224 KB (firmware.md H.1);
pamiec modulu wyswietlacza 32 MB i pamiec graficzna EVE4 1 MB (firmware.md J.1).
"""
import sys
from bilans_logu import podzial, PAMIEC, GRANICA as GRANICA_W25Q
from bilans_map import MIEJSCA as MIEJSCA_MAP, LIMIT_KB as PROFIL_KB

KB = 1024
# --- granice (SYS-RES-001..003)
G_CPU, G_FLASH, G_RAM, G_CAN, G_CAN_AKT = 0.60, 0.50, 0.50, 0.50, 0.80
G_EVE = 0.75  # pamiec graficzna i lista wyswietlania EVE4 (decyzja Pawla 26.11.2026)

# --- uklad Flash ECU (firmware.md H.1)
SLOT_KB, BOOT_KB, RAM_KB = 444, 64, 128

# --- pomiar szkieletu 26.11.2026 (scripts/szkielet/README.md)
SZK_APP_FLASH, SZK_APP_RAM = 37.7, 9.5   # KB; RAM z 4 KB stosu
SZK_BOOT_FLASH = 15.9
SZK_HMI_FLASH, SZK_HMI_RAM, SZK_HMI_BOOT = 14.8, 5.2, 6.2

# --- HMI STM32G474RE: 170 MHz Cortex-M4F, 128 KB RAM (od 26.11.2026); ekran wzorcowy HMI-UI-015 przy 60 Hz
HMI_SLOT_KB, HMI_BOOT_KB, HMI_RAM_KB, HMI_MHZ = 224, 32, 128, 170
HMI_LOGIKA = [
    ('sterownik EVE4 BT817Q: koprocesor, Quad-SPI z DMA, flash modulu', 6, 12),
    ('silnik animacji: krzywe, przejscia, sekwencje klatek', 3, 6),
    ('interpreter ukladow (3 profile), widgety z efektami', 8, 16),
    ('ekrany systemowe: menu, DTC, K4, komunikaty, przejscia', 10, 20),
    ('teksty, formatowanie liczb', 3, 6),
    ('protokol CAN, swiezosc danych, wygladzanie wskazan', 4, 8),
    ('dostep do pamieci HMI z trybu deweloperskiego (D.4)', 1, 2),
    ('aktualizacja, rekordy, zarzadzanie pamiecia modulu (J.1)', 4, 8),
    ('przyciski, czujniki swiatla i temperatury, jasnosc', 2, 4),
    ('usypianie, watchdog, zgloszenia DTC', 1, 3),
]
HMI_BOOT_LOGIKA = [('odbior obrazu po CAN, rekord startowy, CRC, wybor banku', 3, 5)]
HMI_RAM = [
    ('opis aktywnego ukladu + nastepny przy zmianie profilu', 8, 16),
    ('bufor listy polecen przed DMA do EVE4 (podwojny)', 8, 16),
    ('stan animacji, model danych, swiezosc', 2, 4),
    ('bufory CAN i ISO-TP', 1, 2),
    ('aktualizacja: strona Flash 2 KB + bufor zasobow', 6, 8),
    ('menu, teksty, stan', 2, 4),
    ('dodatkowe stosy', 0, 4),
]
HMI_CPU = [  # (zrodlo, zdarzen/s, us min, us max) przy 170 MHz
    ('ekran wzorcowy 60 Hz: lista ~1000 polecen, animacje, liczby', 60, 250, 600),
    ('CAN: ramki odbierane i nadawane', 200, 2, 4),
    ('przyciski: ADC co 5 ms', 200, 3, 6),
    ('czujniki I2C 10 Hz', 10, 30, 60),
    ('SysTick, watchdog', 1000, 0.5, 1),
]
# --- pamiec modulu wyswietlacza 32 MB (firmware.md J.1) i EVE4
MODUL_KB = 32 * 1024
MODUL = [
    ('sterownik flash koprocesora', 4),
    ('zasoby systemowe 2 x 4 MB', 2 * 4096),
    ('wyglad uzytkownika (3 uklady + biblioteka) 2 x 3 MB', 2 * 3072),
    ('ustawienia HMI (rekordy H.3)', 64),
]
EVE_RAM_G_KB, EVE_DL = 1024, 2048
EVE_RAM_G = (250, 550)   # KB, szacunek: czcionki, obrazy czeste, stale fragmenty listy, dekodowanie animacji startowej
EVE_DL_WZOR = (600, 1000)  # polecen na klatke ekranu wzorcowego, szacunek

# --- logika aplikacji ECU: (modul, KB min, KB max) - szacunek
LOGIKA = [
    ('A  maszyna stanow, rozrusznik, usypianie', 3, 5),
    ('B  macierz 75 DTC z progami, limp-home, zatrzask, interlocki', 8, 14),
    ('C.1 synchronizacja, estymator E1, alfa_max, ogranicznik', 6, 10),
    ('C.2 mapy i korekty (interpolacja)', 3, 6),
    ('C.3 wentylator, swiatla, profile, liczniki, RTC', 3, 5),
    ('D  granice map, rekordy atomowe, tryb kalibracji', 5, 8),
    ('E  dziennik usterek, ramki danych', 2, 4),
    ('F  czarna skrzynka (pierscien, zdarzenia)', 4, 7),
    ('H  aktualizacja w aplikacji, transakcja ECU+HMI', 4, 7),
    ('I.2 nadzor PMIC pytanie-odpowiedz', 2, 4),
    ('XCP (DAQ, kalibracja, PGM, USER_CMD), SxI, transakcje, ramki z CRC, ISO-TP (K)', 6, 12),
    ('tryb deweloperski: haslo (wyzwanie-odpowiedz), dostep do pamieci, CAN przez USB (D.4)', 4, 10),
    ('sterowniki: W25Q128, AIS2IH, KP464, PMIC, PROFET, NTC', 4, 7),
]
BOOT_LOGIKA = [
    ('sterownik SPI i W25Q128 (odczyt, kopiowanie)', 2, 3),
    ('rekord startowy, kopiowanie, CRC, powrot', 2, 3),
    ('protokol odzyskiwania USB, warunki ECU-BTL-001', 3, 4),
]
# --- RAM ECU: (pozycja, KB min, KB max) - szacunek
RAM = [
    ('mapy: profil aktywny + nastepny, profil <= 8 KB (bilans_map.py, D.3)', MIEJSCA_MAP * PROFIL_KB, MIEJSCA_MAP * PROFIL_KB),
    ('bufory stron czarnej skrzynki (bilans_logu.py)', 2, 2),
    ('bufory CAN, kolejki ramek', 1, 2),
    ('stan 75 DTC, liczniki potwierdzen', 2, 3),
    ('rekord usterki w budowie, kopiowanie zdarzen', 1, 2),
    ('zmienne sterowania, kalibracja, konfiguracja', 4, 8),
    ('FreeRTOS-MPU (ECU-SAF-023): jadro i stosy ~7 zadan', 5, 9),  # do 27.11.2026 blednie 0-4 KB
    ('XCP: pakiety, listy i kolejka DAQ; ISO-TP (bloki w miejscu "nastepny")', 2.5, 4.5),
]
# --- procesor ECU przy 10 000 obr/min: (zrodlo, zdarzen/s, us min, us max) - szacunek
OBR_S = 10_000 / 60
CPU = [
    ('zbocza VR (2 na obrot): przechwyt, estymator', 2 * OBR_S, 3, 6),
    ('planowanie iskry: mapa, alfa_max, HRTIM', OBR_S, 3, 6),
    ('ADC wstrzykiwane: kondensator, wzbudzajacy', 2 * OBR_S, 2, 3),
    ('petla 1 kHz: stany, wyjscia, 75 kontroli DTC', 1000, 30, 80),
    ('czarna skrzynka: rekord 100 Hz', 100, 20, 40),
    ('akcelerometr 200 Hz, wywrotka', 200, 5, 10),
    ('CAN: ramki nadawane i odbierane', 200, 3, 6),
    ('USB: podglad na zywo, strojenie', 1000, 10, 20),
    ('nadzor PMIC, SysTick', 1050, 1, 2),
]
# --- CAN 500 kbit/s, ramka 8 B, identyfikator 11 bit, najgorsze wypelnienie bitami
BITY_RAMKI, PREDKOSC = 135, 500_000
CAN_RAMKI = [  # (ramka, Hz) - szacunek z SYS-COM-002a/b; lista ramek: O-043
    ('ECU->HMI szybkozmienne (obroty, predkosc) x2', 2 * 50),
    ('ECU->HMI wolnozmienne, stany, DTC, swiatla x6', 6 * 10),
    ('HMI->ECU przyciski, zycie x2', 2 * 20),
]
DANE_RAMKI = 7  # B danych na ramke aktualizacji (1 B naglowka) - zalozenie

def wiersz(n, a, b, jedn=''):
    print(f'  {n:62s} {a:7.1f} - {b:7.1f} {jedn}')

def ocena(nazwa, lo, hi, granica, jedn):
    ok = hi <= granica
    print(f'  {"=> " + nazwa:62s} {lo:7.1f} - {hi:7.1f} {jedn}  granica {granica:.1f} {jedn}  '
          + ('OK' if ok else ('PRZEKROCZENIE przy gornym szacunku' if lo <= granica else 'PRZEKROCZENIE')))
    return ok

def main():
    ok = True
    print('ECU - pamiec programu aplikacji (slot %d KB)' % SLOT_KB)
    wiersz('sterowniki HAL + USB (pomiar szkieletu)', SZK_APP_FLASH, SZK_APP_FLASH, 'KB')
    for n, a, b in LOGIKA:
        wiersz(n, a, b, 'KB')
    lo = SZK_APP_FLASH + sum(a for _, a, _ in LOGIKA); hi = SZK_APP_FLASH + sum(b for *_, b in LOGIKA)
    ok &= ocena('razem', lo, hi, G_FLASH * SLOT_KB, 'KB')

    print('\nECU - bootloader (obszar %d KB)' % BOOT_KB)
    wiersz('sterowniki HAL + USB (pomiar szkieletu)', SZK_BOOT_FLASH, SZK_BOOT_FLASH, 'KB')
    for n, a, b in BOOT_LOGIKA:
        wiersz(n, a, b, 'KB')
    lo = SZK_BOOT_FLASH + sum(a for _, a, _ in BOOT_LOGIKA); hi = SZK_BOOT_FLASH + sum(b for *_, b in BOOT_LOGIKA)
    ok &= ocena('razem', lo, hi, G_FLASH * BOOT_KB, 'KB')

    print('\nECU - RAM (%d KB)' % RAM_KB)
    wiersz('sterowniki HAL + USB + stos 4 KB (pomiar szkieletu)', SZK_APP_RAM, SZK_APP_RAM, 'KB')
    for n, a, b in RAM:
        wiersz(n, a, b, 'KB')
    lo = SZK_APP_RAM + sum(a for _, a, _ in RAM); hi = SZK_APP_RAM + sum(b for *_, b in RAM)
    ok &= ocena('razem', lo, hi, G_RAM * RAM_KB, 'KB')

    print('\nECU - procesor przy 10 000 obr/min (170 MHz)')
    lo = hi = 0.0
    for n, f, a, b in CPU:
        wiersz(f'{n} ({f:.0f}/s)', 100 * f * a * 1e-6, 100 * f * b * 1e-6, '%')
        lo += 100 * f * a * 1e-6; hi += 100 * f * b * 1e-6
    ok &= ocena('razem', lo, hi, 100 * G_CPU, '%')

    print('\nCAN 500 kbit/s (ramka %d bitow w najgorszym przypadku)' % BITY_RAMKI)
    zaj = 0.0
    for n, hz in CAN_RAMKI:
        z = 100 * hz * BITY_RAMKI / PREDKOSC; zaj += z
        wiersz(f'{n} ({hz}/s)', z, z, '%')
    ok &= ocena('praca', zaj, zaj, 100 * G_CAN, '%')
    ramki_akt = G_CAN_AKT * PREDKOSC / BITY_RAMKI
    kbs = ramki_akt * DANE_RAMKI / 1000
    print(f'  aktualizacja przy {G_CAN_AKT:.0%}: {ramki_akt:.0f} ramek/s x {DANE_RAMKI} B = {kbs:.1f} kB/s;'
          f' firmware HMI 256 KB w {256 * KB / 1000 / kbs:.0f} s; w 5 min miesci sie {kbs * 300 / 1000:.1f} MB zasobow')

    print('\nW25Q128 ECU (%d MB)' % (PAMIEC // KB // KB))
    uz = sum(v for _, v in podzial()[2]) / KB
    ok &= ocena('przydzialy (bilans_logu.py)', uz, uz, GRANICA_W25Q * PAMIEC / KB, 'kB')

    print('\nHMI - pamiec programu (slot %d KB)' % HMI_SLOT_KB)
    wiersz('sterowniki HAL (pomiar szkieletu)', SZK_HMI_FLASH, SZK_HMI_FLASH, 'KB')
    for n, a, b in HMI_LOGIKA:
        wiersz(n, a, b, 'KB')
    lo = SZK_HMI_FLASH + sum(a for _, a, _ in HMI_LOGIKA); hi = SZK_HMI_FLASH + sum(b for *_, b in HMI_LOGIKA)
    ok &= ocena('razem', lo, hi, G_FLASH * HMI_SLOT_KB, 'KB')

    print('\nHMI - bootloader (obszar %d KB)' % HMI_BOOT_KB)
    wiersz('sterowniki HAL (pomiar szkieletu)', SZK_HMI_BOOT, SZK_HMI_BOOT, 'KB')
    for n, a, b in HMI_BOOT_LOGIKA:
        wiersz(n, a, b, 'KB')
    lo = SZK_HMI_BOOT + sum(a for _, a, _ in HMI_BOOT_LOGIKA); hi = SZK_HMI_BOOT + sum(b for *_, b in HMI_BOOT_LOGIKA)
    ok &= ocena('razem', lo, hi, G_FLASH * HMI_BOOT_KB, 'KB')

    print('\nHMI - RAM (%d KB)' % HMI_RAM_KB)
    wiersz('sterowniki HAL + stos 4 KB (pomiar szkieletu)', SZK_HMI_RAM, SZK_HMI_RAM, 'KB')
    for n, a, b in HMI_RAM:
        wiersz(n, a, b, 'KB')
    lo = SZK_HMI_RAM + sum(a for _, a, _ in HMI_RAM); hi = SZK_HMI_RAM + sum(b for *_, b in HMI_RAM)
    ok &= ocena('razem', lo, hi, G_RAM * HMI_RAM_KB, 'KB')

    print('\nHMI - procesor (%d MHz, Cortex-M4F), ekran wzorcowy' % HMI_MHZ)
    lo = hi = 0.0
    for n, f, a, b in HMI_CPU:
        wiersz(f'{n} ({f:.0f}/s)', 100 * f * a * 1e-6, 100 * f * b * 1e-6, '%')
        lo += 100 * f * a * 1e-6; hi += 100 * f * b * 1e-6
    ok &= ocena('razem', lo, hi, 100 * G_CPU, '%')

    print('\nHMI - pamiec modulu wyswietlacza (%d MB)' % (MODUL_KB // 1024))
    for n, v in MODUL:
        wiersz(n, v, v, 'KB')
    uz = sum(v for _, v in MODUL)
    ok &= ocena('razem', uz, uz, 0.5 * MODUL_KB, 'KB')
    print('\nHMI - EVE4 (szacunek, dowod na makiecie T-UI-015)')
    ok &= ocena('pamiec graficzna RAM_G', EVE_RAM_G[0], EVE_RAM_G[1], G_EVE * EVE_RAM_G_KB, 'KB')
    ok &= ocena('lista wyswietlania (polecen)', EVE_DL_WZOR[0], EVE_DL_WZOR[1], G_EVE * EVE_DL, '')

    print('\nOK - wszystkie zasoby w granicach' if ok else '\nPRZEKROCZENIE')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
