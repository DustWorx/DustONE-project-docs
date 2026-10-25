# Pomiar drgań w miejscu montażu ECU — Beta 300 RR 2015

**Cel:** dane do profilu wibracji SYS-ENV-006 (pozycja O-047) i sprawdzenie, czy zakres akcelerometru **±16 g** nie nasyca się przy pracy silnika (ECU-SAF-005, ECU-LOG-006).

**Miejsce montażu ECU:** pod siedzeniem, przy airboxie (decyzja Pawła 25.10.2026).

## Dwa pomiary, dwa przyrządy

| Pomiar | Przyrząd | Dlaczego ten |
|---|---|---|
| **A. Drgania silnika** — na stojąco, przegazowania | **ST STEVAL-MKI218V1** (AIS2IH na płytce DIL24) + **STEVAL-MKI109D** (płytka bazowa, USB-C, MEMS Studio) | Docelowy czujnik ECU, do 1600 próbek/s — obejmuje drgania dwusuwa do ~10 000 obr/min (≈ 167 Hz podstawowej) z harmonicznymi |
| **B. Udary w jeździe** — hopy, kamienie, korzenie | **iPhone + phyphox** | Aplikacje na iPhone'a dostają ~100 próbek/s — wystarcza do wolnych udarów, **nie** do drgań silnika powyżej ~3000 obr/min |

Orientacyjnie: STEVAL-MKI218V1 ~€15 (Farnell, w magazynie); STEVAL-MKI109D ~104 USD (sklep ST). STEVAL-MKI109V3 jest wycofany — nie kupować. Dostępność w kolejności TME → Mouser → Farnell → DigiKey do sprawdzenia przed zakupem.

## Pomiar A — drgania silnika (na stojąco)

1. Płytkę MKI218V1 przymocować **sztywno** w miejscu montażu ECU (pod siedzeniem, przy airboxie) — opaska + klej dwuskładnikowy albo docisk do sztywnego elementu. **Nie na gąbce** — mierzymy drgania podłoża, nie mocowania.
2. Osie zapisać względem motocykla: X — wzdłuż (przód), Y — w bok (lewo), Z — w górę. Zdjęcie ułożenia płytki.
3. MEMS Studio: zakres **±16 g**, częstotliwość **1600 Hz**, filtr pasma ODR/2, zapis do pliku.
4. Silnik rozgrzany, motocykl na podstawce, bieg luz. Zapis po **10 s** w punktach: bieg jałowy, 3000, 5000, 7000, 9000 obr/min (krótko), oraz jedno płynne przegazowanie od jałowego do odcięcia.
5. Przy każdym zapisie odnotować obroty (obrotomierz albo okres z oscyloskopu na pick-upie).

## Pomiar B — udary w jeździe

1. iPhone w etui, **sztywno** przymocowany pod siedzeniem przy airboxie (opaski przez etui, bez luzu). Ułożenie osi jak wyżej — zdjęcie.
2. phyphox: eksperyment **„Przyspieszenie (bez g)”** albo **„Surowe dane czujników”**, eksport CSV.
3. Przejazd 10–15 min: teren typowy dla Ciebie, **w tym hopy i twarde lądowania**. Zapisać godzinę hop, żeby odnaleźć je w danych.

## Co z tego wyliczę

| Wielkość | Z czego | Do czego |
|---|---|---|
| Widmo drgań w funkcji obrotów (gęstość widmowa mocy) | A | Porównanie z profilami ISO 16750-3 — wybór profilu z zapasem |
| Szczyty przyspieszenia, nasycenie ±16 g | A, B | Potwierdzenie zakresu akcelerometru |
| Udary: wartość szczytowa i czas trwania | B | Profil udarów mechanicznych SYS-ENV-006, czarna skrzynka |
| Częstotliwości dominujące | A | Strojenie mocowania ECU — rezonans tulei nie może wypaść w paśmie silnika |

**Prześlij:** pliki z MEMS Studio i phyphox, zdjęcia ułożenia przyrządów, notatki z obrotami i godzinami hop.
